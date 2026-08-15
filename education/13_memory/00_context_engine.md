# 13: Context engine

After this page the message list can shrink: window, summary, or prune.

## Data
- Working memory: the POST payload
- Compaction: drop old turns, summarize, or trim tool stdout
- Moved from modules/12

## Information
Chapter 05 saves the list. This chapter makes it smaller.

## Knowledge
1. Count tokens or chars.
2. Keep system + last N.
3. Optionally summarize the middle.

## Wisdom
Do not add a vector DB on this page.

## The When and Why
- **When:** the list no longer fits.
- **Why:** TTFT and cost grow with the raw history.

## How it works

```mermaid
flowchart LR
    L["long list"] --> C["compact"]
    C --> P["POST"]
```

## Data contract
Keep: system + last N messages.

## Lab
No dedicated compaction script in the old labs; use notes here.

## Related
- **Chapter 05:** the store.

## Notes
Moved from modules/12.
