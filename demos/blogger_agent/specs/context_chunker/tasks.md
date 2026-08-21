# Context Chunker Implementation Tasks

- [ ] Task 1: Create `core/context_chunker.py` with boundary-aware text splitting algorithm.
- [ ] Task 2: Implement `chunk_text()` supporting file delimiter and paragraph splitting logic.
- [ ] Task 3: Integrate `ContextChunker` into `MultiStageReasoningPipeline.run_pipeline()`.
- [ ] Task 4: Implement intermediate chunk result merging for Stage 1 and Stage 2 outputs.
- [ ] Task 5: Instrument `chunk_count` logging in `evals/otel_tracer.py`.
- [ ] Task 6: Add pytest unit tests in `tests/test_context_chunker.py` verifying that payloads > 40,000 characters split into at least 2 valid chunks.
