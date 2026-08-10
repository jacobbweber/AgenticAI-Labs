# 02: Local-First & Private Data Architecture

## 1. Macro Concept & Industry Need

In enterprise domains—such as healthcare, defense, financial services, and proprietary software development—strict data governance mandates (HIPAA, GDPR, SOC 2, and defense air-gap requirements) prohibit transmitting confidential documents, source code, or customer PII to external cloud LLM APIs. Furthermore, cloud-dependent architectures introduce operational fragility: cloud outages, API deprecations, network partition failures, and unannounced vendor data mining policies can disrupt critical infrastructure.

**Local-First Private Data Architecture** is the design pattern for building 100% offline, zero-trust AI agent stacks. By executing every layer of the intelligence pipeline—document parsing, PII sanitization, vector embedding generation, sparse/dense indexing, re-ranking, and LLM inference—on local, self-contained hardware, local-first architectures guarantee absolute data privacy, zero outbound telemetry, and continuous operation in network-isolated environments.

---

## 2. Architectural Component Mapping

| AI Jargon / Buzzword | Actual Software Component / Standard Primitive |
| :--- | :--- |
| **Air-Gapped Stack** | Process-isolated runtime environment bound strictly to loopback interfaces (`127.0.0.1`) with zero outbound socket creation permissions. |
| **Hybrid Sparse-Dense Retrieval** | Dual-index search engine combining lexical keyword matching (BM25 in SQLite FTS5/Tantivy) with semantic vector search (HNSW in Chroma/Qdrant). |
| **Reciprocal Rank Fusion (RRF)** | Rank-merging algorithm combining sparse and dense retrieval result sets into a unified relevancy ranking without score normalization issues. |
| **Local PII Redactor** | Named Entity Recognition (NER) and regex sanitization middleware replacing sensitive string spans with anonymous tokens (`[PERSON_1]`). |
| **Local Re-ranker** | Local cross-encoder neural network (`bge-reranker-large` on ONNX/llama.cpp) scoring query-document pair relevancy locally. |

---

## 3. Key Technical Aspects & Dig-In Topics

### 3.1 Air-Gapped Agent Execution & Zero-Trust Topologies

A enterprise local-first agent stack operates under a strict **Zero Outbound Egress** policy. The software architecture isolates runtime components using process sandboxing, loopback bindings, and network namespace isolation (`unshare -n` in Linux or Docker network isolation `--network none`):

```
                       AIR-GAPPED AGENT EXECUTION BOUNDARY
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│  ┌──────────────────┐    IPC / Loopback     ┌───────────────────────────┐  │
│  │ Local Agent Core │ <───────────────────> │  Local Ollama / vLLM      │  │
│  │ (Python Engine)  │                       │  Inference Server         │  │
│  └────────┬─────────┘                       └───────────────────────────┘  │
│           │                                                                │
│           ├───────────────> Local PII Sanitizer (spaCy / GLiNER NER)       │
│           │                                                                │
│           ├───────────────> Hybrid Storage (SQLite FTS5 + HNSW Vector Store)│
│           │                                                                │
│           └───────────────> Local ONNX Re-ranker (bge-reranker-large)       │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
         X (Blocked: All outbound WAN network interfaces drops traffic)
```

1. **Loopback Binding**: Local server endpoints (Ollama, vLLM, Chroma) bind exclusively to `127.0.0.1` rather than `0.0.0.0` to block external network access on local LAN interfaces.
2. **Offline Model Provisioning**: Weights, tokenizers, vector indices, and ONNX runtimes are pre-downloaded, verified via cryptographic SHA-256 hashes, and stored on encrypted local disk volumes.

### 3.2 Hybrid Sparse-Dense Retrieval (BM25 + HNSW) & RRF Scoring

Pure dense vector search (HNSW) frequently fails in enterprise technical domains when queries contain exact code identifiers, error trace codes, or variable names (e.g., `ERR_CONN_REFUSED` or `auth_token_v2`). Hybrid retrieval combines **sparse lexical search (BM25)** with **dense semantic vector search (HNSW)**.

The two candidate lists are merged using **Reciprocal Rank Fusion (RRF)**:

$$RRF\_Score(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$

Where $M$ is the set of retrieval systems (sparse and dense), $r_m(d)$ is document $d$'s rank in retriever $m$, and $k$ is a smoothing constant (typically $k = 60$).

```python
# Reciprocal Rank Fusion (RRF) Implementation
def reciprocal_rank_fusion(sparse_results: list[str], dense_results: list[str], k: int = 60) -> list[tuple[str, float]]:
    scores = {}
    
    for rank, doc_id in enumerate(sparse_results, start=1):
        scores[doc_id] = scores.get(doc_id, 0.0) + (1.0 / (k + rank))
        
    for rank, doc_id in enumerate(dense_results, start=1):
        scores[doc_id] = scores.get(doc_id, 0.0) + (1.0 / (k + rank))
        
    sorted_docs = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return sorted_docs
```

RRF operates on ordinal ranks rather than raw similarity scores, making it immune to scale differences between BM25 scores and cosine vector similarities.

### 3.3 Local PII Detection & Context Masking Pipeline

To ensure absolute privacy when passing documents into agent execution context, a **Local PII Redaction Middleware** intercepts text before vector embedding and context insertion:

1. **Entity Extraction**: Combined regex engines (for credit cards, SSNs, API keys) and local Named Entity Recognition models (spaCy `en_core_web_sm` or GLiNER) identify sensitive spans.
2. **Reversible Token Substitution**: Sensitive strings are replaced with deterministic placeholders (`John Doe` $\to$ `[PERSON_1]`, `john@company.com` $\to$ `[EMAIL_1]`).
3. **De-Anonymization Vault**: A mapping dictionary is stored strictly in ephemeral memory. After the local LLM generates its response containing placeholder tokens, the vault restores the original text before presenting the final result to the user.

### 3.4 Local Embedding & Re-Ranking Runtimes

Local retrieval stacks run high-dimensional embedding models (`bge-m3`, `nomic-embed-text`) and cross-encoder re-rankers (`bge-reranker-large`) on local accelerators:

- **Local Embeddings**: Generating 1024-dim dense float vectors via local ONNX runtime or Ollama `/api/embeddings` endpoints in $<10\text{ms}$ per batch.
- **Cross-Encoder Re-Ranking**: Passing the top-50 RRF candidate documents through a local cross-encoder model to score joint query-document interactions, selecting the top-5 most relevant chunks for LLM context insertion.

---

## 4. Future Lab Blueprint

### Lab 1: Baseline Architecture & Offline Vector Indexing
- **Objective**: Build a 100% local document ingestion and vector search pipeline.
- **Tasks**:
  1. Set up a local ChromaDB / Qdrant store in Python.
  2. Configure local vector embedding generation using Ollama (`nomic-embed-text`) or HuggingFace `sentence-transformers`.
  3. Ingest a batch of local text documents, generate vector embeddings, and verify semantic search queries offline with Wi-Fi disabled.

### Lab 2: Intermediate Capability Integration & Local PII Redaction Pipeline
- **Objective**: Construct a local PII sanitization middleware with reversible placeholder mapping.
- **Tasks**:
  1. Build a text interceptor using regex and spaCy NER to detect personal names, email addresses, and API credentials.
  2. Map detected PII entities to anonymous tokens (`[PERSON_1]`, `[EMAIL_1]`) and store mappings in an ephemeral vault.
  3. Wire the interceptor into a local agent loop, verifying that context passed to the local LLM is sanitized and that generated responses are correctly de-anonymized.

### Lab 3: Enterprise Resilience & Hybrid BM25 + HNSW RRF Search Engine
- **Objective**: Implement a hybrid search engine combining SQLite FTS5 (BM25) and local HNSW vector search with Reciprocal Rank Fusion.
- **Tasks**:
  1. Set up a local SQLite database with FTS5 enabled for full-text keyword indexing alongside a Chroma vector index.
  2. Implement an RRF rank-merging algorithm to combine search results from both indices.
  3. Benchmark retrieval accuracy for queries containing exact technical identifiers (variable names, error codes) versus pure vector search.

### Stretch Goal: Production Hardening & Air-Gapped Security Audit
- **Objective**: Package the complete local-first stack into a network-isolated container environment with zero outbound access.
- **Tasks**:
  1. Containerize the local agent, vector store, and inference endpoints using Docker with `--network none` or Linux `unshare -n`.
  2. Execute a packet capture audit (`tcpdump` / Wireshark) during agent execution to prove zero outbound WAN network traffic.
  3. Implement local disk encryption (LUKS / SQLCipher) for the vector database and GGUF model repositories.
