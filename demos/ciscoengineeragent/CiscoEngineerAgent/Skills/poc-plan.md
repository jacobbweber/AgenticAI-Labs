# PoC plan

**Load when:** PoC, proof of concept, pilot, lab, test plan, success criteria

## When to load
HLD is approved or the customer asked for a trial. Before any live lab window.

## What the SE must produce
1. Objective, environment, duration, data-capture list, sign-off block.
2. Test matrix: ID / scenario / pass-fail / tool.
3. Rollback. Success criteria that a skeptical architect would accept.
4. Park for approval before a live lab or production change. Human executes the change.

## Multi-vendor notes
Include incumbent gear in the test matrix (PAN failover, existing DHCP, ISE vs existing NAC). Do not test only the happy Cisco path.

## Never invent SKUs
Lab BOM lines are `[UNVERIFIED]`. No dCloud reservation IDs unless a human supplied them.
