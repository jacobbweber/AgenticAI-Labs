"""
MultiStageReasoningPipeline Primitive
Executes a multi-stage reasoning loop:
1. DIKW Extraction (Data, Information, Knowledge, Wisdom) per chunk
2. Diagram & Code Formatting per chunk
3. Persona Synthesis - writes as Jacob, zero prompt leakage (on merged chunk outputs)
"""

import re
from datetime import datetime

from api.llm_gateway import MultiModelGatewayRouter
from api.schema_steering import LogitSteeringGuard
from core.context_chunker import ContextChunker


class MultiStageReasoningPipeline:
    def __init__(self, llm_router: MultiModelGatewayRouter, style_prompt: str):
        self.llm_router = llm_router
        self.style_prompt = style_prompt
        self.sanitizer = LogitSteeringGuard()
        self.chunker = ContextChunker()
        self.last_chunk_count = 1
        self.last_chunk_sizes: list[int] = []

    def execute_pipeline(self, raw_input_text: str) -> str:
        """
        Executes multi-stage synthesis to produce a deep, high-coverage DIKW blog post.
        Handles chunking for inputs exceeding context limits.
        """
        # Pre-clean raw input text
        cleaned_input = self.sanitizer.sanitize_prompt_leakage(raw_input_text)
        today = datetime.now().strftime("%Y-%m-%d")

        # Context Window Chunking (<= 40,000 chars per chunk)
        chunks = self.chunker.chunk_text(cleaned_input, max_chars=40000)
        self.last_chunk_count = len(chunks)
        self.last_chunk_sizes = [len(c) for c in chunks]

        stage1_outputs: list[str] = []
        stage2_outputs: list[str] = []

        for idx, chunk in enumerate(chunks, start=1):
            # ------------------------------------------------------------------ #
            # STAGE 1: DIKW Extraction per chunk
            # ------------------------------------------------------------------ #
            chunk_header = (
                f" (CHUNK {idx}/{self.last_chunk_count})" if self.last_chunk_count > 1 else ""
            )
            stage1_output = self.llm_router.generate(
                prompt=(
                    f"You are a technical analyst. Read the following lab notes, code files, and resources carefully{chunk_header}.\n"
                    "Extract and organize the content into four clearly labelled sections:\n\n"
                    "DATA: List every raw fact, command, file path, class name, config value, or code snippet present.\n"
                    "INFORMATION: Describe how the components interact, the process flow, and the context.\n"
                    "KNOWLEDGE: State the architectural principles, design patterns, and technical learnings.\n"
                    "WISDOM: List the personal recommendations, trade-offs, and key takeaways.\n\n"
                    f"--- NOTES TO ANALYZE{chunk_header} ---\n{chunk}\n--- END NOTES ---"
                ),
                system_prompt=self.style_prompt,
                temperature=0.3,
            )
            stage1_outputs.append(stage1_output)

            # ------------------------------------------------------------------ #
            # STAGE 2: Code blocks + Mermaid diagram per chunk
            # ------------------------------------------------------------------ #
            stage2_output = self.llm_router.generate(
                prompt=(
                    f"You are a technical writer and diagram specialist{chunk_header}.\n"
                    "Using the DIKW analysis below, do two things:\n"
                    "1. Wrap every code snippet in a properly fenced markdown code block with the correct language tag.\n"
                    "2. Write one Mermaid flowchart (```mermaid ... ```) that shows how the system components connect.\n"
                    "Return only the formatted code blocks and the diagram — nothing else.\n\n"
                    f"--- DIKW ANALYSIS{chunk_header} ---\n{stage1_output}\n--- END ANALYSIS ---"
                ),
                system_prompt=self.style_prompt,
                temperature=0.2,
            )
            stage2_outputs.append(stage2_output)

        # Merge chunk outputs before Stage 3 persona synthesis
        merged_stage1 = "\n\n".join(stage1_outputs)
        merged_stage2 = "\n\n".join(stage2_outputs)

        # ------------------------------------------------------------------ #
        # STAGE 3a: Generate TITLE only (short, focused call)
        # ------------------------------------------------------------------ #
        raw_title = self.llm_router.generate(
            prompt=(
                "Based on the technical material below, write a single short blog post title (5-10 words).\n"
                "The title must describe the actual technical subject matter — NOT the writing task.\n"
                "Output ONLY the title text. No quotes, no punctuation at the end, no explanation.\n\n"
                f"--- TECHNICAL MATERIAL ---\n{merged_stage1[:3000]}\n--- END MATERIAL ---"
            ),
            system_prompt=self.style_prompt,
            temperature=0.3,
        )
        # Clean the title — strip quotes, newlines, leading/trailing spaces
        title = raw_title.strip().strip('"').strip("'").split("\n")[0].strip()
        if not title or len(title) > 120:
            title = "Lab Notes and Technical Reflections"

        # ------------------------------------------------------------------ #
        # STAGE 3b: Generate BODY only — no frontmatter, sections only
        # ------------------------------------------------------------------ #
        stage3_body = self.llm_router.generate(
            prompt=(
                "You are Jacob Weber, a hands-on software engineer who writes a personal technical blog.\n"
                "Write the BODY of a detailed blog post (400-600 words) in Jacob's first-person voice.\n"
                "Jacob is direct, candid, technically precise, and reflective.\n\n"
                "RULES:\n"
                "- Write using these exact section headings in order, nothing before the first heading:\n"
                "    # What I Worked On, My Thoughts & Findings\n"
                "    ## Data & Technical Facts\n"
                "    ## Information & System Connections\n"
                "    ## Knowledge & Key Learnings\n"
                "    ## Wisdom & My Take\n"
                "- Fill every section with real technical content from the material below.\n"
                "- Do NOT include Jekyll frontmatter, YAML, or any --- delimiters.\n"
                "- Do NOT start with 'Here is', 'As requested', 'I will now', or any meta-commentary.\n"
                "- Write actual sentences in every section. No placeholder text.\n\n"
                f"--- TECHNICAL MATERIAL ---\n{merged_stage1}\n\n{merged_stage2}\n--- END MATERIAL ---"
            ),
            system_prompt=self.style_prompt,
            temperature=0.7,
        )

        # ------------------------------------------------------------------ #
        # STAGE 3c: Assemble final post deterministically (frontmatter is ours)
        # ------------------------------------------------------------------ #
        frontmatter = (
            f"---\n"
            f"layout: post\n"
            f'title: "{title}"\n'
            f"date: {today} 12:00:00 -0000\n"
            f"categories:\n"
            f"tags: [ai, learning, architecture]\n"
            f"---\n"
        )

        # Strip any accidental frontmatter the model may have emitted in body
        body = re.sub(r"^---.*?---\s*", "", stage3_body, flags=re.DOTALL).strip()

        full_post = frontmatter + "\n" + body

        # Sanitize any residual prompt leakage from final output
        return self.sanitizer.sanitize_prompt_leakage(full_post)


