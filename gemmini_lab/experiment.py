"""Validate the educational tiled systolic algorithm and export honest JSON."""
from __future__ import annotations
import argparse,json,platform,time,hashlib
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
from .simulator import WavefrontArray,reference_gemm,simulate_tiled_gemm


def experiment(m=16,n=16,k=16,rows=16,cols=16,k_tile=16,seed=42):
    if min(m,n,k,rows,cols,k_tile)<1 or max(m,n,k)>512:raise ValueError('invalid dimensions (1..512)')
    rng=np.random.default_rng(seed)
    a=rng.integers(-3,4,size=(m,k),dtype=np.int8)
    b=rng.integers(-3,4,size=(k,n),dtype=np.int8)
    expected=reference_gemm(a,b)
    start=time.perf_counter()
    actual,model=simulate_tiled_gemm(a,b,WavefrontArray(rows,cols,k_tile))
    duration=time.perf_counter()-start
    if not np.array_equal(actual,expected):raise AssertionError('systolic-array model diverged from NumPy GEMM')
    return {
        'status':'host_reference_vs_educational_wavefront_correctness_passed',
        'created_at_utc':datetime.now(timezone.utc).isoformat(),
        'host':platform.platform(), 'matrix_dims':[m,n,k],'seed':seed,
        'input_dtype':'int8','accumulator_dtype':'int64 (software reference)',
        'model':model,'wall_seconds_host_python':duration,
        'output_sha256':hashlib.sha256(actual.tobytes()).hexdigest(),
        'max_absolute_error':int(np.max(np.abs(actual-expected))),
        'warning':'This experiment does not access Gemmini silicon, RTL, Spike, Verilator, or Chipyard.'
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for key,default in [('m',16),('n',16),('k',16),('rows',16),('cols',16),('k_tile',16),('seed',42)]:
        p.add_argument('--'+key.replace('_','-'),type=int,default=default)
    p.add_argument('--output',type=Path,default=Path('results/wavefront_model.json'))
    a=p.parse_args()
    values={x:getattr(a,x) for x in ('m','n','k','rows','cols','k_tile','seed')}
    result=experiment(**values)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'logical_steps':result['model']['logical_wavefront_steps_sequential_tiles'],
                      'output':str(a.output)},indent=2))
if __name__=='__main__':main()
