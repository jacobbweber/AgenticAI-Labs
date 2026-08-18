# Pester 5 — LAN Ollama. Skip unless CISCO_SE_INTEGRATION=1.
$script:IntegrationOn = ($env:CISCO_SE_INTEGRATION -eq '1')

BeforeAll {
    if ($env:CISCO_SE_INTEGRATION -eq '1') {
        $script:SeHome = Join-Path ([System.IO.Path]::GetTempPath()) ('cse-int-' + [guid]::NewGuid().ToString('N'))
        $env:CISCO_SE_HOME = $script:SeHome
        $module = Join-Path $PSScriptRoot (Join-Path '..' (Join-Path 'CiscoEngineerAgent' 'CiscoEngineerAgent.psd1'))
        Import-Module $module -Force
        Install-CiscoEngineerAgent | Out-Null
    }
}

AfterAll {
    if ($env:CISCO_SE_INTEGRATION -eq '1') {
        Remove-Module CiscoEngineerAgent -ErrorAction SilentlyContinue
    }
}

Describe 'LAN Ollama' -Tag 'Integration' {
    It 'installs and Invoke-CiscoSE returns visible text from 192.168.1.29 qwen3.8:latest' -Skip:(-not $script:IntegrationOn) {
        $cfg = Get-CiscoSEConfig
        $cfg.host | Should -Be 'http://192.168.1.29:11434'
        $cfg.model | Should -Be 'qwen3.8:latest'
        $cfg.timeout_sec | Should -Be 300

        $prompt = 'Open a discovery note: 200 user campus, existing Palo Alto edge, need SD-Access vs keep PAN. Do not invent SKUs.'
        $text = Invoke-CiscoSE -Message $prompt
        $text | Should -BeOfType [string]
        $text.Trim().Length | Should -BeGreaterThan 0
        $text | Should -Not -Match '(?s)^\s*<think>.*</think>\s*$'

        $demux = InModuleScope CiscoEngineerAgent -Parameters @{ Raw = $text } {
            Demux-ThinkTags -Text $Raw
        }
        $demux.response | Should -Not -BeNullOrEmpty
        $demux.response.Trim().Length | Should -BeGreaterThan 0
    }
}
