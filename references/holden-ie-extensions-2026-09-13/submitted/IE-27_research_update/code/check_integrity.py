#!/usr/bin/env python3
"""Validate the delivered SHA-256 manifest (integrity only, not mathematics)."""
from pathlib import Path
import hashlib
import sys


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    manifest = root/'MANIFEST.sha256'
    failures = []
    count = 0
    try:
        lines = manifest.read_text(encoding='utf-8').splitlines()
    except OSError as exc:
        print(f'Cannot read manifest: {exc}', file=sys.stderr)
        return 1
    for line in lines:
        digest, relative = line.split('  ', 1)
        path = root/relative
        if root not in path.resolve().parents:
            failures.append(f'Unsafe manifest path: {relative}')
            continue
        try:
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError as exc:
            failures.append(f'{relative}: {exc}')
            continue
        count += 1
        if actual != digest:
            failures.append(f'Hash mismatch: {relative}')
    if failures:
        print('\n'.join(failures), file=sys.stderr)
        return 1
    print(f'PASS: {count} file hashes match. This establishes integrity, not mathematical truth.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
