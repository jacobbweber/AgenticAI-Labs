"""
Unit tests for InboxManager primitive
"""

from tools.inbox_manager import InboxManager


def test_inbox_manager_has_content_and_read_and_archive(tmp_path):
    """
    Core behavior test:
    Populates inbox directory with test files, verifies has_inbox_content(),
    reads all contents, and archives them into processed_dir.
    """
    inbox_dir = tmp_path / "inbox"
    processed_dir = tmp_path / "processed"

    manager = InboxManager(inbox_dir, processed_dir)
    assert not manager.has_inbox_content()

    # Create dummy inbox content
    file1 = inbox_dir / "lab1.md"
    file1.write_text("# Lab 1 Notes\nSome content.", encoding="utf-8")

    sub_dir = inbox_dir / "01_sub"
    sub_dir.mkdir()
    file2 = sub_dir / "script.py"
    file2.write_text("print('hello')", encoding="utf-8")

    assert manager.has_inbox_content()

    data = manager.read_all_inbox_contents()
    assert "primary_slug" in data
    assert "lab1.md" in data["item_names"]
    assert "# Lab 1 Notes" in data["combined_content"]
    assert "print('hello')" in data["combined_content"]

    archive_path = manager.archive_inbox_contents("test_topic")
    assert archive_path.exists()
    assert not manager.has_inbox_content()
    assert (archive_path / "lab1.md").exists()


def test_inbox_manager_empty_inbox_negative_path(tmp_path):
    """
    Failure / Negative path test:
    Verifies behavior when inbox is empty.
    """
    inbox_dir = tmp_path / "inbox"
    processed_dir = tmp_path / "processed"

    manager = InboxManager(inbox_dir, processed_dir)
    assert not manager.has_inbox_content()

    data = manager.read_all_inbox_contents()
    assert data["item_names"] == []
    assert data["combined_content"] == ""
    assert data["primary_slug"] == "inbox_synthesis"

    archive_path = manager.archive_inbox_contents("empty_topic")
    assert archive_path.exists()
    assert len(list(archive_path.iterdir())) == 0
