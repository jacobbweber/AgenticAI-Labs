# Cisco Solutions Engineer Agent

Per-user PowerShell agent for Cisco pre-sales design work. The CLI is the front door. It talks to a LAN Ollama host, runs a ReAct tool loop, and writes session JSON, facts, skills, artifacts, and a jobs table under a user home directory.

The system prompt is [`prompts/operating-manual.md`](prompts/operating-manual.md). Code does not ship a second persona.

Workflows are named steps in that manual — **discovery → HLD → LLD → BoM** — not a graph runtime.

## Install

From this folder, in Windows PowerShell 5.1 or PowerShell 7:

```powershell
Import-Module .\CiscoEngineerAgent\CiscoEngineerAgent.psd1
Install-CiscoEngineerAgent
```

Install creates `$env:LOCALAPPDATA\CiscoEngineerAgent` (override with `$env:CISCO_SE_HOME`), writes `config.json`, and copies Skills plus the operating manual into that home.

## Environment and defaults

| Name | Default |
|---|---|
| `CISCO_SE_HOME` | `$env:LOCALAPPDATA\CiscoEngineerAgent` |
| `CISCO_SE_HOST` | `http://192.168.1.29:11434` |
| `CISCO_SE_MODEL` | `qwen3.8:latest` |
| `CISCO_SE_TIMEOUT` | `300` (seconds) |
| `CISCO_SE_INTEGRATION` | unset; set to `1` to run the LAN test |

`Get-CiscoSEConfig` shows the merged file + env values. Timeout is 300s. Failed POSTs retry with exponential backoff (labs ch 11).

## Chat

```powershell
Invoke-CiscoSE -Message "Open a discovery note: 200 user campus, existing Palo Alto edge, need SD-Access vs keep PAN. Do not invent SKUs."
Get-CiscoSESession
Get-CiscoSEJob
```

`-SessionId` defaults to `default`. Sessions live as JSON under the home `sessions` folder.

Tools the model may call: `remember_fact`, `recall_facts`, `load_skill`, `save_artifact`, `build_bom_draft`, `park_for_approval`.

`build_bom_draft` runs only after an LLD artifact exists. Every price is `[UNVERIFIED]`. The agent never invents SKUs.

## HITL (human in the loop)

Some work must stop for a person:

- Customer-ready / send documents
- Final BoM (unlocked from draft)
- Live lab or production changes

The model calls `park_for_approval`. The session and job go to `needs_hitl`. The CLI returns instead of pretending the doc was sent.

```powershell
Invoke-CiscoSE -Message "approve the parked BoM" -Approve
Invoke-CiscoSE -Message "reject the parked BoM" -Deny
Resume-CiscoSEJob -JobId job-1 -Approved
Resume-CiscoSEJob -JobId job-1 -Denied
```

## CCW is human-side

There is no Cisco Commerce Workspace or dCloud API in this module. List prices and SKUs stay `[UNVERIFIED]` until a human confirms them in CCW or a partner tool. Do not treat a BoM draft as a quote.

## Tests

Pester 5. Unit tests do **not** use the network.

```powershell
# unit (mock HTTP)
Invoke-Pester -Path .\tests\CiscoEngineerAgent.Tests.ps1

# integration (LAN Ollama at 192.168.1.29, model qwen3.8:latest, 300s)
$env:CISCO_SE_INTEGRATION = '1'
Invoke-Pester -Path .\tests\Integration.Ollama.Tests.ps1
```

Or exclude the integration tag from a folder run:

```powershell
Invoke-Pester -Path .\tests -ExcludeTag Integration
```
