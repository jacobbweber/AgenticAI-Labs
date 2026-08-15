# OT: Pretrain a tiny LLM

This folder is optional. It is not on the 00–15 path. After this page you can name the three objects in a pretrain step: the tokenized tensors, the train loop, and the weight file it writes. That is not an agent chapter. Finishing this page does not unlock chapter 15.

## Data
Three objects exist, and they are not the same as chapter 00.

A **corpus** is text you tokenize into tensors (arrays of token IDs). Those IDs are the data. There is no HTTP POST. There is no `OLLAMA_HOST`. Lab 0 uses three strings: `aba`, `abc`, `cab`. Tokens are characters. Vocab size is 3.

A **train loop** is a Python process that reads a batch of those IDs, predicts the next ID, compares the prediction to the real next ID, and computes a **loss** (one float). It then updates the weight numbers so the next prediction is closer. Lab 0 is a `V` by `V` logit table plus `softmax` and a mean `-log(p[next])`.

A **weight file** is the same kind of file chapter 00 named (`.safetensors` or `.gguf`). After a train step the numbers inside it have changed. Chapter 00 never writes that file. This page does. Lab 0 writes `weights.json` with `stoi` and `W`.

Lab 0 is `lab0_pretrain_tiny.py`. Functions: `build_vocab`, `make_pairs`, `softmax`, `train_step`, `train`. `steps` is 40. `lr` is 0.5. CPU only. No Hugging Face. The runnable labs that also live here are LoRA, GGUF, and GRPO.

## Information
The only path on this page is:

tokenized tensors → train loop → loss (float) → optimizer step → updated weights on disk

Chapter 00 is a different path:

script → HTTP POST (JSON) → provider at `192.168.1.29:11434` → JSON `response` → script

If you are calling Ollama with `OLLAMA_HOST` (`http://192.168.1.29:11434`) and `OLLAMA_MODEL` (`qwen3.6:35b-a3b-65k`), you are not pretraining. You are using a provider that already loaded someone else's weights.

## Knowledge
1. Confirm you actually want to train. The 00–15 line never requires this folder.
2. Tokenize a small text file into token IDs. A first pretrain uses a small file, not a large crawl. Lab 0 tokenizes three short strings.
3. Run a loop: take a window of IDs, predict the next ID, compute `loss` as a float, step the optimizer, write weights.
4. Read `loss` after each step. If it is not a number, the loop is not training.
5. Stop when `loss` has gone down on that small file. Do not start LoRA, GGUF, or GRPO on this page.

## Wisdom
Skip this folder unless you care about training. It is optional. Finishing it does not unlock chapter 15. If you only need a model to answer, go back to [00_script_provider_weights.md](../00_atoms/00_script_provider_weights.md) and POST to `http://192.168.1.29:11434`.

## The When and Why
- **When:** you want to train weights from text you own, not call a server.
- **Why:** calling a server is chapter 00. Pretrain is the step that creates the weight file that chapter 00 later loads.

## How it works

```mermaid
flowchart TD
    subgraph ot00_disk [Disk in]
        CORP["Tokenized text tensors"]
    end
    subgraph ot00_loop [Train process]
        LOOP["Next-token train loop"]
        LOSS["loss float"]
    end
    subgraph ot00_out [Disk out]
        W["Updated weight file"]
    end
    CORP --> LOOP
    LOOP --> LOSS
    LOOP --> W
```

Walkthrough of one train step:

1. The process reads a batch of token IDs from the tensors on disk.
2. It asks the current weights to predict the next token ID.
3. It compares that prediction to the real next ID and writes one float named `loss`.
4. It updates the weight numbers so `loss` is smaller on the next batch.
5. It writes the new numbers to a weight file.

Walkthrough of lab 0:

1. `build_vocab` maps `a` / `b` / `c` to 0 / 1 / 2.
2. `make_pairs` builds next-char pairs from `aba`, `abc`, `cab`.
3. `train_step` does softmax plus `-log(p[next])` and a gradient step on `W`.
4. After 40 steps, `last_loss` is smaller than `first_loss` (about `math.log(3)` on a zero matrix).
5. `weights.json` holds `stoi` and `W`. No POST. No GPU.

Nothing in that walkthrough opens a port. Nothing sends `model`, `prompt`, or `stream`. Those keys belong to chapter 00.

## Data contract
A train step produces one number. There is no request JSON and no HTTP route.

**Output of one step**

```json
{
  "loss": 0.0
}
```

**Lab 0 train return**

```json
{
  "first_loss": 1.098612,
  "last_loss": 0.4
}
```

`loss` is a float. Lab 0 prints `first_loss` and `last_loss` and writes `weights.json`.

## Lab
Done when `last_loss` is a smaller float than `first_loss` and `weights.json` exists.

- Module: [this file](./00_pretrain_tiny.md)
- Lab 0: [lab0_pretrain_tiny.md](./lab0_pretrain_tiny.md) - write `lab0_pretrain_tiny.py`. Next-token table on three strings. Done when `last_loss < first_loss`.
- Next module: [01_lora_qlora.md](./01_lora_qlora.md) / [lab1_lora_qlora.md](./lab1_lora_qlora.md) - adapter math, not pretrain.

## Related
- **Chapter 00:** you usually just call. Script, provider, weights. POST to `/api/generate`.
- **01_lora_qlora:** adapter matrices over frozen weights. That is finetune, not pretrain.
- **02_gguf:** fewer bits per weight so llama.cpp or Ollama can load the file.
- **03_grpo:** group-relative preference update after a model already exists.

## Notes
- This page was moved from `modules/10/00`. The LoRA, GGUF, and GRPO labs were moved from `modules/10` and `labs/10` into this folder.
- Lab 0 has no reference `.py` yet. The intended contract is `loss` as a number. CPU lists (or numpy) only. Do not edit the `.py` files in the repo.
