"""
Unit tests for ContextChunker (R4 Context Window Chunking)
"""

from core.context_chunker import ContextChunker


def test_chunk_text_small_input():
    """Verifies text <= max_chars returns a single chunk."""
    chunker = ContextChunker()
    text = "Short lab notes.\n" * 10
    chunks = chunker.chunk_text(text, max_chars=40000)
    assert len(chunks) == 1
    assert chunks[0] == text


def test_chunk_text_exceeding_40k_chars_splits_into_multiple_chunks():
    """
    Verifies that aggregated text exceeding 40,000 characters
    is split into at least 2 chunks, and every chunk is <= 40,000 characters.
    """
    chunker = ContextChunker()

    # Create 3 sections of 25,000 characters each separated by \n\n (total 75,000+ chars)
    file1 = "--- File: doc1.md ---\n" + ("A" * 25000)
    file2 = "--- File: doc2.md ---\n" + ("B" * 25000)
    file3 = "--- File: doc3.md ---\n" + ("C" * 25000)

    combined_text = f"{file1}\n\n{file2}\n\n{file3}"
    assert len(combined_text) > 40000

    chunks = chunker.chunk_text(combined_text, max_chars=40000)

    # Must be split into at least 2 chunks (here 3 chunks of ~25k each)
    assert len(chunks) >= 2
    for idx, chunk in enumerate(chunks):
        assert len(chunk) <= 40000, f"Chunk {idx} exceeded 40,000 chars ({len(chunk)} chars)"

    # Verify content coverage
    assert "--- File: doc1.md ---" in chunks[0]
    assert "--- File: doc2.md ---" in chunks[1]
    assert "--- File: doc3.md ---" in chunks[2]


def test_chunk_text_natural_boundary_splitting():
    """Verifies chunking preserves paragraph double-newline boundaries."""
    chunker = ContextChunker()

    # Create paragraphs of ~15k characters each
    para1 = "Paragraph 1: " + ("1" * 15000)
    para2 = "Paragraph 2: " + ("2" * 15000)
    para3 = "Paragraph 3: " + ("3" * 15000)

    text = f"{para1}\n\n{para2}\n\n{para3}"

    chunks = chunker.chunk_text(text, max_chars=32000)
    assert len(chunks) == 2
    # First chunk should contain para1 and para2 (30k chars <= 32k)
    assert para1 in chunks[0]
    assert para2 in chunks[0]
    # Second chunk should contain para3
    assert para3 in chunks[1]


def test_chunk_text_empty_and_edge_cases():
    """Verifies behavior on empty string and long single line."""
    chunker = ContextChunker()
    assert chunker.chunk_text("", max_chars=40000) == [""]

    long_line = "X" * 50000
    chunks = chunker.chunk_text(long_line, max_chars=20000)
    assert len(chunks) == 3
    for chunk in chunks:
        assert len(chunk) <= 20000
