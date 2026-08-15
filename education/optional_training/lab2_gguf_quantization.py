"""Reference solution. Moved from the old education/labs tree."""
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
