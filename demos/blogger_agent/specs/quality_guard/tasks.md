# Quality Guard Implementation Tasks

- [ ] Task 1: Create `core/quality_guard.py` module and `QualityGuard` class.
- [ ] Task 2: Implement Pass 1 self-review verification against inbox content.
- [ ] Task 3: Implement Pass 2 skeptic rubric evaluator with 1-10 numerical scoring and penalty rules.
- [ ] Task 4: Implement Pass 3 targeted rewrite mechanism replacing only flagged paragraphs.
- [ ] Task 5: Add OpenTelemetry logging instrumentation for `self_review_pass`, `skeptic_review_pass`, and `final_polish_pass`.
- [ ] Task 6: Add pytest unit tests in `tests/test_quality_guard.py` verifying review passes, scoring penalties, targeted rewrites, and trace logging.
