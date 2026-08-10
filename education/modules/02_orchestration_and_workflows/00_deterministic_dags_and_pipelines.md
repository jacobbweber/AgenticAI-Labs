# 00: Deterministic DAGs and Pipelines

## 1. Macro Concept & Industry Need

Autonomous agent control loops (such as ReAct) offer unmatched flexibility for open-ended reasoning and complex tool use. However, when deployed in enterprise production environments, unconstrained autonomous execution loops introduce significant operational risk: high output variance, unpredictable execution costs, latency spikes, and non-reproducible behavior. Standard enterprise workflows—such as invoice processing, KYC (Know Your Customer) verification, and customer support escalation—require strict execution guarantees, predictable latency SLAs, and auditability.

To bridge this gap, modern production agent architectures combine autonomous reasoning with **Deterministic Workflows (Directed Acyclic Graphs, or DAGs)**. By structuring the overall process as a hardcoded topological execution graph, software engineers restrict non-deterministic AI capabilities to targeted processing or routing nodes while retaining deterministic control over global orchestration.

```
       +--------------------------------------------------+
       |           Ingestion Step (Deterministic)         |
       +--------------------------------------------------+
                                |
                                v
       +--------------------------------------------------+
       |            LLM Intent Router Node                |
       |  (Structured JSON: "billing" | "tech" | "other") |
       +--------------------------------------------------+
           /                    |                     \
          /                     |                      \
         v                      v                       v
+------------------+   +------------------+   +------------------+
| Billing Pipeline |   | Technical Support|   | Standard Triage  |
|  (Deterministic) |   |    Pipeline      |   |     Fallback     |
+------------------+   +------------------+   +------------------+
```

### The Orchestration Spectrum

1. **Pure Deterministic DAG**: Execution proceeds along fixed topological dependencies ($A \rightarrow B \rightarrow C$). LLMs operate strictly inside processing nodes to perform transformations (e.g., text extraction, entity parsing) with zero side-effects on control flow.
2. **Dynamic LLM Routing (Router-DAG)**: The workflow skeleton remains fixed and deterministic, but key junction nodes use structured LLM outputs (e.g., JSON schema classification) to dynamically choose downstream branch paths.
3. **Hybrid State-Guarded Flow**: Autonomous agent loops are embedded within bounded sub-graphs. Outer deterministic guardrails validate state inputs and outputs, halting or redirecting execution if agent behavior violates invariants.

### Real-World Enterprise Use Cases

- **Automated Loan Application Processing**: Document ingestion (OCR) $\rightarrow$ Deterministic schema validation $\rightarrow$ LLM risk summary router $\rightarrow$ High-risk manual review queue vs. low-risk automated decision branch.
- **DevOps Incident Triage & Remediation**: Alarm ingestion $\rightarrow$ Deterministic metric/log gathering $\rightarrow$ LLM root cause classifier $\rightarrow$ Deterministic remediation script execution.

---

## 2. Architectural Component Mapping

To design resilient pipeline architectures, software engineers must map emerging AI agent concepts to proven distributed systems primitives:

| AI Jargon / Buzzword | Standard Software Engineering Primitive | Functional Architectural Description |
| :--- | :--- | :--- |
| **DAG Engine** | Directed Acyclic Graph Pipeline Runtime | An execution engine (e.g., Airflow, Prefect, Celery workflow, or custom async graph runner) that executes tasks according to topological dependency ordering. |
| **Router Node** | Polymorphic Conditional Control Dispatcher | A software `switch` or `if/else` block evaluated against a validated LLM structured JSON response payload. |
| **Dynamic Branching** | Runtime Evaluated Function Dispatch | Triggering specific downstream sub-routine functions based on classification outputs or schema evaluation results. |
| **Fallback Cascade** | Exception Handler / Circuit Breaker Degradation | Automatic step degradation from autonomous model routing to a hardcoded default rule-based path upon low confidence or model API failure. |
| **Node Schema Contract** | Strongly-Typed Inter-Step Interface | Pydantic / JSON Schema contracts validating intermediate data payloads passed between pipeline steps. |

---

## 3. Key Technical Aspects & Dig-In Topics

### SLA, Cost, and Latency Benchmarking

Mixing deterministic code with LLM routing requires explicit trade-off management across latency, cost, and determinism:

- **Hardcoded Code Branch**: Costs **$0.00**, executes in **<1ms**, and offers **100% determinism**.
- **LLM Router Node**: Costs **~$0.002–$0.01 per call**, incurs **300ms–1500ms latency**, and produces **probabilistic outcomes**.

Architects must enforce cost and latency budgets by confining LLM calls strictly to high-ambiguity decision boundaries, using deterministic algorithms (regex, string matching, rule tables) everywhere else.

### Schema Contracts & Inter-Node Invariants

Data passing between pipeline nodes must be bounded by strict schema contracts. Using libraries like Pydantic (Python) or Zod (TypeScript), each node validates incoming inputs and outgoing outputs.

```python
from pydantic import BaseModel, Field
from typing import Literal

class RouterOutput(BaseModel):
    intent: Literal["billing", "technical", "general_inquiry"]
    confidence_score: float = Field(ge=0.0, le=1.0)
    extracted_account_id: str | None = None

def evaluate_router_response(raw_json: str) -> RouterOutput:
    # Enforces strict schema validation before downstream step execution
    return RouterOutput.model_validate_json(raw_json)
```

If an LLM routing node returns invalid JSON or fails schema validation, the runtime catches the validation error at the boundary before downstream execution can be corrupted.

### Deterministic Guardrails & Fallback Cascades

Production systems implement a multi-tier fallback cascade to guarantee high availability even during LLM provider outages or model hallucination spikes:

1. **Tier 1 (Primary LLM Router)**: High-capability model executing structured JSON decoding.
2. **Tier 2 (Self-Correction Retry)**: If parsing or validation fails, retry with error context injected into prompt.
3. **Tier 3 (Secondary Lightweight Model)**: Fall back to a smaller, faster local or alternative model.
4. **Tier 4 (Hardcoded Default Rule)**: Fall back to a deterministic rule-based route (e.g., send to general queue).

```python
async def route_with_fallback(user_payload: str) -> str:
    try:
        res = await primary_llm_route(user_payload)
        return res.intent
    except (LLMError, ValidationError):
        try:
            res = await secondary_llm_route(user_payload)
            return res.intent
        except Exception:
            # Deterministic circuit breaker fallback
            return "general_inquiry"
```

### State Propagation & Topological Execution

In deterministic DAGs, pipeline state can be passed as an **immutable context object** created at execution initialization. Nodes receive the context, execute isolated logic, and produce explicit payload deltas. Topological sorting guarantees dependencies are resolved sequentially or concurrently in parallel execution branches without race conditions.

---

## 4. Future Lab Blueprint

### Lab 1: Baseline Architecture
- **Prompt Direction**: Architect a hybrid Router-DAG pipeline engine in Python/TypeScript without third-party agent frameworks. Implement an ingestion step, an LLM intent routing node returning structured JSON, and two deterministic downstream processing pipelines with strict Pydantic/Zod schema contracts.

### Lab 2: Intermediate Capability Integration
- **Prompt Direction**: Integrate a multi-tier resilience fallback cascade and execution telemetry meter into the DAG engine. Measure execution latency, token consumption, and path determinism under simulated LLM API timeouts, schema parsing errors, and malformed inputs.

### Lab 3: Enterprise Resilience & Advanced Edge Cases
- **Prompt Direction**: Extend the pipeline to handle dynamic topological step expansion and state rollback capabilities. Implement step-level idempotency keys, persistent step outcome caching (preventing redundant LLM re-computation on pipeline retries), and strict inter-node data sanitization boundaries.

### Stretch Goal: Production Hardening
- **Prompt Direction**: Package the Router-DAG engine into a distributed workflow framework deployment (e.g., Temporal or Prefect). Implement OpenTelemetry context propagation across pipeline steps, real-time node state monitoring, and automated SLA violation circuit breakers that automatically drop down to static rules under high model latency.
