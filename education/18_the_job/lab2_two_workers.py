"""Lab: claimed_by so a row cannot be claimed twice. Chapter 16."""
import json
import os

PATH = os.path.join(os.path.dirname(__file__), "jobs.json")


def _load():
    if not os.path.exists(PATH):
        return []
    with open(PATH, encoding="utf-8") as f:
        return json.load(f)


def _dump(jobs):
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)


def enqueue_job(prompt):
    jobs = _load()
    row = {
        "job_id": f"job-{len(jobs) + 1}",
        "status": "pending",
        "prompt": prompt,
        "result": None,
        "claimed_by": None,
    }
    jobs.append(row)
    _dump(jobs)
    return row


def claim_job(worker):
    jobs = _load()
    for row in jobs:
        if row["status"] == "pending" and not row.get("claimed_by"):
            row["status"] = "running"
            row["claimed_by"] = worker
            _dump(jobs)
            return row
    return None


if __name__ == "__main__":
    if os.path.exists(PATH):
        os.remove(PATH)
    enqueue_job("Add 2 and 3")
    enqueue_job("Add 4 and 5")
    a = claim_job("worker_a")
    b = claim_job("worker_b")
    print(a["job_id"], a["claimed_by"], a["status"])
    print(b["job_id"], b["claimed_by"], b["status"])
    assert a["job_id"] != b["job_id"]
