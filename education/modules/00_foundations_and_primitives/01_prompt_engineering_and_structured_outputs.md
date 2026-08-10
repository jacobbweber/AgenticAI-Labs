# 01: Prompt Engineering & Structured Outputs

## 1. Macro Concept & Industry Need

While natural language prompts allow human communication with Large Language Models, enterprise software systems cannot process non-deterministic unstructured text responses. **Prompt Engineering** is the discipline of structuring system directives, contextual data, and in-context examples to programmatically guide model behavior. **Structured Outputs** elevate this paradigm by enforcing deterministic, type-safe output formats (such as JSON Schema, Pydantic, or Zod) directly at the inference layer.

In production architectures, relying on post-hoc regex parsing or hoping an LLM outputs valid JSON leads to silent system failures, invalid data mutations, and runtime crash loops. Guaranteeing 100% schema compliance at the inference boundary is essential for reliable integration with downstream databases, REST APIs, and microservices.

Typical enterprise use cases include automated document entity extraction (e.g., parsing financial invoices), intent classification with parameter extraction, and natural-language-to-SQL query generation.

---

## 2. Architectural Component Mapping

The following table maps prompt engineering and structured output terminology to core software engineering primitives:

| AI Jargon / Buzzword | Actual Software Component / Standard Primitive |
| :--- | :--- |
| **Structured Output** | Schema-Constrained JSON Payload output by API or inference engine |
| **Pydantic / Zod Binding** | Type-Safe Object Deserializer and Data Transfer Object (DTO) Validator |
| **Logit Bias** | Token Probability Distribution Scalar Filter applied before sampling |
| **Constrained Sampling / CFG** | Context-Free Grammar Token Trie Masking at Model Inference Layer |
| **Few-Shot Exemplars** | In-Context Demonstration Payload Array passed within request state |
| **System Prompt Isolation** | Structural Container Policy Boundary (`<instructions>`, `<rules>`) |

---

## 3. Key Technical Aspects & Dig-In Topics

### Constrained Sampling Decoding (CFG & Logit Masking)
Traditional structured output approaches relied on asking the model for JSON and running post-generation Pydantic validation, which wastes compute tokens on invalid output and requires retry loops. Modern 2025/2026 inference engines (e.g., Outlines, vLLM, HuggingFace TGI) execute **Constrained Sampling Decoding** using Context-Free Grammars (CFG).

During the autoregressive decode phase, a finite state machine (FSM) or JSON Schema grammar trie evaluates candidate tokens at each generation step. Invalid tokens that would violate the JSON Schema are assigned a logit probability of $-\infty$, guaranteeing with 100% mathematical certainty that the generated output is syntactically valid JSON.

```
Token Vocabulary      CFG Grammar Trie Mask               Model Logit Layer
  [ "{", "foo", ... ]  ====>  Check JSON Schema FSM  ====>  Set invalid tokens to -inf
                                                            Sample only valid JSON tokens
```

### System Prompt Composition & Injection Firewalling
To prevent prompt injection attacks and context bleed, system prompts must use explicit XML structural tags (`<system_instructions>`, `<data_context>`, `<user_input>`, `<output_format>`). Enclosing untrusted user input within structural boundary tags prevents adversarial users from hijacking model directives through prompt injection vectors.

### Programmatic Prompt Optimization (The DSPy Paradigm)
Manual prompt engineering ("prompt tweaking") is being superseded by programmatic prompt compilation frameworks such as DSPy. Instead of hand-crafting prompt strings, developers define declarative input/output signatures and assertions. DSPy compiles the pipeline by automatically selecting optimal few-shot exemplars, tuning prompt directives against metric validation suites, and optimizing system instructions programmatically.

### Strict Schema Compilation & Deserialization
Modern API providers enforce strict JSON Schema specifications (Draft-07 / 2020-12). All fields must be explicitly declared, additional properties set to false (`"additionalProperties": false`), and optional fields typed with explicit union types. This ensures zero-drop deserialization into strongly-typed domain models.

---

## 4. Future Lab Blueprint

The following directional prompts guide the construction of hands-on technical labs for this module:

### Lab 1: Baseline Architecture (Schema-Constrained Extractor with Pydantic/Zod)
Construct a structured entity extraction pipeline that converts a complex domain model (e.g., an invoice with line items, tax IDs, and vendor metadata) into a JSON Schema. Invoke an LLM API using native JSON Schema structured output mode and deserialize the raw JSON payload directly into strongly-typed Pydantic/Zod domain instances.

### Lab 2: Intermediate Capability Integration (Grammar-Guided Constrained Sampling Engine)
Implement a local constrained sampling pipeline using Outlines or vLLM CFG grammars. Build a custom JSON Schema state machine that intercepts model logit probabilities at each token generation step, demonstrating guaranteed schema compliance without post-generation validation or retry loops.

### Lab 3: Enterprise Resilience & Advanced Edge Cases (Adversarial Prompt Injection Firewall)
Develop an enterprise system prompt compiler that structures multi-part prompts using XML container tags. Test the architecture against a benchmark suite of adversarial prompt injection attacks, verifying that structural tag boundaries and schema constraints prevent model instruction hijacking.

### Stretch Goal: Production Hardening (DSPy-Inspired Automated Prompt Compiler)
Build an automated evaluation and prompt compilation harness inspired by DSPy. Create a pipeline that evaluates prompt variations against a test dataset, automatically selects optimal few-shot exemplars, tunes system directives based on validation assertions, and maximizes schema adherence.
