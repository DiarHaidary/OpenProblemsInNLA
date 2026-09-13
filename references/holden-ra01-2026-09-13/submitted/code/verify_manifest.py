"""Verify the delivered snapshot before regenerating PDFs or JSON outputs."""
from __future__ import annotations
from hashlib import sha256
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'SHA256SUMS.txt'

def main()->None:
    expected={}
    for line in MANIFEST.read_text().splitlines():
        if not line.strip():continue
        digest,name=line.split('  ',1)
        path=(ROOT/name).resolve()
        if ROOT not in path.parents:raise ValueError('Unsafe manifest path')
        expected[name]=digest
        if not path.is_file():raise FileNotFoundError(name)
        got=sha256(path.read_bytes()).hexdigest()
        if got!=digest:raise RuntimeError(f'Hash mismatch: {name}')
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
            if p.is_file() and p!=MANIFEST and '__pycache__' not in p.parts and p.suffix!='.pyc'}
    if actual!=set(expected):
        raise RuntimeError(f'File list mismatch: extra={actual-set(expected)}, missing={set(expected)-actual}')
    print(f'PASS: {len(expected)} files match SHA-256 manifest.')

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print(f'FAIL: {exc}',file=sys.stderr);sys.exit(1)
