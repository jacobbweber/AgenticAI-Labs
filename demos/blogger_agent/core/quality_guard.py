"""
QualityGuard / MultiPassQualityPipeline Primitive
Enforces multi-pass post quality review:
Pass 1: Self Review (topic coverage against raw inbox content)
Pass 2: Human Fidelity / Skeptic Review (scores 1-10 on explicit rubric penalizing AI tropes)
Pass 3: Targeted Rewrite (rewrites flagged sections if score < 7 until score >= 7)
Integrates with OpenTelemetry tracing.
"""

import re
import time
from typing import Any

from api.llm_gateway import MultiModelGatewayRouter
from evals.otel_tracer import OTelEvalTracer

SELF_REVIEW_SYSTEM_PROMPT = """You are a technical editor conducting a self-review of a technical blog post.
Compare the generated draft against the raw source notes/payload.

Evaluate:
1. Topic Coverage: Are all primary technical concepts and topics from the source payload represented?
2. Code/Technical Accuracy: Are code snippets and technical facts present and accurate?
3. Missing Context: Are there any critical details from the source payload omitted from the draft?

Provide a concise summary of your self-review findings.
"""

SKEPTIC_REVIEW_SYSTEM_PROMPT = """You are a skeptical senior technical editor reviewing a blog post draft.
Score the draft strictly on a scale of 1 to 10 for human technical writing fidelity:
- 10: Indistinguishable from an expert human technical blogger. Sharp, natural technical voice, zero AI filler.
- 1: Obvious AI-generated content, full of generic buzzwords, transition tropes, and structural fluff.

RUBRIC & MANDATORY PENALTIES:
1. AI Transitions (-2 points per occurrence): Penalize phrases like "Furthermore", "It is worth noting", "Additionally", "Moreover", "In summary", "It is important to keep in mind".
2. Bracketed Placeholders (-3 points per occurrence): Penalize any placeholder text in brackets like [Insert code], [...], [TODO], [Your name].
3. Generic Summarizing Conclusions (-2 points): Penalize generic wrap-ups like "In conclusion", "To sum up", "In summary", or generic recap paragraphs that add no technical value.
4. Instruction Text Leakage (-5 points): Penalize prompt instructions appearing in draft (e.g., "synthesize", "here is a blog post", "based on the notes", "as an AI").
5. Repetitive Phrasing Patterns (-2 points): Penalize repetitive sentence structures, robotic list intros, or identical paragraph openings.

OUTPUT FORMAT:
Your response MUST be formatted exactly as follows:
SCORE: <integer from 1 to 10>
FINDINGS:
- <bullet point of flagged issue>
"""

TARGETED_REWRITE_SYSTEM_PROMPT = """You are an expert technical blogger and editor.
You are tasked with targeted polishing of a blog post draft to address specific editor findings.

CRITICAL DIRECTIVES:
1. Rewrite ONLY the flagged sentences and sections identified in the review findings.
2. Preserve all passing sections, technical code blocks, facts, and YAML frontmatter VERBATIM.
3. Eliminate all AI transitions (such as "Furthermore", "It is worth noting"), generic concluding phrases, bracketed placeholders, and instruction text leakage.
4. Do NOT add conversational meta-commentary (like "Here is the revised draft:"). Output ONLY the complete revised markdown blog post.
"""


class QualityGuard:
    def __init__(
        self,
        router: MultiModelGatewayRouter,
        tracer: OTelEvalTracer | None = None,
        max_rewrites: int = 3,
    ):
        self.router = router
        self.tracer = tracer
        self.max_rewrites = max_rewrites

    def self_review_pass(self, draft: str, inbox_content: str) -> dict[str, Any]:
        """
        Pass 1: Evaluates topic coverage of inbox content against draft post.
        """
        start_time = time.time()
        user_prompt = (
            f"SOURCE INBOX CONTENT:\n{inbox_content[:4000]}\n\n"
            f"GENERATED DRAFT POST:\n{draft[:4000]}\n\n"
            "Please conduct Pass 1 Self-Review."
        )

        try:
            findings = self.router.generate(
                prompt=user_prompt, system_prompt=SELF_REVIEW_SYSTEM_PROMPT
            )
        except Exception as e:
            findings = f"Self review LLM call fallback: {e}"

        duration = time.time() - start_time

        if self.tracer:
            self.tracer.log_step(
                step_name="self_review_pass",
                duration_seconds=duration,
                success=True,
                metadata={"findings": findings},
            )

        return {"findings": findings, "duration": duration}

    def _check_deterministic_penalties(self, draft: str) -> tuple[list[str], int]:
        """
        Scans draft deterministically for AI transitions, bracketed placeholders,
        and prompt leakage phrases.
        """
        flagged: list[str] = []
        penalty = 0

        # Title check for "synthesize"
        parts = draft.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            title_match = re.search(r'title:\s*"([^"]*)"', frontmatter, re.IGNORECASE)
            if title_match and "synthesize" in title_match.group(1).lower():
                flagged.append("Forbidden word 'synthesize' found in frontmatter title.")
                penalty += 4

        body = parts[2] if len(parts) >= 3 else draft

        # AI Transitions
        ai_transitions = [
            (r"\bfurthermore\b", "Furthermore"),
            (r"\bit is worth noting\b", "It is worth noting"),
            (r"\badditionally\b", "Additionally"),
            (r"\bmoreover\b", "Moreover"),
            (r"\bit is important to note\b", "It is important to note"),
            (r"\bin conclusion\b", "In conclusion"),
        ]
        for pattern, label in ai_transitions:
            matches = re.findall(pattern, body, re.IGNORECASE)
            if matches:
                flagged.append(f"AI transition trope detected ({len(matches)}x): '{label}'")
                penalty += 2 * len(matches)

        # Bracketed placeholders
        placeholder_pattern = (
            r"\[(?!\s*https?://|\s*#|\s*\/)(?![^\]]+\()(?![^\]]+\]\[)"
            r"[^\]\n]*(?:insert|placeholder|todo|tbd|code|link|your|author|text|\.\.\.)[^\]\n]*\]"
        )
        placeholder_matches = re.findall(placeholder_pattern, body, re.IGNORECASE)
        if placeholder_matches:
            flagged.append(f"Bracketed placeholder(s) detected: {placeholder_matches}")
            penalty += 3 * len(placeholder_matches)

        # Instruction text leakage
        leakage_patterns = [
            (r"here is a blog post", "here is a blog post"),
            (r"based on the notes", "based on the notes"),
            (r"create a blog post", "create a blog post"),
            (r"here is a structured synthesis", "here is a structured synthesis"),
        ]
        for pattern, label in leakage_patterns:
            if re.search(pattern, body, re.IGNORECASE):
                flagged.append(f"Instruction text leakage detected: '{label}'")
                penalty += 4

        return flagged, penalty

    def skeptic_review_pass(self, draft: str) -> dict[str, Any]:
        """
        Pass 2: Evaluates draft on 1-10 human fidelity rubric, penalizing AI tropes.
        """
        start_time = time.time()
        user_prompt = f"DRAFT POST TO REVIEW:\n{draft}\n\nPlease score this draft 1-10 based on the rubric."

        try:
            raw_response = self.router.generate(
                prompt=user_prompt, system_prompt=SKEPTIC_REVIEW_SYSTEM_PROMPT
            )
        except Exception as e:
            raw_response = f"SCORE: 5\nFINDINGS:\n- LLM call exception: {e}"

        # Parse score
        score_match = re.search(r"SCORE:\s*(\d+)", raw_response, re.IGNORECASE)
        parsed_score = int(score_match.group(1)) if score_match else 5
        parsed_score = max(1, min(10, parsed_score))

        # Check deterministic penalties
        det_findings, det_penalty = self._check_deterministic_penalties(draft)

        # If deterministic penalties found, adjust score and findings
        final_score = max(1, parsed_score - det_penalty)
        if det_findings and final_score >= 7:
            final_score = 6  # Enforce failure if deterministic tropes remain

        findings_text = raw_response
        if det_findings:
            det_summary = "\n- Deterministic Penalties:\n  " + "\n  ".join(det_findings)
            findings_text += det_summary

        duration = time.time() - start_time
        passed = final_score >= 7

        if self.tracer:
            self.tracer.log_step(
                step_name="skeptic_review_pass",
                duration_seconds=duration,
                success=passed,
                metadata={"score": final_score, "findings": findings_text},
            )

        return {
            "score": final_score,
            "findings": findings_text,
            "passed": passed,
            "duration": duration,
        }

    def final_polish_pass(self, draft: str, skeptic_findings: str) -> str:
        """
        Pass 3: Targeted rewrite of flagged sentences/sections, preserving remaining content.
        """
        user_prompt = (
            f"SKEPTIC REVIEW FINDINGS:\n{skeptic_findings}\n\n"
            f"ORIGINAL DRAFT POST:\n{draft}\n\n"
            "Please produce the updated draft with ONLY flagged sections rewritten."
        )

        try:
            polished = self.router.generate(
                prompt=user_prompt, system_prompt=TARGETED_REWRITE_SYSTEM_PROMPT
            )
        except Exception:
            polished = draft

        return polished

    def run_pipeline(self, draft: str, inbox_content: str) -> dict[str, Any]:
        """
        Executes Pass 1 (Self Review), Pass 2 (Skeptic Review), and Pass 3 (Targeted Rewrite if score < 7).
        Enforces recorded skeptic score >= 7 for final draft.
        """
        # Pass 1: Self Review
        self_res = self.self_review_pass(draft, inbox_content)

        # Pass 2: Skeptic Review
        skeptic_res = self.skeptic_review_pass(draft)
        initial_score = skeptic_res["score"]
        current_draft = draft
        current_findings = skeptic_res["findings"]
        current_score = initial_score
        rewrites_applied = 0

        # Pass 3: Targeted Rewrite loop if skeptic score < 7
        if current_score < 7:
            polish_start = time.time()
            while current_score < 7 and rewrites_applied < self.max_rewrites:
                rewrites_applied += 1
                current_draft = self.final_polish_pass(current_draft, current_findings)
                re_skeptic = self.skeptic_review_pass(current_draft)
                current_score = re_skeptic["score"]
                current_findings = re_skeptic["findings"]

            polish_duration = time.time() - polish_start
            if self.tracer:
                self.tracer.log_step(
                    step_name="final_polish_pass",
                    duration_seconds=polish_duration,
                    success=(current_score >= 7),
                    metadata={
                        "initial_score": initial_score,
                        "final_score": current_score,
                        "rewrites_applied": rewrites_applied,
                    },
                )

            if current_score < 7:
                raise ValueError(
                    f"QualityGuard failed to achieve skeptic score >= 7 after {self.max_rewrites} rewrite attempts. Final score: {current_score}"
                )
        else:
            if self.tracer:
                self.tracer.log_step(
                    step_name="final_polish_pass",
                    duration_seconds=0.0,
                    success=True,
                    metadata={
                        "initial_score": initial_score,
                        "final_score": current_score,
                        "rewrites_applied": 0,
                    },
                )

        return {
            "final_draft": current_draft,
            "self_review": self_res,
            "skeptic_score": current_score,
            "skeptic_findings": current_findings,
            "rewrites_applied": rewrites_applied,
            "passed": True,
        }


def run_quality_pipeline(
    draft: str,
    inbox_content: str,
    router: MultiModelGatewayRouter,
    tracer: OTelEvalTracer | None = None,
) -> dict[str, Any]:
    """Helper function wrapping QualityGuard.run_pipeline."""
    guard = QualityGuard(router, tracer)
    return guard.run_pipeline(draft, inbox_content)
