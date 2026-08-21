# Inbox Manager Design Specification

## 1. Overview & Architecture
The Inbox Manager module (`tools/inbox_manager.py`) provides file system scanning, aggregation, boundary tagging, and post-run archiving functions for input notes dropped into `inbox/`.

It decouples file system operations from the core reasoning pipeline, ensuring clean file ingestion and atomic workspace cleanup.

---

## 2. Component Responsibilities
- **Inbox Scanning**: Traverses `inbox/` recursively to collect supported text format files (`.py`, `.md`, `.txt`, `.json`, `.yaml`, `.yml`, `.sh`, `.ps1`).
- **Context Aggregation**: Combines collected files into a single text payload while prepending explicit header delimiters (`--- File: filename ---`) to preserve file context and origin.
- **Topic Slug Generation**: Derives a clean directory slug from folder names or filenames to structure output posts and archive targets.
- **Inbox Archiving**: Atomically moves processed items from `inbox/` to `processed/<timestamp>_<topic_slug>/` upon successful run completion.

---

## 3. Interfaces & Key Functions
- `has_unprocessed_items() -> bool`: Returns `True` if readable text/code files exist in `inbox/`.
- `read_all_inbox_contents() -> dict[str, Any]`: Aggregates all inbox files into a single string payload, returning a dictionary containing `aggregated_text`, `item_names`, `character_count`, and `topic_slug`.
- `archive_inbox(topic_slug: str) -> Path`: Creates a timestamped directory under `processed/` and moves all items currently in `inbox/` into it.

---

## 4. Error Handling
- **Binary / Corrupted Files**: Encounters with binary or unparseable text files catch file reading errors gracefully and continue reading remaining files.
- **Empty Inbox**: Returns explicit empty payload flags allowing callers to halt execution safely without processing empty inputs.
