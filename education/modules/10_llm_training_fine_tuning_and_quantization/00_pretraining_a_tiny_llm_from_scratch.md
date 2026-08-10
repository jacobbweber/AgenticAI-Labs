# 00: Pre-Training a Tiny LLM from Scratch

## 1. Macro Concept & Industry Need

**Pre-training an LLM from scratch** involves constructing a neural network architecture from ground zero and optimizing its parameters via unsupervised next-token prediction over massive text corpora. Pre-training a **Tiny LLM (~1M to 100M parameters)** locally in PyTorch demystifies how foundation models operate under the hood without requiring multi-million-dollar cloud GPU clusters.

In modern AI engineering, relying solely on commercial closed-source APIs creates critical knowledge and capability gaps:
1. **The "Black Box" Engineering Barrier**: Developers consuming LLM APIs treat model behavior as magical, struggling to diagnose tokenization artifacts, context window memory scaling limits ($O(N^2)$ attention complexity), loss spikes, or generation decay.
2. **Domain-Specific Micro-Model Requirements**: Embedded systems, IoT microcontrollers, real-time edge appliances, and ultra-low-latency classification pipelines often require highly specialized micro-models (<100M parameters) that execute locally with microsecond latency and near-zero memory footprints.
3. **Synthetic Data Curation Shift (2025/2026 Frontier)**: The industry paradigm has shifted from training on raw, noisy web crawls (e.g., Common Crawl) to training on high-quality **synthetic pre-training corpora** (such as Cosmopedia, UltraText, and synthetic code suites). By using LLM-driven filtering, MinHash deduplication, perplexity scoring, and automated dataset synthesis, modern engineers can pre-train high-performing micro-models using 10x smaller token budgets.

By building a Transformer model from scratch in PyTorch, engineers master modern architectural primitives—including **Rotary Position Embeddings (RoPE)**, **SwiGLU activations**, **Grouped-Query Attention (GQA)**, **RMSNorm**, and **FlashAttention**—establishing the foundation for custom pre-training and fine-tuning.

---

## 2. Architectural Component Mapping

The following table translates core machine learning and pre-training concepts into standard software engineering primitives:

| AI / ML Buzzword | Standard Software Engineering Primitive | System Function / Role |
| :--- | :--- | :--- |
| **Tokenizer (BPE)** | Trie-based String Chunker & Integer Vocabulary Lookup Table | Converts raw string characters into integer token IDs using Byte-Pair Encoding (BPE). |
| **Embedding Matrix** | 2D Dense Float Tensor Lookup Table (`nn.Embedding`) | Maps discrete integer token IDs into continuous $d_{model}$-dimensional float vectors. |
| **Rotary Position Embedding (RoPE)** | Complex Tensor Rotation Function ($R_{\Theta, m}^d$) | Encodes token position by rotating query and key vectors in complex 2D planes, preserving relative distance. |
| **Self-Attention ($Q, K, V$)** | Batched Matrix Multiplication & Softmax Normalization | Calculates dynamic contextual weights between tokens via $\text{Softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V$. |
| **Grouped-Query Attention (GQA)** | Tensor Reshaping & Key/Value Head Sharing | Shares Key and Value projection heads across Query head groups to reduce KV-cache VRAM memory bandwidth. |
| **Causal Attention Mask** | Lower-Triangular Boolean Tensor | Masks future token positions by setting upper-triangle attention logits to $-\infty$. |
| **SwiGLU Activation** | Gated Linear Combination (`Swish(x W_g) * (x W_1)`) | Non-linear activation replacing standard GeLU to improve gradient flow and representation capacity. |
| **RMSNorm** | Root Mean Square Normalization Scaling | Normalizes activation vectors by their root mean square without subtracting scalar mean, saving compute cycles. |
| **Cross-Entropy Loss** | Multiclass Log-Loss Function | Measures divergence between predicted token probability distribution and target token index. |
| **AdamW Optimizer** | Gradient Momentum & Weight Decay State Updater | Adjusts model parameters using first/second gradient moments with decoupled $L_2$ regularization. |

---

## 3. Key Technical Aspects & Dig-In Topics

### Modern Transformer Primitives (2025/2026 Standards)
Modern open-weight foundation models (such as Llama 3, Qwen 2.5, and DeepSeek) have evolved beyond the original 2017 Transformer architecture. Implementing a modern pre-training pipeline requires incorporating four architectural primitives:

1. **Rotary Position Embedding (RoPE)**: Replaces absolute position embeddings by rotating query ($Q$) and key ($K$) representation vectors in 2D complex planes. RoPE naturally encodes relative token distances ($m - n$) and supports context window extension via linear scaling or YaRN (Yet Another RoPE Extension).
2. **SwiGLU Activation Function**: Replaces standard GeLU activations with Swish-Gated Linear Units ($\text{SwiGLU}(x) = (\text{Swish}(x W_g)) \otimes (x W_1)$), allocating hidden dimension size to $d_{ff} = \frac{8}{3} d_{model}$ for superior gradient propagation.
3. **Grouped-Query Attention (GQA)**: Groups multiple Query heads to share single Key ($K$) and Value ($V$) heads (e.g., 8:1 query-to-KV ratio). GQA drastically reduces KV-cache memory bandwidth during inference while preserving multi-head attention expressiveness.
4. **RMSNorm (Root Mean Square Normalization)**: Replaces standard LayerNorm by normalizing inputs by their root-mean-square statistic ($\text{RMS}(x) = \sqrt{\frac{1}{d}\sum x_i^2 + \epsilon}$), omitting mean subtraction for a 10-30% speedup in GPU normalization kernels.

```python
# Conceptual PyTorch Modern Transformer Layer Implementation (< 50 lines)
import torch
import torch.nn as nn
import torch.nn.functional as F

class RMSNorm(nn.Module):
    def __init__(self, dim: int, eps: float = 1e-6):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Normalize by root mean square without mean subtraction
        var = torch.mean(x ** 2, dim=-1, keepdim=True)
        return x * torch.rsqrt(var + self.eps) * self.weight

class SwiGLUFeedForward(nn.Module):
    def __init__(self, d_model: int, d_ff: int):
        super().__init__()
        self.w_gate = nn.Linear(d_model, d_ff, bias=False)
        self.w_1 = nn.Linear(d_model, d_ff, bias=False)
        self.w_2 = nn.Linear(d_ff, d_model, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Swish(x * W_g) * (x * W_1) projected back via W_2
        return self.w_2(F.silu(self.w_gate(x)) * self.w_1(x))
```

### Synthetic Data Curation & Data Pipeline Mechanics
Pre-training efficiency depends heavily on dataset quality. The synthetic curation pipeline follows three steps:
- **Corpus Generation & Extraction**: Using frontier LLMs to synthesize high-quality textbook explanations, code snippets, and structured Q&A data.
- **MinHash Deduplication**: Running Locality-Sensitive Hashing (LSH) and MinHash to eliminate duplicate or near-duplicate documents across pre-training shards.
- **Sequence Packing & Loss Masking**: Concatenating tokenized documents into contiguous fixed-length sequence blocks ($N = 2048$ or $4096$ tokens) separated by `<|endoftext|>` tokens, maximizing GPU batch utilization.

### Training Dynamics, Mixed Precision & Stability
Training neural networks requires strict numerical stability management:
- **Mixed-Precision Training**: Running forward/backward passes in `bfloat16` or `float16` while maintaining `float32` master weights in the AdamW optimizer to prevent gradient underflow.
- **Learning Rate Warmup & Cosine Decay**: Linearly warming up learning rates for the first 1,000 steps, followed by cosine decay down to 10% of maximum LR.
- **Gradient Clipping & Loss Spike Recovery**: Applying `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)` to prevent exploding gradients, accompanied by automated checkpoint saving for loss spike recovery.

---

## 4. Future Lab Blueprint

The following directional prompts guide the construction of hands-on technical labs for this module:

### Lab 1: Baseline Architecture (Minimal PyTorch GPT Transformer & Next-Token Training Loop)
Construct a minimal PyTorch GPT-style causal language model (~5M parameters) featuring Multi-Head Attention (MHA) and absolute positional embeddings. Write a self-contained training loop that tokenizes a sample text corpus, computes cross-entropy next-token loss, and executes AdamW optimization iterations.

### Lab 2: Intermediate Capability Integration (Modern Primitives: RoPE, SwiGLU, GQA, RMSNorm & FlashAttention)
Upgrade the PyTorch Transformer architecture to modern 2025/2026 standards: Replace absolute positional embeddings with Rotary Position Embeddings (RoPE), replace GeLU with SwiGLU activations, implement Grouped-Query Attention (GQA), and integrate RMSNorm. Incorporate PyTorch `F.scaled_dot_product_attention` for FlashAttention hardware acceleration.

### Lab 3: Enterprise Resilience & Advanced Edge Cases (Synthetic Data Curation Pipeline & Mixed-Precision BF16 Training)
Build an automated pre-training data curation pipeline featuring MinHash/LSH deduplication, sequence packing into contiguous token blocks, and perplexity quality filtering. Implement a mixed-precision `bfloat16` training harness with cosine learning rate warmup/decay schedules, gradient norm clipping, and automated loss spike checkpoint recovery.

### Stretch Goal: Production Hardening (100M Parameter Multi-GPU Pre-Training & Hugging Face Checkpoint Export)
Scale pre-training to a 100M parameter micro-foundation model distributed across multi-GPU nodes using PyTorch Distributed Data Parallel (DDP). Measure real-time token processing throughput (tokens/sec/GPU), monitor training metrics via WandB/TensorBoard, and export final model weights directly to Hugging Face `AutoModelForCausalLM` format.
