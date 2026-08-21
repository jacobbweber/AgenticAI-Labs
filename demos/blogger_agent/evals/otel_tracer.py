"""
OTelEvalTracer Primitive
Logs execution traces, token counts, step latencies, and outcome metrics.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class OTelEvalTracer:
    def __init__(self, trace_filepath: Path):
        self.trace_filepath = trace_filepath
        self.trace_filepath.parent.mkdir(parents=True, exist_ok=True)

    def log_step(
        self,
        step_name: str,
        duration_seconds: float,
        success: bool,
        input_tokens: int = 0,
        output_tokens: int = 0,
        metadata: dict[str, Any] | None = None,
        error: str | None = None,
        chunk_count: int | None = None,
    ) -> None:
        meta = metadata or {}
        if chunk_count is not None:
            meta["chunk_count"] = chunk_count

        effective_chunk_count = (
            chunk_count if chunk_count is not None else meta.get("chunk_count", 1)
        )

        trace_record = {
            "timestamp": datetime.now().isoformat(),
            "step_name": step_name,
            "duration_seconds": round(duration_seconds, 4),
            "success": success,
            "tokens": {
                "prompt": input_tokens,
                "completion": output_tokens,
                "total": input_tokens + output_tokens,
            },
            "chunk_count": effective_chunk_count,
            "metadata": meta,
            "error": error,
        }

        with open(self.trace_filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(trace_record) + "\n")

