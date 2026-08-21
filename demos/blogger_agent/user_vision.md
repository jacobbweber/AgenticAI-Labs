# User Vision

## Summary
An autonomous, headless blogging agent system that periodically checks an inbox directory for any un-dated folders, technical notes, lab artifacts, code scripts, or links, aggregates all inbox contents into a single unified blog post, extracts Jacob's writing style across the blog archive (`D:\Projects\Active\jacobbweber-github.io\_posts`), executes a multi-stage reasoning loop using the DIKW (Data, Information, Knowledge, Wisdom) framework, eliminates AI instruction/prompt leakage, creates a GitHub Pull Request for human review, and moves all processed inbox items into a newly created timestamped folder in `processed/`.

## Problem Statement
Jacob performs intensive technical learning, lab exercises, and hands-on project work, but experiences high cognitive load and time constraints when attempting to manually re-process, summarize, format, and publish these efforts into structured, high-coverage, reflective blog posts with code examples and flowcharts.

## Goal
Establish a scheduled, headless background system that:
1. **Un-dated Inbox Intake & Single Post Aggregation**: Accepts any un-dated folders, files, or scripts in `inbox/` and synthesizes everything present into a single, cohesive technical blog post per run.
2. **Full Corpus Style Extraction**: Scans ALL blog posts in `_posts/` to extract Jacob's exact writing style, vocabulary, tone, section patterns, and formatting rules.
3. **Multi-Stage Reasoning & DIKW Loop**:
   - **Stage 1 (Analysis & DIKW Extraction)**: Extracts Data (raw facts/code), Information (context), Knowledge (architectural insights), and Wisdom (takeaways).
   - **Stage 2 (Diagrams & Code Formulation)**: Formulates clean code blocks and ASCII/Mermaid flowcharts.
   - **Stage 3 (Drafting & Zero-Leakage Polish)**: Synthesizes a deep, high-coverage post under "What I Worked On, My Thoughts & Findings", removing all meta-text and prompt instructions.
4. **Automated Drafting & Pull Request Gate**: Validates post schema via `LogitSteeringGuard`, verifies builds, pushes a Git branch, and opens a GitHub Pull Request (`SDUIHITLApprovalGate`) for Jacob's review.
5. **Timestamped Archiving & Portability**: Moves all processed inbox contents into a newly created timestamped directory in `processed/YYYY-MM-DD-HHMMSS_topic_name/`, logs telemetry (`OTelEvalTracer`), and operates cross-platform on Windows and Ubuntu CLI Linux.
