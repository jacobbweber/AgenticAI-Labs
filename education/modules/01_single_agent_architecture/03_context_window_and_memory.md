# 03: Context Window & Memory Management

## 1. Macro Concept & Industry Need

The context window is the fundamental constraint of LLM-based autonomous agents. While modern models support expanding context limits (e.g., 128k to 1M+ tokens), long-horizon agent operations naturally accumulate thousands of lines of turn history, raw tool outputs, file snapshots, and system prompts.

Unmanaged context growth leads to catastrophic API truncation crashes, ballooning token costs, high Time to First Token (TTFT) latency, and degraded reasoning accuracy ("lost in the middle" phenomenon).

To operate reliably over extended workflows, single-agent architectures rely on structured **Context Window & Memory Management**. By implementing AST-aware context compaction, hardware-level KV prompt caching, and persistent 4-tier memory state stores, agents can run indefinitely while keeping active context payloads lean, performant, and cost-effective.

---

## 2. Architectural Component Mapping

To demystify agentic concepts into standard software engineering primitives, the table below maps context and memory terminology to established software components:

| AI Buzzword / Paradigm | Standard Software Engineering Primitive | System Description & Mechanics |
| :--- | :--- | :--- |
| **Working Memory** | Active In-Flight API Payload Buffer | Immediate prompt context sent in the LLM call payload. |
| **Short-Term Memory** | Session Turn Execution Graph | Stateful in-memory message history maintained during active session execution. |
| **Long-Term Memory** | Persistent Vector / Relational DB Store | External database (SQLite, PostgreSQL, Qdrant) storing past session facts. |
| **Procedural Memory** | Dynamic System Policy Instructions | System prompt rules, loaded `SKILL.md` playbooks, and workflow guidelines. |
| **Context Compaction** | Garbage Collection & Trimming Engine | Algorithmic reduction of message arrays via AST pruning, summarization, or trimming. |
| **Prompt Caching** | GPU KV-Cache Prefix Pointer Hit | Inference engine optimization reusing compiled prompt key-value tensor states. |

---

## 3. Key Technical Aspects & Dig-In Topics

### 1. Advanced Context Compaction & AST-Aware Pruning
Legacy context reduction relies on naive sliding windows or basic text truncation. Modern production harnesses employ syntax-aware pruning strategies:
- **Sliding Window Truncation**: Retaining system prompts + the last $N$ turns while dropping older turns. Risk: losing initial user directives.
- **LLM-Based Summarization**: Periodically summarizing turns $2 \dots N-k$ into a compact history summary block `<turn_history_summary>`.
- **AST-Aware Code Pruning**: Parsing code blocks in historical tool execution logs using Abstract Syntax Trees (ASTs). Stripping raw stdout/stderr logs and unchanged code while preserving function signatures, class definitions, and diff blocks.

### 2. Hardware & Inference Optimizations (KV-Cache & Prompt Caching)
Modern inference providers and local engines (e.g., Anthropic Prompt Caching, vLLM PagedAttention prefix caching) dramatically reduce TTFT latency and cost by caching prompt KV states on GPUs:
- **Prefix Matching**: If the system prompt, tool definitions, and initial conversation turns remain unchanged across API calls, the inference engine reuses pre-computed KV matrices.
- **Cache Boundary Alignment**: Structuring context buffers so static system instructions and tool schemas are placed at the beginning of the context payload. Avoiding dynamic timestamp modifications in static headers to maintain 90%+ KV cache hit rates.

### 3. Comprehensive 4-Tier Memory Taxonomy
Production agent memory is categorized into 4 distinct functional tiers:
- **Working Memory**: Transient, active context buffer injected into the immediate model inference payload.
- **Short-Term Memory**: In-memory turn graph capturing full raw execution history during an active task session.
- **Long-Term Memory**: External episodic and semantic database storage (vector store + relational DB) for cross-session entity recall and past task learnings.
- **Procedural Memory**: Injected guidelines, loaded `SKILL.md` playbooks, and learned tool execution rules governing model behavior.

### 4. Durable Memory State Persistence & Restarts
Agents operating in enterprise environments must survive process crashes, server restarts, and human pause requests:
- **SQLite / PostgreSQL Checkpointing**: Persisting session state, turn graphs, tool payloads, and memory vectors into persistent database tables after every turn.
- **State Snapshot Restarts**: Enabling agent sessions to be paused, serialized, transferred across workers, and resumed seamlessly without losing execution context.

```python
# Conceptual AST-Aware Turn Pruner
import ast

class ContextPruner:
    def prune_tool_output(self, raw_output: str, max_lines: int = 50) -> str:
        lines = raw_output.splitlines()
        if len(lines) <= max_lines:
            return raw_output
        
        # Summarize verbose execution logs into signature summary
        head = "\n".join(lines[:15])
        tail = "\n".join(lines[-15:])
        omitted_count = len(lines) - 30
        return f"{head}\n... [AST Pruned: {omitted_count} lines of raw execution output] ...\n{tail}"
```

---

## 4. Future Lab Blueprint

High-level directional prompts for subsequent hands-on lab creation:

- **Lab 1: Baseline Architecture** — Construct a message buffer manager supporting token counting, sliding window truncation, and basic turn summarization.
- **Lab 2: Intermediate Capability Integration** — Integrate AST-aware code turn pruning and a key-value/vector-backed long-term memory store for cross-session entity recall.
- **Lab 3: Enterprise Resilience & Advanced Edge Cases** — Implement KV-prompt cache boundary optimization (matching system/tool prefixes for prompt caching) and a persistent state checkpointing engine (SQLite/Postgres) supporting agent pause/resume.
- **Stretch Goal: Production Hardening** — Construct a multi-tier memory management system with dynamic lossy/lossless compaction strategies, automated memory garbage collection, and sub-millisecond vector memory retrieval.
