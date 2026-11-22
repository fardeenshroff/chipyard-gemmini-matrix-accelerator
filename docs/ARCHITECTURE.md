# Architecture notes: RISC-V CPU, Gemmini, and matrix acceleration

## Why I am investigating this system

Dense matrix multiplication is a useful workload for understanding computation and data movement: the same mathematical operation can exhibit very different performance depending on register reuse, on-chip scratchpad capacity, tiling, array utilization, and the transfer path between memory and compute.

## Conceptual execution paths

```text
                         Matrix workload
                               |
                +--------------+--------------+
                |                             |
         CPU software path              RISC-V + Gemmini
       C / RISC-V instructions            accelerator path
                |                             |
         General-purpose               Tiled accelerator
         compute / memory               software interface
                |                             |
         Output + checksum            Systolic array / scratchpad
                |                             |
                +----------- verification ----+
```

The current checked-in source implements **only the left-hand CPU reference**. A legitimate Gemmini run requires a pinned Chipyard/Gemmini configuration and an accelerator-linked workload; these components must not be inferred from the C baseline.

## Variables to control when the original accelerator is restored

| Variable | Why it matters |
|---|---|
| Array dimensions and datatype | Determines peak arithmetic throughput and numerical semantics |
| Scratchpad / accumulator capacity | Determines available data reuse and traffic |
| Tiling and dataflow | Changes utilization and movement across the memory hierarchy |
| Input and output data layout | Affects transfer and conversion overhead |
| Simulator, clock, and measurement region | Defines what cycle counts represent |
| Cache state and warm-up | Alters first-call versus steady-state behavior |
| Compile flags and runtime calls | Can change the actual workload being timed |

## Attribution

Gemmini and Chipyard are independently published research systems. Any results in this repository must identify their upstream versions, then distinguish my experiment configuration and code changes from the original framework.
