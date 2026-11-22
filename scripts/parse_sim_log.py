"""Import a real externally generated Gemmini simulation transcript.

Never manufactures timing numbers. Successful correctness is only recorded if
explicitly present in the raw log. Provenance is a hash, not a proof of origin.
"""
from __future__ import annotations
import argparse,hashlib,json,re
from pathlib import Path

MARKER=re.compile(r'^GEMMINI_RESULT n=(\d+) status=(PASS|FAIL) errors=(\d+)(?: cycles=(\d+))?$',re.MULTILINE)

def parse_log(path:Path):
    raw=path.read_bytes()
    report=raw.decode('utf-8',errors='replace')
    matches=list(MARKER.finditer(report))
    if len(matches)!=1:raise ValueError('Expect exactly one GEMMINI_RESULT result marker')
    m=matches[0]
    size,status,errors,cycles=m.groups()
    if status=='PASS' and int(errors)!=0:raise ValueError('PASS must have errors=0')
    return {'status':'external_log_parsed_not_independently_verified',
            'source':str(path),'source_sha256':hashlib.sha256(raw).hexdigest(),
            'dimension':int(size),'correctness':status,'error_count':int(errors),
            'cycles':int(cycles) if cycles else None,
            'note':'Timing and hardware identity must be independently verified from the original toolchain and simulator logs.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('log',type=Path);p.add_argument('--output',type=Path,default=Path('results/imported_simulator_log.json'))
    args=p.parse_args()
    try:report=parse_log(args.log)
    except (ValueError,OSError) as e:p.error(str(e))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
