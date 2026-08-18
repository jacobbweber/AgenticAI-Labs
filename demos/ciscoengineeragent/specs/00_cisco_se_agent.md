# Cisco SE agent

**Status:** active
**Parent:** script-to-agent-labs ch 03–18 (ReAct, state, skills, HITL, jobs, budget, reliability)

## Goal

Ship a per-user PowerShell Cisco Solutions Engineer agent. The CLI is the front door. It POSTs `messages[]` + `tools` to a LAN Ollama host, runs a ReAct loop, and persists session JSON, episodic facts, skills, artifacts, and a jobs table. The distilled [operating-manual.md](../prompts/operating-manual.md) **is** the system prompt.

## Success check

1. `Install-CiscoEngineerAgent` writes `$env:LOCALAPPDATA\CiscoEngineerAgent` (or `$env:CISCO_SE_HOME`): `config.json`, copied Skills, copied operating manual.
2. `Invoke-CiscoSE` POSTs to the configured host/model (`http://192.168.1.29:11434`, `qwen3.8:latest`, 300s timeout).
3. Tools persist facts and artifacts; `park_for_approval` sets `needs_hitl`.
4. Unit tests mock HTTP (no network). One integration test hits LAN Ollama when `CISCO_SE_INTEGRATION=1`.

## Must-haves

- POST `/api/chat` + `messages[]` + `tools` + ReAct loop (03/04/07)
- Session JSON persist (05/07)
- Skills as markdown loaded on trigger and via `load_skill` (14)
- Episodic facts file (13)
- Artifact save for HLD / LLD / BoM / PoC / RFP / Discovery
- `build_bom_draft` only after LLD; every price `[UNVERIFIED]`; never invent SKUs
- HITL park/resume (09/18) for customer-ready, final BoM, live lab
- Jobs table for long work (16)
- Budget `max_turns` / `max_tokens` with reason (17)
- Cycle hash on tool name+args+result (12)
- CoT demux strip think tags (12)
- CLI is the front door (10)
- Named workflow steps in the prompt/manual: discovery → HLD → LLD → BoM (not a graph runtime)
- Retries with backoff on 5xx/429 (11)

## Non-goals

- FastAPI, Redis, MCP server
- Real Cisco CCW / dCloud APIs
- Invented list prices or SKUs
- LangGraph or any graph engine
- A second persona in code (one-line wrapper around the operating manual only)

## Contracts

### Home and config

| Key | Default |
|---|---|
| Home | `$env:LOCALAPPDATA\CiscoEngineerAgent` or `$env:CISCO_SE_HOME` |
| `host` | `http://192.168.1.29:11434` |
| `model` | `qwen3.8:latest` |
| `timeout_sec` | `300` |
| `max_retries` | `2` (3 attempts, backoff 1/2/4s) |
| `max_turns` | `8` |
| `max_tokens` | `32000` |

Env overlays: `CISCO_SE_HOST`, `CISCO_SE_MODEL`, `CISCO_SE_TIMEOUT`.

### Session JSON

```json
{
  "session_id": "default",
  "messages": [],
  "turn_count": 0,
  "needs_hitl": false,
  "parked_artifact": null,
  "park_reason": null,
  "hitl_decision": null,
  "job_id": null,
  "spent": { "turns": 0, "tokens": 0 },
  "stop_reason": null
}
```

### Tools the model may call

| Name | Args | Result |
|---|---|---|
| `remember_fact` | `key`, `value` | `{ ok, key }` |
| `recall_facts` | (none) | `{ facts: [{key,value}] }` |
| `load_skill` | `id` | `{ loaded, id, body }` or `{ error }` |
| `save_artifact` | `kind`, `name`, `body` | `{ ok, path, kind, name }` |
| `build_bom_draft` | `artifact_name` | `{ ok, path, body }` or `{ error }` |
| `park_for_approval` | `artifact_name`, `reason` | `{ needs_hitl: true, ... }` |

`kind` ∈ `HLD`, `LLD`, `BoM`, `PoC`, `RFP`, `Discovery`.

Unknown tool name → error JSON, do not throw (grant miss).

### Module API

- `Install-CiscoEngineerAgent`
- `Get-CiscoSEConfig`
- `Invoke-CiscoSE -Message <string> [-SessionId default] [-Approve] [-Deny]`
- `Get-CiscoSESession [-SessionId]`
- `Get-CiscoSEJob [-JobId]`
- `Resume-CiscoSEJob -JobId <id> [-Approved] [-Denied]`

### HITL

`park_for_approval` parks the session and the job (`needs_hitl`). Resume with `Invoke-CiscoSE -Approve|-Deny` or `Resume-CiscoSEJob`. Human confirms customer-ready text, final BoM, and live lab. CCW stays human-side.

## Acceptance tests

1. `Demux-ThinkTags` removes think fences.
2. `Test-CiscoSEBudget` stops on turns, then tokens, with a reason.
3. `Test-CiscoSECycleDetect` halts on a repeated tool hash.
4. Session JSON save/load round-trips.
5. `remember_fact` / `recall_facts` persist to the facts file.
6. `load_skill` known vs unknown.
7. `save_artifact` writes a file.
8. `build_bom_draft` marks `[UNVERIFIED]` and invents no list prices / SKUs.
9. `park_for_approval` sets `needs_hitl`; resume approved → done, denied → failed.
10. `Invoke-OllamaChat` retries on 5xx (mocked HTTP).
11. Unknown tool name returns error JSON and does not throw.
12. Integration (`CISCO_SE_INTEGRATION=1`): install + `Invoke-CiscoSE` discovery prompt; non-empty string that is not only think tags; host `192.168.1.29`, model `qwen3.8:latest`, timeout 300s.

## Build order

1. Spec (this file) — operating manual already distilled
2. Home / config / JSON helpers
3. Tools + session + facts + skills + artifacts + jobs
4. Ollama client (retries) + ReAct loop (budget, cycle, demux, HITL)
5. Public CLI
6. Unit tests (mock HTTP)
7. Integration test (LAN Ollama)
