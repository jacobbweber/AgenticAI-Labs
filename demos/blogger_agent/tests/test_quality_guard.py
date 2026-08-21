"""
Unit tests for QualityGuard primitive (Pass 1 Self Review, Pass 2 Skeptic Review, Pass 3 Targeted Rewrite)
"""

from unittest.mock import MagicMock

import pytest

from api.llm_gateway import MultiModelGatewayRouter
from core.quality_guard import QualityGuard, run_quality_pipeline
from evals.otel_tracer import OTelEvalTracer


def test_quality_guard_multi_pass_success(tmp_path):
    """
    Core behavior test:
    Executes Pass 1 (Self Review), Pass 2 (Skeptic Review score 9 >= 7),
    Pass 3 (0 rewrites applied), and logs OTel trace entries.
    """
    mock_router = MagicMock(spec=MultiModelGatewayRouter)
    mock_router.generate.side_effect = [
        "Self Review: All concepts covered.",  # Pass 1
        "SCORE: 9\nFINDINGS:\n- Excellent human-like technical blog post.",  # Pass 2
    ]

    trace_file = tmp_path / "otel_traces.jsonl"
    tracer = OTelEvalTracer(trace_file)
    guard = QualityGuard(mock_router, tracer)

    draft = (
        "---\n"
        "layout: post\n"
        'title: "Clean Technical Notes"\n'
        "date: 2026-08-09 12:00:00 -0000\n"
        "tags: [ai]\n"
        "---\n\n"
        "# What I Worked On, My Thoughts & Findings\n"
        "Today I worked on building robust LLM evaluation pipelines.\n\n"
        "## Data & Technical Facts\n"
        "The system uses Python 3.12 and pytest.\n\n"
        "## Knowledge & Key Learnings\n"
        "Multi-pass evaluation improves output fidelity.\n\n"
        "## Wisdom & My Take\n"
        "Automated gates provide strong quality guarantees.\n"
    )
    inbox_content = "Lab notes on LLM evaluation pipelines."

    result = guard.run_pipeline(draft, inbox_content)

    assert result["passed"]
    assert result["skeptic_score"] == 9
    assert result["rewrites_applied"] == 0
    assert result["final_draft"] == draft

    # Verify OTel trace records created
    trace_text = trace_file.read_text(encoding="utf-8")
    assert "self_review_pass" in trace_text
    assert "skeptic_review_pass" in trace_text
    assert "final_polish_pass" in trace_text


def test_quality_guard_triggers_targeted_rewrite_on_low_score(tmp_path):
    """
    Rewrite path test:
    Pass 2 skeptic review initially scores < 7 due to AI transitions.
    Pass 3 targeted rewrite runs, updating the draft, and re-evaluates to score >= 7.
    """
    mock_router = MagicMock(spec=MultiModelGatewayRouter)

    polished_draft = (
        "---\n"
        "layout: post\n"
        'title: "Polished Technical Notes"\n'
        "date: 2026-08-09 12:00:00 -0000\n"
        "tags: [ai]\n"
        "---\n\n"
        "# What I Worked On, My Thoughts & Findings\n"
        "I built resilient LLM evaluation pipelines today.\n\n"
        "## Data & Technical Facts\n"
        "The system runs on Python 3.12.\n\n"
        "## Knowledge & Key Learnings\n"
        "Direct writing voice is clearer than AI transition filler.\n\n"
        "## Wisdom & My Take\n"
        "Quality gates ensure production standard posts.\n"
    )

    mock_router.generate.side_effect = [
        "Self Review: Needs polish.",  # Pass 1
        "SCORE: 5\nFINDINGS:\n- AI transition 'Furthermore' used.",  # Pass 2 (Initial)
        polished_draft,  # Pass 3 Rewrite
        "SCORE: 8\nFINDINGS:\n- Cleaned up, strong human voice.",  # Pass 2 (Re-evaluation)
    ]

    trace_file = tmp_path / "otel_traces.jsonl"
    tracer = OTelEvalTracer(trace_file)

    initial_draft = (
        "---\n"
        "layout: post\n"
        'title: "Polished Technical Notes"\n'
        "date: 2026-08-09 12:00:00 -0000\n"
        "tags: [ai]\n"
        "---\n\n"
        "# What I Worked On, My Thoughts & Findings\n"
        "Furthermore, it is worth noting I built evaluation pipelines.\n"
    )

    result = run_quality_pipeline(initial_draft, "Lab notes", mock_router, tracer)

    assert result["passed"]
    assert result["skeptic_score"] == 8
    assert result["rewrites_applied"] == 1
    assert result["final_draft"] == polished_draft

    trace_text = trace_file.read_text(encoding="utf-8")
    assert "final_polish_pass" in trace_text


def test_quality_guard_raises_error_if_score_remains_low(tmp_path):
    """
    Failure path test:
    Skeptic score remains < 7 after max rewrite attempts, raising ValueError.
    """
    mock_router = MagicMock(spec=MultiModelGatewayRouter)
    mock_router.generate.side_effect = [
        "Self Review: Poor coverage.",  # Pass 1
        "SCORE: 4\nFINDINGS:\n- Low quality draft.",  # Pass 2 attempt 0
        "Draft Attempt 1",  # Rewrite 1
        "SCORE: 4\nFINDINGS:\n- Still low quality.",  # Pass 2 attempt 1
        "Draft Attempt 2",  # Rewrite 2
        "SCORE: 4\nFINDINGS:\n- Still low quality.",  # Pass 2 attempt 2
        "Draft Attempt 3",  # Rewrite 3
        "SCORE: 4\nFINDINGS:\n- Still low quality.",  # Pass 2 attempt 3
    ]

    guard = QualityGuard(mock_router, max_rewrites=3)
    draft = "Low quality content"

    with pytest.raises(ValueError) as exc_info:
        guard.run_pipeline(draft, "Lab notes")

    assert "QualityGuard failed to achieve skeptic score >= 7" in str(exc_info.value)
