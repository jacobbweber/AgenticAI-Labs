"""
Style Extractor Tool
Scans the ENTIRE corpus of posts in the Jekyll blog repo to extract Jacob's tone, structure, and style rules.
"""

from pathlib import Path


class StyleExtractor:
    def __init__(self, posts_dir: Path):
        self.posts_dir = posts_dir

    def get_style_system_prompt(self, max_posts_sample: int = 10) -> str:
        """
        Scans ALL .md post files in _posts/ directory and compiles Jacob's tone,
        structural preferences, and persona rules into a system prompt context.
        """
        samples_block_list: list[str] = []
        if self.posts_dir.exists():
            post_files = sorted(
                [f for f in self.posts_dir.glob("*.md") if f.is_file() and not f.name.startswith(".")],
                reverse=True,
            )

            for file in post_files[:max_posts_sample]:
                try:
                    text = file.read_text(encoding="utf-8")
                    # Clean snippet preview
                    samples_block_list.append(
                        f"--- SAMPLE POST ({file.name}) ---\n{text[:1200]}\n"
                    )
                except Exception:
                    pass

        samples_text = "\n".join(samples_block_list) if samples_block_list else "No prior samples found."

        return (
            "You are writing strictly AS JACOB (human software developer and AI engineer).\n\n"
            "CRITICAL PERSONALITY & TONE RULES:\n"
            "1. NEVER USE AI META-TEXT OR PROMPT INSTRUCTIONS. Do NOT say 'Here is a blog post...', 'Based on the notes provided...', or 'Create a blog post...'. Start directly with the blog title and intro text.\n"
            "2. Write in first-person ('I built...', 'My goal was...', 'I observed...'). Tone must be direct, authentic, pragmatic, and clear.\n"
            "3. High Content Depth: Be detailed, explanatory, and thorough. Include raw technical data, commands, code blocks, and diagrams.\n"
            "4. Follow the DIKW (Data, Information, Knowledge, Wisdom) Layout Structure:\n"
            "   - Title in Chirpy Jekyll YAML Frontmatter (`layout: post`, `title`, `date`, `tags`)\n"
            "   - Top Header: `# What I Worked On, My Thoughts & Findings`\n"
            "   - Section 1: `## Data & Technical Facts` (Raw commands, code snippets, specs, configs)\n"
            "   - Section 2: `## Information & System Connections` (Context, process flow, and Mermaid/ASCII diagrams)\n"
            "   - Section 3: `## Knowledge & Key Learnings` (Architectural patterns, key learnings, trade-offs)\n"
            "   - Section 4: `## Wisdom & My Take` (Honest takeaways, practical recommendations, future steps)\n\n"
            f"BENCHMARK EXAMPLES OF JACOB'S WRITING STYLE ACROSS ALL POSTS:\n{samples_text}\n"
        )
