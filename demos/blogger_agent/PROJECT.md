# Project: Autonomous Headless Blogging Agent

## Architecture
- Decoupled System Architecture: `core/`, `api/`, `tools/`, `evals/`, `specs/`, `docs/`, `tests/`
- Data flow: `inbox/` -> `tools/inbox_manager.py` -> `core/context_chunker.py` (Stage 1 DIKW + Stage 2 Code/Diagrams per chunk -> merge) -> `core/multi_stage_pipeline.py` (Stage 3 Persona Synthesis) -> `core/quality_guard.py` (Pass 1 Self Review -> Pass 2 Skeptic Review 1-10 -> Pass 3 Targeted Rewrite) -> `evals/otel_tracer.py` -> Git PR creation -> `processed/` archive.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | R1 Spec-Driven Foundation | Create `specs/` directory with EARS requirements (`design.md`, `requirements.md`, `tasks.md`) for `blog_pipeline`, `inbox_manager`, `llm_gateway`, `quality_guard`, `context_chunker`. | M1 | ORIGINAL_REQUEST R1 |
| 2 | R2 Coding Standards & Docs | Create `docs/coding_standards.md` documenting architecture, code style, linter, pytest conventions. | M1 | ORIGINAL_REQUEST R2 |
| 3 | R2 Linter Configuration | Add `pyproject.toml` with `ruff` config for `core/`, `api/`, `tools/`, `evals/`. Zero linter errors. | M1 | ORIGINAL_REQUEST R2 |
| 4 | R2 Unit Test Suite | Create `tests/` with >= 8 pytest unit tests covering core behavior and negative paths for 6 primitives: `InboxManager`, `LogitSteeringGuard`, `MultiStageReasoningPipeline`, `MultiModelGatewayRouter`, `ReflexionEngine`, `SessionStateHydrator`. | M3 | ORIGINAL_REQUEST R2 |
| 5 | R5 Resilient Ollama Integration | Update `api/llm_gateway.py` (`MultiModelGatewayRouter`) with timeout >= 300s, max 5 retries, exponential backoff (5s->15s->45s->135s->405s), terminal retry logging, RuntimeError on exhaustion, and pytest failure mocking. | M2 | ORIGINAL_REQUEST R5 |
| 6 | R4 Context Window Chunking | Implement `core/context_chunker.py` (>40k chars chunking at file/paragraph boundaries, independent Stage 1 & 2 per chunk, merge before Stage 3, log `chunk_count` to OTel, pytest chunking test). | M2 | ORIGINAL_REQUEST R4 |
| 7 | R3 Multi-Pass Review Pipeline | Implement `core/quality_guard.py` (Pass 1 Self Review, Pass 2 Skeptic 1-10 rubric, Pass 3 Targeted Rewrite if score < 7, recorded skeptic score >= 7, OTel trace logging for `self_review_pass`, `skeptic_review_pass`, `final_polish_pass`). | M3 | ORIGINAL_REQUEST R3 |
| 8 | R6 End-to-End Verified Run | Integration of pipeline in `main.py` / `core/orchestrator.py`. Reset `session_state.json`, process inbox, zero `failed[]`, PR created, archived to `processed/`, markdown post quality check. | M4 | ORIGINAL_REQUEST R6 |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | M1: Specs & Coding Standards | R1 specs (`specs/` with EARS requirements) + R2 coding standards (`docs/coding_standards.md`) & linter config (`pyproject.toml`) | None | DONE |
| 2 | M2: Ollama Resilience & Context Chunking | R5 Resilient Ollama Integration (`api/llm_gateway.py`) + R4 Context Window Chunking (`core/context_chunker.py`, `core/multi_stage_pipeline.py`) | M1 | DONE |
| 3 | M3: Multi-Pass Quality Pipeline & Unit Tests | R3 Quality Guard (`core/quality_guard.py`) + R2 Unit Test Suite (`tests/` >= 8 tests) + OTel trace logging | M2 | DONE |
| 4 | M4: End-to-End Verification & Test Suite Hardening | R6 Integration execution (`python main.py` E2E verification) + E2E test suite validation | M3 | DONE |

## Interface Contracts
### `core/context_chunker.py` ↔ `core/multi_stage_pipeline.py`
- `chunk_text(text: str, max_chars: int = 40000) -> list[str]`
- Splits text on paragraph double-newlines or file boundaries into chunks <= max_chars.

### `core/quality_guard.py` ↔ `core/multi_stage_pipeline.py` / `core/orchestrator.py`
- `run_quality_pipeline(draft: str, inbox_content: str, router, tracer) -> dict`
- Executes Pass 1 (Self Review), Pass 2 (Skeptic Review 1-10 scoring), Pass 3 (Targeted Rewrite if score < 7 until score >= 7 or max rewrites).

### `api/llm_gateway.py` (`MultiModelGatewayRouter`)
- `generate(prompt: str, system_prompt: str = None) -> str`
- Timeout: >= 300s. Max retries: 5. Exponential backoff: `5 * (3 ** (attempt - 1))`. Raises `RuntimeError` on failure.

## Code Layout
- `specs/` — EARS specs (`blog_pipeline`, `inbox_manager`, `llm_gateway`, `quality_guard`, `context_chunker`)
- `docs/coding_standards.md` — Architectural and coding guidelines
- `pyproject.toml` — Ruff linting config
- `core/` — `orchestrator.py`, `multi_stage_pipeline.py`, `context_chunker.py`, `quality_guard.py`, `reflexion_engine.py`, `session_hydrator.py`, `cycle_detector.py`
- `api/` — `llm_gateway.py`, `schema_steering.py`
- `tools/` — `inbox_manager.py`, `style_extractor.py`, `sandbox_worker.py`
- `evals/` — `otel_tracer.py`
- `tests/` — pytest test suite (`test_inbox_manager.py`, `test_schema_steering.py`, `test_multi_stage_pipeline.py`, `test_llm_gateway.py`, `test_reflexion_engine.py`, `test_session_hydrator.py`, `test_context_chunker.py`, `test_quality_guard.py`)
