# 03: Self-Evolution & Long-Horizon Execution

## 1. Macro Concept & Industry Need

Autonomous software engineering and operational tasks frequently require continuous execution across hours, days, or weeks. Over long horizons, agents encounter severe failure modes: context window overflow, process crashes, unhandled rate limits, memory bloat, and repeated attempts at known failing strategies. 

To achieve continuous, reliable self-evolution and long-horizon execution, autonomous platforms implement four core engineering subsystems:
- **Persistent Heartbeat & State Engines**: Relational database-backed state machines (PostgreSQL/SQLite) tracking task checkpoints, heartbeat pings, lock renewals, and process crash recovery.
- **Skill Synthesis from Execution Traces**: Automated trajectory analysis engines that mine high-reward tool sequences from past executions and parameterize them into reusable Markdown skill modules (`.agents/skills/`).
- **Context Compaction & Memory Decay**: Algorithms that prune, compress, and evict obsolete conversation tokens while maintaining critical system instructions and active task state.
- **Failure Root-Cause Indexing**: Classifying execution failures into structured taxonomy databases to inject failure-avoidance rules into system prompts before task retries.

## 2. Architectural Component Mapping

| AI Jargon / Buzzword | Actual Software Component / Standard Primitive |
| :--- | :--- |
| **Long-Horizon Execution** | Durable DB-backed state machine with background queues, heartbeats, and checkpoint recovery. |
| **Skill Synthesis** | Trajectory analyzer mining successful spans and writing modular Markdown skills (`.agents/skills/`). |
| **Playbook Compaction** | Context decay engine applying token pruning, vector deduplication, and KV cache eviction. |
| **Failure Root-Cause Indexer** | Taxonomy database mapping errors (Context Overflow, Schema Error, Loop, Rate Limit) into retry prompts. |
| **Heartbeat & Cron Engine** | Recurring worker process (`cron`, Temporal, Celery) updating task locks and executing scheduled audits. |
| **Persistent Task Store** | Relational DB schema (PostgreSQL/SQLite) tracking states (`PENDING`, `IN_PROGRESS`, `COMPLETED`). |

## 3. Key Technical Aspects & Dig-In Topics

### 1. Skill Synthesis from Trace Logs
- **Trajectory Mining**: Post-task evaluation routines scan OpenTelemetry trace graphs for successful multi-turn tool interaction sequences that achieved high reward scores.
- **Parameterization & Serialization**: The synthesis engine extracts reusable tool parameters, abstracts domain-specific variables, and serializes the procedure into a standardized `SKILL.md` file saved in `.agents/skills/<skill_name>/`.
- **Skill Registration & Discovery**: Newly synthesized skills are indexed in the agent's prompt catalog, allowing future agent turns to dynamically load and execute the skill.

### 2. Context Compaction & Memory Pruning Algorithms
- **Decay Scoring**: Applying exponential time/turn decay weights to historical message tokens ($S = e^{-\lambda \cdot \Delta t}$). High-scoring structural instructions are retained, while old intermediate outputs decay.
- **Hierarchical Summarization**: Summarizing finished task branches into compact status nodes, replacing hundreds of raw execution tokens with a 2-line summary.
- **KV Cache Management**: Selectively evicting obsolete KV cache blocks in inference engines while preserving root system prompt tokens.

### 3. Failure Root-Cause Indexers & Error Taxonomy
- **Taxonomy Database Classification**:
  - *Category 1*: Context Window Overflow / Token Exhaustion.
  - *Category 2*: Tool Parameter Schema Validation Failure.
  - *Category 3*: Stagnant ReAct Loop / Infinite Execution Loop.
  - *Category 4*: External API Rate Limit / Dependency Timeout.
  - *Category 5*: Requirement Ambiguity / Spec Contradiction.
- **Negative Prompt Injection**: When an agent task fails, the failure indexer queries the taxonomy database for matching error signatures and injects targeted negative constraints into the retry prompt.

### 4. Persistent Heartbeat & Cron State Engines
- **Heartbeat & Lock Management**: Worker agents periodically update a `last_heartbeat` timestamp in the database. If an agent crashes or stalls, the supervisor detects the stale lock and reassigns the task checkpoint to a new worker.
- **Cron Schedulers**: Periodic background jobs triggering scheduled maintenance, security scans, and playbook optimization loops.

```
+-----------------------------------------------------------------------------------+
|                  LONG-HORIZON STATE & SKILL SYNTHESIS ENGINE                      |
+-----------------------------------------------------------------------------------+
|  [Agent Execution Loop] ---> Emits OTel Traces ---> [Database Task Checkpoint]    |
|            ^                                                |                     |
|            |                                                v                     |
|  [Inject Synthesized Skill] <--- [Mine High-Reward] <--- [Task Completion]        |
|            |                      Trace Spans               (Status: SUCCESS)     |
|            |                                                                      |
|  [Inject Failure Constraint] <--- [Index Taxonomy] <--- [Task Failure]            |
|                                    Database             (Status: FAILED)          |
+-----------------------------------------------------------------------------------+
```

## 4. Future Lab Blueprint

### Lab 1: Baseline Architecture
Build a persistent task execution engine using SQLite and Python. Define a `tasks` table tracking state, progress checkpoints, and retry counts. Implement a background heartbeat worker that polls pending tasks, invokes an agent loop, updates checkpoints after each step, and recovers gracefully from simulated process crashes.

### Lab 2: Intermediate Capability Integration
Implement an automated post-task skill synthesis module. After an agent completes a complex multi-step task, analyze the trace log, extract successful tool sequences, auto-generate a structured `.agents/skills/<skill_name>/SKILL.md` file, and verify that the agent can discover and use the new skill in subsequent runs.

### Lab 3: Enterprise Resilience & Advanced Edge Cases
Develop a memory compaction and context pruning engine for long-horizon execution. Simulate a 100-turn agent execution log, apply decay scoring and hierarchical summarization to prune token count by 70% while retaining critical task state, and verify that the agent maintains reasoning context without exceeding context window limits.

### Stretch Goal: Production Hardening
Architect an enterprise self-evolving agent platform. The platform features persistent SQLite/Postgres task state queues, distributed heartbeat lock managers, automated failure root-cause indexing into an error taxonomy database, continuous skill synthesis from execution trace logs, and dynamic playbook optimization across long-horizon multi-day execution workflows.
