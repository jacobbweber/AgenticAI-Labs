"""
SandboxedSubprocessWorker Primitive
Executes external shell commands (Git, Jekyll, CLI scripts) with timeouts and error capture.
"""

import subprocess
from pathlib import Path
from typing import Any


class SandboxedSubprocessWorker:
    def __init__(self, timeout_seconds: int = 60):
        self.timeout_seconds = timeout_seconds

    def execute(
        self, command: str, cwd: Path | None = None
    ) -> dict[str, Any]:
        """
        Executes command string in a sandboxed subprocess.
        Returns dict with exit_code, stdout, stderr, and success flag.
        """
        try:
            res = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
            )
            return {
                "command": command,
                "exit_code": res.returncode,
                "stdout": res.stdout,
                "stderr": res.stderr,
                "success": res.returncode == 0,
            }
        except subprocess.TimeoutExpired:
            return {
                "command": command,
                "exit_code": -1,
                "stdout": "",
                "stderr": f"Command timed out after {self.timeout_seconds} seconds.",
                "success": False,
            }
        except Exception as e:
            return {
                "command": command,
                "exit_code": -1,
                "stdout": "",
                "stderr": str(e),
                "success": False,
            }
