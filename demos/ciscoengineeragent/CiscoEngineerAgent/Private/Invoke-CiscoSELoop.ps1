function Get-CiscoSEMessageContent {
    [CmdletBinding()]
    param($Message)
    if ($null -eq $Message) { return '' }
    $t = ConvertTo-CiscoSETable -Value $Message
    if ($t.ContainsKey('content') -and $null -ne $t.content) {
        return [string]$t.content
    }
    return ''
}

function Get-CiscoSEToolCalls {
    [CmdletBinding()]
    param($Message)
    if ($null -eq $Message) { return @() }
    $t = ConvertTo-CiscoSETable -Value $Message
    if (-not $t.ContainsKey('tool_calls') -or $null -eq $t.tool_calls) {
        return @()
    }
    return (ConvertTo-CiscoSEList -Value $t.tool_calls)
}

function Invoke-CiscoSELoop {
    [CmdletBinding()]
    param(
        $Session,
        $Config
    )
    $cfg = $Config
    $seen = New-Object System.Collections.Generic.List[string]
    $spent = ConvertTo-CiscoSETable -Value $Session.spent
    if (-not $spent.ContainsKey('turns')) { $spent.turns = 0 }
    if (-not $spent.ContainsKey('tokens')) { $spent.tokens = 0 }
    $budget = @{
        max_turns  = [int]$cfg.max_turns
        max_tokens = [int]$cfg.max_tokens
    }
    $tools = Get-CiscoSEToolSchema
    $stopReason = $null
    $final = ''

    while ($true) {
        $check = Test-CiscoSEBudget -Budget $budget -Spent $spent
        if ($check.stop) {
            $stopReason = [string]$check.reason
            $final = "Stopped: $stopReason"
            break
        }

        $resp = Invoke-OllamaChat -Messages $Session.messages -Tools $tools -Config $cfg
        $spent.turns = [int]$spent.turns + 1
        $tokenAdd = 0
        if ($null -ne $resp.eval_count) { $tokenAdd += [int]$resp.eval_count }
        if ($null -ne $resp.prompt_eval_count) { $tokenAdd += [int]$resp.prompt_eval_count }
        if ($tokenAdd -le 0) {
            $approx = (Get-CiscoSEMessageContent -Message $resp.message)
            $tokenAdd = [Math]::Max(1, [int]($approx.Length / 4))
        }
        $spent.tokens = [int]$spent.tokens + $tokenAdd

        $msg = $resp.message
        $assistant = @{
            role    = 'assistant'
            content = (Get-CiscoSEMessageContent -Message $msg)
        }
        $calls = ConvertTo-CiscoSEList -Value (Get-CiscoSEToolCalls -Message $msg)
        if ($calls.Count -gt 0) {
            $assistant.tool_calls = $calls
        }
        $Session = Add-CiscoSESessionMessage -Session $Session -Message $assistant

        if ($calls.Count -eq 0) {
            $demux = Demux-ThinkTags -Text $assistant.content
            $final = $demux.response
            if ([string]::IsNullOrWhiteSpace($final)) {
                $final = $assistant.content
            }
            break
        }

        $haltLoop = $false
        foreach ($call in $calls) {
            $callTable = ConvertTo-CiscoSETable -Value $call
            $fn = ConvertTo-CiscoSETable -Value $callTable.function
            $name = [string]$fn.name
            $toolArgs = $fn.arguments
            if ($toolArgs -is [string]) {
                $toolArgs = ConvertTo-CiscoSETable -Value $toolArgs
            }
            else {
                $toolArgs = ConvertTo-CiscoSETable -Value $toolArgs
            }
            $result = Invoke-CiscoSETool -Name $name -Arguments $toolArgs
            $cycle = Test-CiscoSECycleDetect -ToolName $name -Arguments $toolArgs -Result $result -Seen $seen
            $Session = Add-CiscoSESessionMessage -Session $Session -Message @{ role = 'tool'; content = $result }
            if ($cycle.halt) {
                $stopReason = 'cycle'
                $final = 'Stopped: repeated tool cycle.'
                $haltLoop = $true
                break
            }
            $fresh = Read-CiscoSESession -SessionId ([string]$Session.session_id)
            if ($fresh.needs_hitl) {
                $Session.needs_hitl = $true
                $Session.parked_artifact = $fresh.parked_artifact
                $Session.park_reason = $fresh.park_reason
                $Session.stop_reason = 'needs_hitl'
                $stopReason = 'needs_hitl'
                $final = "Parked for approval: $($fresh.park_reason). Use Invoke-CiscoSE -Approve or -Deny."
                $haltLoop = $true
                break
            }
        }
        if ($haltLoop) { break }
    }

    $Session.spent = $spent
    $Session.stop_reason = $stopReason
    $Session.turn_count = [int]$Session.turn_count + 1
    Save-CiscoSESession -Session $Session | Out-Null
    if ($Session.job_id -and $stopReason -ne 'needs_hitl') {
        $jobStatus = 'done'
        if ($stopReason -eq 'max_turns' -or $stopReason -eq 'max_tokens' -or $stopReason -eq 'cycle') {
            $jobStatus = 'failed'
        }
        Set-CiscoSEJobStatus -JobId ([string]$Session.job_id) -Status $jobStatus -Result $final | Out-Null
    }
    return $final
}
