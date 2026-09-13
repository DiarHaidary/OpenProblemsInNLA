#!/usr/bin/env python3
"""Recheck all included results; Python >= 3.10, no third-party dependencies."""
from pathlib import Path
import argparse
import subprocess
import sys


def main():
    root=Path(__file__).resolve().parents[1]
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=root/'recheck')
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    subprocess.run([sys.executable,str(root/'code/test_verify.py')],check=True)
    with (args.output/'exact_q3.json').open('w',encoding='utf-8') as out:
        subprocess.run([sys.executable,str(root/'code/exact_q3.py')],stdout=out,check=True)
    certs=sorted((root/'certificates').glob('q*.json'))
    subprocess.run([sys.executable,str(root/'code/verify.py'),*map(str,certs),
                    '--json-output',str(args.output/'verified.json')],check=True)
    print(f'All {len(certs)} certificates verified. Results: {args.output.resolve()}')


if __name__=='__main__':
    main()
