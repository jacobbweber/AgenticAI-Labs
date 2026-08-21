# Blog Pipeline Design Specification

## 1. Overview & Architecture
The Blog Pipeline system (`core/multi_stage_pipeline.py` and `core/orchestrator.py`) is responsible for orchestrating the multi-stage conversion of raw technical notes into high-quality, human-sounding technical blog posts written in Jacob Weber's voice.

It coordinates:
1. Input ingestion from `inbox/` via `InboxManager`.
2. Large context partitioning via `ContextChunker`.
3. Stage 1 Data-Information-Knowledge-Wisdom (DIKW) concept extraction.
4. Stage 2 Code & Diagram structure extraction.
5. Stage 3 Persona & Voice synthesis combining Jacob Weber's historical writing style with extracted insights.
6. Quality verification via `QualityGuard`.
7. Git Pull Request creation and inbox archiving.

---

## 2. Component Responsibilities
- **Stage 1 (DIKW Extractor)**: Reads raw text/code notes and identifies foundational principles, key terms, data points, and practical wisdom.
- **Stage 2 (Code/Diagram Synthesizer)**: Extracts raw code snippets, refactors them for presentation, and generates standard Mermaid sequence/flowchart diagrams.
- **Stage 3 (Persona Synthesizer)**: Merges Stage 1 and Stage 2 outputs with Jacob Weber's persona rules and style samples to draft a comprehensive, human-sounding blog post in Chirpy Jekyll format.
- **Orchestrator**: Controls the execution flow, state checkpoints, error recovery, Git branch creation, PR opening, and inbox archiving.

---

## 3. Interface Contracts & Data Flow
- **Input**: Aggregated text string containing raw file content from `inbox/`.
- **Intermediate Artifacts**:
  - `stage1_dikw`: Extracted concepts and wisdom.
  - `stage2_code`: Formatted code blocks and Mermaid diagrams.
  - `stage3_draft`: Full draft of the blog post in markdown format.
- **Output**: Validated markdown post file saved under `_posts/` in the Jekyll repository, accompanied by a GitHub PR URL.

---

## 4. Failure Modes & Error Recovery
- **Ollama Timeout / Connection Drop**: Handled by LLM Gateway retries with exponential backoff.
- **Validation Failure (leakage or missing frontmatter)**: Handled by `LogitSteeringGuard` auto-repair or `ReflexionEngine` feedback retry loop.
- **Low Skeptic Score (<7)**: Handled by `QualityGuard` Pass 3 targeted section rewrites.
