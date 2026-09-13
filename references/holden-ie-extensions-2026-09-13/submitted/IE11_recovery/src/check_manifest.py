#!/usr/bin/env python3
"""Check the distribution hashes before rerunning scripts that rewrite results."""
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parents[1]

def main():
    path=ROOT/'MANIFEST.sha256'
    if not path.exists():raise SystemExit('MANIFEST.sha256 is missing')
    count=0
    for line in path.read_text().splitlines():
        expected,name=line.split('  ',1);target=(ROOT/name).resolve()
        if ROOT not in target.parents:raise SystemExit('Unsafe manifest path: '+name)
        if not target.is_file():raise SystemExit('Missing file: '+name)
        actual=hashlib.sha256(target.read_bytes()).hexdigest()
        if actual!=expected:raise SystemExit('Hash mismatch: '+name)
        count+=1
    print(f'PASS: {count} distributed files match SHA-256 manifest')
if __name__=='__main__':main()
