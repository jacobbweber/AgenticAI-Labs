# Stub: lab numbering in 12_reliability

This folder has three files named lab2: cycle detection, logit steering, and agent evals. They kept the `labN` prefix they had in the old tree (`modules/08`, `labs/01`, `labs/04`). The ideas are different. The numbers are not. This page is not a lab. There is no script to run.

Read them in this order:

- `lab2_cycle_detection` — hash a tool step, halt on a repeat.
- `lab2_logit_steering` — bias or stop a token.
- `lab2_agent_evals` — fixture list, print a pass count.
- `lab3_reflexion_loop` — append a failed check and retry.

Why the numbers collide:

- Each file kept the name it had when it was moved in.
- This pass does not rename files, even when names collide.

What a later cleanup would do:

- Renumber only (for example lab2 cycle, lab3 steering, lab4 evals, lab5 reflexion).
- Not rewrite the ideas.
- Not edit the `.py` files unless a path string must change.
- Not edit `PATH.md` in this pass.

What not to add:

- Runnable steps, a new `.py` file, or a fourth lab2.
- A rename of the three lab2 files in this pass. The duplicate numbering stays until that later cleanup.
