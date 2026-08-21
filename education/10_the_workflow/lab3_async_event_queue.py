"""Reference solution: asyncio.Queue + 202 + event frames. Chapter 06."""
import asyncio
import json
import os
import sys
import time
import urllib.request
from pathlib import Path
from typing import Dict, Any

_ROOT = next(
    p for p in [Path(__file__).resolve().parent, *Path(__file__).resolve().parent.parents]
    if (p / "load_env.py").is_file()
)
sys.path.insert(0, str(_ROOT))
from load_env import load_env

load_env()
OLLAMA_URL = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/") + "/api/generate"
MODEL_NAME = os.environ.get("OLLAMA_MODEL", "llama3.2:1b")

task_queue = asyncio.Queue()
event_bus = asyncio.Queue()

async def emit_event(event_type: str, job_id: str, data: Dict[str, Any]):
    event_frame = {
        "event_type": event_type,
        "job_id": job_id,
        "timestamp": time.time(),
        "data": data
    }
    await event_bus.put(event_frame)

async def async_agent_worker(worker_id: int):
    print(f"[WORKER-{worker_id}] Started & listening on task queue...")
    while True:
        job = await task_queue.get()
        job_id = job["job_id"]
        prompt = job["prompt"]
        await emit_event("job.started", job_id, {"worker_id": worker_id, "prompt": prompt})
        loop = asyncio.get_running_loop()
        payload = {
            "model": MODEL_NAME,
            "prompt": f"Analyze in 1 sentence how async queues prevent timeouts: {prompt}",
            "stream": False,
            "options": {"temperature": 0.0}
        }
        json_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            OLLAMA_URL, data=json_bytes, headers={"Content-Type": "application/json"}
        )
        await emit_event("agent.thought", job_id, {"status": "Inference running on GPU..."})
        try:
            response_bytes = await loop.run_in_executor(
                None, lambda: urllib.request.urlopen(req, timeout=30).read()
            )
            result = json.loads(response_bytes.decode("utf-8"))
            answer = result.get("response", "").strip()
            await emit_event("agent.completed", job_id, {"result": answer, "status": "SUCCESS"})
        except Exception as err:
            await emit_event("agent.failed", job_id, {"error": str(err), "status": "FAILED"})
        task_queue.task_done()

async def event_stream_subscriber():
    while True:
        event = await event_bus.get()
        print(f"  [STREAM EVENT] [{event['event_type']}] Job: {event['job_id']} | Data: {event['data']}")
        event_bus.task_done()

async def api_submit_task(prompt: str) -> Dict[str, Any]:
    job_id = f"job_{int(time.time() * 1000)}"
    await task_queue.put({"job_id": job_id, "prompt": prompt})
    return {
        "status_code": 202,
        "message": "Accepted",
        "job_id": job_id,
        "status_url": f"/api/jobs/{job_id}"
    }

async def main():
    print("=== STARTING ASYNC EVENT-DRIVEN AGENT ENGINE ===")
    worker_task = asyncio.create_task(async_agent_worker(worker_id=1))
    subscriber_task = asyncio.create_task(event_stream_subscriber())
    print("\n[CLIENT] Submitting long-running task via POST /api/agent/task...")
    start_time = time.time()
    response = await api_submit_task("Explain async event queues.")
    print(f"[CLIENT] Received HTTP {response['status_code']} response in {time.time() - start_time:.4f}s!")
    print(f"[CLIENT] Job Handle: {response['job_id']} (Web thread is unblocked!)\n")
    await task_queue.join()
    await asyncio.sleep(0.5)
    worker_task.cancel()
    subscriber_task.cancel()
    print("\n=== ASYNC EVENT PIPELINE COMPLETE ===")

if __name__ == "__main__":
    asyncio.run(main())
