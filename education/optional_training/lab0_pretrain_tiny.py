"""Lab: CPU next-token table writes weights.json. Optional training."""
import json
import math
import os

PATH = os.path.join(os.path.dirname(__file__), "weights.json")


def build_vocab(texts):
    chars = sorted({ch for text in texts for ch in text})
    stoi = {ch: i for i, ch in enumerate(chars)}
    itos = {i: ch for ch, i in stoi.items()}
    return stoi, itos


def make_pairs(texts, stoi):
    pairs = []
    for s in texts:
        for i in range(len(s) - 1):
            pairs.append((stoi[s[i]], stoi[s[i + 1]]))
    return pairs


def softmax(logits):
    exps = [math.exp(x) for x in logits]
    total = sum(exps)
    return [e / total for e in exps]


def train_step(W, pairs, lr):
    total = 0.0
    for i, j in pairs:
        probs = softmax(W[i])
        total += -math.log(max(probs[j], 1e-12))
        for k in range(len(W[i])):
            W[i][k] -= lr * (probs[k] - (1.0 if k == j else 0.0))
    return total / len(pairs)


def train(texts, steps, lr):
    stoi, _itos = build_vocab(texts)
    pairs = make_pairs(texts, stoi)
    v = len(stoi)
    W = [[0.0] * v for _ in range(v)]
    first_loss = last_loss = None
    for n in range(steps):
        last_loss = train_step(W, pairs, lr)
        if n == 0:
            first_loss = last_loss
    return {"first_loss": first_loss, "last_loss": last_loss, "W": W, "stoi": stoi}


if __name__ == "__main__":
    out = train(["aba", "abc", "cab"], 40, 0.5)
    print("first_loss", out["first_loss"])
    print("last_loss", out["last_loss"])
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump({"stoi": out["stoi"], "W": out["W"]}, f, indent=2)
    print(PATH)
    if not (out["last_loss"] < out["first_loss"]):
        raise SystemExit("loss did not drop")
