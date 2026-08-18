function Get-CiscoSECycleHash {
    [CmdletBinding()]
    param(
        [string]$ToolName,
        $Arguments,
        [string]$Result
    )
    $argJson = ConvertTo-CiscoSEJson -Value $(if ($null -eq $Arguments) { @{} } else { $Arguments })
    $raw = "$ToolName|$argJson|$Result"
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($raw)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $hash = $sha.ComputeHash($bytes)
        return (([BitConverter]::ToString($hash) -replace '-', '').ToLowerInvariant())
    }
    finally {
        $sha.Dispose()
    }
}

function Test-CiscoSECycleDetect {
    [CmdletBinding()]
    param(
        [string]$ToolName,
        $Arguments,
        [string]$Result,
        [System.Collections.IList]$Seen
    )
    $hash = Get-CiscoSECycleHash -ToolName $ToolName -Arguments $Arguments -Result $Result
    if ($null -eq $Seen) {
        return @{ halt = $false; hash = $hash }
    }
    if ($Seen -contains $hash) {
        return @{ halt = $true; reason = 'cycle'; hash = $hash }
    }
    [void]$Seen.Add($hash)
    return @{ halt = $false; hash = $hash }
}
