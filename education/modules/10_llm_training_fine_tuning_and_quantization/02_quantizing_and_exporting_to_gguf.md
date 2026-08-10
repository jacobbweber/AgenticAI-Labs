# 02: Quantizing, GGUF Export & Edge Runtimes

## 1. Macro Concept & Industry Need

**Post-training quantization, GGUF binary export, and edge compilation** represent the final bridge between machine learning model training (in PyTorch / Hugging Face) and high-performance, low-latency model deployment in production agent applications. This stage encompasses Post-Training Quantization (PTQ), binary container serialization (GGUF, AWQ, EXL2), 1.58-bit ternary quantization (BitNet), and low-latency edge execution runtimes (Apple MLX, WebGPU/WASM, ONNX Runtime, and `llama.cpp`).

Deploying unquantized floating-point model checkpoints (FP32 or BF16/FP16) directly to production endpoints creates four major operational roadblocks:
1. **Excessive VRAM Footprints**: A 70B parameter model in FP16 format requires ~140 GB of VRAM just to load model weights, forcing reliance on expensive multi-GPU cloud instances.
2. **Inference Latency & Memory Bandwidth Bottlenecks**: Autoregressive decoding performance is strictly bound by memory bandwidth. Transporting 16-bit float weights from GPU/CPU RAM to compute cores for every token slows throughput.
3. **Cloud Dependency & Data Privacy Risk**: Edge devices, developer laptops, and local enterprise agent workbenches require fully offline, private execution without sending data over network connections.
4. **Platform Incompatibility**: Raw PyTorch `.safetensors` checkpoints cannot run natively inside client web browsers, mobile NPUs, or embedded hardware without platform-specific compilation.

To solve these challenges, quantization compresses model weights from 16-bit floats down to 4-bit, 3-bit, 2-bit, or even 1.58-bit ternary representations, reducing VRAM footprints by 4x to 8x while preserving > 95% of original model intelligence.

---

## 2. Architectural Component Mapping

The following table translates quantization, binary format, and edge runtime concepts into standard software engineering primitives:

| AI / ML Buzzword | Standard Software Engineering Primitive | System Function / Role |
| :--- | :--- | :--- |
| **Adapter Merging** | Tensor Addition ($W_{final} = W_0 + \Delta W$) | Merges LoRA delta weights directly into base model float tensors using `merge_and_unload()`. |
| **Post-Training Quantization (PTQ)** | Scalar Scale & Zero-Point Mapping | Maps 16-bit floating point weights to lower-bit integers ($Q4_K_M, Q8_0$) via quantization scale factors. |
| **GGUF Format** | Single-File Binary Container & Metadata Serializer | Stores aligned quantized tensors, vocabulary tables, and key-value metadata for `llama.cpp` runtimes. |
| **BitNet 1.58-Bit (Ternary)** | Ternary Weight Constraint ($\{-1, 0, 1\}$) | Restricts weights to -1, 0, or 1, replacing matrix multiplications with conditional additions/subtractions. |
| **AWQ (Activation-aware Quantization)** | Salient Activation Channel Protection | Quantizes weights while protecting 1% most salient activation channels for GPU serving engines (vLLM/SGLang). |
| **EXL2 (ExLlamaV2)** | Variable Bit-Rate Layer Quantization | Applies variable sub-byte quantization (e.g., 3.0 to 6.0 bits/weight) tailored to layer-by-layer sensitivity. |
| **Apple MLX** | Metal Unified Memory Execution Engine | Framework optimized for native Apple Silicon execution, enabling zero-copy CPU/GPU memory access. |
| **WebGPU / WASM** | In-Browser Compute Shader Runtime | Compiles quantized model weights into WebGPU storage buffers for zero-install client-side browser execution. |

---

## 3. Key Technical Aspects & Dig-In Topics

### Quantization Schemes & Trade-Offs (GGUF vs AWQ vs EXL2)
Quantization maps high-precision float values to low-precision integers ($q = \text{round}(w / S) + Z$). Different serving targets rely on specialized binary container formats:

- **GGUF (GPT-Generated Unified Format)**: The standard single-file binary container format for `llama.cpp` and Ollama. Stores tensor weights, token vocabulary, and key-value metadata in a single contiguous file. Supports CPU vector instructions (AVX-512, ARM Neon), Apple Metal unified memory, and CUDA offloading.
  - $Q4_K_M$: 4-bit quantization using 6-bit quant scales for critical attention projection tensors (optimal balance of size, speed, and accuracy).
  - $Q8_0$: 8-bit quantization with near-zero perplexity loss.
- **AWQ (Activation-aware Weight Quantization)**: Protects top 1% salient activation channels from quantization noise. Designed specifically for high-throughput GPU serving engines like vLLM and SGLang.
- **EXL2 (ExLlamaV2)**: Enables fine-grained variable bit-rate quantization (e.g., 3.5 or 4.25 bits per weight), tuning bit precision on a layer-by-layer basis for high-speed single-GPU inference.

### Extreme Low-Bit Frontier: BitNet 1.58-Bit Ternary Quantization
BitNet 1.58-bit represents a radical shift in neural network architecture. Model weights are constrained strictly to ternary values $\{-1, 0, 1\}$:

$$W_{quant} = \text{RoundClip}\left(\frac{W}{\gamma + \epsilon}, -1, 1\right), \quad \text{where } \gamma = \frac{1}{m \cdot n}\sum_{i,j} |W_{ij}|$$

- **Elimination of Floating-Point Matrix Multiplication**: Traditional matrix multiplication ($Y = W \cdot X$) is replaced entirely with integer addition and subtraction ($Y = \sum \pm X$).
- **Hardware Impact**: Reduces matrix multiplication energy consumption by up to 10x and boosts throughput by 3x on standard CPU and NPU hardware.

```
Traditional Matrix Multiplication:
Y = (W_0 * X_0) + (W_1 * X_1) + (W_2 * X_2)  [FP16 Multiplications]

BitNet 1.58-bit Ternary Execution:
Y = (+X_0) + (0) - (X_2)                      [Integer Add / Subtract Only]
```

### Edge Execution Runtimes (Apple MLX, WebGPU, ONNX)
- **Apple MLX Framework**: Optimized for Apple Silicon unified memory architecture. Eliminates memory copy overhead between CPU and GPU cores, allowing 70B models to run locally on M-series Macs at high tokens-per-second rates.
- **WebGPU & WASM (WebLLM / Transformers.js)**: Compiles model weights into WebGPU storage buffers, executing compute shaders directly inside client web browsers (Chrome, Edge, Safari) without server backend calls.
- **ONNX Runtime & DirectML**: Converts models into ONNX computational graphs for cross-platform hardware acceleration across Windows DirectML, Android NNAPI, and iOS CoreML.

### Production Export & Ollama Serving Workflow
Exporting a custom fine-tuned PyTorch model to Ollama follows a 5-step build pipeline:

```bash
# Step 1: Merge LoRA Adapters into Base Model
python merge_adapter.py --base_model ./base_qwen --adapter ./lora_adapter --output ./merged_fp16

# Step 2: Convert Merged PyTorch Checkpoint to GGUF (FP16)
python llama.cpp/convert_hf_to_gguf.py ./merged_fp16 --outtype f16 --outfile model_fp16.gguf

# Step 3: Quantize GGUF to Q4_K_M
./llama.cpp/llama-quantize ./model_fp16.gguf ./model_q4_k_m.gguf Q4_K_M

# Step 4: Create Ollama Modelfile
cat <<EOF > Modelfile
FROM ./model_q4_k_m.gguf
PARAMETER temperature 0.2
PARAMETER stop "<|im_end|>"
SYSTEM "You are a specialized enterprise AI agent."
EOF

# Step 5: Register & Serve in Ollama
ollama create custom-agent -f Modelfile
```

---

## 4. Future Lab Blueprint

The following directional prompts guide the construction of hands-on technical labs for this module:

### Lab 1: Baseline Architecture (LoRA Adapter Merging & GGUF Conversion Pipeline)
Construct a model export pipeline that merges a fine-tuned LoRA adapter into base model weights using PyTorch/PEFT (`merge_and_unload`). Convert the merged FP16 model checkpoint into GGUF format using `llama.cpp` conversion scripts.

### Lab 2: Intermediate Capability Integration (Post-Training Quantization & Ollama Modelfile Packaging)
Execute post-training quantization using `llama-quantize` to produce $Q4_K_M$ and $Q8_0$ GGUF model variants. Write a custom Ollama `Modelfile`, register the quantized model (`ollama create`), and benchmark generation throughput (tokens/sec) and VRAM usage across quantization levels.

### Lab 3: Enterprise Resilience & Advanced Edge Cases (Edge Compilation with Apple MLX & WebGPU Browser Serving)
Compile a fine-tuned model checkpoint for Edge runtimes: Convert weights to Apple MLX format for native Apple Silicon unified memory execution, and export to WebGPU/WASM format for zero-install client-side browser execution via compute shaders.

### Stretch Goal: Production Hardening (BitNet 1.58-Bit Ternary Model Deployment & High-Concurrency AWQ Serving)
Deploy a BitNet 1.58-bit ternary quantized model or high-concurrency AWQ/EXL2 model on a local serving gateway. Build an automated CI/CD pipeline that fine-tunes, quantizes, tests format compliance, and deploys model artifacts to production agent serving clusters.
