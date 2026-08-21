"""
CycleOscillationDetector Primitive
Detects and breaks infinite execution loops or repeating tool error cycles.
"""

import hashlib
from typing import Any


class OscillationDetectedException(Exception):
    """Raised when an infinite loop or repeated failure state is detected."""

    pass


class CycleOscillationDetector:
    def __init__(self, max_repeated_patterns: int = 3):
        self.max_repeated_patterns = max_repeated_patterns
        self.action_history: list[str] = []

    def _hash_action(self, action_name: str, payload: Any) -> str:
        raw_str = f"{action_name}:{str(payload)}"
        return hashlib.md5(raw_str.encode("utf-8")).hexdigest()

    def record_and_check(self, action_name: str, payload: Any) -> None:
        """
        Record an action signature and raise OscillationDetectedException
        if the signature recurs beyond max_repeated_patterns.
        """
        action_hash = self._hash_action(action_name, payload)
        self.action_history.append(action_hash)

        # Count consecutive identical actions
        consecutive_count = 0
        for item in reversed(self.action_history):
            if item == action_hash:
                consecutive_count += 1
            else:
                break

        if consecutive_count >= self.max_repeated_patterns:
            raise OscillationDetectedException(
                f"Oscillation detected: Action '{action_name}' repeated {consecutive_count} times with identical inputs."
            )

    def reset(self) -> None:
        self.action_history.clear()
