# Chipyard + Gemmini | RISC-V Matrix Acceleration Research

**Research and development portfolio — Fardeen Shroff**  
**Focus:** computer architecture · RISC-V · systolic arrays · memory systems · workload characterization

## Project overview

I am interested in how accelerator architecture, data movement, and software execution interact to determine the performance of matrix-heavy workloads. My earlier Chipyard/Gemmini work explored RISC-V simulation, matrix-multiplication execution, and cycle-level analysis. This repository provides an independently reproducible foundation for rebuilding and extending that investigation.

**What is available today:** a portable FP32 matrix-multiplication reference, a deterministic test harness, a clear experimental protocol, and a checklist for restoring the original Gemmini/Chipyard implementation. **What is not available yet:** the original Gemmini-linked workload, full accelerator configuration, and historical simulator logs. The present C executable runs on the host CPU; it does not issue Gemmini commands.

## Architecture and research context

[Chipyard](https://github.com/ucb-bar/chipyard) is a RISC-V SoC design and simulation environment. [Gemmini](https://github.com/ucb-bar/gemmini) is an open-source generator for DNN accelerators with systolic-array architectures. I use the two projects as a research context for evaluating the relationship among instruction-level workloads, accelerator mappings, memory hierarchy, and cycle counts. I will preserve upstream authorship and identify my own contributions separately when recovering the original project.

A meaningful accelerator comparison needs more than a raw cycle count. The CPU and accelerator paths must perform the same operation, use clearly defined datatypes, validate their outputs, and record what is included in measurement: computation, transfers, setup, and simulator overhead. My emphasis is on **measured, attributable performance**, not unsupported speedup claims.

## Repository contents

| Path | Purpose |
|---|---|
| [`src/matmul_reference.c`](src/matmul_reference.c) | Newly developed C11 FP32 dense GEMM CPU baseline; deterministic matrices and checksum |
| [`tests/test_reference.py`](tests/test_reference.py) | Output, parameter validation, and checksum repeatability tests |
| [`Makefile`](Makefile) | Build and smoke-test entry point |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Chipyard/Gemmini execution concepts and comparison boundaries |
| [`docs/EXPERIMENT_METHOD.md`](docs/EXPERIMENT_METHOD.md) | Fairness criteria, metrics, and simulator protocol |
| [`EVIDENCE_CHECKLIST.md`](EVIDENCE_CHECKLIST.md) | Original files and run logs needed for restoration |
| [`results/README.md`](results/README.md) | Evidence policy and result-recording format |

## Run the portable reference

Requires a C11 compiler, GNU Make, and Python 3 for the expanded tests.

```bash
make
./matmul_reference 64
./matmul_reference 128
make test
```

This verifies a deterministic CPU-side matrix multiplication. It **does not benchmark the Gemmini accelerator** and should not be used to infer its throughput, speedup, or energy efficiency.

## Research record and validation status

| Experiment or claim | Status | Interpretation |
|---|---|---|
| New portable FP32 GEMM reference | Source included | Local tests / GitHub Actions validate the reference |
| Previously described 64³ and 128³ workloads | Historical project description | Original workload source and simulator environment still need recovery |
| Previously reported 2,334 and 10,711 cycles | **Not independently reproduced here** | Do not cite as verified measurements |
| Gemmini-versus-CPU speedup | **Not measured** | Cannot be computed responsibly from unrelated platforms or units |

## Next engineering milestones

1. Restore the original Chipyard/Gemmini commits, submodules, RISC-V toolchain, simulator configuration, and my workload modifications.
2. Rebuild the workload using its original data types, array configuration, and supported Gemmini APIs.
3. Validate functional equivalence and collect cycle traces for multiple matrix sizes and memory configurations.
4. Report raw measurements, software and hardware configuration, data-transfer overhead, and sensitivity to tiling and memory bandwidth.

The objective is to turn a previously explored accelerator problem into a **transparent, reproducible computer-architecture study**. I will publish new measurements only after the corresponding commands and evidence are available.

## Related research

- [My NeuPIMs fork](https://github.com/fardeenshroff/NeuPIMs): heterogeneous NPU/PIM simulation and memory-system research. NeuPIMs itself originates from its upstream authors.
- [My CUDA / TVM LeNet-5 experiments](https://github.com/fardeenshroff/lenet5-gpu-autotvm-optimization): complementary GPU execution and compiler optimization work.

**Author:** [Fardeen Shroff](https://github.com/fardeenshroff). New reference implementation prepared for research reconstruction. Original upstream toolchains remain the work of their respective maintainers.
