"""
Inbox Manager Tool
Scans un-dated inbox contents, aggregates all files for single-post generation,
and moves processed materials into a newly created timestamped directory in processed/.
"""

import shutil
from datetime import datetime
from pathlib import Path
from typing import Any


class InboxManager:
    def __init__(self, inbox_dir: Path, processed_dir: Path):
        self.inbox_dir = inbox_dir
        self.processed_dir = processed_dir
        self.inbox_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def has_inbox_content(self) -> bool:
        """Returns True if there are any files or directories inside inbox/."""
        items = list(self.inbox_dir.iterdir())
        return len(items) > 0

    def read_all_inbox_contents(self) -> dict[str, Any]:
        """
        Scans all files and directories inside inbox/ and combines all text, markdown,
        and code script files into a single aggregated payload.
        """
        content_pieces: list[str] = []
        item_names: list[str] = []

        supported_extensions = [
            ".md", ".txt", ".json", ".yaml", ".yml",
            ".py", ".sh", ".ps1", ".js", ".ts", ".html", ".css"
        ]

        for item in sorted(self.inbox_dir.iterdir(), key=lambda x: x.name):
            item_names.append(item.name)
            if item.is_file():
                if item.suffix.lower() in supported_extensions or item.name.startswith("README"):
                    try:
                        text = item.read_text(encoding="utf-8")
                        content_pieces.append(f"--- File: {item.name} ---\n{text}\n")
                    except Exception:
                        pass
            elif item.is_dir():
                for subfile in sorted(item.rglob("*")):
                    if subfile.is_file() and (subfile.suffix.lower() in supported_extensions or subfile.name.startswith("README")):
                        try:
                            rel_path = subfile.relative_to(self.inbox_dir)
                            text = subfile.read_text(encoding="utf-8")
                            content_pieces.append(f"--- File: {rel_path} ---\n{text}\n")
                        except Exception:
                            pass

        if len(item_names) == 1:
            primary_slug = item_names[0].replace(" ", "_").lower()
        elif len(item_names) > 1:
            primary_slug = f"{item_names[0]}_and_{len(item_names)-1}_more"
        else:
            primary_slug = "inbox_synthesis"

        return {
            "primary_slug": primary_slug,
            "item_names": item_names,
            "combined_content": "\n".join(content_pieces),
        }

    def archive_inbox_contents(self, topic_slug: str) -> Path:
        """
        Creates a new timestamped directory in processed/ (e.g. processed/YYYY-MM-DD-HHMMSS_topic_slug)
        and moves all items currently in inbox/ into it.
        """
        timestamp_str = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        clean_slug = topic_slug.replace(" ", "_").lower()
        archive_dir_name = f"{timestamp_str}_{clean_slug}"
        target_archive_dir = self.processed_dir / archive_dir_name

        target_archive_dir.mkdir(parents=True, exist_ok=True)

        for item in list(self.inbox_dir.iterdir()):
            dest = target_archive_dir / item.name
            if dest.exists():
                if dest.is_dir():
                    shutil.rmtree(dest)
                else:
                    dest.unlink()
            shutil.move(str(item), str(dest))

        return target_archive_dir
