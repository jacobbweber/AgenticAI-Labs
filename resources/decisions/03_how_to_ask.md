# How to Frame Technical Questions and Architecture Problems

When designing or debugging an AI application, it is easy to get distracted by industry buzzwords, product names, or fictional agent job titles. Instead, focus on the concrete components, data contracts, and execution boundaries.

Whenever you want to clarify a requirement or ask a question, frame it around these practical questions:

1. **What concrete file, network port, or process is involved?**
   - Look at the physical components: your Python script, the provider endpoint, or the weight file ([Chapter 00](../../education/00_atoms/00_script_provider_weights.md) and [Script, Provider, and Weights](./00_script_server_weights.md)).
2. **What exact JSON keys are being sent in the request and received in the response?**
   - Trace the data payload directly ([Chapter 00 Lab 2](../../education/00_atoms/lab2_read_the_json.md), [Chapter 02](../../education/02_the_contract/00_messages_and_json.md), and [Chapter 03](../../education/03_the_dispatcher/00_tool_dispatch.md)).
3. **Where is code execution actually happening?**
   - Remember: the model and provider only suggest tool calls; your local Python script executes the actual Python functions ([Chapter 03](../../education/03_the_dispatcher/00_tool_dispatch.md)).
4. **Does this subtask need an isolated `messages` history?**
   - Determine whether intermediate trial-and-error tokens should be kept in a separate child wrapper rather than polluting the main conversation history ([Chapter 14](../../education/14_two_agents/03_skill_vs_two_agents.md)).
5. **Does the task need to persist across restarts or outlive the current session?**
   - Decide if you need a persistent job record in a database or file ([Chapter 18](../../education/18_the_job/00_the_job.md)).
6. **Does the agent need a written standard operating procedure?**
   - Check if the instructions belong in a structured markdown skill file ([Chapter 15 Lab 2](../../education/15_mcp_and_skills/lab2_skills.md)).

---

## Example: Shifting from Jargon to Concrete Questions

- **Instead of asking**: *"How do I build an autonomous observability agent?"*
- **Ask**: *"Does my log-monitoring process need an LLM to evaluate anomalies, or can a cron script run a regex tool and enqueue a record in `jobs.json`?"*

For a complete decision flowchart, consult [01_when_x_vs_y.md](./01_when_x_vs_y.md). To see how common buzzwords map to real code concepts, visit the [Shape Tree Guide](../notes/04_shape_tree.md).

