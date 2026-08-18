"""Lab: named nodes plus edge_after_tests. Chapter 06."""


def draft(state: dict) -> dict:
    state["code"] = "def calculate_total(price, tax): return price + tax"
    state["test_passed"] = False
    return state


def run_tests(state: dict) -> dict:
    state["attempts"] += 1
    state["test_passed"] = state["attempts"] >= 2
    return state


def refactor(state: dict) -> dict:
    state["code"] = (
        "def calculate_total(price, tax):\n"
        "    if price < 0:\n"
        "        raise ValueError('price must be >= 0')\n"
        "    return price + tax"
    )
    return state


def edge_after_tests(state, max_retries=3):
    if not state["test_passed"] and state["attempts"] < max_retries:
        return "refactor"
    return "finish"


def run_graph(state, max_retries=3):
    nodes = {"draft": draft, "run_tests": run_tests, "refactor": refactor}
    name = "draft"
    while name != "finish" and state["attempts"] < max_retries:
        print(name)
        nodes[name](state)
        if name == "draft":
            name = "run_tests"
        elif name == "run_tests":
            name = edge_after_tests(state, max_retries)
            print("edge", name)
        else:
            name = "run_tests"
    print("attempts", state["attempts"], "test_passed", state["test_passed"])


if __name__ == "__main__":
    run_graph({"code": "", "attempts": 0, "test_passed": False})
