#!/usr/bin/env python3
"""Create this bounded author-evidence seal; no whole-project freeze."""
from pathlib import Path
import datetime
import hashlib
import json

E = Path(__file__).resolve().parent
P = E.parents[1]
M = E / 'EVIDENCE-MANIFEST.json'
assert not M.exists(), 'Preserve an existing seal; do not silently reseal.'
paths = {p for p in E.rglob('*') if p.is_file() and p != M}
external = [
    'NLA/IE05/Witness.lean', 'NLA/IE05/Definitions.lean', 'Challenge.lean',
    'lean-toolchain', 'lakefile.toml', 'lake-manifest.json', 'comparator.json',
    'reviews/statement-freeze.json', 'verification/proof-start.json',
    'NLA/IE05/Pivot.lean', 'NLA/IE05/GEPP.lean', 'NLA/IE05/LUTrajectory.lean',
    'NLA/IE05/Scaling.lean', 'NLA/IE05/QR.lean', 'NLA/IE05/IntegerQR.lean',
    'NLA/IE05/ExactCertificates.lean',
    'verification/gepp-development/EVIDENCE-MANIFEST.json',
    'verification/gepp-development/HANDOFF.json', 'reviews/gepp-completion.md',
    'verification/lu-development/EVIDENCE-MANIFEST.json',
    'verification/lu-development/HANDOFF.json', 'reviews/lu-completion.md',
    'verification/qr-scaling-handoff/EVIDENCE-MANIFEST.json',
    'verification/qr-scaling-handoff/HANDOFF.json',
    'verification/exactcert-diagnostic-referee/EVIDENCE-MANIFEST.json',
    'verification/exactcert-diagnostic-referee/HANDOFF.json',
]
paths.update(P / rel for rel in external)
files = {}
for p in sorted(paths):
    assert p.is_file() and not p.is_symlink(), str(p)
    files[str(p.relative_to(P))] = {
        'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size}
data = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope': 'Complete Witness author evidence, Witness source and explicitly listed immutable dependencies; excludes concurrent growth work',
    'files': files, 'bound_file_count': len(files),
    'exact_self_exclusion': str(M.relative_to(P)),
    'inventory_rule': 'Every file in witness-development, including nested manifests, except only this exact outer file; plus explicit immutable external inputs.'}
M.write_text(json.dumps(data, indent=2) + '\n')
print(json.dumps({'bound_files': len(files), 'outer_sha256': hashlib.sha256(M.read_bytes()).hexdigest()}))
