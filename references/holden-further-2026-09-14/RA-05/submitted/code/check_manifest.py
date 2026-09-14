#!/usr/bin/env python3
"""Verify every SHA-256 entry without mutating deliverable files."""
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parents[1]
manifest=ROOT/'SHA256SUMS'
if not manifest.is_file(): raise SystemExit('Missing SHA256SUMS')
count=0
for line in manifest.read_text().splitlines():
    if not line.strip(): continue
    expected,rel=line.split('  ',1)
    path=(ROOT/rel).resolve()
    if ROOT.resolve() not in path.parents: raise SystemExit('Unsafe manifest path: '+rel)
    if not path.is_file(): raise SystemExit('Missing file: '+rel)
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    if actual!=expected: raise SystemExit('Hash mismatch: '+rel)
    count+=1
print(f'PASS: {count} SHA-256 file hashes')
