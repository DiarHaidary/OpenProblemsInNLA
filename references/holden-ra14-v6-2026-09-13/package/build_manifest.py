"""Generate a local SHA-256 payload manifest, not a proof certificate.

The original manifest should be checked before running code that changes the
results. Regenerating it deliberately records a new working copy's bytes.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = 'MANIFEST.json'
TRANSIENT_ROOT_FILES = {
    'report.aux', 'report.log', 'report.out', 'report.toc',
    'report.fls', 'report.fdb_latexmk', 'report.synctex.gz',
}


def excluded(relative: Path) -> bool:
    """Ignore only named build/cache byproducts, not result logs."""
    return (
        relative.as_posix() == MANIFEST
        or (len(relative.parts) == 1 and relative.name in TRANSIENT_ROOT_FILES)
        or '__pycache__' in relative.parts
        or relative.suffix in {'.pyc', '.pyo'}
    )


def payload_paths(root: Path = ROOT) -> list[Path]:
    paths = []
    for path in root.rglob('*'):
        relative = path.relative_to(root)
        if excluded(relative):
            continue
        if path.is_symlink():
            raise ValueError(f'Symbolic link is not an allowed payload: {relative}')
        if path.is_file():
            paths.append(path)
    return sorted(paths, key=lambda path: path.relative_to(root).as_posix())


def digest_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    entries = [
        {'path': path.relative_to(ROOT).as_posix(),
         'size': path.stat().st_size, 'sha256': digest_file(path)}
        for path in payload_paths()
    ]
    manifest = {
        'format': 'ra14-integrity-v1',
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'PARTIAL',
        'purpose': 'Byte integrity only; not mathematical certification or authentication.',
        'file_count': len(entries),
        'files': entries,
    }
    (ROOT / MANIFEST).write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'manifest': MANIFEST, 'file_count': len(entries)}))


if __name__ == '__main__':
    main()
