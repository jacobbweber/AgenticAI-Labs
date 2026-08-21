# Architectural Decisions and Guidelines (When X vs Y)

These decision guides explain the *When* and the *Why* behind the patterns you build across the labs. They help you choose the right design—such as when to use a simple tool function versus when to launch a background job or a multi-agent handoff. 

Before introducing additional complexity or running multiple processes, walk through [01_when_x_vs_y.md](./01_when_x_vs_y.md) to choose the simplest pattern that fits your needs. 

> **Note**: If any decision guide ever conflicts with a specific lab brief, the lab brief is always the source of truth for that lab.

## Guide Index

- [00_script_server_weights.md](./00_script_server_weights.md): The three distinct parts of the system and how `tool_calls` flow between them.
- [01_when_x_vs_y.md](./01_when_x_vs_y.md): A step-by-step decision framework to choose between tools, wrappers, loops, and background jobs.
- [02_path_canvas.md](./02_path_canvas.md): A visual map of the entire course architecture, including a real-world walkthrough.
- [03_how_to_ask.md](./03_how_to_ask.md): Clear, concrete questions to ask when designing or troubleshooting a system.
- [04_bands_and_features.md](./04_bands_and_features.md): How course chapters are grouped into tiers, and how real-world features map directly to specific labs.

To explore how common industry buzzwords translate into concrete code objects, see the [Shape Tree Guide](../notes/04_shape_tree.md).

