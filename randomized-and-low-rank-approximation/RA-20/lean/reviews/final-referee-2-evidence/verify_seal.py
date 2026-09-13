#!/usr/bin/env python3
"""Read-only verification of the retained referee-2 scope, including exact coverage."""
import hashlib, json, os, pathlib
P = pathlib.Path(__file__).resolve().parents[2]
E = pathlib.Path(__file__).resolve().parent
G = P.parents[2]
M = E / 'EVIDENCE-MANIFEST.json'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
manifest = json.loads(M.read_text())
fpath = P / 'verification/proof-freeze.json'
freeze = json.loads(fpath.read_text())
assert digest(fpath) == manifest['proof_freeze_sha256']
expected = {P / n for n in freeze['files']}
expected |= {G / n for n in freeze['source_files']}
expected |= {fpath, P / 'reviews/final-referee-2.md'}
expected |= {p for p in E.rglob('*') if p.is_file() and p != M}
assert set(manifest['files']) == {os.path.relpath(p, E) for p in expected}
assert manifest['file_count'] == len(expected)
for name, record in manifest['files'].items():
    target = E / name
    assert digest(target) == record['sha256'], name
    assert target.stat().st_size == record['bytes'], name
print(json.dumps({'result': 'PASS', 'files': len(expected), 'manifest_sha256': digest(M),
                  'report_sha256': digest(P / 'reviews/final-referee-2.md')}))
