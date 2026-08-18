"""Lab: facts.json episodic vs system content procedural. Chapter 13."""
import json
import os

PATH = os.path.join(os.path.dirname(__file__), "facts.json")


def save_fact(row):
    facts = load_facts()
    facts.append(row)
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(facts, f, indent=2)
    print(PATH)


def load_facts():
    if not os.path.exists(PATH):
        return []
    with open(PATH, encoding="utf-8") as f:
        return json.load(f)


def route_query(query, facts, procedural_content):
    q = query.lower()
    for fact in facts:
        key, value = fact["key"], fact["value"]
        spaced = key.replace("_", " ")
        if key.lower() in q or spaced.lower() in q or value.lower() in q:
            return {"store": "episodic", "row": fact}
    if "how" in q or "step" in q:
        return {"store": "procedural", "content": procedural_content}
    return {"store": "none"}


if __name__ == "__main__":
    save_fact({"key": "preferred_name", "value": "Ada"})
    procedural_content = "You add numbers. Show each step."
    messages = [{"role": "system", "content": procedural_content}]
    facts = load_facts()
    first = route_query("What is the preferred name?", facts, procedural_content)
    print("query", "What is the preferred name?", "store", first["store"], "row", first["row"])
    second = route_query("How do I add numbers?", facts, procedural_content)
    print("query", "How do I add numbers?", "store", second["store"], "content", second["content"])
    _ = messages
