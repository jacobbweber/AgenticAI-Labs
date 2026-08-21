"""
Unit tests for ReflexionEngine primitive
"""

from core.reflexion_engine import ReflexionEngine


def test_reflexion_engine_success_with_reflection():
    """
    Core behavior test:
    Attempts fail initial validation, but succeeds on reflection after feedback is provided.
    """
    engine = ReflexionEngine(max_reflections=3)
    attempt_counter = 0

    def mock_gen(feedback: str | None) -> str:
        nonlocal attempt_counter
        attempt_counter += 1
        if attempt_counter == 1:
            return "Attempt 1 content without header"
        return "Attempt 2 content with # What I Worked On header"

    def mock_val(output: str) -> tuple[bool, str | None]:
        if "# What I Worked On" in output:
            return True, None
        return False, "Missing header '# What I Worked On'"

    out, is_valid, attempts = engine.execute_with_reflection(mock_gen, mock_val)
    assert is_valid
    assert attempts == 2
    assert "# What I Worked On" in out


def test_reflexion_engine_exhausts_attempts_on_failure():
    """
    Failure / Negative path test:
    All attempts fail validation, and ReflexionEngine returns (last_output, False, max_reflections).
    """
    engine = ReflexionEngine(max_reflections=3)

    def mock_gen(feedback: str | None) -> str:
        return "Always invalid content"

    def mock_val(output: str) -> tuple[bool, str | None]:
        return False, "Always failing validation rule"

    out, is_valid, attempts = engine.execute_with_reflection(mock_gen, mock_val)
    assert not is_valid
    assert attempts == 3
    assert out == "Always invalid content"
