"""Check payload sizes and SHA-256 hashes in an untouched package extraction.

Exit 0 means the payload matches the manifest. This does not establish that
any mathematical claim is correct or that the manifest is authenticated.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path, PurePosixPath
from build_manifest import ROOT, MANIFEST, digest_file, excluded, payload_paths


def verify(root: Path = ROOT) -> dict:
    root = root.resolve()
    manifest_path = root / MANIFEST
    if manifest_path.is_symlink():
        raise ValueError('Manifest must not be a symbolic link')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest.get('format') != 'ra14-integrity-v1':
        raise ValueError('Unknown manifest format')
    entries = manifest.get('files')
    if not isinstance(entries, list) or manifest.get('file_count') != len(entries):
        raise ValueError('Invalid manifest entries or count')
    seen: set[str] = set()
    problems: list[dict] = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError('Invalid manifest entry')
        name = entry.get('path')
        if not isinstance(name, str) or not name or '\\' in name:
            raise ValueError('Invalid payload path')
        relative = PurePosixPath(name)
        if relative.is_absolute() or '..' in relative.parts or str(relative) != name:
            raise ValueError(f'Unsafe or noncanonical payload path: {name}')
        if name in seen or excluded(Path(name)):
            raise ValueError(f'Duplicate or excluded payload path: {name}')
        seen.add(name)
        expected_size = entry.get('size')
        expected_hash = entry.get('sha256')
        if (not isinstance(expected_size, int) or expected_size < 0
                or not isinstance(expected_hash, str)
                or not re.fullmatch(r'[0-9a-f]{64}', expected_hash)):
            raise ValueError(f'Invalid size or digest: {name}')
        target = root.joinpath(*relative.parts)
        if not target.resolve().is_relative_to(root):
            raise ValueError(f'Payload escapes root: {name}')
        if target.is_symlink() or not target.is_file():
            problems.append({'path': name, 'problem': 'missing, not a regular file, or symbolic link'})
            continue
        if target.stat().st_size != expected_size or digest_file(target) != expected_hash:
            problems.append({'path': name, 'problem': 'size or SHA-256 mismatch'})
    actual = {path.relative_to(root).as_posix() for path in payload_paths(root)}
    for name in sorted(actual - seen):
        problems.append({'path': name, 'problem': 'unexpected payload file'})
    return {'ok': not problems, 'checked_files': len(entries),
            'problems': problems,
            'meaning': 'Byte integrity only, not mathematical proof verification.'}


def main() -> int:
    try:
        result = verify()
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as error:
        result = {'ok': False, 'error': f'{type(error).__name__}: {error}'}
    print(json.dumps(result, indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
