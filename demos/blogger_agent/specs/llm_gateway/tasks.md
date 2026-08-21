# LLM Gateway Implementation Tasks

- [x] Task 1: Create `api/llm_gateway.py` with `MultiModelGatewayRouter` class.
- [ ] Task 2: Update `generate()` function with socket timeout >= 300s.
- [ ] Task 3: Implement exponential backoff retry loop with delay formula `5 * (3 ** (attempt - 1))`.
- [ ] Task 4: Add explicit terminal output for retries and backoff delays.
- [ ] Task 5: Implement `RuntimeError` raising on 5th failure attempt.
- [ ] Task 6: Add pytest unit tests in `tests/test_llm_gateway.py` verifying backoff retries, terminal output, and exception raising under mocked failure conditions.
