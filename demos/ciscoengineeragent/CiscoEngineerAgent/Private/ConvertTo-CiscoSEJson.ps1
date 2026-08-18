function ConvertTo-CiscoSEJson {
    [CmdletBinding()]
    param(
        $Value,
        [int]$Depth = 20
    )
    function Encode-CiscoSEJsonValue {
        param($V, [int]$D)
        if ($D -lt 0) { return 'null' }
        if ($null -eq $V) { return 'null' }
        if ($V -is [bool]) {
            if ($V) { return 'true' } else { return 'false' }
        }
        if ($V -is [byte] -or $V -is [int16] -or $V -is [uint16] -or $V -is [int] -or $V -is [long] -or $V -is [uint32] -or $V -is [uint64] -or $V -is [double] -or $V -is [decimal] -or $V -is [single]) {
            return ([string]$V)
        }
        if ($V -is [datetime]) {
            $s = $V.ToString('o')
            return ('"' + $s + '"')
        }
        if ($V -is [string]) {
            $escaped = $V.Replace('\', '\\').Replace('"', '\"').Replace("`r", '\r').Replace("`n", '\n').Replace("`t", '\t')
            return ('"' + $escaped + '"')
        }
        if ($V -is [System.Collections.IDictionary]) {
            $parts = New-Object System.Collections.Generic.List[string]
            foreach ($k in $V.Keys) {
                $parts.Add(('"' + [string]$k + '":' + (Encode-CiscoSEJsonValue -V $V[$k] -D ($D - 1))))
            }
            return ('{' + ($parts -join ',') + '}')
        }
        if ($V -is [System.Collections.IEnumerable] -and -not ($V -is [string]) -and -not ($V -is [System.Collections.IDictionary])) {
            $parts = New-Object System.Collections.Generic.List[string]
            foreach ($item in $V) {
                [void]$parts.Add((Encode-CiscoSEJsonValue -V $item -D ($D - 1)))
            }
            return ('[' + ($parts -join ',') + ']')
        }
        if ($V -is [pscustomobject]) {
            $parts = New-Object System.Collections.Generic.List[string]
            foreach ($p in $V.PSObject.Properties) {
                $parts.Add(('"' + $p.Name + '":' + (Encode-CiscoSEJsonValue -V $p.Value -D ($D - 1))))
            }
            return ('{' + ($parts -join ',') + '}')
        }
        return (Encode-CiscoSEJsonValue -V ([string]$V) -D $D)
    }
    return (Encode-CiscoSEJsonValue -V $Value -D $Depth)
}

function ConvertTo-CiscoSETable {
    [CmdletBinding()]
    param($Value)
    if ($null -eq $Value) { return @{} }
    if ($Value -is [hashtable]) { return $Value }
    if ($Value -is [System.Collections.IDictionary]) {
        $h = @{}
        foreach ($k in $Value.Keys) { $h[$k] = $Value[$k] }
        return $h
    }
    if ($Value -is [string]) {
        if ([string]::IsNullOrWhiteSpace($Value)) { return @{} }
        $parsed = $Value | ConvertFrom-Json
        return (ConvertTo-CiscoSETable -Value $parsed)
    }
    $h = @{}
    foreach ($p in $Value.PSObject.Properties) {
        $h[$p.Name] = $p.Value
    }
    return $h
}

function Get-CiscoSEArg {
    [CmdletBinding()]
    param(
        $Arguments,
        [string[]]$Names,
        $Default = $null
    )
    $table = ConvertTo-CiscoSETable -Value $Arguments
    foreach ($n in $Names) {
        if ($table.ContainsKey($n) -and $null -ne $table[$n]) {
            return $table[$n]
        }
    }
    return $Default
}

function Write-CiscoSEJsonFile {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        $Value
    )
    $dir = Split-Path -Parent $Path
    if ($dir -and -not (Test-Path -LiteralPath $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    $json = [string](ConvertTo-CiscoSEJson -Value $Value)
    [System.IO.File]::WriteAllText($Path, $json)
}

function Read-CiscoSEJsonFile {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        $Default = $null
    )
    if (-not (Test-Path -LiteralPath $Path)) {
        return $Default
    }
    $raw = [System.IO.File]::ReadAllText($Path)
    if ([string]::IsNullOrWhiteSpace($raw)) {
        return $Default
    }
    $parsed = $raw | ConvertFrom-Json
    if ($null -eq $parsed) {
        return $Default
    }
    return $parsed
}

function ConvertTo-CiscoSEList {
    [CmdletBinding()]
    param($Value)
    $acc = New-Object 'System.Collections.Generic.List[System.Object]'
    if ($null -eq $Value) {
        return ,([object[]]@())
    }
    # A hashtable is one row. @($hashtable) or foreach-on-IEnumerable would walk keys.
    if ($Value -is [System.Collections.IDictionary]) {
        $acc.Add($Value)
        return ,$acc.ToArray()
    }
    if ($Value -is [string]) {
        $acc.Add($Value)
        return ,$acc.ToArray()
    }
    if ($Value -is [System.Collections.IEnumerable]) {
        foreach ($item in $Value) {
            if ($null -ne $item) {
                $acc.Add($item)
            }
        }
        return ,$acc.ToArray()
    }
    $acc.Add($Value)
    return ,$acc.ToArray()
}
