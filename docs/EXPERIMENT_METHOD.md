# Experimental methodology and reproducibility protocol

## Question

For an identical matrix operation and a documented accelerator configuration, how do workload dimensions and data movement influence the observed cycles and end-to-end execution cost?

## Reference computation

For input matrices A and B of dimension N × N, the reference computes C[i,j] = Σ A[i,k] × B[k,j]. The included C11 program uses deterministic FP32 inputs; its checksum is intended as a lightweight regression indicator, not a substitute for elementwise comparison.

## Comparison requirements

1. **Functional equivalence:** Fix dimensions, layout, arithmetic datatype, accumulation rules, and output tolerance. An int8 systolic-array result is not directly equivalent to FP32 CPU computation without explicit quantization semantics.
2. **System configuration:** Record Chipyard and Gemmini commits, submodule hashes, simulator version, runtime/compiler flags, and accelerator configuration.
3. **Timing scope:** Distinguish device compute cycles, accelerator initialization, DMA or scratchpad transfers, and end-to-end invocation. Do not mix host seconds with simulated accelerator cycles as if they were directly comparable.
4. **Repetitions:** Repeat runs, report dispersion, and retain the raw results and logs. Investigate warm-up effects and setup costs.
5. **Sensitivity analysis:** Re-run with multiple N, scratchpad allocations, tile sizes, and dataflows when supported by the hardware generation.
6. **Claim provenance:** Every chart should point back to a command, a source revision, and an unmodified machine-readable record.

## Proposed experiments

| Question | Required evidence |
|---|---|
| Does larger N improve array utilization? | Raw cycle counts, throughput definitions, same hardware |
| Does tile size change memory traffic? | Configuration changes and per-stage counters |
| What fraction of runtime is transfer-bound? | Clear breakdown of compute, load, and store |
| How does baseline CPU execution compare? | Equivalent numerical work and a carefully specified timing basis |

## What the repository does not establish yet

The portable C baseline is a validation starting point, not a restored Gemmini implementation. No new accelerator cycle count, processor speedup, or performance-per-watt figure should be inferred from it.
