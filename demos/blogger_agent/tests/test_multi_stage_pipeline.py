"""
Unit tests for MultiStageReasoningPipeline (Context Chunking Integration)
"""

from unittest.mock import MagicMock

import pytest

from api.llm_gateway import MultiModelGatewayRouter
from core.multi_stage_pipeline import MultiStageReasoningPipeline


def test_pipeline_single_chunk_execution():
    """Verifies pipeline execution when input fits in a single chunk."""
    mock_router = MagicMock(spec=MultiModelGatewayRouter)
    mock_router.generate.side_effect = [
        "DATA:\nInformation:\nKnowledge:\nWisdom:",  # Stage 1
        "```python\nprint('hello')\n```",  # Stage 2
        "Test Title",  # Stage 3a Title
        '# What I Worked On, My Thoughts & Findings\n## Data & Technical Facts\nTest',  # Stage 3b Body
    ]

    pipeline = MultiStageReasoningPipeline(mock_router, "Style prompt")
    result = pipeline.execute_pipeline("Short input text")

    assert "layout: post" in result
    assert 'title: "Test Title"' in result
    assert pipeline.last_chunk_count == 1
    assert mock_router.generate.call_count == 4


def test_pipeline_multi_chunk_execution():
    """
    Verifies pipeline execution when input exceeds 40,000 characters.
    Stage 1 & Stage 2 run independently per chunk, outputs are merged,
    and Stage 3 runs once on the merged output.
    """
    mock_router = MagicMock(spec=MultiModelGatewayRouter)

    # Create input text > 40,000 chars (2 blocks of ~25,000 chars)
    block1 = "--- File: part1.md ---\n" + ("1" * 25000)
    block2 = "--- File: part2.md ---\n" + ("2" * 25000)
    large_input = f"{block1}\n\n{block2}"

    # For 2 chunks, router will be called:
    # Chunk 1 Stage 1, Chunk 1 Stage 2
    # Chunk 2 Stage 1, Chunk 2 Stage 2
    # Stage 3a Title, Stage 3b Body
    mock_router.generate.side_effect = [
        "Stage 1 Chunk 1 DIKW",  # Chunk 1 Stage 1
        "Stage 2 Chunk 1 Code",  # Chunk 1 Stage 2
        "Stage 1 Chunk 2 DIKW",  # Chunk 2 Stage 1
        "Stage 2 Chunk 2 Code",  # Chunk 2 Stage 2
        "Large Synthesis Title",  # Stage 3a Title
        '# What I Worked On, My Thoughts & Findings\nMerged content synthesis',  # Stage 3b Body
    ]

    pipeline = MultiStageReasoningPipeline(mock_router, "Style prompt")
    result = pipeline.execute_pipeline(large_input)

    assert pipeline.last_chunk_count == 2
    assert len(pipeline.last_chunk_sizes) == 2
    assert mock_router.generate.call_count == 6
    assert "Large Synthesis Title" in result


def test_pipeline_gateway_error_propagation():
    """
    Failure / Negative path test:
    Verifies that if LLM gateway raises an exception, the pipeline propagates the error.
    """
    mock_router = MagicMock(spec=MultiModelGatewayRouter)
    mock_router.generate.side_effect = RuntimeError("Ollama service unavailable")

    pipeline = MultiStageReasoningPipeline(mock_router, "Style prompt")
    with pytest.raises(RuntimeError) as exc_info:
        pipeline.execute_pipeline("Sample text")

    assert "Ollama service unavailable" in str(exc_info.value)
