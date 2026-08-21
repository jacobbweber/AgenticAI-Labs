"""Lab: window plus local summary. Chapter 13."""
import json


def count_chars(messages):
    return len(json.dumps(messages))


def window_messages(messages, last_n):
    kept = []
    rest = list(messages)
    if rest and rest[0]["role"] == "system":
        kept.append(rest.pop(0))
    dropped = rest[:-last_n] if last_n else rest
    tail = rest[-last_n:] if last_n else []
    return {"kept": kept + tail, "dropped": dropped}


def summarize_dropped(dropped):
    joined = "; ".join(f"{m['role']} {m['content']}" for m in dropped)
    return {"role": "assistant", "content": f"Summary: {joined}"}


def compact_messages(messages, last_n):
    parts = window_messages(messages, last_n)
    out = list(parts["kept"])
    if parts["dropped"]:
        sys_n = 1 if out and out[0]["role"] == "system" else 0
        out[sys_n:sys_n] = [summarize_dropped(parts["dropped"])]
    return out


if __name__ == "__main__":
    messages = [{"role": "system", "content": "You add numbers."}]
    for a, b in ((1, 2), (2, 4), (3, 6), (4, 8)):
        messages.append({"role": "user", "content": f"What is {a} plus {a}?"})
        messages.append({"role": "assistant", "content": str(b)})
    print("before_count", len(messages), "before_chars", count_chars(messages))
    compact = compact_messages(messages, 4)
    print("after_count", len(compact), "after_chars", count_chars(compact))
    for item in compact:
        print(item["role"], item["content"])
