function Read-CiscoSEJobs {
    [CmdletBinding()]
    param()
    $path = Get-CiscoSEPath -Name jobs
    $obj = Read-CiscoSEJsonFile -Path $path -Default @()
    return (ConvertTo-CiscoSEList -Value $obj)
}

function Write-CiscoSEJobs {
    [CmdletBinding()]
    param($Jobs)
    Initialize-CiscoSEHomeDirs
    $path = Get-CiscoSEPath -Name jobs
    Write-CiscoSEJsonFile -Path $path -Value (ConvertTo-CiscoSEList -Value $Jobs)
}

function Add-CiscoSEJob {
    [CmdletBinding()]
    param(
        [string]$Prompt,
        [string]$SessionId = 'default'
    )
    $jobs = ConvertTo-CiscoSEList -Value (Read-CiscoSEJobs)
    $row = @{
        job_id          = ('job-' + ($jobs.Count + 1))
        status          = 'pending'
        prompt          = $Prompt
        session_id      = $SessionId
        result          = $null
        proposed_action = $null
    }
    $jobs += $row
    Write-CiscoSEJobs -Jobs $jobs
    return $row
}

function Set-CiscoSEJobStatus {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$JobId,
        [string]$Status,
        $Result,
        $ProposedAction
    )
    $jobs = ConvertTo-CiscoSEList -Value (Read-CiscoSEJobs)
    $found = $false
    $updated = @()
    foreach ($row in $jobs) {
        $t = ConvertTo-CiscoSETable -Value $row
        if ([string]$t.job_id -eq $JobId) {
            $t.status = $Status
            if ($PSBoundParameters.ContainsKey('Result')) { $t.result = $Result }
            if ($PSBoundParameters.ContainsKey('ProposedAction')) { $t.proposed_action = $ProposedAction }
            $found = $true
        }
        $updated += $t
    }
    if (-not $found) {
        return $null
    }
    Write-CiscoSEJobs -Jobs $updated
    foreach ($row in $updated) {
        if ([string]$row.job_id -eq $JobId) { return $row }
    }
    return $null
}

function Find-CiscoSEJob {
    [CmdletBinding()]
    param([string]$JobId)
    foreach ($row in (ConvertTo-CiscoSEList -Value (Read-CiscoSEJobs))) {
        $t = ConvertTo-CiscoSETable -Value $row
        if ([string]$t.job_id -eq $JobId) { return $t }
    }
    return $null
}
