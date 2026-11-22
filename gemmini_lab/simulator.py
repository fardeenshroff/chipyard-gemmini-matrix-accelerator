"""Functional output-stationary systolic-array wavefront model.

This model explicitly advances individual PE multiply-accumulate operations
one logical step per cycle. It is *not* a Gemmini RTL simulation, DMA model,
cycle-accurate Chipyard model, or validated prediction of actual latency.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np


def validate_inputs(a,b):
    a=np.asarray(a)
    b=np.asarray(b)
    if a.ndim!=2 or b.ndim!=2 or a.shape[1]!=b.shape[0] or min(*a.shape,*b.shape)<1:
        raise ValueError('Expected nonempty compatible two-dimensional matrices')
    if not np.issubdtype(a.dtype,np.integer) or not np.issubdtype(b.dtype,np.integer):
        raise ValueError('Integer matrices are required (int8 recommended)')
    return a.astype(np.int64),b.astype(np.int64)


def reference_gemm(a,b):
    a,b=validate_inputs(a,b)
    return a@b


@dataclass(frozen=True)
class WavefrontArray:
    rows: int=16
    cols: int=16
    k_tile: int=16
    def __post_init__(self):
        if min(self.rows,self.cols,self.k_tile)<1:raise ValueError('positive PE dimensions required')


def _wavefront_block(a,b,c,offset_i,offset_j,k_start,k_end):
    """Run one wavefront for a single C output tile and K reduction slice."""
    rows=min(c.shape[0]-offset_i,a.shape[0]-offset_i)
    cols=min(c.shape[1]-offset_j,b.shape[1]-offset_j)
    length=k_end-k_start
    count=0
    # A(i,k) injected at t=i+k; B(k,j) injected at t=j+k.
    # Their operands meet at PE(i,j) on t=i+j+k.
    for t in range(length+rows+cols-2):
        for i in range(rows):
            for j in range(cols):
                k=t-i-j
                if 0<=k<length:
                    c[offset_i+i,offset_j+j] += int(a[offset_i+i,k_start+k])*int(b[k_start+k,offset_j+j])
                    count += 1
    return length+rows+cols-2,count


def simulate_tiled_gemm(a,b,array:WavefrontArray=WavefrontArray()):
    """Compute C=A@B with explicit tiled PE activity and logical cycles.

    Tiles run sequentially in this educational model. Cycle count describes
    *abstract wavefront steps*, not measured accelerator hardware cycles.
    """
    a,b=validate_inputs(a,b)
    m,k=a.shape
    _,n=b.shape
    c=np.zeros((m,n),dtype=np.int64)
    steps=0
    macs=0
    tiles=0
    for ii in range(0,m,array.rows):
        for jj in range(0,n,array.cols):
            for kk in range(0,k,array.k_tile):
                # local views prevent rows/columns from leaking into neighbor tiles
                ar=min(array.rows,m-ii)
                bc=min(array.cols,n-jj)
                ak=a[ii:ii+ar,kk:min(kk+array.k_tile,k)]
                bk=b[kk:min(kk+array.k_tile,k),jj:jj+bc]
                scratch=np.zeros((ar,bc),dtype=np.int64)
                tile_steps,tile_macs=_wavefront_block(ak,bk,scratch,0,0,0,ak.shape[1])
                c[ii:ii+ar,jj:jj+bc] += scratch
                steps += tile_steps
                macs += tile_macs
                tiles += 1
    assert macs==m*n*k
    return c,{
        'mode':'educational_wavefront_model_not_rtl',
        'array_rows':array.rows,'array_cols':array.cols,'k_tile':array.k_tile,
        'logical_wavefront_steps_sequential_tiles':steps,
        'multiply_accumulate_operations':macs,
        'tile_evaluations':tiles,
        'scope':'Algorithmic PE simulation; not real Gemmini cycles, energy, or clock rate.'
    }
