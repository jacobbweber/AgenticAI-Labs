# Stub: pretrain a tiny model

[00_pretrain_tiny.md](./00_pretrain_tiny.md) names next-token training on tensors you own, then a write of updated weights. This folder has no `lab0_pretrain_tiny.py`. The labs that did move here start at LoRA (`lab1_lora_qlora.py`), which is an adapter on a frozen base, not a pretrain loop.

A real lab 0 would cover:
- A script such as `lab0_pretrain_tiny.py` next to this file
- A small text file tokenized into token IDs
- A loop that predicts the next ID, prints `loss` as a float, and writes a weight file
- No HTTP POST, no `OLLAMA_HOST`, no LoRA adapter, no GGUF export, no GRPO group

This folder is optional. Finishing a pretrain lab would not unlock chapter 15. This stub is not a full lab. Do not treat it as steps to run.
