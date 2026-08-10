# 00: Sandboxing & Secure Code Execution

## 1. Macro Concept & Industry Need

Allowing autonomous AI agents to execute untrusted code or terminal commands directly on host infrastructure presents massive security risks, including container escapes, host credential exfiltration, resource exhaustion attacks, and unauthorized system access. In enterprise software platforms, agent execution environments must guarantee deterministic isolation, strict resource boundaries, ephemeral memory management, and real-time security probes.

Production-grade code execution sandboxing relies on multi-layer isolation technologies:
- **WebAssembly (Wasm) Runtimes**: Near-instantaneous (sub-1ms startup) sandboxed execution of compiled binaries within linear memory bounds, completely bypassing host kernel exposure.
- **MicroVM Hypervisors & Warm Pools**: Light-weight micro-virtual machines (Firecracker, gVisor) providing hardware-level virtualized boundaries with sub-10ms instantiation latency via copy-on-write snapshot pools.
- **Kernel Syscall Filtering & eBPF Observers**: Intercepting process execution at the Linux kernel boundary using `seccomp-bpf` syscall filters and eBPF probes to enforce zero-trust security profiles.
- **Ephemeral Memory Sanitization & Secret Vaults**: In-memory `tmpfs` mounts that isolate API secrets during execution and perform complete RAM sanitization post-execution.

## 2. Architectural Component Mapping

| AI Jargon / Buzzword | Actual Software Component / Standard Primitive |
| :--- | :--- |
| **Code Execution Sandbox** | Ephemeral OCI container or microVM worker spawned via Docker API or Firecracker socket. |
| **Wasm Sandbox** | In-process WebAssembly Virtual Machine (Wasmtime/Extism) enforcing linear memory limits. |
| **MicroVM Warm-Pool** | Pre-warmed pool of microVM snapshots (Firecracker/gVisor) managed by a local daemon. |
| **Syscall Filter Boundary** | Linux kernel `seccomp-bpf` profile blocking unauthorized syscalls (`ptrace`, `execve`). |
| **Ephemeral Secret Injector** | In-memory `tmpfs` vault injecting scoped credentials and wiping RAM post-execution. |
| **Sandbox Execution Gateway** | Subprocess supervisor setting POSIX resource limits (`rlimit`), non-root `uid`, and read-only mounts. |

## 3. Key Technical Aspects & Dig-In Topics

### 1. WebAssembly Isolation (Wasmtime & Extism Runtimes)
- **Linear Memory Safety**: Wasm runtimes allocate isolated linear memory arrays for execution. WebAssembly code cannot read or write outside its allocated memory segment, rendering buffer overflow attacks ineffective.
- **Host Function Binding (HFC)**: Explicit interface imports (`extism:host/user`) defining permissible host calls (e.g., restricted file read/write within virtual directories), preventing arbitrary OS access.
- **Performance Characteristics**: Sub-millisecond cold start times allow instant agent tool invocation without container overhead.

### 2. MicroVM Hypervisors & Warm-Pooling Pools
- **Container vs. MicroVM Boundaries**: Standard Docker containers share the host Linux kernel, exposing container escape vectors. MicroVMs (Firecracker, gVisor) provide separate kernel instances per sandbox.
- **Copy-on-Write (CoW) Warm Pools**: Maintaining a pool of pre-warmed, paused VM snapshots. When an agent requests a code execution sandbox, the daemon restores a snapshot in sub-10ms using CoW memory page mapping.
- **Teardown & Re-warming**: Destroying the used microVM instance immediately after tool execution finishes and instantiating a fresh snapshot into the warm pool.

### 3. Linux Kernel Syscall Filtering & eBPF Observability
- **Seccomp-BPF Filters**: Crafting system call allowlists for agent subprocesses. Blocking dangerous syscalls like `ptrace` (process inspection), `kexec_load` (kernel alteration), and raw network socket creation.
- **eBPF Execution Probes**: Real-time security telemetry tracing file system modifications, process branching, and outbound network attempts across sandbox boundaries.

### 4. Secret Injection & Memory Sanitization
- **Ephemeral Credential Provisioning**: Mounting secrets into RAM-backed `tmpfs` volumes rather than persistent disk storage.
- **Post-Execution RAM Wiping**: Overwriting execution RAM space, terminating process trees, and purging temporary working directories upon code completion.

```
+-----------------------------------------------------------------------------------+
|                     MULTI-LAYER AGENT SANDBOX ARCHITECTURE                        |
+-----------------------------------------------------------------------------------+
|  [Agent Harness]                                                                  |
|        |                                                                          |
|        +---> [Wasm Engine] (Wasmtime/Extism) ---> [Linear Memory] (1ms startup)  |
|        |                                                                          |
|        +---> [MicroVM Pool] (Firecracker/gVisor) -> [Hardware Isolated MicroVM]   |
|        |                                           (CoW Snapshot, 10ms acquisition)|
|        |                                                                          |
|        +---> [Kernel Gate] (seccomp-bpf / eBPF) -> [Filtered Syscall Execution]   |
|                                                    (Blocked: ptrace, kexec, raw_net)|
+-----------------------------------------------------------------------------------+
```

## 4. Future Lab Blueprint

### Lab 1: Baseline Architecture
Build an ephemeral Docker-based code execution runner in Python using the Docker SDK. Enforce non-root user execution (`uid=1000`), a read-only root filesystem with a temporary `tmpfs` workspace mount, 512MB RAM ceiling, 1.0 CPU limit, and a strict 10-second execution timeout.

### Lab 2: Intermediate Capability Integration
Embed an in-process WebAssembly runtime (Wasmtime/Extism) inside a Python agent harness. Expose isolated host functions for file reading/writing within a virtual directory while preventing raw OS command execution and unapproved network calls.

### Lab 3: Enterprise Resilience & Advanced Edge Cases
Implement a pre-warmed microVM execution daemon managing a pool of isolated Firecracker or gVisor instances. Achieve sub-10ms sandbox acquisition latency, execute untrusted code snippets concurrently across multiple isolated sandboxes, and automatically destroy/re-warm sandboxes post-execution.

### Stretch Goal: Production Hardening
Architect a zero-trust multi-tenant code execution gateway featuring eBPF-based syscall filtering (`seccomp`), automated network egress blocking, ephemeral secret injection via in-memory vaults, and an automated red-teaming test harness that attempts container escapes and file exfiltration attacks.
