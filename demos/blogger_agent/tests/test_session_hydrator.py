"""
Unit tests for SessionStateHydrator primitive
"""

from core.session_hydrator import SessionStateHydrator


def test_session_hydrator_mark_processed_and_checkpoint(tmp_path):
    """
    Core behavior test:
    Loads state, marks folder as processed, sets checkpoint, saves, and reloads state.
    """
    state_file = tmp_path / "session_state.json"
    hydrator = SessionStateHydrator(state_file)

    assert not hydrator.is_processed("2026-08-09_folder1")
    hydrator.mark_processed("2026-08-09_folder1")
    assert hydrator.is_processed("2026-08-09_folder1")

    hydrator.set_checkpoint("stage2_complete", {"chunks": 2})
    assert hydrator.state["checkpoint"]["name"] == "stage2_complete"

    # Reload from disk
    hydrator2 = SessionStateHydrator(state_file)
    assert hydrator2.is_processed("2026-08-09_folder1")
    assert hydrator2.state["checkpoint"]["name"] == "stage2_complete"

    hydrator2.clear_checkpoint()
    assert hydrator2.state["checkpoint"] is None


def test_session_hydrator_handles_corrupted_json(tmp_path):
    """
    Failure / Negative path test:
    Handles invalid or corrupted state JSON file by initializing default state cleanly.
    """
    state_file = tmp_path / "corrupt_state.json"
    state_file.write_text("{invalid json content:", encoding="utf-8")

    hydrator = SessionStateHydrator(state_file)
    assert hydrator.state["last_run"] is None
    assert hydrator.state["processed_folders"] == []
    assert hydrator.state["checkpoint"] is None
