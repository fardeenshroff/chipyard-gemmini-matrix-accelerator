# Chipyard + Gemmini — Matrix Accelerator Research

**RISC-V · systolic arrays · integer matrix multiplication · simulation · hardware/software co-design**

I am investigating how matrix computation maps to a systolic array and how tiling, data movement, and system integration influence performance. I previously explored the Chipyard/Gemmini ecosystem and its matrix workloads. I have now created a reproducible **host-side wavefront simulator** and prepared a **Gemmini-linked RISC-V workload** for integration into an appropriately configured upstream simulator.

> **Source and results boundary:** This is a new, independent reconstruction. The Python wavefront model is a functional educational implementation, **not Chipyard RTL or a cycle-accurate Gemmini simulator**. My historical reported 2,334 and 10,711 cycles have not been reproduced here. The bare-metal Gemmini C program has not been compiled or executed against a pinned upstream configuration in this environment.

## Implementation

| Path | Responsibility | Status |
|---|---|---|
| `src/matmul_reference.c` | Deterministic C11 FP32 CPU matrix multiplication | Locally tested |
| `gemmini_lab/simulator.py` | Output-stationary PE wavefront and tiled integer GEMM | Verified against NumPy |
| `gemmini_lab/experiment.py` | Generate deterministic matrix workload, compare results and write JSON | Locally tested |
| `baremetal/gemmini_matmul.c` | RISC-V Gemmini library example using `tiled_matmul_auto` | Integration target; requires upstream build |
| `scripts/parse_sim_log.py` | Parse explicit simulator output markers with SHA-256 provenance | Locally tested |
| `tests/` | Numerical correctness, input validation, deterministic checks | Automated |
| `docs/` | Architecture, hardware integration and measurement standards | Documented |

## Run the functional research model

Install Python, NumPy, pytest, C compiler and GNU Make:

```bash
python -m pip install -r requirements.txt
make test
python -m gemmini_lab.experiment --m 16 --n 16 --k 16 --rows 8 --cols 8 --k-tile 8
```

The JSON report records **multiply-accumulate counts** and **logical wavefront steps** for sequentially evaluated tiles. These are not Gemmini hardware cycles, ISA timing, throughput, or memory-transfer measurements.

## Run on an actual Gemmini configuration

The integration example requires a pinned [Chipyard](https://github.com/ucb-bar/chipyard) and [Gemmini](https://github.com/ucb-bar/gemmini) checkout, a RISC-V cross toolchain, compatible generated `gemmini_params.h`, and Spike or Verilator. Review [hardware integration](docs/HARDWARE_INTEGRATION.md) before adapting the program into the upstream `gemmini-rocc-tests` tree. The Gemmini API varies by revision, so no universal one-command hardware build can be claimed without the exact upstream configuration.

## Why this matters

A valid accelerator study needs three layers of evidence: correct arithmetic, attribution of observed cycles to a known simulator/hardware configuration, and a matched CPU baseline. My current implementation establishes the first layer on the host and the integration structure for the next two layers. I will publish accelerator speedups only after the upstream target successfully executes and generates attributable logs.

**Related work:** [NeuPIMs](https://github.com/fardeenshroff/NeuPIMs) · [GPU/compiler optimization](https://github.com/fardeenshroff/lenet5-gpu-autotvm-optimization).

**Researcher:** Fardeen Shroff. Chipyard/Gemmini design and research credit remains with their upstream authors.
