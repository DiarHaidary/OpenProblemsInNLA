#!/usr/bin/env python3
"""Rebuild a certificate from numerical discovery, then check it exactly.

The discovery phase is floating-point and may produce a different certificate
on another numerical stack. Only the final exact verifier establishes success.
The supplied certificate does not require running this reconstruction.
"""
from __future__ import annotations
import argparse,os,subprocess,sys
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--work-dir',type=Path,default=Path('reconstruction_work'))
    args=p.parse_args();work=args.work_dir.resolve();work.mkdir(parents=True,exist_ok=True)
    here=Path(__file__).resolve().parent
    env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'}
    steps=[['dual_certificate.py','4','0'],['exact_reconstruct.py'],
           ['initial_coordinates.py'],['rationalize_certificate.py'],['package_certificate.py']]
    for step in steps:
        command=[sys.executable,str(here/step[0]),*step[1:]]
        print('\nRUN',step[0],flush=True)
        subprocess.run(command,cwd=work,env=env,check=True)
    cert=work/'krause_certificate.json'
    for checker in ['verify_certificate.py','verify_witness_and_rigidity.py']:
        subprocess.run([sys.executable,'-O',str(here.parent/'certificate'/checker),str(cert)],
                       cwd=work,env=env,check=True)
    print('\nExact certificate rebuilt and verified:',cert)
if __name__=='__main__':main()
