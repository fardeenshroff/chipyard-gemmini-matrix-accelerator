# Real Chipyard/Gemmini integration

My host-side wavefront model is a **separate implementation** and cannot replace a Gemmini ISA or RTL simulation. To run the example in `baremetal/gemmini_matmul.c`, obtain a supported upstream version of Chipyard and Gemmini, a matching RISC-V compiler, and the hardware-generated Gemmini parameter headers.

## Upstream reference material

- Gemmini official source: https://github.com/ucb-bar/gemmini
- Chipyard Gemmini documentation: https://chipyard.readthedocs.io/en/stable/generators/gemmini/
- Gemmini bare-metal C examples: https://github.com/ucb-bar/gemmini-rocc-tests

## Integration steps

1. Pin and record the Chipyard/Gemmini commits, submodule state and generated accelerator config.
2. Locate the supported Gemmini library and the checked-out tests' build system.
3. Copy or adapt `baremetal/gemmini_matmul.c` into the upstream tests with its own target definition. Ensure `gemmini.h` and `gemmini_params.h` match the same hardware configuration.
4. Cross-compile for the supported RISC-V target. The code is **not** intended for host x86 compilation.
5. Execute the resulting program on Spike with the Gemmini extension or the matching Verilator RTL simulator.
6. Preserve the original simulator stdout, tool versions, and correctness markers, then run `python scripts/parse_sim_log.py <captured.log>`.
7. Report cycle counts **only** when a real simulator/hardware counter is connected and its timing scope is documented. The example emits a correctness marker without a cycle number.

The exact upstream `tiled_matmul_auto` arguments may change by revision. Validate the call signature against the checked-out header before building. No configuration-specific compatibility is claimed in advance.
