# Source restoration checklist

- [ ] Exact Chipyard Git commit, original fork and recursive submodule hashes
- [ ] Gemmini revision, matrix dimensions, numeric precision and systolic-array configuration
- [ ] User-authored C, RTL or simulator changes with contribution history
- [ ] Original `tiled_matmul_ws.c` and other target workloads
- [ ] RISC-V compiler, flags, build system, Spike or Verilator versions
- [ ] Exact commands for 64³ and 128³ workloads
- [ ] Raw cycle-counter logs, definitions, timing scope and checksum outputs
- [ ] Baseline, correctness comparison, independent runs and error analysis
- [ ] Upstream authorship and licensing review

Until recovered, do not quote previously reported cycles as reproduced results.
