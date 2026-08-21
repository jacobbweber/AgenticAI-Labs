"""
MultiModelGatewayRouter Primitive
Handles routing generation prompts to local Ollama host or fallback providers.
Raises a hard RuntimeError if Ollama is unreachable rather than silently returning a fake post.
"""

import json
import re
import time
import urllib.error
import urllib.request

try:
    from config import LLM_TIMEOUT, MAX_LLM_RETRIES
except ImportError:
    LLM_TIMEOUT = 300
    MAX_LLM_RETRIES = 5


class MultiModelGatewayRouter:
    def __init__(
        self,
        ollama_host: str,
        default_model: str,
        timeout: int = LLM_TIMEOUT,
        max_attempts: int = MAX_LLM_RETRIES,
    ):
        if "0.0.0.0" in ollama_host:
            ollama_host = ollama_host.replace("0.0.0.0", "192.168.1.29")
        if not ollama_host.startswith("http://") and not ollama_host.startswith("https://"):
            ollama_host = f"http://{ollama_host}"
        if ":11434" not in ollama_host and ":" not in ollama_host.split("//")[-1]:
            ollama_host = f"{ollama_host}:11434"
        self.ollama_host = ollama_host.rstrip("/")
        self.default_model = default_model
        self.timeout = timeout
        self.max_attempts = max_attempts

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        model: str | None = None,
        temperature: float = 0.7,
        timeout: int | None = None,
        max_attempts: int | None = None,
    ) -> str:
        selected_model = model or self.default_model
        req_timeout = timeout if timeout is not None else self.timeout
        attempts_limit = max_attempts if max_attempts is not None else self.max_attempts
        endpoint = f"{self.ollama_host}/api/generate"

        payload = {
            "model": selected_model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature},
        }
        if system_prompt:
            payload["system"] = system_prompt

        json_data = json.dumps(payload).encode("utf-8")
        last_error = ""

        for attempt in range(1, attempts_limit + 1):
            try:
                req = urllib.request.Request(
                    endpoint,
                    data=json_data,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=req_timeout) as response:
                    if response.status == 200:
                        resp_body = json.loads(response.read().decode("utf-8", errors="replace"))
                        result = resp_body.get("response", "").strip()
                        # Strip Qwen3 / thinking-model <think>...</think> blocks
                        result = re.sub(r"<think>.*?</think>", "", result, flags=re.DOTALL).strip()
                        if not result:
                            raise RuntimeError(
                                f"Ollama returned an empty response on attempt {attempt}."
                            )
                        return result
                    else:
                        raise RuntimeError(f"Ollama API returned status code {response.status}")
            except Exception as e:
                last_error = str(e)
                wait_time = 5 * (3 ** (attempt - 1))
                if attempt < attempts_limit:
                    print(
                        f"    [LLM Gateway] Retry attempt {attempt}/{attempts_limit} failed: {last_error}. "
                        f"Sleeping for {wait_time}s before retrying..."
                    )
                    time.sleep(wait_time)
                else:
                    print(
                        f"    [LLM Gateway] Retry attempt {attempt}/{attempts_limit} failed: {last_error}. "
                        "All retry attempts exhausted."
                    )

        # Hard fail — never silently return a fake/mock post
        raise RuntimeError(
            f"Ollama LLM gateway failed after {attempts_limit} attempts. "
            f"Last error: {last_error}. "
            f"Check that Ollama is running at {self.ollama_host} with model '{selected_model}'."
        )

