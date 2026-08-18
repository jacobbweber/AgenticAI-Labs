function Get-CiscoSEConfig {
    <#
    .SYNOPSIS
        Returns merged config (defaults, config.json, env overlays).
    #>
    [CmdletBinding()]
    param()
    $file = $null
    try {
        $path = Get-CiscoSEPath -Name config
        $file = Read-CiscoSEJsonFile -Path $path -Default $null
    }
    catch {
        $file = $null
    }
    return (Merge-CiscoSEConfig -FileConfig $file)
}
