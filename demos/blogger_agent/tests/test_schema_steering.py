"""
Unit tests for LogitSteeringGuard primitive
"""

from api.schema_steering import LogitSteeringGuard


def test_logit_steering_valid_post_structure():
    """
    Core behavior test:
    Validates a correctly formatted Chirpy Jekyll blog post with DIKW headers.
    """
    guard = LogitSteeringGuard()
    valid_post = (
        "---\n"
        "layout: post\n"
        'title: "Building Resilient Agent Systems"\n'
        "date: 2026-08-09 12:00:00 -0000\n"
        "categories: [ai]\n"
        "tags: [agents, python]\n"
        "---\n\n"
        "# What I Worked On, My Thoughts & Findings\n"
        "Today I built a resilient blogging pipeline with OpenTelemetry tracing and schema steering.\n\n"
        "## Data & Technical Facts\n"
        "The system uses Python 3.12, Ollama gateway retry loops with exponential backoff, and pytest.\n\n"
        "## Information & System Connections\n"
        "The orchestrator connects the inbox manager to context chunking and reflexion loops.\n\n"
        "## Knowledge & Key Learnings\n"
        "Reflexion engines allow agents to self-correct validation errors automatically.\n\n"
        "## Wisdom & My Take\n"
        "Automated evaluation gates prevent bad drafts from leaking into production blog repositories.\n"
    )

    is_valid, error = guard.validate_post_structure(valid_post)
    assert is_valid, f"Expected valid post, got error: {error}"
    assert error is None


def test_logit_steering_detects_prompt_leakage_and_missing_frontmatter():
    """
    Failure / Negative path test:
    Verifies detection of prompt leakage, forbidden terms in title, and missing DIKW headers.
    """
    guard = LogitSteeringGuard()

    # 1. Missing frontmatter declaration
    invalid_no_fm = "Just some text without frontmatter"
    is_valid, err = guard.validate_post_structure(invalid_no_fm)
    assert not is_valid
    assert "Post must start with '---'" in err

    # 2. Forbidden title phrase
    invalid_title = (
        "---\n"
        "layout: post\n"
        'title: "Synthesize notes into a post"\n'
        "date: 2026-08-09 12:00:00 -0000\n"
        "tags: [ai]\n"
        "---\n"
        "# What I Worked On\n" + ("content " * 20)
    )
    is_valid, err = guard.validate_post_structure(invalid_title)
    assert not is_valid
    assert "Post title contains prompt instruction text" in err

    # 3. Prompt leakage pattern in body
    invalid_leakage = (
        "---\n"
        "layout: post\n"
        'title: "Valid Title"\n'
        "date: 2026-08-09 12:00:00 -0000\n"
        "tags: [ai]\n"
        "---\n"
        "Here is a blog post based on the notes provided in the prompt.\n"
        "# What I Worked On\n" + ("content " * 20)
    )
    is_valid, err = guard.validate_post_structure(invalid_leakage)
    assert not is_valid
    assert "AI Meta-Text Prompt Leakage detected" in err
