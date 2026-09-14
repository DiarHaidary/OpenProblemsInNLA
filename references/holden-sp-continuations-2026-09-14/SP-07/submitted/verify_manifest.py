#!/usr/bin/env python3
"""Check every file hash in the delivered SHA-256 manifest."""
from pathlib import Path
import hashlib,sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent

def main():
    manifest=ROOT/'MANIFEST.sha256'
    count=0
    for line in manifest.read_text().splitlines():
        if not line.strip():continue
        expected,name=line.split('  ',1)
        path=(ROOT/name).resolve()
        if ROOT not in path.parents or not path.is_file():raise ValueError('Missing or unsafe manifest path: '+name)
        actual=hashlib.sha256(path.read_bytes()).hexdigest()
        if actual!=expected:raise ValueError('Hash mismatch: '+name)
        count+=1
    print('PASS: '+str(count)+' delivered file hashes verified.')
if __name__=='__main__':
    try:main()
    except (OSError,ValueError) as exc:
        print('INTEGRITY CHECK FAILED: '+str(exc),file=sys.stderr);raise SystemExit(1)
