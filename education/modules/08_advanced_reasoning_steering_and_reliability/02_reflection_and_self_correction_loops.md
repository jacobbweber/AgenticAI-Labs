# 02: Reflection & Self-Correction Loops

## 1. Macro Concept & Industry Need

Single-pass generation in autonomous LLM systems is inherently brittle. Complex software engineering, multi-step logical reasoning, and structured data transformations frequently produce subtle bugs, syntax errors, or unhandled edge cases when executed in a single forward pass. In production environments, allowing unverified LLM generations to execute directly against live databases, APIs, or software repositories leads to cascading system failures.

**Reflection & Self-Correction Loops** are architectural state machine patterns where agents audit, critique, verify, and refine their own intermediate outputs before emitting final answers or committing tool actions. By coupling multi-pass Generator-Critic topologies with sandboxed execution feedback, error oscillation detection, state rollback, and self-consistency voting, agents achieve autonomous self-healing capabilities—drastically raising task success rates on complex workloads.

---

## 2. Architectural Component Mapping

| AI Jargon / Buzzword | Actual Software Component / Standard Primitive |
| :--- | :--- |
| **Generator-Critic Loop** | Dual-node state graph where Node A synthesizes output and Node B evaluates output against structured rubric criteria. |
| **Automated Traceback Feedback** | Subprocess wrapper executing generated code in a sandbox, parsing stack traces, and injecting line-specific errors into context. |
| **Self-Consistency (Majority Voting)** | Parallel stochastic sampling (`temperature > 0`) aggregating candidate responses via frequency distribution matching. |
| **Oscillation Prevention** | State machine tracking error signature hashes to detect fix-break-fix loops and trigger strategy pivots. |
| **State Rollback & Branch Pruning** | Checkpoint manager saving graph state prior to revisions and purging corrupted context iterations if self-correction regresses. |

---

## 3. Key Technical Aspects & Dig-In Topics

### 3.1 Generator-Critic Architecture & Structured Rubric Auditing

A **Generator-Critic Architecture** decouples primary task execution from quality evaluation. Rather than relying on unstructured text critique, the Critic node emits a structured JSON verdict based on explicit evaluation rubrics:

```
[ Generator Node ] ─── Output Code ───> [ Critic Node ]
       ^                                      │
       │                                      ├─ Verdict: PASS ──> [ Exit / Commit ]
       │                                      │
       └──── Structured Critique JSON ────────┴─ Verdict: FAIL ──> [ Increment Turn ]
```

```json
{
  "verdict": "FAIL",
  "score": 0.65,
  "defects": [
    {"line": 42, "category": "Security", "issue": "Unsanitized SQL string interpolation"},
    {"line": 88, "category": "Syntax", "issue": "Missing KeyError exception handler"}
  ],
  "recommended_edits": "Use parameterized queries and add try/except KeyError block."
}
```

By constraining the Critic to structured rubrics, the Generator receives actionable, line-specific feedback rather than vague generalities.

### 3.2 Automated Execution Traceback Feedback

For coding and data transformation agents, human-like critique is augmented by **Automated Execution Verification**. 

1. **Sandboxed Execution**: Generated code is written to an isolated sandbox (Docker / PyFilesystem) and executed against test suites or compilers.
2. **Traceback Parsing**: Standard error output (`stderr`) is captured and parsed into line numbers, exception types, and error signatures (`Error on line 14: IndexOutOfBounds`).
3. **Targeted Repair Prompting**: The error traceback is appended directly to the Generator's reflection context, enabling the model to pinpoint and patch the exact failing lines without altering valid code.

### 3.3 Oscillation Prevention & Strategy Switching

A common failure mode in self-correction loops is **Error Oscillation**, where an agent alternates between two complementary error states across turns (e.g., Turn 1: fixes Syntax Error A but introduces Logic Error B; Turn 2: fixes Logic Error B but re-introduces Syntax Error A).

```python
# Reflection Engine with Oscillation Detection & State Rollback
import hashlib

class ReflectionEngine:
    def __init__(self, max_turns: int = 3):
        self.max_turns = max_turns
        self.seen_signatures = set()
        self.checkpoints = []

    def run_loop(self, generator, critic, prompt: str):
        code = generator(prompt)
        self.checkpoints.append(code)

        for turn in range(self.max_turns):
            passed, critique, error_sig = critic(code)
            if passed:
                return {"status": "SUCCESS", "code": code, "turns": turn}

            # Check for error signature oscillation
            sig_hash = hashlib.md5(error_sig.encode()).hexdigest()
            if sig_hash in self.seen_signatures:
                # Oscillation detected! Rollback to initial checkpoint & alter strategy
                code = self.checkpoints[0]
                repair_prompt = f"CRITICAL: Oscillation detected. Reverting to base.\nError: {critique}\nStrategy: Refactor completely."
            else:
                self.seen_signatures.add(sig_hash)
                repair_prompt = f"Fix defects:\n{critique}\nCode:\n{code}"

            code = generator(repair_prompt)
            self.checkpoints.append(code)

        return {"status": "FAILED_MAX_TURNS", "code": code}
```

- **Hash Signatures**: MD5 hashes of raw error tracebacks detect repeating failure patterns.
- **Strategy Pivoting**: When an oscillation is detected, the engine aborts incremental patching and instructs the Generator to alter its solution strategy completely or request human-in-the-loop (HITL) intervention.

### 3.4 State Rollback & Context Pruning

Unconstrained reflection passes cause context bloat: accumulating multiple turns of bad code, long stack traces, and repeated critiques exhausts context windows and degrades LLM reasoning.

**State Rollback & Context Pruning** maintains a clean agent state:
- **Graph Checkpointing**: Prior to every revision pass, the agent state (graph variables, working memory) is snapshotted.
- **Context Pruning**: If a self-correction pass fails or degrades performance, the framework purges intermediate failure turns from context, preserving only the initial prompt, verified learnings, and the latest clean checkpoint.

---

## 4. Future Lab Blueprint

### Lab 1: Baseline Architecture & Generator-Critic Verification Loop
- **Objective**: Implement a multi-pass Generator-Critic reflection loop with structured JSON rubric evaluation.
- **Tasks**:
  1. Build a `Generator` function generating python code and a `Critic` function auditing code against security and style rubrics.
  2. Implement structured JSON output enforcement for the Critic verdict.
  3. Wire the iterative critique-refinement loop with max turn caps (e.g., 3 turns) and log turn convergence rates.

### Lab 2: Intermediate Capability Integration — Automated Traceback Feedback Coder
- **Objective**: Develop an autonomous coding agent that executes generated code in a sandbox and self-corrects using compiler tracebacks.
- **Tasks**:
  1. Build a sandboxed execution wrapper (`subprocess` / PyFilesystem) that compiles generated Python code and runs unit tests.
  2. Parse compiler errors (`SyntaxError`, `KeyError`, `AssertionError`) and stack traces into structured repair prompts.
  3. Verify that the agent autonomously resolves test failures within 3 reflection turns.

### Lab 3: Enterprise Resilience & Oscillation Prevention with State Rollback
- **Objective**: Implement an advanced reflection engine featuring error signature hashing, oscillation detection, and state rollback capabilities.
- **Tasks**:
  1. Build an error signature hashing module tracking failure signatures across turns.
  2. Implement state rollback logic that reverts corrupted context states to known-good checkpoints upon detecting oscillation.
  3. Test resilience against synthetic oscillating error scenarios.

### Stretch Goal: Production Hardening & Multi-Agent Self-Consistency Consensus Engine
- **Objective**: Construct a multi-agent self-consistency and consensus harness using parallel generation and Process-Guided Critic verification.
- **Tasks**:
  1. Generate $N$ parallel candidate solutions at `temperature = 0.7`.
  2. Pass candidate solutions through a multi-agent Critic panel scoring outputs on functional correctness and security.
  3. Implement majority voting and branch pruning algorithms to select the optimal consensus output for production deployment.
