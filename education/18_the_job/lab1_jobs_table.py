"""Lab: enqueue, claim, finish jobs.json. Chapter 16."""
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
    row = {"job_id": f"job-{len(jobs) + 1}", "status": "pending", "prompt": prompt, "result": None}
    jobs.append(row)
    _dump(jobs)
    return row


def claim_job():
    jobs = _load()
    for row in jobs:
        if row["status"] == "pending":
            row["status"] = "running"
            _dump(jobs)
            return row
    return None


def finish_job(job_id, result):
    jobs = _load()
    for row in jobs:
        if row["job_id"] == job_id:
            row["status"] = "done"
            row["result"] = result
    _dump(jobs)


def mock_run_turn(prompt):
    return "ok"


def run_worker():
    row = claim_job()
    if row is None:
        return
    print(row["status"])
    finish_job(row["job_id"], mock_run_turn(row["prompt"]))
    print("done")


if __name__ == "__main__":
    if os.path.exists(PATH):
        os.remove(PATH)
    for prompt in ("Add 2 and 3", "Add 4 and 5"):
        print(enqueue_job(prompt)["status"])
    run_worker()
    run_worker()
