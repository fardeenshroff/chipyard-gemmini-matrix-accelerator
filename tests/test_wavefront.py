import numpy as np
import pytest
from gemmini_lab import WavefrontArray,reference_gemm,simulate_tiled_gemm
from gemmini_lab.experiment import experiment
from scripts.parse_sim_log import parse_log

@pytest.mark.parametrize('shape,tiles',[
 ((1,1,1),(1,1,1)),
 ((4,7,3),(3,4,2)),
 ((16,16,16),(8,8,8)),
 ((9,11,13),(4,5,6)),
 ((2,3,23),(2,3,7)),
])
def test_wavefront(shape,tiles):
    m,n,k=shape; rng=np.random.default_rng(42)
    a=rng.integers(-5,6,size=(m,k),dtype=np.int8)
    b=rng.integers(-5,6,size=(k,n),dtype=np.int8)
    actual,info=simulate_tiled_gemm(a,b,WavefrontArray(*tiles))
    np.testing.assert_array_equal(actual,reference_gemm(a,b))
    assert info['multiply_accumulate_operations']==m*n*k
    assert info['logical_wavefront_steps_sequential_tiles']>0

def test_report_correctness_and_scope():
    r=experiment(4,5,7,2,2,3)
    assert r['max_absolute_error']==0
    assert 'not' in r['warning']

def test_invalid_shapes():
    with pytest.raises(ValueError):WavefrontArray(0,1,1)
    with pytest.raises(ValueError):simulate_tiled_gemm(np.ones((2,3)),np.ones((4,2)))
    with pytest.raises(ValueError):simulate_tiled_gemm(np.ones((2,3),dtype=float),np.ones((3,2),dtype=int))

def test_real_log_import(tmp_path):
    path=tmp_path/'simulation.log';path.write_text('hardware log\nGEMMINI_RESULT n=16 status=PASS errors=0\n')
    result=parse_log(path)
    assert result['correctness']=='PASS' and result['cycles'] is None
    assert len(result['source_sha256'])==64
    path.write_text('GEMMINI_RESULT n=16 status=PASS errors=7\n')
    with pytest.raises(ValueError):parse_log(path)
