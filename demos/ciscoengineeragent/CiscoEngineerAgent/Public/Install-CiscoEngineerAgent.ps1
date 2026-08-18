function Install-CiscoEngineerAgent {
    <#
    .SYNOPSIS
        Creates the per-user Cisco SE agent home, config, skills, and operating manual.
    #>
    [CmdletBinding()]
    param()
    Initialize-CiscoSEHomeDirs
    $bundledManual = Join-Path (Split-Path -Parent $script:CiscoSEModuleRoot) (Join-Path 'prompts' 'operating-manual.md')
    $destManual = Get-CiscoSEPath -Name manual
    if (Test-Path -LiteralPath $bundledManual) {
        Copy-Item -LiteralPath $bundledManual -Destination $destManual -Force
    }
    $bundledSkills = Join-Path $script:CiscoSEModuleRoot 'Skills'
    $destSkills = Get-CiscoSEPath -Name skills
    if (Test-Path -LiteralPath $bundledSkills) {
        Get-ChildItem -Path $bundledSkills -Filter '*.md' | ForEach-Object {
            Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $destSkills $_.Name) -Force
        }
    }
    $configPath = Get-CiscoSEPath -Name config
    if (-not (Test-Path -LiteralPath $configPath)) {
        Write-CiscoSEJsonFile -Path $configPath -Value (Get-CiscoSEDefaultConfig)
    }
    if (-not (Test-Path -LiteralPath (Get-CiscoSEPath -Name facts))) {
        Write-CiscoSEJsonFile -Path (Get-CiscoSEPath -Name facts) -Value @()
    }
    if (-not (Test-Path -LiteralPath (Get-CiscoSEPath -Name jobs))) {
        Write-CiscoSEJsonFile -Path (Get-CiscoSEPath -Name jobs) -Value @()
    }
    return (Get-CiscoSEHome)
}
