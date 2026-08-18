function Demux-ThinkTags {
    [CmdletBinding()]
    param(
        [AllowNull()]
        [AllowEmptyString()]
        [string]$Text
    )
    if ([string]::IsNullOrEmpty($Text)) {
        return [pscustomobject]@{ thinking = ''; response = '' }
    }
    $thinkingParts = New-Object System.Collections.Generic.List[string]
    $response = $Text

    $fence = [regex]::new('(?is)```(?:think|thinking)\s*\r?\n.*?```', [System.Text.RegularExpressions.RegexOptions]::Singleline)
    foreach ($m in $fence.Matches($response)) {
        $inner = $m.Value
        $inner = $inner -replace '(?is)^```(?:think|thinking)\s*\r?\n', ''
        $inner = $inner -replace '(?is)```\s*$', ''
        $thinkingParts.Add($inner.Trim())
    }
    $response = $fence.Replace($response, '')

    $tag = [regex]::new('(?is)<think>(.*?)</think>', [System.Text.RegularExpressions.RegexOptions]::Singleline)
    foreach ($m in $tag.Matches($response)) {
        $thinkingParts.Add($m.Groups[1].Value.Trim())
    }
    $response = $tag.Replace($response, '')
    $response = [regex]::Replace($response, '(?is)</?think>', '')

    return [pscustomobject]@{
        thinking = (($thinkingParts | Where-Object { $_ }) -join "`n").Trim()
        response = $response.Trim()
    }
}

function Test-CiscoSEVisibleText {
    [CmdletBinding()]
    param([string]$Text)
    $d = Demux-ThinkTags -Text $Text
    return -not [string]::IsNullOrWhiteSpace($d.response)
}
