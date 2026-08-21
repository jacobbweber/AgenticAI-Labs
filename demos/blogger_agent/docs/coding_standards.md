# Coding Standards & Architectural Guidelines

This document outlines the coding standards, decoupled system architecture, linting configuration, and testing conventions for the Autonomous Headless Blogging Agent.

---

## 1. Decoupled System Architecture

The codebase is organized into clean, decoupled software layers to promote separation of concerns, testability, and maintainability:

```
demos/blogger_agent/
├── specs/                   # System feature specification documents (EARS format)
├── docs/                    # Architectural and developer documentation
├── core/                    # Domain logic & pipeline orchestration primitives
│   ├── orchestrator.py      # High-level pipeline lifecycle control
│   ├── multi_stage_pipeline.py # 3-stage synthesis pipeline
│   ├── context_chunker.py   # Large input payload chunking logic
│   ├── quality_guard.py     # Multi-pass review pipeline (Self, Skeptic, Rewrite)
│   ├── reflexion_engine.py  # Validation and retry loop
│   ├── session_hydrator.py  # Checkpoint persistence and resume state
│   └── cycle_detector.py    # Loop detection and oscillation prevention
├── api/                     # External service & LLM gateway interfaces
│   ├── llm_gateway.py       # Resilient Ollama HTTP client (MultiModelGatewayRouter)
│   └── schema_steering.py   # Frontmatter and structure validation (LogitSteeringGuard)
├── tools/                   # File system, process, and external integrations
│   ├── inbox_manager.py     # Inbox scanning and archiving
│   ├── style_extractor.py   # Voice/style sample extraction from target blog
│   └── sandbox_worker.py    # Process execution wrapper
├── evals/                   # Observability, tracing, and evaluation
│   └── otel_tracer.py       # OpenTelemetry structured JSONL trace recorder
├── tests/                   # Pytest unit and integration test suite
└── pyproject.toml           # Project metadata, Ruff linter config, pytest config
```

### Module Boundary Guidelines
- **`core/`**: Implements domain logic. Must NOT depend directly on specific UI layers or un-abstracted external HTTP frameworks.
- **`api/`**: Encapsulates external LLM API communications and schema steering validation.
- **`tools/`**: Contains utility classes for file system manipulation, shell execution, and style extraction.
- **`evals/`**: Observability layer. Responsible for capturing structured OpenTelemetry traces to `otel_traces.jsonl`.

---

## 2. Python Coding Standards

### Code Style & Formatting
- **Python Version**: Python 3.10+ modern syntax (e.g., `list[str]`, `dict[str, Any]`, `X | None`).
- **PEP 8 Compliance**: Strictly follow standard PEP 8 naming conventions (PascalCase for classes, snake_case for functions/variables, UPPER_CASE for constants).
- **Type Annotations**: All function signatures must include modern Python type annotations for all parameters and return values.
- **Docstrings**: All modules, classes, and public functions must include Google-style or standard Sphinx docstrings explaining purpose, arguments, and return types.
- **Explicit Error Handling**: Catch specific exceptions rather than bare `except Exception:`. Never catch blind exceptions silently unless intentionally ignoring non-critical file read errors with logging.

### Immutability & Clean State
- Functions should avoid mutating global state or input dictionaries in-place.
- Return explicit new data structures or dataclasses where appropriate.

---

## 3. Ruff Linting Configuration

The project utilizes [Ruff](https://github.com/astral-sh/ruff) as the official linter and formatter.

### Configuration (`pyproject.toml`)
The linting rules are defined in `pyproject.toml` at the project root:

```toml
[tool.ruff]
target-version = "py310"
line-length = 100
src = ["core", "api", "tools", "evals"]

exclude = [
    ".git",
    ".agents",
    "__pycache__",
    "inbox",
    "processed",
    "venv",
    ".venv",
]

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # Pyflakes
    "I",   # isort import sorting
    "B",   # flake8-bugbear
    "UP",  # pyupgrade (modern python syntax)
]
ignore = [
    "E501", # Line length handled by formatter
]

[tool.ruff.lint.isort]
known-first-party = ["core", "api", "tools", "evals", "config"]
```

### Running the Linter
To verify zero lint errors across the codebase, execute:
```bash
python -m ruff check .
```
To automatically fix safe linting violations:
```bash
python -m ruff check --fix .
```

---

## 4. Pytest Test Conventions

### Directory Layout
All test cases reside in the `tests/` directory at the project root:
```
tests/
├── test_inbox_manager.py
├── test_schema_steering.py
├── test_multi_stage_pipeline.py
├── test_llm_gateway.py
├── test_reflexion_engine.py
├── test_session_hydrator.py
├── test_context_chunker.py
└── test_quality_guard.py
```

### Naming Conventions
- **Test Modules**: `test_<feature_or_primitive>.py`
- **Test Functions**: `test_<behavior>_<scenario>()` or `test_<function>_<expected_outcome>()` (e.g., `test_generate_retries_on_http_500_and_succeeds()`, `test_read_all_inbox_contents_empty_dir()`).

### Test Coverage & Design Rules
1. **Behavioral Testing**: Tests must assert real behavior and outputs, not internal implementation details.
2. **Core Path & Negative Path Requirements**: Every primitive must have at minimum:
   - One test covering normal operational behavior (happy path).
   - One test covering failure modes / edge cases / negative paths (e.g., network timeout, corrupt file, invalid schema, threshold failure).
3. **Isolation & Mocking**:
   - Use `unittest.mock.patch` or `pytest-mock` to isolate external dependencies like Ollama HTTP endpoints or GitHub API calls.
   - Do NOT hit real external network services during unit tests.
4. **Clean Test State**:
   - Use temporary directories (`tmp_path` fixture) for file system operations.
   - Reset global configurations or mock environments before each test run.

### Running Tests
Execute unit tests from the project root:
```bash
pytest tests/
```
To run tests with detailed verbosity:
```bash
pytest tests/ -v
```
