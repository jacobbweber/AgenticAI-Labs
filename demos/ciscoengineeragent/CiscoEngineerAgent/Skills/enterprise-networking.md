# Enterprise networking

**Load when:** campus, LAN, SD-Access, Catalyst, switching, routing, DNA Center, SDA, WAN, SD-WAN

## When to load
Campus, branch, or WAN design. SD-Access vs brownfield. Catalyst / ISR / ASR / Meraki decisions.

## What the SE must produce
1. Discovery note: sites, users, existing edge, VLANs/VRFs, SLA, `[OPEN]` gaps.
2. HLD: logical hops, segmentation, HA, out of scope.
3. LLD only after gaps are mostly closed: device roles, routing, QoS, rollback.
4. Do not jump to BoM before an LLD artifact exists.

## Multi-vendor notes
Inventory Palo Alto, Fortinet, Juniper, Arista, HPE before proposing rip-and-replace. Call BGP, VXLAN, and NetFlow integration points. If keeping a non-Cisco edge is simpler, say so and list the Cisco option as optional.

## Never invent SKUs
Platform families (Catalyst 9000, ISR 1100) are fine. Exact part numbers and list prices are `[UNVERIFIED – confirm via CCW/partner]`.
