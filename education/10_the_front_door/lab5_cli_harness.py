"""Lab: mock_run_turn plus y/n HITL from a fixture list. Chapter 10."""


def mock_run_turn(session_id, user_prompt):
    if "write" in user_prompt.lower():
        return {
            "session_id": session_id,
            "turn_count": 1,
            "thinking": "will write config",
            "response": "Apply write to config.json?",
            "high_risk": True,
            "tool": "write_file",
        }
    return {
        "session_id": session_id,
        "turn_count": 1,
        "thinking": "add the numbers",
        "response": "4",
        "high_risk": False,
    }


def apply_hitl(turn, answer):
    if not turn.get("high_risk"):
        return {"applied": False, "reason": "not_high_risk"}
    if answer.strip().lower() == "y":
        return {"applied": True, "tool": turn["tool"]}
    return {"applied": False, "tool": turn["tool"]}


def run_cli(lines, run_turn):
    session_id, i = "cli-1", 0
    while i < len(lines):
        line = lines[i]
        i += 1
        print("USER:", line)
        turn = run_turn(session_id, line)
        print("ASSISTANT:", turn["response"])
        if turn.get("high_risk"):
            answer = lines[i]
            i += 1
            print("HITL: Apply write to config.json? [y/n]")
            print("USER:", answer)
            hitl = apply_hitl(turn, answer)
            print(("APPLY:" if hitl["applied"] else "SKIP:"), hitl["tool"])


if __name__ == "__main__":
    run_cli(["What is 2+2?", "Write config.json", "n"], mock_run_turn)
    run_cli(["Write config.json", "y"], mock_run_turn)
