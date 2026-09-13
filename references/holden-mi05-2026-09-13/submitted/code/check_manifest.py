#!/usr/bin/env python3
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parents[1]
count=0
for line in (ROOT/'MANIFEST.sha256').read_text().splitlines():
    digest,name=line.split('  ',1)
    p=(ROOT/name).resolve()
    if ROOT not in p.parents or not p.is_file():
        raise ValueError('Missing or unsafe manifest path: '+name)
    if hashlib.sha256(p.read_bytes()).hexdigest()!=digest:
        raise ValueError('Hash mismatch: '+name)
    count+=1
print('PASS:',count,'manifest entries')
