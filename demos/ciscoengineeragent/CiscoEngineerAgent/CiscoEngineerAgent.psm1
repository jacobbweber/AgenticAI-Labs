# CiscoEngineerAgent — CLI front door (labs ch 10). Persona lives in operating-manual.md.
$script:CiscoSEModuleRoot = $PSScriptRoot
$script:CiscoSEBackoffSeconds = $null
$script:CiscoSECurrentSessionId = 'default'
$script:CiscoSEWorkflowSteps = @('discovery', 'HLD', 'LLD', 'BoM')
$script:CiscoSEArtifactKinds = @('HLD', 'LLD', 'BoM', 'PoC', 'RFP', 'Discovery')
$script:CiscoSEAllowedTools = @(
    'remember_fact',
    'recall_facts',
    'load_skill',
    'save_artifact',
    'build_bom_draft',
    'park_for_approval'
)

$privateDir = Join-Path $PSScriptRoot 'Private'
$publicDir = Join-Path $PSScriptRoot 'Public'

Get-ChildItem -Path $privateDir -Filter '*.ps1' -ErrorAction Stop |
    Sort-Object Name |
    ForEach-Object { . $_.FullName }

Get-ChildItem -Path $publicDir -Filter '*.ps1' -ErrorAction Stop |
    Sort-Object Name |
    ForEach-Object { . $_.FullName }

Export-ModuleMember -Function @(
    'Install-CiscoEngineerAgent',
    'Get-CiscoSEConfig',
    'Invoke-CiscoSE',
    'Get-CiscoSESession',
    'Get-CiscoSEJob',
    'Resume-CiscoSEJob'
)
