# Data center

**Load when:** Nexus, ACI, VXLAN, EVPN, UCS, HyperFlex, data center, leaf-spine, VPC

## When to load
Leaf-spine, ACI vs NX-OS EVPN, compute fabric, or DC interconnect.

## What the SE must produce
1. Discovery: existing fabric (ACI, NX-OS, Arista, Juniper), workloads, east-west profile.
2. HLD: underlay/overlay, border, L4-7 insertion, failure domains.
3. LLD: vPC/MCLAG, BGP AS plan, anycast GW, rollback.
4. BoM only after LLD is saved.

## Multi-vendor notes
Arista/Juniper EVPN interop is common. Call out what will not interoperate. Keep existing load balancers unless the customer asked to move them.

## Never invent SKUs
No N9K / UCS PIDs or optics SKUs from memory. Write the role (leaf, spine, border) and `[UNVERIFIED – confirm via CCW/partner]`.
