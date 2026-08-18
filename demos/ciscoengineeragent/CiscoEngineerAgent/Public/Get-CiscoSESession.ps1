function Get-CiscoSESession {
    <#
    .SYNOPSIS
        Loads a persisted session JSON document.
    #>
    [CmdletBinding()]
    param(
        [string]$SessionId = 'default'
    )
    return (Read-CiscoSESession -SessionId $SessionId)
}
