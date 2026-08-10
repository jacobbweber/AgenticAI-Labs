# 00: Local LLM Servers: Ollama, vLLM & llama.cpp

## 1. Macro Concept & Industry Need

Relying exclusively on commercial cloud APIs (such as OpenAI, Anthropic, or Google Gemini) introduces severe constraints for autonomous agentic systems: unpredictable token billing during multi-turn agent loops, variable network latency, API rate limits, vendor lock-in, and compliance risks associated with transmitting proprietary code or personal data across external networks. High-performance **Local LLM Inference Engines** solve these challenges by hosting open-weight models locally with zero external API fees, deterministic low-latency execution, and total data privacy.

Modern open-weight model families (such as Llama 3.3, Qwen 2.5, and DeepSeek-R1) offer capabilities matching cloud models for specialized developer tasks. Modern hardware architectures—ranging from consumer Apple Silicon workstations with high-bandwidth Unified Memory (128GB–192GB RAM) to multi-GPU Linux servers—allow teams to run 7B, 14B, 32B, and 70B parameter models concurrently on local infrastructure. Understanding the software engineering primitives powering local inference engines (Ollama, `llama.cpp`, and vLLM) is critical for building enterprise-grade, air-gapped agentic workflows.

---

## 2. Architectural Component Mapping

| AI Jargon / Buzzword | Actual Software Component / Standard Primitive |
| :--- | :--- |
| **Quantization (GGUF / AWQ / EXL2)** | Fixed-point weight compression algorithms (`FP16` $\to$ `INT4`/`INT8`) reducing VRAM footprints by 60%–75% while preserving perplexity via custom CUDA/Metal kernel math. |
| **PagedAttention** | Virtual memory page table manager allocating non-contiguous physical VRAM memory blocks to Key-Value (KV) cache tensors, eliminating VRAM fragmentation and boosting batching concurrency. |
| **OpenAI-Compatible Server** | HTTP REST & SSE middleware translating standardized `/v1/chat/completions` JSON payloads into native C++ engine function calls. |
| **Unified Memory Offloading** | Zero-copy memory-mapped file access (`mmap`) enabling direct shared memory access between CPU cores and integrated Metal GPU pipelines without PCIe bus transfer bottlenecks. |
| **Speculative Decoding** | Dual-model inference pipeline using a lightweight draft model ($M_{draft}$) to generate candidate tokens sequentially, validated in parallel by a target model ($M_{target}$). |

---

## 3. Key Technical Aspects & Dig-In Topics

### 3.1 vLLM PagedAttention & KV Cache Memory Management

Standard transformer decoding suffers from VRAM fragmentation because Key-Value (KV) cache tensors are traditionally allocated in contiguous memory blocks for the maximum context length ($N_{\text{max}}$). This results in 60%–80% VRAM waste. **PagedAttention** (introduced by vLLM) adapts operating system virtual memory paging to KV cache management. 

KV caches are partitioned into fixed-size physical blocks (e.g., 16 tokens per block). A centralized Block Manager maps logical sequence blocks to physical VRAM blocks dynamically:

```
Logical KV Memory (Sequence A)    Physical VRAM Block Table
+-------------------------------+  +--------------------------+
| Block 0 | Block 1 | Block 2   |  | Physical Block 7  (RAM)  |
+-------------------------------+  | Physical Block 12 (RAM)  |
               |                   | Physical Block 3  (RAM)  |
               v                   +--------------------------+
  Virtual Block Allocator ───> Non-Contiguous Physical Memory
```

By decoupling logical context allocation from physical VRAM layouts, PagedAttention eliminates internal fragmentation, enables dynamic copy-on-write memory sharing during parallel beam search / subagent branching, and increases concurrent request batching throughput by 2x–4x.

### 3.2 llama.cpp Multi-GPU Offloading & Apple Silicon Unified Memory

`llama.cpp` powers local execution across heterogeneous hardware via C/C++ implementations of transformer architectures:

- **Apple Silicon Unified Memory**: On M-series chips (Pro, Max, Ultra), CPU cores, Neural Engines, and Metal GPU cores share a single unified physical RAM pool with up to 800 GB/s memory bandwidth. Using zero-copy memory mapping (`mmap`), `llama.cpp` maps GGUF model files directly into GPU-accessible memory without copying weights across a PCIe bus.
- **Multi-GPU Tensor Splitting**: On Linux/Windows workstations with multiple discrete GPUs, `llama.cpp` provides layer-wise and tensor-wise offloading:
  - `--n-gpu-layers N`: Offloads the first $N$ transformer layers to GPU VRAM, executing remaining layers in system CPU RAM.
  - `--tensor-split fraction`: Distributes layer weight tensors across multiple GPUs according to VRAM capacity ratios (e.g., `--tensor-split 0.6,0.4` for an RTX 4090 + RTX 3090 setup).

### 3.3 Speculative Decoding Mechanics & Acceleration

Speculative decoding accelerates inference latency for large target models ($M_{target}$, e.g., Llama-3.3-70B) by pairing them with a smaller, faster draft model ($M_{draft}$, e.g., Llama-3.2-1B):

1. **Draft Generation**: $M_{draft}$ sequentially predicts $K$ candidate tokens ($x_1, x_2, \dots, x_K$) at high speed (e.g., 150 tokens/sec).
2. **Parallel Verification**: $M_{target}$ evaluates all $K$ candidate tokens simultaneously in a single parallel forward pass.
3. **Acceptance Sampling**: The engine compares probability distributions $P_{target}(x)$ and $P_{draft}(x)$. Tokens meeting the rejection sampling criteria are accepted; the first rejected token is resampled from the adjusted distribution, discarding subsequent draft tokens.

```python
# Speculative Decoding Acceptance Loop State Machine
def speculative_step(draft_model, target_model, context, K=4):
    draft_tokens, draft_probs = draft_model.generate_draft(context, K)
    target_probs = target_model.evaluate_parallel(context, draft_tokens)
    
    accepted_tokens = []
    for i in range(K):
        r = random.uniform(0, 1)
        token = draft_tokens[i]
        p_target, p_draft = target_probs[i][token], draft_probs[i][token]
        
        if r < (p_target / p_draft):
            accepted_tokens.append(token)
        else:
            # Resample rejected token from adjusted distribution
            corrected_token = sample_adjusted(target_probs[i], draft_probs[i])
            accepted_tokens.append(corrected_token)
            break
            
    return accepted_tokens
```

Because verification is parallelized across GPU matrix multiplication units, speculative decoding yields 1.5x–2.5x speedups without altering output quality.

### 3.4 Local Server Engine Architecture & Load Balancing

Ollama encapsulates `llama.cpp` inside a Go binary that provides model management, automatic hardware discovery, and REST API serving:

- **Lifecycle Management**: Ollama loads models on demand and unloads them after an idle timeout (`OLLAMA_KEEP_ALIVE`) to free VRAM for other tasks.
- **Concurrent Request Dispatching**: By setting `OLLAMA_NUM_PARALLEL`, Ollama provisions multiple KV cache sequences inside `llama.cpp` to process concurrent subagent HTTP requests without reloading model weights.

---

## 4. Future Lab Blueprint

### Lab 1: Baseline Architecture & Local Server Deployment
- **Objective**: Set up Ollama and `llama.cpp` server instances locally, configuring OpenAI-compatible `/v1/chat/completions` REST endpoints.
- **Tasks**:
  1. Download and deploy `qwen2.5:14b` and `llama3.3:70b` models via Ollama.
  2. Implement a Python benchmark client using the standard `openai` SDK with `base_url="http://localhost:11434/v1"`.
  3. Measure baseline generation latency (time-to-first-token TTFT and tokens-per-second TPS) across both models.

### Lab 2: Intermediate Capability Integration & Speculative Decoding Engine
- **Objective**: Implement a dual-model speculative decoding pipeline using a local draft model and target model.
- **Tasks**:
  1. Pair a 1.5B draft model (`Qwen2.5-1.5B`) with a 70B target model (`Qwen2.5-70B-Instruct`) in `llama.cpp` or vLLM.
  2. Write a verification script that tracks token acceptance rates across code generation and mathematical reasoning prompts.
  3. Benchmark total generation latency gains compared to standalone target model generation.

### Lab 3: Enterprise Resilience & High-Throughput vLLM PagedAttention Benchmark
- **Objective**: Deploy vLLM with PagedAttention to serve concurrent multi-agent simulation workloads.
- **Tasks**:
  1. Configure vLLM engine arguments (`--gpu-memory-utilization`, `--max-num-seqs`, `--block-size 16`).
  2. Simulate a multi-agent swarm generating 50 concurrent tool call requests to the local endpoint.
  3. Profile VRAM block allocation, cache hit rates, and request latency curves under heavy concurrent load.

### Stretch Goal: Production Hardening & Multi-GPU / Unified Memory Tuning
- **Objective**: Architect a zero-downtime, load-balanced local inference cluster with dynamic fallback and memory bounds safety.
- **Tasks**:
  1. Configure `llama.cpp` multi-GPU tensor splitting (`--tensor-split`) or Apple Silicon unified RAM allocation.
  2. Build a process supervisor that monitors VRAM allocation, auto-swaps models, and implements a health-check circuit breaker to prevent out-of-memory (OOM) panics.
