function Resume-CiscoSEJob {
    <#
    .SYNOPSIS
        Resume a parked job as approved (done) or denied (failed).
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$JobId,
        [switch]$Approved,
        [switch]$Denied
    )
    if ($Approved -and $Denied) {
        throw "Specify only one of -Approved or -Denied."
    }
    if (-not $Approved -and -not $Denied) {
        throw "Specify -Approved or -Denied."
    }
    $job = Find-CiscoSEJob -JobId $JobId
    if ($null -eq $job) {
        throw "Job not found: $JobId"
    }
    $sessionId = 'default'
    if ($job.session_id) { $sessionId = [string]$job.session_id }
    $ok = [bool]$Approved
    $session = Invoke-CiscoSEHitlResume -SessionId $sessionId -Approved $ok
    return @{
        job     = (Find-CiscoSEJob -JobId $JobId)
        session = $session
    }
}
