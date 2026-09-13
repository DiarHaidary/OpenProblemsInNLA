#!/usr/bin/env python3
"""Seal only owned Frames material and explicitly immutable boundaries."""
from pathlib import Path
import datetime
import hashlib
import json

E = Path(__file__).resolve().parent
P = E.parents[1]
M = E / 'EVIDENCE-MANIFEST.json'
assert not M.exists(), 'Preserve the previous seal; do not silently replace it.'
paths = {p for p in E.rglob('*') if p.is_file() and p != M}
external = ['NLA/KE04/Frames.lean', 'NLA/KE04/Definitions.lean', 'Challenge.lean',
    'NUMERICAL_TARGETS.md', 'SourceCorrespondence.md', 'README.md', 'lean-toolchain',
    'lakefile.toml', 'lake-manifest.json', 'comparator.json', 'reviews/statement-freeze.json',
    'verification/proof-start.json', 'verification/original-source-inventory.json',
    'reviews/frames-development.md']
paths.update(P / rel for rel in external)
files = {}
for p in sorted(paths):
    assert p.is_file() and not p.is_symlink(), str(p)
    files[str(p.relative_to(P))] = {'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
        'bytes': p.stat().st_size}
data = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope': 'KE04 Frames helper, full owned author evidence and explicit immutable boundary; concurrent proof modules excluded',
    'files': files, 'bound_file_count': len(files), 'exact_self_exclusion': str(M.relative_to(P)),
    'inventory_rule': 'All files in frames-development including nested manifests except only this exact outer manifest, plus named immutable external inputs.'}
M.write_text(json.dumps(data, indent=2) + '\n')
print(json.dumps({'bound_files': len(files), 'outer_sha256': hashlib.sha256(M.read_bytes()).hexdigest()}))
