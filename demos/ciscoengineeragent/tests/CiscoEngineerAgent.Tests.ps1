# Pester 5 — unit tests. No network.
BeforeAll {
    $script:SeHome = Join-Path $TestDrive 'CiscoEngineerAgent'
    $env:CISCO_SE_HOME = $script:SeHome
    $module = Join-Path $PSScriptRoot (Join-Path '..' (Join-Path 'CiscoEngineerAgent' 'CiscoEngineerAgent.psd1'))
    Import-Module $module -Force
    Install-CiscoEngineerAgent | Out-Null
}

AfterAll {
    Remove-Module CiscoEngineerAgent -ErrorAction SilentlyContinue
}

Describe 'Demux-ThinkTags' {
    It 'removes think fences and returns visible text' {
        InModuleScope CiscoEngineerAgent {
            $r = Demux-ThinkTags -Text "<think>hidden plan</think>visible answer"
            $r.thinking | Should -Match 'hidden plan'
            $r.response | Should -Be 'visible answer'
            $r.response | Should -Not -Match '<think>'
        }
    }

    It 'strips fenced think blocks' {
        InModuleScope CiscoEngineerAgent {
            $raw = @'
```think
scratch
```
keep me
'@
            $r = Demux-ThinkTags -Text $raw
            $r.response | Should -Match 'keep me'
            $r.response | Should -Not -Match 'scratch'
        }
    }
}

Describe 'Test-CiscoSEBudget' {
    It 'stops on turns before tokens' {
        InModuleScope CiscoEngineerAgent {
            $r = Test-CiscoSEBudget -Budget @{ max_turns = 2; max_tokens = 1000 } -Spent @{ turns = 2; tokens = 10 }
            $r.stop | Should -Be $true
            $r.reason | Should -Be 'max_turns'
        }
    }

    It 'stops on tokens when turns remain' {
        InModuleScope CiscoEngineerAgent {
            $r = Test-CiscoSEBudget -Budget @{ max_turns = 10; max_tokens = 50 } -Spent @{ turns = 1; tokens = 50 }
            $r.stop | Should -Be $true
            $r.reason | Should -Be 'max_tokens'
        }
    }

    It 'is ok under budget' {
        InModuleScope CiscoEngineerAgent {
            $r = Test-CiscoSEBudget -Budget @{ max_turns = 8; max_tokens = 32000 } -Spent @{ turns = 1; tokens = 10 }
            $r.stop | Should -Be $false
            $r.ok | Should -Be $true
        }
    }
}

Describe 'Test-CiscoSECycleDetect' {
    It 'halts when the same tool name+args+result repeats' {
        InModuleScope CiscoEngineerAgent {
            $seen = New-Object System.Collections.Generic.List[string]
            $args = @{ key = 'site'; value = 'hq' }
            $first = Test-CiscoSECycleDetect -ToolName 'remember_fact' -Arguments $args -Result '{"ok":true}' -Seen $seen
            $first.halt | Should -Be $false
            $again = Test-CiscoSECycleDetect -ToolName 'remember_fact' -Arguments $args -Result '{"ok":true}' -Seen $seen
            $again.halt | Should -Be $true
            $again.reason | Should -Be 'cycle'
        }
    }
}

Describe 'Session JSON' {
    It 'saves and loads messages' {
        InModuleScope CiscoEngineerAgent {
            $s = New-CiscoSESession -SessionId 'roundtrip'
            $s.messages = @(@{ role = 'user'; content = 'hello campus' })
            Save-CiscoSESession -Session $s | Out-Null
            $loaded = Read-CiscoSESession -SessionId 'roundtrip'
            $loaded.session_id | Should -Be 'roundtrip'
            @($loaded.messages).Count | Should -Be 1
            $first = ConvertTo-CiscoSETable -Value @($loaded.messages)[0]
            $first.content | Should -Be 'hello campus'
        }
    }

    It 'appends one hashtable as one message' {
        InModuleScope CiscoEngineerAgent {
            $s = New-CiscoSESession -SessionId 'append-one'
            $s = Add-CiscoSESessionMessage -Session $s -Message @{ role = 'system'; content = 'manual' }
            $s = Add-CiscoSESystemContext -Session $s -Text 'skill body'
            $s = Add-CiscoSESessionMessage -Session $s -Message @{ role = 'user'; content = 'hi' }
            $msgs = ConvertTo-CiscoSEList -Value $s.messages
            $msgs.Count | Should -Be 2
            $sys = ConvertTo-CiscoSETable -Value $msgs[0]
            $sys.role | Should -Be 'system'
            $sys.content | Should -Match 'manual'
            $sys.content | Should -Match 'skill body'
            (ConvertTo-CiscoSETable -Value $msgs[1]).role | Should -Be 'user'
        }
    }
}

Describe 'remember_fact / recall_facts' {
    It 'persists a fact and recalls it' {
        InModuleScope CiscoEngineerAgent {
            $null = Invoke-CiscoSETool -Name remember_fact -Arguments @{ key = 'edge'; value = 'palo-alto' }
            $raw = Invoke-CiscoSETool -Name recall_facts -Arguments @{}
            $raw | Should -Match 'palo-alto'
            $obj = $raw | ConvertFrom-Json
            $keys = @($obj.facts | ForEach-Object { $_.key })
            $keys | Should -Contain 'edge'
        }
    }
}

Describe 'load_skill' {
    It 'loads a known skill' {
        InModuleScope CiscoEngineerAgent {
            $raw = Invoke-CiscoSETool -Name load_skill -Arguments @{ id = 'enterprise-networking' }
            $obj = $raw | ConvertFrom-Json
            $obj.loaded | Should -Be $true
            $obj.body | Should -Match 'Never invent SKUs'
        }
    }

    It 'returns error json for an unknown skill' {
        InModuleScope CiscoEngineerAgent {
            $raw = Invoke-CiscoSETool -Name load_skill -Arguments @{ id = 'not-a-skill' }
            $obj = $raw | ConvertFrom-Json
            $obj.loaded | Should -Be $false
            $obj.error | Should -Match 'unknown'
        }
    }
}

Describe 'save_artifact' {
    It 'writes a file under artifacts/kind' {
        InModuleScope CiscoEngineerAgent {
            $raw = Invoke-CiscoSETool -Name save_artifact -Arguments @{
                kind = 'HLD'
                name = 'campus-hld'
                body = '# HLD`n200 user campus'
            }
            $obj = $raw | ConvertFrom-Json
            $obj.ok | Should -Be $true
            Test-Path -LiteralPath $obj.path | Should -Be $true
            (Get-Content -LiteralPath $obj.path -Raw) | Should -Match '200 user campus'
        }
    }
}

Describe 'build_bom_draft' {
    It 'marks UNVERIFIED and does not invent list prices or SKUs' {
        InModuleScope CiscoEngineerAgent {
            $null = Invoke-CiscoSETool -Name save_artifact -Arguments @{
                kind = 'LLD'
                name = 'campus-lld'
                body = "hostname leaf-1`nrole: access switch`nhostname edge-1`n"
            }
            $raw = Invoke-CiscoSETool -Name build_bom_draft -Arguments @{ artifact_name = 'campus-lld' }
            $obj = $raw | ConvertFrom-Json
            $obj.ok | Should -Be $true
            $obj.body | Should -Match '\[UNVERIFIED\]'
            $obj.body | Should -Not -Match '\$\d'
            $obj.body | Should -Not -Match '(?i)list price\s*[:=]\s*\d'
            $obj.body | Should -Not -Match 'C9300-\d+'
            $obj.body | Should -Not -Match 'C9K-'
            Test-Path -LiteralPath $obj.path | Should -Be $true
        }
    }
}

Describe 'park_for_approval / resume' {
    It 'sets needs_hitl and resumes approved or denied' {
        InModuleScope CiscoEngineerAgent {
            $script:CiscoSECurrentSessionId = 'hitl-demo'
            $s = New-CiscoSESession -SessionId 'hitl-demo'
            $job = Add-CiscoSEJob -Prompt 'send BoM' -SessionId 'hitl-demo'
            $s.job_id = $job.job_id
            Save-CiscoSESession -Session $s | Out-Null
            Set-CiscoSEJobStatus -JobId $job.job_id -Status 'running' | Out-Null

            $raw = Invoke-CiscoSETool -Name park_for_approval -Arguments @{
                artifact_name = 'campus-bom'
                reason        = 'final BoM'
            }
            $park = $raw | ConvertFrom-Json
            $park.needs_hitl | Should -Be $true
            $loaded = Read-CiscoSESession -SessionId 'hitl-demo'
            $loaded.needs_hitl | Should -Be $true
            $loaded.park_reason | Should -Be 'final BoM'
            (Find-CiscoSEJob -JobId $job.job_id).status | Should -Be 'needs_hitl'

            $approved = Invoke-CiscoSEHitlResume -SessionId 'hitl-demo' -Approved $true
            $approved.needs_hitl | Should -Be $false
            $approved.hitl_decision | Should -Be 'approved'
            (Find-CiscoSEJob -JobId $job.job_id).status | Should -Be 'done'

            $script:CiscoSECurrentSessionId = 'hitl-deny'
            $s2 = New-CiscoSESession -SessionId 'hitl-deny'
            $job2 = Add-CiscoSEJob -Prompt 'send HLD' -SessionId 'hitl-deny'
            $s2.job_id = $job2.job_id
            Save-CiscoSESession -Session $s2 | Out-Null
            $null = Invoke-CiscoSETool -Name park_for_approval -Arguments @{
                artifact_name = 'campus-hld'
                reason        = 'customer-ready'
            }
            $denied = Invoke-CiscoSEHitlResume -SessionId 'hitl-deny' -Approved $false
            $denied.hitl_decision | Should -Be 'denied'
            (Find-CiscoSEJob -JobId $job2.job_id).status | Should -Be 'failed'
        }
    }
}

Describe 'Invoke-OllamaChat retries' {
    It 'retries on 5xx then returns the 200 body' {
        InModuleScope CiscoEngineerAgent {
            $script:CiscoSEBackoffSeconds = 0
            $script:HttpHits = 0
            Mock Invoke-CiscoSEHttp {
                $script:HttpHits++
                if ($script:HttpHits -lt 3) {
                    return @{ StatusCode = 503; Content = 'busy' }
                }
                $ok = '{"message":{"role":"assistant","content":"ok-from-mock"},"eval_count":3,"prompt_eval_count":2}'
                return @{ StatusCode = 200; Content = $ok }
            }
            $cfg = @{
                host        = 'http://192.168.1.29:11434'
                model       = 'qwen3.8:latest'
                timeout_sec = 300
                max_retries = 2
            }
            $r = Invoke-OllamaChat -Messages @(@{ role = 'user'; content = 'hi' }) -Tools @() -Config $cfg
            $script:HttpHits | Should -Be 3
            $r.message.content | Should -Be 'ok-from-mock'
            $script:CiscoSEBackoffSeconds = $null
        }
    }
}

Describe 'tool grant' {
    It 'unknown tool name returns error json and does not throw' {
        InModuleScope CiscoEngineerAgent {
            { Invoke-CiscoSETool -Name 'not_a_real_tool' -Arguments @{} } | Should -Not -Throw
            $raw = Invoke-CiscoSETool -Name 'not_a_real_tool' -Arguments @{}
            $obj = $raw | ConvertFrom-Json
            $obj.error | Should -Match 'unknown'
            $obj.name | Should -Be 'not_a_real_tool'
        }
    }
}

Describe 'ConvertTo-CiscoSEJson' {
    It 'keeps a single hashtable inside an array' {
        InModuleScope CiscoEngineerAgent {
            $rows = @()
            $rows += @{ key = 'edge'; value = 'palo-alto' }
            $json = ConvertTo-CiscoSEJson -Value $rows
            $json | Should -Match '^\['
            $obj = $json | ConvertFrom-Json
            @($obj).Count | Should -Be 1
            $obj[0].key | Should -Be 'edge'
        }
    }
}

Describe 'Get-CiscoSEConfig' {
    It 'defaults to LAN host and qwen3.8:latest' {
        $cfg = Get-CiscoSEConfig
        $cfg.host | Should -Be 'http://192.168.1.29:11434'
        $cfg.model | Should -Be 'qwen3.8:latest'
        $cfg.timeout_sec | Should -Be 300
    }
}
