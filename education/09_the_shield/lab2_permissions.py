"""Lab: TOOL_HIGH_RISK plus lookup_permission. Chapter 09."""

TOOL_HIGH_RISK = {
    "read_file": False,
    "write_file": True,
    "run_command": True,
    "apply_db_migration": True,
}


def lookup_permission(tool_name):
    high_risk = TOOL_HIGH_RISK.get(tool_name, True)
    if not high_risk:
        return {"allowed": True}
    return {"needs_hitl": True, "tool": tool_name}


if __name__ == "__main__":
    for name in ("read_file", "write_file", "run_command", "apply_db_migration"):
        print(name, lookup_permission(name))
