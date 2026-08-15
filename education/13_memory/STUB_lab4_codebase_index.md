# Stub: codebase index hits

Chapter 03 is a separate idea from private RAG: walk a repo, store path plus text or symbols, return hits `{ "path", "span" }`. This folder has no lab for that. Lab 3 searches hardcoded document strings and has no `path`. Grep is named as the simple form, then the reader has nothing to run. The missing lab is a small walk-and-print, not a language-server product.

A real lab 4 would cover:
- A script such as `lab4_codebase_index.py` next to this file
- `os.walk` (or `rg --files`) over a tiny tree, for example this `education/13_memory` folder
- Skip `.git` and binary files
- Store `{ "path": "string", "text": "string" }` or a short symbol list (`def` / `class` names)
- Query for one name such as `run_airgapped_private_rag`
- Print hits `{ "path": "string", "span": "string" }` (line range or snippet)
- Optional: stuff the top hit into `prompt` and POST to `{OLLAMA_HOST}/api/generate` (defaults `http://192.168.1.29:11434`, `qwen3.6:35b-a3b-65k`)

Do not add PII redaction, a hosted vector service, a tree-sitter stack, or a new indexer product. Do not treat lab 3 as this lab. This stub is not a full lab. Do not treat it as steps to run.
