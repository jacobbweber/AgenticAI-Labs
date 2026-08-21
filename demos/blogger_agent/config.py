"""
Global Configuration for Autonomous Blogger Agent
"""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).parent.resolve()
INBOX_DIR = BASE_DIR / "inbox"
PROCESSED_DIR = BASE_DIR / "processed"
STATE_FILE = BASE_DIR / "session_state.json"
TRACES_FILE = BASE_DIR / "otel_traces.jsonl"

# Blog Target Site Configuration
BLOG_REPO_DIR = Path(r"/home/nimoadmin/WorkShop/projects/active/jacobbweber-github.io")
POSTS_DIR = BLOG_REPO_DIR / "_posts"

# Infrastructure & LLM Defaults
raw_ollama_host = os.getenv("OLLAMA_HOST", "http://192.168.1.29:11434")
if "0.0.0.0" in raw_ollama_host:
    raw_ollama_host = raw_ollama_host.replace("0.0.0.0", "192.168.1.29")
if ":11434" not in raw_ollama_host and ":" not in raw_ollama_host.split("//")[-1]:
    raw_ollama_host = f"{raw_ollama_host}:11434"
if not raw_ollama_host.startswith("http://") and not raw_ollama_host.startswith("https://"):
    raw_ollama_host = f"http://{raw_ollama_host}"
OLLAMA_HOST = raw_ollama_host
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "qwen3.6:35b-a3b-65k")

# Agent Operating Parameters
MAX_RETRY_LIMIT = 3
DEFAULT_TIMEZONE = "America/New_York"
ENABLE_GIT_PR = True  # Enabled Git PR workflow
LLM_TIMEOUT = 300  # Minimum 300 seconds timeout for Ollama HTTP requests
MAX_LLM_RETRIES = 5  # Maximum retry attempts per generation call

