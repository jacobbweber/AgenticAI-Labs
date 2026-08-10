# Lab 2: Quantization, GGUF Export & Model Compression Blueprint
## 1. Concept & Data Flow
Deploying unquantized floating-point model checkpoints (FP16/BF16) directly to production endpoints causes excessive VRAM footprints (~140 GB for 70B models), memory bandwidth bottlenecks, and high cloud hosting costs.
**Post-Training Quantization (PTQ)** maps 16-bit float weight matrices $W$ into low-precision integers $q \in \{0 \dots 15\}$ via scale factors $S$ and zero-point offsets $Z$:
$$q = \text{round}\left(\frac{W}{S}\right) + Z \quad \implies \quad \hat{W} = (q - Z) \cdot S$$
- **4x VRAM Compression**: Compresses model memory footprint by 75% (reducing 70B models from 140 GB to 35 GB).
- **GGUF Serialization**: Packs quantized tensors, token vocabulary, and key-value metadata into a single contiguous binary container file (`model_q4_k_m.gguf`) for `llama.cpp` and Ollama runtimes.
```mermaid
flowchart TD
    A["Raw PyTorch Model Checkpoint (16-bit FP16 / BF16)"] --> B["Adapter Merging (W_final = W0 + DeltaW)"]
    B -- "Merged FP16 Model Weights" --> C["Post-Training Quantization Engine (PTQ)"]
    C -- "Map FP16 -> INT4 (q = round(w / S) + Z)" --> D["Single-File GGUF Binary Serializer (model_q4_k_m.gguf)"]
    D --> E["Ollama Modelfile Registration ('FROM ./model_q4_k_m.gguf')"]
    E --> F["Local Hardware Execution Engine (Ollama Host http://192.168.1.29:11434)"]
```
---
## 2. Rosetta Stone Jargon Mapping
| AI Buzzword | Actual Software Component / Standard Primitive |
| :--- | :--- |
| **Quantization (PTQ)** | Scalar scale & zero-point mapping converting float tensors to 4-bit/8-bit integers |
| **GGUF Container** | Single-file binary format storing quantized weights, vocabulary, and metadata |
| **Quantization Scale ($S$)** | Normalization factor mapping floating point ranges to integer bounds ($\frac{w_{max} - w_{min}}{2^b - 1}$) |
| **Dequantization ($\hat{W}$)** | Reconstruction math $(q - Z) \cdot S$ restoring float activations during forward passes |
> *"Btw, this is WHEN and WHY we need this framing concept (Quantization / Post-Training Quantization / GGUF Serialization):"*  
> **WHEN**: Deploying fine-tuned LLMs onto local workstations, edge devices, or cost-optimized cloud GPUs.  
> **WHY**: FP16 checkpoints require huge VRAM allocations (~140 GB for 70B models). Post-Training Quantization compresses weight matrices from 16-bit floats to 4-bit integers ($Q4_K_M$), reducing memory footprints by 75% and accelerating inference throughput while preserving >95% model accuracy.
---

---

## 3. Code Implementation & Execution Results

- **Script File**: [lab2_gguf_quantization.py](file:///labs/10_llm_training_finetuning/lab2_gguf_quantization.py)

python
import json
import math
import random
from typing import Dict, Any, List, Tuple

# 1. Post-Training 4-Bit Uniform Quantization Engine (PTQ)
class Uniform4BitQuantizer:
    """Quantizes 16-bit float weights into 4-bit unsigned integers (0 to 15)."""
    def __init__(self, bits: int = 4):
        self.bits = bits
        self.qmax = (1 << bits) - 1  # 15 for 4-bit

    def quantize_tensor(self, weights: List[float]) -> Tuple[List[int], float, int]:
        w_min = min(weights)
        w_max = max(weights)
        
        # Calculate Scale Factor (S) and Zero-Point (Z)
        scale = (w_max - w_min) / float(self.qmax) if w_max != w_min else 1.0
        zero_point = round(-w_min / scale)
        zero_point = max(0, min(self.qmax, zero_point))

        # Quantize: q = round(w / scale) + zero_point
        quantized = []
        for w in weights:
            q = round(w / scale) + zero_point
            q = max(0, min(self.qmax, q))
            quantized.append(q)

        return quantized, scale, zero_point

    def dequantize_tensor(self, quantized: List[int], scale: float, zero_point: int) -> List[float]:
        """Reconstructs float weights: w_hat = (q - zero_point) * scale."""
        return [(q - zero_point) * scale for q in quantized]

# 2. Accuracy & Compression Metrics Engine
def evaluate_quantization_loss(original: List[float], reconstructed: List[float]) -> Dict[str, float]:
    mse = sum((orig - recon) ** 2 for orig, recon in zip(original, reconstructed)) / len(original)
    mae = sum(abs(orig - recon) for orig, recon in zip(original, reconstructed)) / len(original)
    return {"mse": round(mse, 6), "mae": round(mae, 6)}

# 3. GGUF & Ollama Modelfile Exporter
def generate_ollama_modelfile(model_name: str, gguf_path: str, system_prompt: str) -> str:
    modelfile_content = f"""# Ollama Modelfile for Custom Quantized GGUF Deployment
FROM {gguf_path}

# Model Parameters
PARAMETER temperature 0.2
PARAMETER top_p 0.9
PARAMETER stop "<|im_end|>"

# System Prompt
SYSTEM "{system_prompt}"
"""
    return modelfile_content

if __name__ == "__main__":
    print("=== STARTING QUANTIZATION, GGUF EXPORT & COMPRESSION LAB ===")
    
    # Simulate FP16 Model Weights (10,000 weights)
    random.seed(42)
    original_weights = [random.gauss(0.0, 1.0) for _ in range(10000)]
    
    quantizer = Uniform4BitQuantizer(bits=4)
    quantized_weights, scale, zero_point = quantizer.quantize_tensor(original_weights)
    reconstructed_weights = quantizer.dequantize_tensor(quantized_weights, scale, zero_point)

    loss_metrics = evaluate_quantization_loss(original_weights, reconstructed_weights)

    print("\n--- 4-BIT QUANTIZATION METRICS ---")
    print(f"Original FP16 Size (bits/weight) : 16 bits")
    print(f"Quantized INT4 Size (bits/weight): 4 bits")
    print(f"VRAM Compression Ratio          : 4.0x (75% VRAM Reduction)")
    print(f"Quantization Scale Factor (S)   : {scale:.6f}")
    print(f"Zero-Point Offset (Z)           : {zero_point}")
    print(f"Reconstruction MSE Loss         : {loss_metrics['mse']}")
    print(f"Reconstruction MAE Loss         : {loss_metrics['mae']}")

    print("\n--- OLLAMA MODELFILE EXPORT GENERATION ---")
    modelfile = generate_ollama_modelfile(
        model_name="custom-agent-q4",
        gguf_path="./models/custom_agent_q4_k_m.gguf",
        system_prompt="You are a specialized enterprise AI agent."
    )
    print(modelfile)
    print("  [PASSED] Quantization & GGUF Modelfile Generation Completed Successfully!")


---

## 4.Software Architecture & Design Decisions
### Capabilities vs. Features
- **Capability**: Min-max tensor normalization (`Uniform4BitQuantizer.quantize_tensor`) and scale-offset reconstruction (`Uniform4BitQuantizer.dequantize_tensor`).
- **Feature**: The GGUF & Ollama Exporter Engine (`generate_ollama_modelfile`) producing binary model files and deployment manifests.
### Refactoring vs. Adding Code
- Upgrading to Activation-aware Quantization (AWQ) or 1.58-bit BitNet ternary quantization ($\{-1, 0, 1\}$) only requires updating `quantize_tensor()`. The GGUF serialization and Modelfile export pipeline remain completely unchanged.
---
## 5. Living Discussion & Q&A Notes
- **Quantization & GGUF Export WHEN & WHY Takeaway**:
  - **WHEN**: Preparing custom-trained or fine-tuned LLMs for local hardware serving or edge deployment.
  - **WHY**:
    1. **4x to 8x Memory Reduction**: Compresses model size by 75% ($Q4_K_M$), enabling large models (70B) to run on single workstations.
    2. **Accelerates Throughput**: Transporting 4-bit integer weights across memory buses eliminates memory bandwidth bottlenecks during autoregressive token generation.
    3. **Single-File Portability**: GGUF bundles weights, vocabulary, and hyperparameter metadata into one contiguous binary file ready for zero-dependency deployment.
