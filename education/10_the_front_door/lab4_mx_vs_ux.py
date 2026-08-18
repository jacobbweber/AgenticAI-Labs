"""Lab: tag ux/mx frames and split a think fence. Chapter 10."""
import json

UX_TYPES = {"token", "token_delta"}


def tag_frame(frame):
    kind = frame.get("type") or frame.get("event_type")
    if kind in UX_TYPES:
        return {"channel": "ux"}
    return {"channel": "mx"}


def split_think_fence(text):
    start, end = text.find("<think>"), text.find("</think>")
    if start == -1 or end == -1:
        return {"ux": text, "mx": ""}
    mx = text[start + 7 : end]
    ux = text[:start] + text[end + 8 :]
    return {"ux": ux, "mx": mx}


def split_streams(frames):
    out = {"ux": [], "mx": []}
    for frame in frames:
        if tag_frame(frame)["channel"] == "ux":
            out["ux"].append(frame.get("text") or frame["data"]["delta"])
        else:
            out["mx"].append(json.dumps(frame))
    return out


if __name__ == "__main__":
    frames = [
        {"type": "token", "text": "Hello "},
        {"event_type": "token_delta", "data": {"delta": "world"}},
        {"type": "tool", "tool_name": "read_file", "args": {"path": "config.json"}},
        {"event_type": "tool_call_start", "data": {"tool_name": "read_file", "args": {"path": "config.json"}}},
        {"event_type": "session_started", "data": {"status": "ACTIVE"}},
    ]
    streams = split_streams(frames)
    fence = split_think_fence("<think>plan the answer</think>The env is prod.")
    streams["ux"].append(fence["ux"])
    if fence["mx"]:
        streams["mx"].append(fence["mx"])
    for item in streams["ux"]:
        print("UX:", item)
    for item in streams["mx"]:
        print("MX:", item)
    joined = "".join(streams["ux"])
    print("ux_joined", joined)
    for bad in ("config.json", "plan the answer", "<think>"):
        if bad in joined:
            raise SystemExit(f"ux leaked {bad}")
