"""Lab: park needs_hitl then resume done/failed. Chapter 18."""
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


def _find(job_id):
    jobs = _load()
    for row in jobs:
        if row["job_id"] == job_id:
            return jobs, row
    return jobs, None


def enqueue_job(prompt):
    jobs = _load()
    row = {
        "job_id": f"job-{len(jobs) + 1}",
        "status": "pending",
        "prompt": prompt,
        "result": None,
        "proposed_action": None,
    }
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


def park_job(job_id, proposed_action):
    jobs, row = _find(job_id)
    row["status"] = "needs_hitl"
    row["proposed_action"] = proposed_action
    _dump(jobs)


def resume_job(job_id, approved):
    jobs, row = _find(job_id)
    row["status"] = "running"
    row["status"] = "done" if approved else "failed"
    _dump(jobs)


if __name__ == "__main__":
    if os.path.exists(PATH):
        os.remove(PATH)
    first = enqueue_job("clean tmp")
    claim_job()
    park_job(first["job_id"], "rm -rf /tmp/demo")
    print(_find(first["job_id"])[1]["status"])
    resume_job(first["job_id"], True)
    print(_find(first["job_id"])[1]["status"])
    second = enqueue_job("clean tmp again")
    claim_job()
    park_job(second["job_id"], "rm -rf /tmp/demo")
    print(_find(second["job_id"])[1]["status"])
    resume_job(second["job_id"], False)
    print(_find(second["job_id"])[1]["status"])
