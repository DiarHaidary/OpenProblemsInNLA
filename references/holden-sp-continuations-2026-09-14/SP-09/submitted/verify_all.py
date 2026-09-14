"""Verify archive integrity and exact proof-critical finite calculations.

The manuscript supplies the analytic proof. These checks do not formalize it.
Optional numerical checks certify only floating-point construction consistency.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def check(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def verify_manifest(root: Path) -> int:
    manifest=root/'SHA256SUMS.txt'
    check(manifest.is_file(),'SHA256SUMS.txt is missing.')
    entries={}
    for line in manifest.read_text().splitlines():
        if not line.strip():continue
        digest,name=line.split('  ',1)
        check(name not in entries,'Duplicate manifest path: '+name)
        path=(root/name).resolve()
        check(path.is_relative_to(root) and path.is_file(),'Invalid manifest path: '+name)
        check(len(digest)==64,'Invalid digest length: '+name)
        check(hashlib.sha256(path.read_bytes()).hexdigest()==digest,'SHA-256 mismatch: '+name)
        entries[name]=digest
    return len(entries)


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report-dir',type=Path)
    parser.add_argument('--include-numerics',action='store_true')
    parser.add_argument('--skip-hash-check',action='store_true',help='For release preparation only.')
    args=parser.parse_args();root=Path(__file__).resolve().parent
    if args.report_dir:
        args.report_dir=args.report_dir.resolve()
        check(not args.report_dir.is_relative_to(root),'Use a report directory outside this immutable archive.')
        args.report_dir.mkdir(parents=True,exist_ok=True)
    hashes=None if args.skip_hash_check else verify_manifest(root)
    if hashes is not None:print(f'PASS: {hashes} SHA-256 file hashes.',flush=True)
    checks=[
        ('retained_eight_exact_programs','prior_round2/verify_all.py','prior'),
        ('new_exact_geometry','certificate/first_order_geometry.py','new'),
        ('new_negative_tests','certificate/test_first_order_geometry.py','new'),
    ]
    if args.include_numerics:
        checks.extend([
            ('constructive_Taylor_demo','experiments/first_order_witness_demo.py','numerical'),
            ('saved_candidate_audit','experiments/verify_candidate34.py','numerical'),
        ])
    rows=[];env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    for name,script,kind in checks:
        command=[sys.executable,'-O',str(root/script)]
        if args.report_dir:
            if kind=='prior':command.extend(['--report-dir',str(args.report_dir/'prior_exact')])
            else:command.extend(['--report',str(args.report_dir/(name+'.json'))])
        start=time.monotonic()
        result=subprocess.run(command,cwd=root,env=env,capture_output=True,text=True)
        print('\n=== '+name+' ===\n'+result.stdout,end='',flush=True)
        if result.stderr:print(result.stderr,file=sys.stderr)
        elapsed=time.monotonic()-start
        if args.report_dir:(args.report_dir/(name+'.log')).write_text(result.stdout+result.stderr)
        check(result.returncode==0,'Verification failed: '+name)
        rows.append({'name':name,'script':script,'kind':kind,'returncode':result.returncode,
                     'result':'PASS','elapsed_seconds':elapsed})
    record={'result':'PASS','python':sys.version,'hashed_files':hashes,
            'exact_programs':10,'new_negative_tests':9,'numerical_programs':2 if args.include_numerics else 0,
            'checks':rows,'scope':'Partial SP-09 result: first-order splitting invariance. General SP-09 is not claimed solved.'}
    if args.report_dir:(args.report_dir/'all_checks.json').write_text(json.dumps(record,indent=2)+'\n')
    print('\nALL REQUESTED CHECKS PASSED. General SP-09 remains unproved in this archive.',flush=True)


if __name__=='__main__':
    main()
