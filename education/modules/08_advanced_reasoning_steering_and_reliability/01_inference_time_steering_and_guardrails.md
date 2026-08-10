# 01: Inference-Time Steering & Guardrails

## 1. Macro Concept & Industry Need

Relying exclusively on system prompts ("You are a helpful assistant, always output valid JSON") to enforce behavior or security boundaries in autonomous agents is fundamentally insufficient. Large Language Models remain susceptible to prompt injection attacks, schema formatting drift, and safety alignment failures. In enterprise agent pipelines, a single malformed JSON response or security violation can crash automated downstream workflows or expose sensitive corporate systems.

**Inference-Time Steering & Guardrails** represent the set of engineering techniques that enforce deterministic, mathematical guarantees directly at the model decoding layer. By operating at the token sampling and neural network activation levels—using Context-Free Grammar (CFG) token masking, activation steering vectors, logit bias manipulation, and parallel speculative guardrails—developers achieve 100% syntactically valid outputs and real-time safety compliance without relying on fragile prompt text.

---

## 2. Architectural Component Mapping

| AI Jargon / Buzzword | Actual Software Component / Standard Primitive |
| :--- | :--- |
| **Grammar-Constrained Decoding** | Softmax logit masking applying token index bitmasks derived from Context-Free Grammars (GBNF/JSON Schema) at each token step. |
| **Logit Bias Manipulation** | Direct scalar addition/subtraction applied to output logit probability vectors prior to Softmax sampling. |
| **Activation Steering Vectors** | Adding directional concept vectors to intermediate layer hidden state activations during forward passes without prompt token overhead. |
| **Speculative Guardrails** | Asynchronous parallel evaluation of streaming tokens by lightweight classifier models (Llama-Guard 3) running concurrently with main generation. |
| **Guardrail Middleware** | Interceptor pipeline pattern executing pre-inference prompt inspection and post-inference completion sanitization. |

---

## 3. Key Technical Aspects & Dig-In Topics

### 3.1 Context-Free Grammar (CFG) Token Masking Mechanics

Constrained decoding engines (such as GBNF in `llama.cpp`, Outlines, or XGrammar) convert formal grammars or JSON Schemas into deterministic Pushdown Automata (PDA). 

At each token generation step $t$:
1. The engine queries the automaton for the set of valid next vocabulary tokens $V_{\text{valid}} \subset V$ allowed by the grammar.
2. The engine constructs a binary bitmask and sets the logits of all invalid tokens $i \notin V_{\text{valid}}$ to $-\infty$:

$$\text{Logits}_{\text{masked}}[i] = \begin{cases} \text{Logits}[i] & \text{if } i \in V_{\text{valid}} \\ -\infty & \text{if } i \notin V_{\text{valid}} \end{cases}$$

```python
# Context-Free Grammar Softmax Logit Masker Simulator
import torch

class CFGLogitMasker:
    def __init__(self, vocab: dict[str, int], transitions: dict[int, list[int]]):
        self.vocab = vocab
        self.inv_vocab = {v: k for k, v in vocab.items()}
        self.transitions = transitions
        self.state = 0  # Start state of grammar automaton

    def apply_mask(self, logits: torch.Tensor) -> torch.Tensor:
        allowed_tokens = self.transitions.get(self.state, [])
        if not allowed_tokens:
            return logits
            
        mask = torch.full_like(logits, float('-inf'))
        mask[allowed_tokens] = 0.0
        return logits + mask

    def advance(self, sampled_token_id: int):
        # Update automaton state based on sampled token
        self.state = sampled_token_id
```

Because invalid tokens receive zero probability during Softmax, the engine guarantees 100% structural and syntax compliance (e.g., producing perfectly formatted JSON tool parameters every single time).

### 3.2 Activation Steering Vectors vs Prompting

Traditional behavior steering modifies system prompts, consuming context window tokens and often degrading model reasoning coherence. **Activation Steering** (derived from mechanistic interpretability) intervenes directly inside the model's residual stream during the forward pass:

```
Token Input ───> [ Layer 1 ] ───> [ Layer L ] ───> [ Output Logits ]
                                       │
                              (Hidden State h_L)
                                       │
                                       v
                             h_L' = h_L + α · v_concept
```

1. **Vector Extraction**: The difference of means across hidden layer activations is computed for a target concept $v_{\text{concept}} = \mu_{\text{positive}} - \mu_{\text{negative}}$ (e.g., refusal suppression, code safety, tone adjustment).
2. **Forward Pass Injection**: At intermediate layer $L$, the hidden state vector is modified: $h_L' = h_L + \alpha \cdot v_{\text{concept}}$, where $\alpha$ is a scaling hyperparameter.

Activation steering alters model behavior instantaneously without consuming prompt tokens or requiring model retraining.

### 3.3 Logit Bias Manipulation & Vocabulary Filtering

Logit bias applies direct scalar modifications $\delta$ to specific vocabulary indices in the output logit array prior to sampling:

$$\text{Logits}'[t_i] = \text{Logits}[t_i] + \delta$$

- **Positive Bias ($\delta > 0$)**: Forces preferred structural tokens (e.g., boosting `{` to ensure immediate JSON response generation).
- **Negative Bias ($\delta = -100$)**: Bans prohibited phrases or tokens (e.g., suppressing `I apologize` or specific sensitive system terms).

### 3.4 Speculative & Parallel Guardrailing

Traditional guardrails act synchronously, introducing 100% latency overhead by inspecting input prompts before LLM execution and outputs after generation completes. **Speculative Parallel Guardrailing** runs lightweight safety models (e.g., Llama-Guard 3 1B) asynchronously alongside token completion streaming:

```
User Prompt ───────┬──────> Main Model Generation ───> SSE Stream to Client
                   │
                   └──────> Parallel Safety Model ───> Abort Signal Generator
                            (Llama-Guard 3)
```

If the parallel safety model detects a policy violation or prompt injection attack mid-generation, it emits an instant abort signal over the event bus, terminating the main model's SSE stream and revoking pending tool execution.

---

## 4. Future Lab Blueprint

### Lab 1: Baseline Architecture & Constrained Grammar Decoding
- **Objective**: Implement a constrained decoding engine using GBNF/JSON Schema via Outlines, XGrammar, or `llama.cpp`.
- **Tasks**:
  1. Define a strict JSON Schema for a complex multi-tool agent call.
  2. Configure GBNF grammar sampling on a local LLM engine endpoint.
  3. Verify that 100% of generated completion outputs pass strict JSON syntax parsing across 100 test iterations.

### Lab 2: Intermediate Capability Integration — Activation Steering & Logit Bias Engine
- **Objective**: Build an inference-time steering harness that applies activation steering vectors and logit bias.
- **Tasks**:
  1. Extract an activation steering vector for tone or refusal suppression across model hidden states.
  2. Implement logit bias parameters to force JSON object initialization characters.
  3. Compare generation quality and context efficiency between prompt-based steering and activation-based steering.

### Lab 3: Enterprise Resilience & Speculative Parallel Safety Pipeline
- **Objective**: Construct an asynchronous speculative guardrail middleware using parallel safety models.
- **Tasks**:
  1. Deploy a parallel Llama-Guard 3 safety classifier instance alongside a local LLM endpoint.
  2. Build a non-blocking streaming pipeline that routes SSE completion chunks to the user while evaluating safety concurrently.
  3. Test mid-stream abort handling by injecting adversarial prompts that trigger safety policy violations.

### Stretch Goal: Production Hardening & Adversarial Red-Teaming Defense
- **Objective**: Build a production red-teaming benchmark and automated injection interceptor stack.
- **Tasks**:
  1. Construct an automated red-teaming harness subjecting the inference pipeline to complex jailbreak payloads, indirect prompt injections, and system prompt extraction attempts.
  2. Implement zero-trust execution boundaries combining input sanitization, CFG grammar sampling, and output PII filters.
  3. Achieve zero successful prompt injection vulnerabilities across an adversarial benchmark suite.
