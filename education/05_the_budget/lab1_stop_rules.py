"""Lab: check_budget stop reasons. Chapter 17."""


def check_budget(budget, spent):
    if spent["turns"] >= budget["max_turns"]:
        return {"stop": True, "reason": "max_turns"}
    if spent["tokens"] >= budget["max_tokens"]:
        return {"stop": True, "reason": "max_tokens"}
    return {"ok": True}


def run_fixture(name, budget):
    spent = {"turns": 0, "tokens": 0}
    print(name, budget)
    for _ in range(5):
        spent["turns"] += 1
        spent["tokens"] += 40
        result = check_budget(budget, spent)
        if result.get("stop"):
            print("stop", result["reason"])
            return result["reason"]
        print("ok")
    return None


if __name__ == "__main__":
    r1 = run_fixture("fixture1", {"max_turns": 3, "max_tokens": 100})
    r2 = run_fixture("fixture2", {"max_turns": 10, "max_tokens": 50})
    print("reasons", r1, r2)
