function Get-CiscoSEHome {
    [CmdletBinding()]
    param()
    if (-not [string]::IsNullOrWhiteSpace($env:CISCO_SE_HOME)) {
        return $env:CISCO_SE_HOME
    }
    if (-not [string]::IsNullOrWhiteSpace($env:LOCALAPPDATA)) {
        return (Join-Path $env:LOCALAPPDATA 'CiscoEngineerAgent')
    }
    throw "Set CISCO_SE_HOME or LOCALAPPDATA for the per-user install home."
}

function Get-CiscoSEPath {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [ValidateSet('home', 'config', 'facts', 'jobs', 'sessions', 'artifacts', 'prompts', 'skills', 'manual', 'session')]
        [string]$Name,
        [string]$SessionId
    )
    $seHome = Get-CiscoSEHome
    switch ($Name) {
        'home' { return $seHome }
        'config' { return (Join-Path $seHome 'config.json') }
        'facts' { return (Join-Path $seHome 'facts.json') }
        'jobs' { return (Join-Path $seHome 'jobs.json') }
        'sessions' { return (Join-Path $seHome 'sessions') }
        'artifacts' { return (Join-Path $seHome 'artifacts') }
        'prompts' { return (Join-Path $seHome 'prompts') }
        'skills' { return (Join-Path $seHome 'Skills') }
        'manual' { return (Join-Path (Join-Path $seHome 'prompts') 'operating-manual.md') }
        'session' {
            if ([string]::IsNullOrWhiteSpace($SessionId)) { $SessionId = 'default' }
            $safe = Get-CiscoSESafeName -Name $SessionId
            return (Join-Path (Join-Path $seHome 'sessions') ($safe + '.json'))
        }
    }
}

function Get-CiscoSESafeName {
    [CmdletBinding()]
    param([string]$Name)
    if ([string]::IsNullOrWhiteSpace($Name)) { return 'unnamed' }
    $clean = $Name -replace '[\\/:\*\?"<>\|]', '_'
    $clean = $clean.Trim()
    if ([string]::IsNullOrWhiteSpace($clean)) { return 'unnamed' }
    return $clean
}

function Initialize-CiscoSEHomeDirs {
    [CmdletBinding()]
    param()
    $seHome = Get-CiscoSEHome
    $dirs = @(
        $seHome,
        (Get-CiscoSEPath -Name sessions),
        (Get-CiscoSEPath -Name artifacts),
        (Get-CiscoSEPath -Name prompts),
        (Get-CiscoSEPath -Name skills)
    )
    foreach ($kind in $script:CiscoSEArtifactKinds) {
        $dirs += (Join-Path (Get-CiscoSEPath -Name artifacts) $kind)
    }
    foreach ($d in $dirs) {
        if (-not (Test-Path -LiteralPath $d)) {
            New-Item -ItemType Directory -Path $d -Force | Out-Null
        }
    }
}

function Get-CiscoSEDefaultConfig {
    [CmdletBinding()]
    param()
    return @{
        host         = 'http://192.168.1.29:11434'
        model        = 'qwen3.8:latest'
        timeout_sec  = 300
        max_retries  = 2
        max_turns    = 8
        max_tokens   = 32000
    }
}

function Merge-CiscoSEConfig {
    [CmdletBinding()]
    param($FileConfig)
    $cfg = Get-CiscoSEDefaultConfig
    if ($null -ne $FileConfig) {
        $table = ConvertTo-CiscoSETable -Value $FileConfig
        foreach ($k in @('host', 'model', 'timeout_sec', 'max_retries', 'max_turns', 'max_tokens')) {
            if ($table.ContainsKey($k) -and $null -ne $table[$k]) {
                $cfg[$k] = $table[$k]
            }
        }
    }
    if (-not [string]::IsNullOrWhiteSpace($env:CISCO_SE_HOST)) {
        $cfg.host = $env:CISCO_SE_HOST.TrimEnd('/')
    }
    if (-not [string]::IsNullOrWhiteSpace($env:CISCO_SE_MODEL)) {
        $cfg.model = $env:CISCO_SE_MODEL
    }
    if (-not [string]::IsNullOrWhiteSpace($env:CISCO_SE_TIMEOUT)) {
        $cfg.timeout_sec = [int]$env:CISCO_SE_TIMEOUT
    }
    $cfg.host = ([string]$cfg.host).TrimEnd('/')
    $cfg.timeout_sec = [int]$cfg.timeout_sec
    $cfg.max_retries = [int]$cfg.max_retries
    $cfg.max_turns = [int]$cfg.max_turns
    $cfg.max_tokens = [int]$cfg.max_tokens
    $cfg.home = Get-CiscoSEHome
    return $cfg
}

function Get-CiscoSESystemPrompt {
    [CmdletBinding()]
    param()
    $manualPath = Get-CiscoSEPath -Name manual
    if (-not (Test-Path -LiteralPath $manualPath)) {
        $bundled = Join-Path (Split-Path -Parent $script:CiscoSEModuleRoot) (Join-Path 'prompts' 'operating-manual.md')
        $manualPath = $bundled
    }
    $manual = ''
    if (Test-Path -LiteralPath $manualPath) {
        $manual = [System.IO.File]::ReadAllText($manualPath)
    }
    $steps = $script:CiscoSEWorkflowSteps -join ' -> '
    $wrapper = "Follow the operating manual exactly. Workflows are named steps: $steps."
    return ($wrapper + "`n`n" + $manual)
}
