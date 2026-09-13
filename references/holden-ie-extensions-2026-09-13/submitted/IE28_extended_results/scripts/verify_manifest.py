#!/usr/bin/env python3
"""Check SHA-256 integrity of the files listed in the root manifest."""
from pathlib import Path
import hashlib

def main():
    root=Path(__file__).resolve().parents[1]
    manifest=root/'MANIFEST.sha256'
    count=0
    for line in manifest.read_text().splitlines():
        digest,name=line.split('  ',1)
        path=(root/name).resolve()
        if not path.is_relative_to(root):raise ValueError('unsafe manifest path')
        if not path.is_file():raise FileNotFoundError(name)
        actual=hashlib.sha256(path.read_bytes()).hexdigest()
        if actual!=digest:raise AssertionError(f'SHA-256 mismatch: {name}')
        count+=1
    print(f'PASS: SHA-256 verified for {count} files')
if __name__=='__main__':main()
