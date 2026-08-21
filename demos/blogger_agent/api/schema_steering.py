"""
LogitSteeringGuard Primitive
Enforces output structure, Chirpy Jekyll YAML frontmatter, DIKW headings, and purges AI prompt leakage.
Auto-repairs minor frontmatter omissions (like missing tags line).
"""

import re


class LogitSteeringGuard:
    def auto_repair_frontmatter(self, content: str) -> str:
        """Auto-repairs missing YAML keys like 'tags:' or 'layout:' in frontmatter."""
        if not content.startswith("---") or content.count("---") < 2:
            return content

        parts = content.split("---", 2)
        frontmatter = parts[1]
        body = parts[2]

        lines = frontmatter.strip().split("\n")
        fm_dict = {}
        for line in lines:
            if ":" in line:
                k, v = line.split(":", 1)
                fm_dict[k.strip().lower()] = v.strip()

        # Repair layout
        if "layout" not in fm_dict:
            lines.insert(0, "layout: post")

        # Repair tags if missing or pluralized as tag
        if "tags" not in fm_dict and "tag" not in fm_dict:
            lines.append("tags: [ai, learning, architecture]")
        elif "tag" in fm_dict and "tags" not in fm_dict:
            # Replace tag: with tags:
            lines = [line.replace("tag:", "tags:") for line in lines]

        # Repair categories
        if "categories" not in fm_dict:
            lines.append("categories:")

        new_fm = "\n".join(lines)
        return f"---\n{new_fm}\n---{body}"

    def validate_post_structure(self, content: str) -> tuple[bool, str | None]:
        """
        Validates post text for required Chirpy Jekyll frontmatter, DIKW headings,
        minimum word count, and zero AI meta-text/prompt leakage.
        Returns (is_valid, error_message).
        """
        if not content or not content.strip():
            return False, "Content is completely empty."

        # Auto-repair frontmatter before validation
        content = self.auto_repair_frontmatter(content)

        # Check frontmatter bounds
        if not content.startswith("---"):
            return False, "Post must start with '---' frontmatter declaration."

        parts = content.split("---", 2)
        if len(parts) < 3:
            return False, "Post frontmatter is unclosed. Missing closing '---'."

        frontmatter = parts[1]
        body = parts[2]

        # Check required YAML frontmatter keys
        required_keys = ["layout: post", "title:", "date:"]
        for key in required_keys:
            if key not in frontmatter:
                return False, f"Frontmatter missing required YAML key: '{key}'"

        if "tags:" not in frontmatter and "tags " not in frontmatter:
            return False, "Frontmatter missing required YAML key: 'tags:'"

        # Check that the title does not contain prompt instruction text
        title_match = re.search(r'title:\s*"([^"]*)"', frontmatter)
        if title_match:
            title_val = title_match.group(1).lower()
            title_instruction_phrases = [
                "synthesize", "write a blog", "clean descriptive", "write strictly",
                "as jacob", "high-coverage", "long-form blog", "aim for",
            ]
            for phrase in title_instruction_phrases:
                if phrase in title_val:
                    return False, f"Post title contains prompt instruction text: '{title_match.group(1)}'"

        # Check for AI Meta-Text Leakage in body
        leakage_patterns = [
            r"create a blog post",
            r"here is a blog post",
            r"based on the notes",
            r"based on the following notes",
            r"here is a structured synthesis",
            r"generated via resilient fallback",
            r"as an ai assistant",
            r"do not include any meta.?text",
            r"required structure",
            r"opening context in jacob",
            r"\[include raw",
            r"\[deep technical",
            r"\[personal evaluation",
            r"\[insert",
            r"\[placeholder",
            r"\[your ",
            r"\[todo\]",
            r"\[tbd\]",
        ]
        for pattern in leakage_patterns:
            if re.search(pattern, body, re.IGNORECASE):
                return False, f"AI Meta-Text Prompt Leakage detected matching pattern: '{pattern}'"

        # Check for DIKW Headings (Flexible Regex across header levels)
        dikw_patterns = [
            (r"#+\s*what i worked on", "# What I Worked On"),
            (r"#+\s*(data|technical|code)", "## Data & Technical Facts"),
            (r"#+\s*(information|system|workflow|connection|context)", "## Information & System Connections"),
            (r"#+\s*(knowledge|learning|insight|takeaway)", "## Knowledge & Key Learnings"),
            (r"#+\s*(wisdom|my take|conclusion|summary)", "## Wisdom & My Take"),
        ]

        found_count = 0
        missing = []
        for pattern, label in dikw_patterns:
            if re.search(pattern, body, re.IGNORECASE):
                found_count += 1
            else:
                missing.append(label)

        if found_count < 2:
            return False, f"Post body missing required DIKW section headers. Found {found_count}/5. Missing: {', '.join(missing)}"

        # Check Coverage Depth (Word Count)
        word_count = len(body.split())
        if word_count < 50:
            return False, f"Post content coverage too low ({word_count} words). Must be at least 50 words."

        return True, None

    def sanitize_prompt_leakage(self, text: str) -> str:
        """Strips leftover meta-text or prompt lines and phrases from body text."""
        leakage_patterns = [
            r"create a blog post[^\n.]*",
            r"based on the following notes[^\n.]*",
            r"here is a structured synthesis[^\n.]*",
            r"generated via resilient fallback[^\n.]*",
            r"as an ai assistant[^\n.]*",
        ]

        cleaned = text
        for pattern in leakage_patterns:
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

        # Remove consecutive blank lines
        lines = cleaned.split("\n")
        res_lines = []
        for line in lines:
            if not line.strip() and res_lines and not res_lines[-1].strip():
                continue
            res_lines.append(line)

        return "\n".join(res_lines)
