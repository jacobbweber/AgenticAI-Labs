# Security

**Load when:** firewall, ISE, Zero Trust, segmentation, SASE, Umbrella, Talos, ACS, 802.1X, VPN

## When to load
Secure edge, campus 802.1X, ISE, Secure Firewall, SASE/Umbrella, or zero-trust overlay on an existing stack.

## What the SE must produce
1. Trust boundaries and identity source (AD, Entra, ISE).
2. Policy sketch: who/what/where, not a full ACL dump on turn one.
3. HLD that names enforcement points (existing PAN/Fortinet/Cisco).
4. HITL before any "customer-ready" security language or live ACL change.

## Multi-vendor notes
Do not default to replacing Palo Alto or Fortinet. Document coexistence (IPsec, IKE, user-id, syslog). If the customer keeps PAN, design the Cisco pieces around it.

## Never invent SKUs
No ASA/FTD/ISE part numbers, subscription PIDs, or list prices. Mark `[UNVERIFIED]`. No config that disables auth, logging, or modern crypto without a written waiver.
