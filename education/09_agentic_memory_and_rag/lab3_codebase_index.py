"""Lab: walk this folder and hit run_airgapped_private_rag. Chapter 13."""
import os


def iter_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for name in filenames:
            if name.endswith((".py", ".md")):
                yield os.path.join(dirpath, name)


def index_file(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    symbols = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("def ") or s.startswith("class "):
            rest = s.split(None, 1)[1]
            symbols.append(rest.split("(")[0].split(":")[0])
    return {"path": path, "text": text, "symbols": symbols}


def search_index(index, query):
    hits = []
    for record in index:
        for n, line in enumerate(record["text"].splitlines(), 1):
            if query in line:
                hits.append({"path": record["path"], "span": f"{n}:{n}"})
    return hits


if __name__ == "__main__":
    root = os.path.dirname(__file__)
    index = [index_file(p) for p in iter_files(root)]
    hits = search_index(index, "run_airgapped_private_rag")
    for hit in hits:
        print("HIT path=" + hit["path"] + " span=" + hit["span"])
    print("hit_count", len(hits))
    if not any(h["path"].endswith("lab2_local_private_rag.py") for h in hits):
        raise SystemExit("missing lab3 hit")
