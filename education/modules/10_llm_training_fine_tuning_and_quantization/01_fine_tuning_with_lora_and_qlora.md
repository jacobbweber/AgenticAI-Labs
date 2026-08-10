# 01: Fine-Tuning with LoRA, QLoRA & RL Post-Training

## 1. Macro Concept & Industry Need

**Post-training fine-tuning and alignment** adapts raw pre-trained base models (e.g., Qwen 2.5, Llama 3.2) into specialized instruction-following, tool-calling, and reasoning models. While pre-training instills world knowledge and language comprehension via next-token prediction, post-training aligns model behavior to adhere to specific output formats, execute function calls, follow complex instructions, and engage in multi-step reasoning.

In enterprise AI engineering, relying solely on base foundation models or standard API prompt engineering creates three main operational hurdles:
1. **Format Hallucination & Schema Failures**: Base models often fail to adhere consistently to rigid corporate JSON schemas, domain coding guidelines, or multi-turn tool calling protocols.
2. **Catastrophic Forgetting & Compute Exhaustion**: Updating 100% of model parameters via full Supervised Fine-Tuning (Full SFT) requires massive multi-GPU clusters and risks destroying general reasoning capabilities ("catastrophic forgetting").
3. **Data Privacy & Customization Bottlenecks**: Fine-tuning proprietary models on cloud platforms exposes sensitive enterprise training data to external third parties.

To solve these challenges, the post-training spectrum incorporates Parameter-Efficient Fine-Tuning (**LoRA / QLoRA NF4**), Direct Preference Optimization (**DPO / ORPO**), and DeepSeek-R1 style **Group Relative Policy Optimization (GRPO)** with **Reinforcement Learning from Verifiable Rewards (RLVR)**.

---

## 2. Architectural Component Mapping

The following table demystifies post-training and fine-tuning concepts into standard software engineering primitives:

| AI / ML Buzzword | Standard Software Engineering Primitive | System Function / Role |
| :--- | :--- | :--- |
| **SFT (Supervised Fine-Tuning)** | Target-Masked Training Loop | Optimizes Cross-Entropy loss exclusively over output completion tokens, ignoring prompt tokens. |
| **LoRA (Low-Rank Adaptation)** | Matrix Decomposition Invalidation Layer ($A \cdot B$) | Freezes base weights $W_0$ and updates low-rank matrices $A \in \mathbb{R}^{r \times d}$ and $B \in \mathbb{R}^{k \times r}$, reducing trainable parameters by >99%. |
| **QLoRA (NF4)** | 4-Bit NormalFloat Quantized Base + 16-Bit Adapter | Quantizes base model weights to 4-bit NormalFloat with double quantization while computing gradients through 16-bit LoRA adapters. |
| **GRPO (Group Relative Policy Optimization)** | Group-Relative Reward Normalization & Policy Gradient | Samples a group of outputs per prompt, computes rule-based rewards $R_i$, normalizes advantages $A_i = \frac{R_i - \mu_R}{\sigma_R}$, and updates policy without a critic model. |
| **RLVR (Verifiable Rewards)** | Deterministic Program Verification Test Suite | Executes Python unit tests, regex parsers, or mathematical checkers to return binary/scalar rewards ($R \in \{0, 1\}$). |
| **DPO / ORPO** | Preference Loss Contrastive Weight Update | Optimizes model preferences directly from chosen vs rejected response pairs without separate reward model training. |
| **Tool Call Tuning** | Schema-Enforced Multi-Turn Conversation Dataset | Fine-tunes model on structured `<tool_call>` generation and `<tool_response>` parsing turns. |

---

## 3. Key Technical Aspects & Dig-In Topics

### Parameter-Efficient Fine-Tuning Mechanics (PEFT / LoRA / QLoRA)
Low-Rank Adaptation (LoRA) freezes the original pre-trained weight matrix $W_0 \in \mathbb{R}^{d \times k}$ and injects trainable rank decomposition matrices $A \in \mathbb{R}^{r \times k}$ and $B \in \mathbb{R}^{d \times r}$ (where rank $r \ll \min(d, k)$):

$$W = W_0 + \Delta W = W_0 + \frac{\alpha}{r} (A \cdot B)$$

- **Rank ($r$) & Alpha ($\alpha$) Selection**: Typical values range from $r=8$ to $r=64$. Scaling factor $\alpha$ (e.g., $\alpha = 16$ or $32$) stabilizes gradient updates when adjusting rank.
- **Target Projection Modules**: Injecting LoRA adapters across all linear attention and feed-forward projections (`q_proj`, `v_proj`, `k_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`) achieves performance on par with full fine-tuning while training under 1% of total parameters.
- **QLoRA NormalFloat4 (NF4)**: Quantizes frozen base model weights to 4-bit NormalFloat with double quantization of scaling factors. Combined with paged CUDA optimizers, QLoRA enables fine-tuning 7B to 14B parameter models on single consumer GPUs (< 12GB VRAM).

### Reinforcement Learning Frontiers: GRPO & RLVR (DeepSeek-R1 Pattern)
Traditional RLHF relies on Proximal Policy Optimization (PPO), which requires maintaining an equally sized Value/Critic model alongside the Policy model, doubling VRAM requirements. **Group Relative Policy Optimization (GRPO)** eliminates the Critic model by computing relative advantages across a group of sampled responses:

```
User Prompt: "Write a python function to check prime numbers."
                                   |
                                   v
+------------------------------------------------------------------+
|                    Sample Response Group (G=4)                   |
| Output 1: Def is_prime(n)...  -> Verifier: PASSED  (Reward R1=1) |
| Output 2: Def prime_check(n)...-> Verifier: FAILED  (Reward R2=0) |
| Output 3: Def check(n)...      -> Verifier: PASSED  (Reward R3=1) |
| Output 4: Def is_prime(n)...  -> Verifier: FAILED  (Reward R4=0) |
+----------------------------------+-------------------------------+
                                   |
                                   v
+------------------------------------------------------------------+
|              Group-Relative Advantage Normalization              |
| Compute Mean (u_R) & Std (sigma_R) across Group Rewards          |
| Advantage A_i = (R_i - u_R) / (sigma_R + eps)                    |
+----------------------------------+-------------------------------+
                                   |
                                   v
+------------------------------------------------------------------+
|               Policy Gradient Update with KL Penalty             |
| Update Policy Weights without Value/Critic Model                 |
+------------------------------------------------------------------+
```

1. **Group Sampling**: For each prompt $q$, the policy $\pi_\theta$ samples a group of $G$ outputs $\{o_1, o_2, \dots, o_G\}$.
2. **Reinforcement Learning from Verifiable Rewards (RLVR)**: Deterministic program verifiers (e.g., `pytest` execution, `sympy` symbolic solvers, or XML tag regex checkers) score outputs directly ($R_i \in \{0, 1\}$) without human annotators.
3. **Group Advantage Calculation**: Calculates advantage $A_i = \frac{R_i - \mu_R}{\sigma_R}$, where $\mu_R$ and $\sigma_R$ are the mean and standard deviation of rewards within the sampled group.
4. **KL-Divergence Constraint**: Adds a KL penalty term $D_{KL}(\pi_\theta || \pi_{ref})$ to prevent policy drift away from the base reference model.

### Direct Preference Optimization (DPO) & ORPO
For preference alignment without reinforcement learning loops:
- **DPO (Direct Preference Optimization)**: Derives an exact analytical solution to the RLHF objective, optimizing policy parameters directly on dataset pairs of chosen ($y_w$) vs rejected ($y_l$) responses using implicit reward functions.
- **ORPO (Odds Ratio Preference Optimization)**: Combines SFT cross-entropy loss with an odds-ratio penalty in a single training pass, eliminating the need for a separate reference model.

### Domain Fine-Tuning for Tool Calling & Structured Outputs
Fine-tuning models for tool execution requires multi-turn dataset formatting with prompt loss masking:

```python
# Conceptual Dataset Loss Masking Structure (< 50 lines)
def format_tool_calling_sample(system_prompt: str, user_query: str, tool_call_json: str):
    # Construct complete ChatML formatted conversation string
    full_prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{user_query}<|im_end|>\n<|im_start|>assistant\n<tool_call>{tool_call_json}</tool_call><|im_end|>"
    
    # Loss masking: Compute Cross-Entropy loss ONLY on completion tokens
    # Prompt tokens (system + user) are assigned label ID -100 (ignored in PyTorch loss)
    return full_prompt
```

---

## 4. Future Lab Blueprint

The following directional prompts guide the construction of hands-on technical labs for this module:

### Lab 1: Baseline Architecture (Supervised Fine-Tuning with LoRA for Custom Formats)
Construct a Supervised Fine-Tuning (SFT) pipeline using Hugging Face `TRL`, `PEFT`, or `Unsloth` on a 1B/3B base model (`Qwen2.5-1.5B` or `Llama-3.2-1B`). Train LoRA rank adapters on a custom JSON dataset, implement target prompt loss masking, and verify output format compliance.

### Lab 2: Intermediate Capability Integration (QLoRA NF4 Multi-Turn Tool Calling Pipeline)
Build a QLoRA fine-tuning pipeline using 4-bit NormalFloat (NF4) quantization to fine-tune a model on a multi-turn tool-calling dataset using a single consumer GPU (< 12GB VRAM). Save adapter weights, merge adapters into base weights (`merge_and_unload`), and test function call generation.

### Lab 3: Enterprise Resilience & Advanced Edge Cases (DeepSeek-R1 Style GRPO / RLVR Reasoning Alignment)
Develop a Group Relative Policy Optimization (GRPO) post-training loop for reasoning tasks. Construct a deterministic Python unit test verifier (`pytest`), sample group responses ($G=4$), calculate group-normalized relative advantages, and update policy weights under KL divergence constraints without a Critic model.

### Stretch Goal: Production Hardening (DPO Preference Tuning, Adapter Merging & Safetensors Export)
Execute a Direct Preference Optimization (DPO) pass over edge-case failure datasets, perform full LoRA adapter weight merging, benchmark model performance against base checkpoints, and export final merged `.safetensors` model artifacts ready for quantization and deployment.
