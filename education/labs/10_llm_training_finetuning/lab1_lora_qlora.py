import math
import random
from typing import Dict, Any, List

# 1. Pure Python Low-Rank Adaptation (LoRA) Layer Implementation
class PurePythonLoRALayer:
    """Simulates a frozen base linear layer with trainable low-rank adapter matrices A and B."""
    def __init__(self, in_features: int, out_features: int, rank: int = 8, alpha: float = 16.0):
        self.in_features = in_features
        self.out_features = out_features
        self.rank = rank
        self.alpha = alpha
        self.scaling = alpha / rank

        # Frozen Base Weight Matrix W0 (out_features x in_features)
        self.weight_base = [[random.uniform(-0.1, 0.1) for _ in range(in_features)] for _ in range(out_features)]
        
        # Trainable Adapter Matrix A (rank x in_features) - initialized with Kaiming uniform
        k = math.sqrt(1.0 / in_features)
        self.lora_A = [[random.uniform(-k, k) for _ in range(in_features)] for _ in range(rank)]
        
        # Trainable Adapter Matrix B (out_features x rank) - initialized with Zeros
        self.lora_B = [[0.0 for _ in range(rank)] for _ in range(out_features)]

    def forward(self, input_vector: List[float]) -> List[float]:
        """Calculates W0*x + (alpha/r)*(B*A*x)."""
        # Base Linear Output: W0 * x
        base_out = [
            sum(w * x for w, x in zip(row, input_vector))
            for row in self.weight_base
        ]

        # Step 1 of LoRA: A * x -> intermediate vector of length 'rank'
        a_out = [
            sum(a * x for a, x in zip(row, input_vector))
            for row in self.lora_A
        ]

        # Step 2 of LoRA: B * (A * x) -> adapter vector of length 'out_features'
        lora_out = [
            sum(b * a for b, a in zip(row, a_out)) * self.scaling
            for row in self.lora_B
        ]

        # Sum: W0*x + (alpha/r)*B*A*x
        return [b + l for b, l in zip(base_out, lora_out)]

# 2. Parameter Budgeting & Metrics Engine
def calculate_lora_parameter_savings(in_features: int, out_features: int, rank: int) -> Dict[str, Any]:
    base_params = in_features * out_features
    lora_params = (rank * in_features) + (out_features * rank)
    savings_pct = (1.0 - (lora_params / base_params)) * 100.0
    return {
        "base_parameters": base_params,
        "lora_parameters": lora_params,
        "trainable_reduction_pct": round(savings_pct, 2)
    }

if __name__ == "__main__":
    print("=== STARTING PARAMETER-EFFICIENT FINE-TUNING (LORA / QLORA) LAB ===")
    
    in_dim, out_dim, r_dim = 4096, 4096, 8
    metrics = calculate_lora_parameter_savings(in_dim, out_dim, r_dim)
    
    print("\n--- PARAMETER BUDGETING COMPARISON ---")
    print(f"Base Layer Parameters (W0)     : {metrics['base_parameters']:,}")
    print(f"LoRA Adapter Parameters (A+B) : {metrics['lora_parameters']:,}")
    print(f"Trainable Parameter Reduction : {metrics['trainable_reduction_pct']}%")

    print("\n--- FORWARD PASS DEMONSTRATION ---")
    layer = PurePythonLoRALayer(in_features=128, out_features=128, rank=4)
    input_vec = [random.uniform(-1.0, 1.0) for _ in range(128)]
    output_vec = layer.forward(input_vec)
    
    print(f"Input Vector Length  : {len(input_vec)}")
    print(f"Output Vector Length : {len(output_vec)}")
    print("  [PASSED] Pure Python LoRA Forward Pass Completed Successfully!")

