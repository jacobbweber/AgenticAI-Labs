@{
    RootModule        = 'CiscoEngineerAgent.psm1'
    ModuleVersion     = '0.1.0'
    GUID              = '7e2c9a14-6b53-4d80-9f1a-3c8e5d2b7041'
    Author            = 'Jacob Weber'
    CompanyName       = 'script-to-agent-labs'
    Copyright         = '(c) Jacob Weber. Local lab use.'
    Description       = 'Cisco Solutions Engineer AI agent. CLI front door to LAN Ollama (ReAct, session JSON, skills, HITL, jobs).'
    PowerShellVersion = '5.1'
    FunctionsToExport = @(
        'Install-CiscoEngineerAgent',
        'Get-CiscoSEConfig',
        'Invoke-CiscoSE',
        'Get-CiscoSESession',
        'Get-CiscoSEJob',
        'Resume-CiscoSEJob'
    )
    CmdletsToExport   = @()
    VariablesToExport = @()
    AliasesToExport   = @()
    PrivateData       = @{
        PSData = @{
            Tags = @('Cisco', 'Ollama', 'Agent', 'ReAct')
        }
    }
}
