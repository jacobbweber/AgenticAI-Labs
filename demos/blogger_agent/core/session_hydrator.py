"""
SessionStateHydrator Primitive
Handles state persistence and checkpoint hydration across agent executions.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class SessionStateHydrator:
    def __init__(self, state_filepath: Path):
        self.state_filepath = state_filepath
        self.state: dict[str, Any] = self._load_state()

    def _load_state(self) -> dict[str, Any]:
        if self.state_filepath.exists():
            try:
                with open(self.state_filepath, encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "last_run": None,
            "processed_folders": [],
            "history": [],
            "checkpoint": None,
        }

    def save(self) -> None:
        self.state_filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_filepath, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2)

    def is_processed(self, folder_name: str) -> bool:
        return folder_name in self.state.get("processed_folders", [])

    def mark_processed(self, folder_name: str) -> None:
        if folder_name not in self.state["processed_folders"]:
            self.state["processed_folders"].append(folder_name)
        self.state["last_run"] = datetime.now().isoformat()
        self.save()

    def log_history_event(self, event_type: str, details: dict[str, Any]) -> None:
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "details": details,
        }
        self.state.setdefault("history", []).append(event)
        self.save()

    def set_checkpoint(self, checkpoint_name: str, payload: dict[str, Any]) -> None:
        self.state["checkpoint"] = {
            "name": checkpoint_name,
            "timestamp": datetime.now().isoformat(),
            "payload": payload,
        }
        self.save()

    def clear_checkpoint(self) -> None:
        self.state["checkpoint"] = None
        self.save()
