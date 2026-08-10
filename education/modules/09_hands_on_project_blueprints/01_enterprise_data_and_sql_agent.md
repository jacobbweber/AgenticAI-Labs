# 01: Enterprise Data & SQL Agent Blueprint

## 1. Macro Concept & Industry Need

An **Enterprise Data & SQL Agent** is an autonomous data engineering and business intelligence assistant that converts natural language user queries into syntactically valid, semantic-layer-compliant, and secure SQL queries against enterprise data warehouses (such as Snowflake, Google BigQuery, PostgreSQL, or Databricks).

In modern data platform engineering, enabling direct self-service analytics for non-technical business stakeholders via basic Text-to-SQL prompts introduces severe operational risks:
1. **Hallucinated Schemas & Invalid Joins**: Unconstrained LLMs frequently invent non-existent database columns, join tables on incompatible primary/foreign key types, or misinterpret complex schema relationships.
2. **Metric Definition Divergence**: Business metrics (such as Monthly Recurrent Revenue / MRR, Net Retention Rate / NRR, or Active Daily Users) often require precise aggregation filters and business logic. Naive SQL generation yields conflicting metric definitions across departments.
3. **Runaway Compute Billing & Performance Degradation**: Generating unindexed `SELECT *` queries or unbounded full-table scans across petabyte-scale data warehouses can trigger catastrophic cloud warehouse compute bills and degrade database throughput.
4. **Security Vulnerabilities & Data Corruption**: Exposing direct SQL execution paths without AST parsing or read-only connection pooling creates severe SQL injection risks and potential data deletion vulnerabilities (`DROP TABLE`, `DELETE FROM`).

To mitigate these enterprise failure modes, the Enterprise Data & SQL Agent integrates **schema vector retrieval (RAG)**, **semantic layer auditing (dbt / Cube)**, **Abstract Syntax Tree (AST) validation**, and **dynamic error-healing execution loops**.

---

## 2. Architectural Component Mapping

The following table demystifies key AI and agentic data concepts by mapping them directly to standard software engineering primitives:

| AI / Agentic Concept | Standard Software Engineering Primitive | System Function / Role |
| :--- | :--- | :--- |
| **Text-to-SQL Generator** | AST Code Transpiler | Translates natural language intent into target-dialect SQL query strings using structured prompts. |
| **Schema Retriever (RAG)** | K-NN Vector Search Index | Indexes table metadata, dbt column descriptions, and sample values to retrieve top-$K$ relevant schemas. |
| **Semantic Layer Auditing** | Business Logic Abstraction API | Intersects queries with dbt Semantic Layer / Cube metrics to enforce canonical metric definitions (e.g., NRR, ARR). |
| **Schema Compiler & Validator** | SQL Abstract Syntax Tree (AST) Parser | Parses SQL via `sqlglot` or `pglast` to verify syntax, table existence, and dialect compatibility before execution. |
| **Safety Guardrail Enforcer** | Read-Only Connection Pool & AST Filter | Restricts DB connection user permissions to `SELECT` only, enforces row limits (`LIMIT 1000`), and caps query timeouts. |
| **Dynamic SQL Healer** | Try-Catch Database Driver Loop | Intercepts SQL runtime errors (e.g., `UndefinedColumn`), formats error payload, and re-prompts model for query repair. |

---

## 3. Key Technical Aspects & Dig-In Topics

### Vector-Based Schema Pruning & Context Management
Enterprise data warehouses frequently contain thousands of tables and tens of thousands of columns. Passing full database DDLs into an LLM context window is cost-prohibitive and degrades generation accuracy. Schema pruning uses a two-stage vector retrieval pipeline:

1. **Schema Chunking & Indexing**: Database metadata, table descriptions, primary/foreign key mappings, and sample column values are chunked into DDL objects and embedded into a vector database (e.g., ChromaDB or Qdrant using BGE-M3 embeddings).
2. **Contextual K-NN Retrieval**: When a user asks "What was our quarterly customer churn in North America?", the retriever queries the vector store for the top $K=5$ most relevant table schemas (e.g., `dim_customers`, `fact_subscriptions`, `dim_regions`), injecting only necessary schema DDLs into the prompt.

### Semantic Layer & dbt Metric Integration
To prevent the agent from guessing complex business logic, user queries are resolved through a **semantic layer** (such as dbt Semantic Layer, Cube, or MetricFlow). Rather than writing raw `GROUP BY` aggregations from scratch, the agent maps business terms to pre-audited metric definitions:

```
User Query: "Show Q3 Net Revenue Retention by Tier"
                       |
                       v
+---------------------------------------------------+
|               Semantic Layer Router               |
| Maps "Net Revenue Retention" -> dbt Metric 'nrr'  |
| Maps "Q3" -> Date Filter '2026-Q3'                |
+----------------------+----------------------------+
                       |
                       v
+---------------------------------------------------+
|            Canonical SQL Compilation              |
| SELECT tier, metric_value FROM semantic_catalog   |
| WHERE metric = 'nrr' AND period = '2026-Q3'       |
+---------------------------------------------------+
```

### SQL Compilation, AST Verification & Dialect Transpilation
Before any query reaches the database driver, the raw SQL string generated by the LLM is parsed into an Abstract Syntax Tree (AST) using libraries like `sqlglot`. This step guarantees syntax validity and enables multi-dialect translation (e.g., transpiling PostgreSQL syntax to Snowflake or BigQuery SQL):

```python
# Conceptual AST Verification & Guardrail Pipeline (< 50 lines)
import sqlglot
from sqlglot import parse_one, exp

def validate_and_format_sql(raw_sql: str, target_dialect: str = "snowflake") -> str:
    # Step 1: Parse SQL into Abstract Syntax Tree (AST)
    expression = parse_one(raw_sql, read="postgres")
    
    # Step 2: AST Keyword Filtering (Reject DDL/DML mutation attempts)
    forbidden_types = (exp.Drop, exp.Delete, exp.Insert, exp.Update, exp.Create, exp.Alter)
    if expression.find(forbidden_types):
        raise ValueError("Security Alert: Mutation AST nodes detected in query!")
        
    # Step 3: Enforce Row Count Hard Ceiling (LIMIT 1000)
    if not expression.find(exp.Limit):
        expression = expression.limit(1000)
        
    # Step 4: Transpile AST to Target Database Dialect
    return expression.sql(dialect=target_dialect)
```

### Security Guardrails & Database Connection Isolation
Production deployment mandates a multi-layered security wrapper around database interactions:
- **Role-Based Read-Only Isolation**: Database connections use dedicated service accounts with strict read-only grants (`GRANT SELECT ON SCHEMA analytics TO agent_role`). Database mutations (`INSERT`, `UPDATE`, `DROP`, `TRUNCATE`) are structurally impossible at the database engine level.
- **Statement Timeout Controls**: All query sessions set strict execution timeouts (e.g., `SET statement_timeout = '15s'`) to prevent runaway queries from exhausting warehouse resources.
- **Data Masking & PII Redaction**: Column-level security policies automatically mask sensitive fields (e.g., SSN, credit card numbers, personal emails) prior to returning query result sets to the agent or user interface.

### Dynamic SQL Healing & Self-Correction Loop
When a generated query fails at database execution time (e.g., syntax error, schema mismatch, or ambiguous column reference), the agent enters an automated dynamic healing loop:
1. Database driver catches `DatabaseError` exception and extracts verbatim error text (e.g., `column "customer_tier" does not exist`).
2. Error handling interceptor packages original prompt, failed SQL query, and exact database error trace into a repair context frame.
3. The LLM processes the repair context frame and generates a corrected SQL query string.
4. Execution retries up to `max_healing_attempts = 3`. If healing fails, execution halts and returns a structured diagnostic report.

---

## 4. Future Lab Blueprint

The following directional prompts guide the construction of hands-on technical labs for this blueprint module:

### Lab 1: Baseline Architecture (Text-to-SQL Pipeline & Read-Only DB Execution Harness)
Construct a basic Text-to-SQL execution pipeline connecting an LLM to a local PostgreSQL or SQLite database. Implement an isolated database execution harness that enforces read-only connections, wraps queries in statement execution timeouts, and formats query results into structured JSON tables.

### Lab 2: Intermediate Capability Integration (Vector Schema Retriever & AST Syntax Validation)
Build a schema vector retrieval system using ChromaDB and BGE-M3 embeddings to index database table DDLs and retrieve top-$K$ schemas dynamically. Integrate `sqlglot` to parse generated SQL queries into Abstract Syntax Trees (ASTs), enforce automatic `LIMIT 1000` clause injection, and validate dialect compatibility before execution.

### Lab 3: Enterprise Resilience & Advanced Edge Cases (dbt Semantic Layer Integration & Dynamic SQL Self-Correction Loop)
Integrate a dbt Semantic Layer or Cube API interface to resolve business metrics into canonical aggregation queries. Construct an automated SQL self-correction loop that catches database runtime exceptions (e.g., missing column, invalid join condition), appends verbatim error traces to context, and re-prompts the model for query repair (with a 3-attempt ceiling).

### Stretch Goal: Production Hardening (Enterprise Multi-Tenant Data Agent with PII Masking & Cost Profiling)
Deploy a multi-tenant enterprise data agent backend featuring automated PII column masking/redaction, pre-execution query cost estimation via `EXPLAIN ANALYZE`, interactive human approval gates for high-cost queries, export pipelines to Parquet/CSV formats, and full OpenTelemetry tracing.
