# Lab {N}: {Title}

One sentence. What you will have running when this lab is done.
This file is the brief. It is short. It does not reteach the module. Read the module first.

## What you touch
Bullets only. The literals this script uses.

- Script: `labN_name.py`
- URL / path:
- Keys sent:
- Keys read:

## Steps
The procedure. Numbered. This is the only long section.
Each step is one action. No extra paragraphs.
A small mermaid is optional, above the numbers, if the hops help.

1.
2.
3.

## Data contract
Only the keys this script sends and reads. Not the full provider catalog.

**Request**

```json
{}
```

**Response**

```json
{}
```

## Run
From the repo root:

```bash
python education/{chapter}/labN_name.py
```

```powershell
$env:OLLAMA_HOST="http://192.168.1.29:11434"
$env:OLLAMA_MODEL="qwen3.6:35b-a3b-65k"
python education/{chapter}/labN_name.py
```

## What you should see
Expected prints. One "if this fails" line.

## Stop here
What this lab is not. What not to add.
One sentence on the next lab or chapter that reuses this script.

## Notes
Results from a real run. Metrics if you have them. Questions that came up while running.
Do not put module teaching here.

<!-- Related is optional. Default: omit. Add it only if this script touches a sibling (example: /api/chat vs /api/generate). One or two sentences. -->
