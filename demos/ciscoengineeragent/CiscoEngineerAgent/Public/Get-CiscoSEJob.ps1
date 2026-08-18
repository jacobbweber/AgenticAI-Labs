function Get-CiscoSEJob {
    <#
    .SYNOPSIS
        Returns the jobs table, or one job by id.
    #>
    [CmdletBinding()]
    param(
        [string]$JobId
    )
    if ([string]::IsNullOrWhiteSpace($JobId)) {
        return (ConvertTo-CiscoSEList -Value (Read-CiscoSEJobs))
    }
    return (Find-CiscoSEJob -JobId $JobId)
}
