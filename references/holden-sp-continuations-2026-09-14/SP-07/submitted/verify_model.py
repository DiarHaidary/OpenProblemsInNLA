#!/usr/bin/env python3
"""Recompute a rigorous enclosure for one chosen lattice-model parameter pair.

This certifies neither the parameter maximum nor a finite SP-07 lower bound.
"""
from pathlib import Path
import argparse,json,sys,time
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from model_certificate import verify_spec

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path)
    p.add_argument('--certificate',type=Path,default=ROOT/'certificates/model_parameters.json')
    a=p.parse_args();start=time.perf_counter()
    out=verify_spec(json.loads(a.certificate.read_text()))
    out['seconds']=time.perf_counter()-start
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,TypeError,ArithmeticError,OSError) as exc:
        print('VERIFICATION FAILED: '+str(exc),file=sys.stderr);raise SystemExit(1)
