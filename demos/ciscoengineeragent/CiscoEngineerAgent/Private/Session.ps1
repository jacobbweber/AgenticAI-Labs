function New-CiscoSESession {
    [CmdletBinding()]
    param(
        [string]$SessionId = 'default'
    )
    return @{
        session_id       = $SessionId
        messages         = @()
        turn_count       = 0
        needs_hitl       = $false
        parked_artifact  = $null
        park_reason      = $null
        hitl_decision    = $null
        job_id           = $null
        spent            = @{ turns = 0; tokens = 0 }
        stop_reason      = $null
    }
}

function Save-CiscoSESession {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        $Session
    )
    Initialize-CiscoSEHomeDirs
    $table = ConvertTo-CiscoSETable -Value $Session
    $id = 'default'
    if ($table.ContainsKey('session_id') -and $table.session_id) {
        $id = [string]$table.session_id
    }
    $path = Get-CiscoSEPath -Name session -SessionId $id
    Write-CiscoSEJsonFile -Path $path -Value $table
    return $path
}

function Read-CiscoSESession {
    [CmdletBinding()]
    param(
        [string]$SessionId = 'default'
    )
    $path = Get-CiscoSEPath -Name session -SessionId $SessionId
    $obj = Read-CiscoSEJsonFile -Path $path -Default $null
    if ($null -eq $obj) {
        return (New-CiscoSESession -SessionId $SessionId)
    }
    $table = ConvertTo-CiscoSETable -Value $obj
    if (-not $table.ContainsKey('session_id') -or -not $table.session_id) {
        $table.session_id = $SessionId
    }
    if (-not $table.ContainsKey('messages') -or $null -eq $table.messages) {
        $table.messages = @()
    }
    else {
        $table.messages = ConvertTo-CiscoSEList -Value $table.messages
    }
    if (-not $table.ContainsKey('needs_hitl')) { $table.needs_hitl = $false }
    if (-not $table.ContainsKey('spent') -or $null -eq $table.spent) {
        $table.spent = @{ turns = 0; tokens = 0 }
    }
    else {
        $table.spent = ConvertTo-CiscoSETable -Value $table.spent
    }
    return $table
}

function Add-CiscoSESessionMessage {
    [CmdletBinding()]
    param(
        $Session,
        $Message
    )
    $existing = ConvertTo-CiscoSEList -Value $Session.messages
    $add = ConvertTo-CiscoSEList -Value $Message
    $Session.messages = $existing + $add
    return $Session
}

function Add-CiscoSESystemContext {
    [CmdletBinding()]
    param(
        $Session,
        [string]$Text
    )
    if ([string]::IsNullOrWhiteSpace($Text)) { return $Session }
    $msgs = ConvertTo-CiscoSEList -Value $Session.messages
    $next = @()
    $found = $false
    foreach ($m in $msgs) {
        $t = ConvertTo-CiscoSETable -Value $m
        if (-not $found -and [string]$t.role -eq 'system') {
            $t.content = ([string]$t.content + "`n`n" + $Text)
            $found = $true
            $next += $t
        }
        else {
            $next += $t
        }
    }
    if (-not $found) {
        $next = @(@{ role = 'system'; content = $Text }) + $next
    }
    $Session.messages = ConvertTo-CiscoSEList -Value $next
    return $Session
}
