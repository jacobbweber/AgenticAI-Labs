# Quality Guard Requirements Specification

All requirements in this document follow the Easy Approach to Requirements Syntax (EARS) standard:
- **Ubiquitous**: The <system> shall <response>.
- **Event-Driven**: When <trigger>, the <system> shall <response>.
- **State-Driven**: While <state>, the <system> shall <response>.
- **Optional**: Where <feature>, the <system> shall <response>.
- **Unwanted Behavior**: If <condition>, then the <system> shall <response>.

---

## Requirements

### Requirement 1: Self-Review Technical Completeness (Event-Driven)
When Stage 3 draft generation finishes, the quality guard system shall execute Pass 1 self review to verify that all core concepts and code snippets from the source inbox payload are present in the draft.

### Requirement 2: Skeptic Human Fidelity Scoring (Event-Driven)
When Pass 1 self review completes, the quality guard system shall execute Pass 2 skeptic review using an explicit 1-10 rubric to evaluate writing authenticity and penalize AI phrasing tropes.

### Requirement 3: Targeted Section Rewriting (Unwanted Behavior)
If the Pass 2 skeptic score is less than 7, then the quality guard system shall execute Pass 3 targeted rewrite on only the flagged sentences and sections while keeping passing content intact.

### Requirement 4: OpenTelemetry Review Logging (Ubiquitous)
The quality guard system shall emit structured trace entries for `self_review_pass`, `skeptic_review_pass`, and `final_polish_pass` to the OpenTelemetry trace log to maintain complete auditability.

### Requirement 5: Threshold Authorization Gate (State-Driven)
While evaluating post drafts for publication, the quality guard system shall withhold publishing authorization until the recorded skeptic fidelity score reaches or exceeds 7.
