# Context Chunker Design Specification

## 1. Overview & Architecture
The Context Chunker system (`core/context_chunker.py`) manages input context windows to ensure large inbox payloads stay well within the model's safe token budget (<= 40,000 characters).

When aggregated inbox notes exceed 40,000 characters, it splits the payload into natural context chunks, processes Stage 1 and Stage 2 independently per chunk, and merges chunk outputs prior to Stage 3 persona synthesis.

---

## 2. Component Responsibilities
- **Boundary-Aware Text Splitting**: Splits long text at natural boundaries in order of precedence: file header delimiters (`--- File: filename ---`), paragraph double-newlines (`\n\n`), and line breaks (`\n`). Never splits mid-word or mid-code block.
- **Independent Stage Execution**: Processes each chunk through Stage 1 (DIKW extraction) and Stage 2 (code snippet formatting & diagrams).
- **Chunk Merging**: Aggregates extracted insights and code blocks across all chunks into unified Stage 1 and Stage 2 representations before persona synthesis.
- **Observability Instrumentation**: Logs `chunk_count` and chunk character lengths to OpenTelemetry traces via `OTelTracer`.

---

## 3. Interfaces & Key Functions
- `chunk_text(text: str, max_chars: int = 40000) -> list[str]`: Takes aggregated input string and splits it into a list of strings where each string is <= `max_chars`.
- `merge_chunk_outputs(stage1_outputs: list[str], stage2_outputs: list[str]) -> tuple[str, str]`: Combines multi-chunk Stage 1 and Stage 2 intermediate outputs into single merged context blocks.

---

## 4. Edge Cases & Safety Margins
- **Payload <= 40,000 chars**: Returns single-item list containing original text without overhead.
- **Single File Exceeding Limit**: Splits on paragraph or line boundaries within the file.
