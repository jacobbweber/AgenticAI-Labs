# BoM draft

**Load when:** BoM, bill of materials, quote, CCW, pricing, SKU, TCO

## When to load
After an LLD artifact is saved. Call `build_bom_draft`. Not before.

## What the SE must produce
1. Role, qty, license model, warranty note.
2. Cisco vs third-party groups.
3. Every list price tagged `[UNVERIFIED]`.
4. Park final BoM for human SKU/price check. CCW is human-side.

## Multi-vendor notes
Keep third-party lines visible. Do not convert a PAN/Fortinet refresh into Cisco SKUs unless the customer asked.

## Never invent SKUs
If you cannot cite the PID from a loaded skill or a partner feed, write `[UNVERIFIED – confirm via CCW/partner]`. Never invent a list price number.
