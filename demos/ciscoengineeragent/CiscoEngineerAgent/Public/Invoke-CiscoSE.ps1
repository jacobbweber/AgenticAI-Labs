function Invoke-CiscoSE {
    <#
    .SYNOPSIS
        Front-door chat turn. POSTs to Ollama, runs the ReAct loop, persists session JSON.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Message,
        [string]$SessionId = 'default',
        [switch]$Approve,
        [switch]$Deny
    )
    if ($Approve -and $Deny) {
        throw "Specify only one of -Approve or -Deny."
    }

    Initialize-CiscoSEHomeDirs
    $script:CiscoSECurrentSessionId = $SessionId
    $cfg = Get-CiscoSEConfig
    $session = Read-CiscoSESession -SessionId $SessionId

    if ($Approve -or $Deny) {
        $session = Invoke-CiscoSEHitlResume -SessionId $SessionId -Approved ([bool]$Approve)
        if ($Deny) {
            return "Denied parked artifact '$($session.parked_artifact)'."
        }
    }
    elseif ($session.needs_hitl) {
        return "Parked for approval: $($session.park_reason). Use Invoke-CiscoSE -Approve or -Deny."
    }

    $job = Add-CiscoSEJob -Prompt $Message -SessionId $SessionId
    Set-CiscoSEJobStatus -JobId $job.job_id -Status 'running' | Out-Null
    $session = Read-CiscoSESession -SessionId $SessionId
    $session.job_id = $job.job_id
    $session.needs_hitl = $false

    $hasSystem = $false
    foreach ($m in (ConvertTo-CiscoSEList -Value $session.messages)) {
        $role = [string]((ConvertTo-CiscoSETable -Value $m).role)
        if ($role -eq 'system') { $hasSystem = $true; break }
    }
    if (-not $hasSystem) {
        $session = Add-CiscoSESessionMessage -Session $session -Message @{
            role    = 'system'
            content = (Get-CiscoSESystemPrompt)
        }
    }

    $matched = ConvertTo-CiscoSEList -Value (Find-CiscoSESkillTriggers -UserText $Message)
    foreach ($id in $matched) {
        $skillJson = Invoke-CiscoSELoadSkill -Arguments @{ id = $id }
        $session = Add-CiscoSESystemContext -Session $session -Text ("Loaded skill $id on trigger.`n" + $skillJson)
    }

    $factsJson = Invoke-CiscoSERecallFacts
    $factsObj = ConvertTo-CiscoSETable -Value ($factsJson | ConvertFrom-Json)
    $factRows = @()
    if ($factsObj.ContainsKey('facts') -and $null -ne $factsObj.facts) {
        $factRows = ConvertTo-CiscoSEList -Value $factsObj.facts
    }
    if ($factRows.Count -gt 0) {
        $session = Add-CiscoSESystemContext -Session $session -Text ("Episodic facts: " + $factsJson)
    }

    $session = Add-CiscoSESessionMessage -Session $session -Message @{
        role    = 'user'
        content = $Message
    }
    Save-CiscoSESession -Session $session | Out-Null

    $text = Invoke-CiscoSELoop -Session $session -Config $cfg
    if ([string]::IsNullOrWhiteSpace($text)) {
        return ''
    }
    return [string]$text
}
