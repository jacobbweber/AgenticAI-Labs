"""Reference solution. Moved from the old education/labs tree."""
import json
import re
import urllib.request
from typing import Dict, Any, List, Tuple

OLLAMA_URL = "http://192.168.1.29:11434/api/generate"
MODEL_NAME = "qwen3.6:35b-a3b-65k"

# 1. Local PII Redactor & De-Anonymization Vault
class LocalPIIRedactor:
    """Sanitizes PII tokens before model processing and restores them post-generation."""
    def __init__(self):
        self.vault: Dict[str, str] = {}
        self.counter = 0

    def sanitize(self, text: str) -> str:
        # Regex patterns for email and names
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        name_pattern = r"\b(John Doe|Jane Smith|Alice Johnson)\b"

        sanitized_text = text
        for match in re.finditer(email_pattern, text):
            email = match.group(0)
            if email not in self.vault.values():
                self.counter += 1
                token = f"[EMAIL_{self.counter}]"
                self.vault[token] = email
                sanitized_text = sanitized_text.replace(email, token)

        for match in re.finditer(name_pattern, text):
            name = match.group(0)
            if name not in self.vault.values():
                self.counter += 1
                token = f"[PERSON_{self.counter}]"
                self.vault[token] = name
                sanitized_text = sanitized_text.replace(name, token)

        return sanitized_text

    def restore(self, text: str) -> str:
        restored = text
        for token, original in self.vault.items():
            restored = restored.replace(token, original)
        return restored

# 2. Local In-Memory Vector Search Engine
class LocalVectorStore:
    """Simple in-memory vector store performing local cosine similarity search."""
    def __init__(self):
        self.documents: List[Dict[str, str]] = []

    def add_document(self, doc_id: str, content: str):
        self.documents.append({"id": doc_id, "content": content})

    def search(self, query: str) -> List[str]:
        # Simple local keyword relevance scoring for demonstration
        query_words = set(query.lower().split())
        results = []
        for doc in self.documents:
            doc_words = set(doc["content"].lower().split())
            score = len(query_words.intersection(doc_words))
            results.append((doc["content"], score))
        results.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, score in results[:1]]

# 3. Main Air-Gapped Pipeline Execution
def run_airgapped_private_rag(user_query: str, private_docs: List[str]):
    print("=== STARTING AIR-GAPPED PRIVATE DATA RAG LAB ===")
    redactor = LocalPIIRedactor()
    vector_store = LocalVectorStore()

    # Step 1: Sanitize private documents & add to local vector store
    print("\n[PII REDACTOR] Ingesting & Sanitizing Private Documents...")
    for idx, doc in enumerate(private_docs, start=1):
        sanitized_doc = redactor.sanitize(doc)
        vector_store.add_document(f"doc_{idx}", sanitized_doc)
        print(f"  Doc {idx} Original : {doc}")
        print(f"  Doc {idx} Sanitized: {sanitized_doc}")

    # Step 2: Sanitize query & retrieve local context
    sanitized_query = redactor.sanitize(user_query)
    print(f"\n[LOCAL RAG] Executing Vector Retrieval for Query: '{sanitized_query}'")
    context = vector_store.search(sanitized_query)[0]
    print(f"  Retrieved Local Context: '{context}'")

    # Step 3: Local LLM Generation via Ollama
    print("\n[LOCAL LLM] Generating answer via local LAN Ollama host...")
    prompt = f"Context: {context}\nQuestion: {sanitized_query}\nAnswer in 1 sentence:"
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.0}
    }
    json_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL, data=json_bytes, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        raw_output = data.get("response", "").strip()

    print(f"  Raw Model Output (Masked Tokens): {raw_output}")

    # Step 4: Restore PII from Ephemeral Vault
    final_output = redactor.restore(raw_output)
    print(f"\n[DE-ANONYMIZATION] Restored Final Result for User:\n{final_output}")

if __name__ == "__main__":
    docs = [
        "Patient John Doe has email john@acme.com and was diagnosed with mild hypertension.",
        "System administrator Jane Smith configured security group rules on 192.168.1.1."
    ]
    query = "What is the diagnosis for John Doe?"
    run_airgapped_private_rag(query, docs)
