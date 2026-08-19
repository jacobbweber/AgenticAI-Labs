"""Load KEY=value pairs from the repo-root .env into os.environ.

Walks from this file (or from start) up until it finds .env.
Does not override vars already set in the shell.
Skips blank lines and # comments. No pip package.
"""

from __future__ import annotations

import os
from pathlib import Path


def load_env(start: Path | None = None) -> Path | None:
    if start is None:
        here = Path(__file__).resolve().parent
    else:
        here = Path(start).resolve()
        if here.is_file():
            here = here.parent
    for folder in [here, *here.parents]:
        path = folder / ".env"
        if path.is_file():
            _apply(path)
            return path
    return None


def _apply(path: Path) -> None:
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        if key and key not in os.environ:
            os.environ[key] = value
