# 11: Resilient gateway

After this page a failed POST retries with backoff. A second host is optional.

## Data
- Lab: `lab3_resilient_gateway` (from old foundations lab 3)
- Errors: 429, 5xx, connection
- Circuit breaker: stop calling a dead host

## Information
Chapter 01 had one POST. This chapter wraps it.

## Knowledge
1. Try the call.
2. On 429/5xx, sleep and retry.
3. After N fails, raise or switch host.

## Wisdom
Do not add multi-region load balancing.

## The When and Why
- **When:** the LAN host blips.
- **Why:** one try is not production.

## How it works

```mermaid
flowchart LR
    A["POST"] -->|fail| B["backoff"]
    B --> A
```

## Data contract
Retry budget: int. Jitter: random delay.

## Lab
- [lab3_resilient_gateway.py](./lab3_resilient_gateway.py) / [lab3_resilient_gateway.md](./lab3_resilient_gateway.md)

## Related
- **Chapter 01 wrapper:** the inner call.

## Notes
Moved from labs/00_foundations/lab3.
