"""
BloggerOrchestrator
Unified control flow orchestrating primitives into the headless blogging agent.
Supports single-post inbox aggregation and timestamped processed archiving.
"""

import re
import time
from datetime import datetime
from typing import Any

from api.llm_gateway import MultiModelGatewayRouter
from api.schema_steering import LogitSteeringGuard
from config import (
    BLOG_REPO_DIR,
    DEFAULT_MODEL,
    ENABLE_GIT_PR,
    INBOX_DIR,
    MAX_RETRY_LIMIT,
    OLLAMA_HOST,
    POSTS_DIR,
    PROCESSED_DIR,
    STATE_FILE,
    TRACES_FILE,
)
from core.cycle_detector import CycleOscillationDetector, OscillationDetectedException
from core.multi_stage_pipeline import MultiStageReasoningPipeline
from core.quality_guard import QualityGuard
from core.reflexion_engine import ReflexionEngine
from core.session_hydrator import SessionStateHydrator
from evals.otel_tracer import OTelEvalTracer
from tools.inbox_manager import InboxManager
from tools.sandbox_worker import SandboxedSubprocessWorker
from tools.style_extractor import StyleExtractor


class BloggerOrchestrator:
    def __init__(self):
        self.hydrator = SessionStateHydrator(STATE_FILE)
        self.cycle_detector = CycleOscillationDetector(max_repeated_patterns=3)
        self.reflexion_engine = ReflexionEngine(max_reflections=MAX_RETRY_LIMIT)
        self.llm_router = MultiModelGatewayRouter(OLLAMA_HOST, DEFAULT_MODEL)
        self.guard = LogitSteeringGuard()
        self.worker = SandboxedSubprocessWorker(timeout_seconds=60)
        self.inbox_manager = InboxManager(INBOX_DIR, PROCESSED_DIR)
        self.style_extractor = StyleExtractor(POSTS_DIR)
        self.tracer = OTelEvalTracer(TRACES_FILE)
        self.quality_guard = QualityGuard(self.llm_router, self.tracer)

    def run_pipeline(self) -> dict[str, Any]:
        """Runs single iteration of the headless blogger agent."""
        start_time = time.time()
        results = {"processed": [], "skipped": [], "failed": []}

        if not self.inbox_manager.has_inbox_content():
            print("--> Inbox is currently empty. No pending posts to generate.")
            self.tracer.log_step(
                step_name="inbox_scan",
                duration_seconds=time.time() - start_time,
                success=True,
                metadata={"message": "Inbox empty."},
            )
            return results

        style_prompt = self.style_extractor.get_style_system_prompt()
        folder_start = time.time()

        try:
            # 1. Read and aggregate all un-dated inbox contents into a single payload
            inbox_data = self.inbox_manager.read_all_inbox_contents()
            topic_slug = inbox_data["primary_slug"]

            # 2. Record action state and check cycle oscillation
            self.cycle_detector.record_and_check("process_inbox", topic_slug)

            # 3. Multi-Stage Generation and Reflexion Loop
            pipeline = MultiStageReasoningPipeline(self.llm_router, style_prompt)

            def generation_fn(feedback: str | None) -> str:
                input_text = inbox_data["combined_content"]
                if feedback:
                    input_text += f"\n\n--- PREVIOUS ATTEMPT VALIDATION ERROR ---\n{feedback}"
                return pipeline.execute_pipeline(input_text)

            def validation_fn(output: str) -> tuple[bool, str | None]:
                return self.guard.validate_post_structure(output)

            post_content, is_valid, attempts = (
                self.reflexion_engine.execute_with_reflection(
                    generation_fn, validation_fn
                )
            )

            post_content = self.guard.auto_repair_frontmatter(post_content)
            final_valid, final_err = self.guard.validate_post_structure(post_content)

            if not final_valid:
                raise ValueError(
                    f"Post failed validation after {attempts} attempts. Error: {final_err}"
                )

            # 3.5 Multi-Pass Quality Review Pipeline (QualityGuard)
            quality_res = self.quality_guard.run_pipeline(
                post_content, inbox_data["combined_content"]
            )
            post_content = quality_res["final_draft"]

            if quality_res["skeptic_score"] < 7:
                raise ValueError(
                    f"Post failed QualityGuard review gate. Skeptic score: {quality_res['skeptic_score']} < 7"
                )

            # 4. Determine Post Filename
            date_str = datetime.now().strftime("%Y-%m-%d")
            clean_slug = re.sub(r"^\d{4}-\d{2}-\d{2}[-_]?(\d{6})?[-_]?", "", topic_slug)
            if not clean_slug:
                clean_slug = "tech_notes"

            post_filename = f"{date_str}-{clean_slug}.md"
            target_post_path = POSTS_DIR / post_filename

            POSTS_DIR.mkdir(parents=True, exist_ok=True)

            # 5. Git & PR Gate (SDUIHITLApprovalGate)
            pr_url = None
            if ENABLE_GIT_PR:
                branch_name = f"post/{date_str}-{clean_slug}"
                print(f"--> Switch to main and checkout branch: {branch_name}")
                self.worker.execute("git checkout main -f", cwd=BLOG_REPO_DIR)
                self.worker.execute(f"git checkout -B {branch_name}", cwd=BLOG_REPO_DIR)

            target_post_path.write_text(post_content, encoding="utf-8")

            if ENABLE_GIT_PR:
                self.worker.execute(f"git add _posts/{post_filename}", cwd=BLOG_REPO_DIR)
                self.worker.execute(
                    f'git commit -m "feat(blog): add post {post_filename}"',
                    cwd=BLOG_REPO_DIR,
                )
                self.worker.execute(f"git push -u origin {branch_name}", cwd=BLOG_REPO_DIR)
                pr_res = self.worker.execute(
                    f'gh pr create --title "feat(blog): {clean_slug}" --body "Automated blog post draft generated by agent for Jacob review." --head {branch_name}',
                    cwd=BLOG_REPO_DIR,
                )

                stdout_txt = pr_res.get("stdout", "").strip()
                stderr_txt = pr_res.get("stderr", "").strip()

                match = re.search(r"https://github\.com/[^\s]+/pull/\d+", stdout_txt + " " + stderr_txt)
                if match:
                    pr_url = match.group(0)
                    print(f"==> PULL REQUEST CREATED ON GITHUB: {pr_url}")
                else:
                    if stdout_txt:
                        print(f"    PR Output: {stdout_txt}")
                    if stderr_txt:
                        print(f"    PR Details: {stderr_txt}")

                # Switch back to main branch
                self.worker.execute("git checkout main -f", cwd=BLOG_REPO_DIR)

            # 6. Archive all inbox contents into a newly created timestamped directory in processed/
            archive_path = self.inbox_manager.archive_inbox_contents(clean_slug)
            print(f"--> Archived inbox items to: processed/{archive_path.name}")
            self.hydrator.mark_processed(archive_path.name)

            folder_duration = time.time() - folder_start
            self.tracer.log_step(
                step_name="process_blog_post",
                duration_seconds=folder_duration,
                success=True,
                chunk_count=getattr(pipeline, "last_chunk_count", 1),
                metadata={
                    "archive_folder": archive_path.name,
                    "post_file": post_filename,
                    "attempts": attempts,
                    "chunk_count": getattr(pipeline, "last_chunk_count", 1),
                    "chunk_sizes": getattr(pipeline, "last_chunk_sizes", []),
                },
            )
            results["processed"].append(archive_path.name)

        except OscillationDetectedException as o_err:
            self.tracer.log_step(
                step_name="process_blog_post",
                duration_seconds=time.time() - folder_start,
                success=False,
                chunk_count=getattr(pipeline, "last_chunk_count", 1),
                error=str(o_err),
            )
            results["failed"].append({"error": str(o_err)})
        except Exception as e:
            self.tracer.log_step(
                step_name="process_blog_post",
                duration_seconds=time.time() - folder_start,
                success=False,
                chunk_count=getattr(pipeline, "last_chunk_count", 1),
                error=str(e),
            )
            results["failed"].append({"error": str(e)})

        return results

