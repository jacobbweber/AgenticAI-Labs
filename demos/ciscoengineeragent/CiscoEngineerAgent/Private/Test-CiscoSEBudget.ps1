function Test-CiscoSEBudget {
    [CmdletBinding()]
    param(
        $Budget,
        $Spent
    )
    $b = ConvertTo-CiscoSETable -Value $Budget
    $s = ConvertTo-CiscoSETable -Value $Spent
    $turns = 0
    $tokens = 0
    $maxTurns = 8
    $maxTokens = 32000
    if ($s.ContainsKey('turns')) { $turns = [int]$s.turns }
    if ($s.ContainsKey('tokens')) { $tokens = [int]$s.tokens }
    if ($b.ContainsKey('max_turns')) { $maxTurns = [int]$b.max_turns }
    if ($b.ContainsKey('max_tokens')) { $maxTokens = [int]$b.max_tokens }
    if ($turns -ge $maxTurns) {
        return @{ stop = $true; reason = 'max_turns' }
    }
    if ($tokens -ge $maxTokens) {
        return @{ stop = $true; reason = 'max_tokens' }
    }
    return @{ ok = $true; stop = $false }
}
