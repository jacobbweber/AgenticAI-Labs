# Quality Guard Design Specification

## 1. Overview & Architecture
The Quality Guard system (`core/quality_guard.py`) enforces a multi-pass evaluation loop after Stage 3 blog post generation. It acts as an automated editorial board ensuring technical completeness, human writing fidelity, and structural integrity before publication.

---

## 2. Review Passes & Rubric
- **Pass 1 — Self Review**: The LLM compares the generated post draft against the raw input inbox payload. Checks whether key technical terms, code snippets, and concepts are accurately represented.
- **Pass 2 — Skeptic / Human Fidelity Review**: An LLM role-playing as a skeptical senior technical editor scores the draft 1-10 on an explicit rubric:
  - **10**: Indistinguishable from an expert human technical blogger.
  - **1**: Obvious AI-generated output.
  - **Penalties**: AI transition buzzwords ("Furthermore", "It is worth noting", "In conclusion"), bracketed placeholders (`[...]`), generic summarization conclusions, instruction text leakage, and repetitive paragraph structures.
- **Pass 3 — Targeted Rewrite**: If Pass 2 score is < 7, the LLM receives the flagged critique and rewrites only the specific failing sections/sentences while leaving surrounding content unchanged.

---

## 3. Data Integration & Observability
- All review passes record telemetry logs (`findings`, `score`, `rewrites_applied`) to `otel_traces.jsonl` using `evals/otel_tracer.py`.
- Final post publication is only authorized when `skeptic_score >= 7`.

---

## 4. Error & Retry Limits
- Maximum rewrite cycles: 3 attempts.
- If skeptic score remains < 7 after max attempts, an exception is raised or state checkpoint updated for manual review.
