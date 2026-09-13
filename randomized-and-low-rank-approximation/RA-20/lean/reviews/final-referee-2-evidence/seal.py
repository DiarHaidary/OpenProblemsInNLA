#!/usr/bin/env python3
"""Seal exactly referee-2 evidence, complete proof boundary, and original sources."""
import hashlib, json, os, pathlib
P = pathlib.Path(__file__).resolve().parents[2]
E = pathlib.Path(__file__).resolve().parent
G = P.parents[2]
M = E / 'EVIDENCE-MANIFEST.json'
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
freeze_path = P / 'verification/proof-freeze.json'
assert digest(freeze_path) == 'f66dfe47527df937de8ed399606206bdaef55717cef8d68808f60834aece0c6f'
freeze = json.loads(freeze_path.read_text())
paths = {P / n for n in freeze['files']}
paths |= {G / n for n in freeze['source_files']}
paths |= {freeze_path, P / 'reviews/final-referee-2.md'}
paths |= {p for p in E.rglob('*') if p.is_file() and p != M}
for name, sha in freeze['files'].items():
    assert digest(P / name) == sha, name
for name, sha in freeze['source_files'].items():
    assert digest(G / name) == sha, name
assert not M.exists(), 'Never silently overwrite a seal'
files = {os.path.relpath(p, E): {'sha256': digest(p), 'bytes': p.stat().st_size}
         for p in sorted(paths)}
result = {
    'reviewer': '/root/ra20_final_referee2', 'verdict': 'APPROVE',
    'phase': 'Independent final mathematical review, local macOS source rebuild only',
    'proof_freeze_sha256': digest(freeze_path),
    'report_sha256': digest(P / 'reviews/final-referee-2.md'),
    'frozen_project_files_including_outer': 522,
    'original_sources': 16,
    'inventory_rule': 'All referee-2 files, its report, the entire 521-file frozen proof boundary plus the proof freeze itself, and all 16 original source files. Every nested manifest is included. Exclude only this exact new outer manifest path. Other agents\u2019 separately owned additive work is outside this review scope.',
    'exact_self_exclusion': str(M.relative_to(P)),
    'file_count': len(files), 'files': files}
M.write_text(json.dumps(result, indent=2) + '\n')
for name, record in files.items():
    target = E / name
    assert digest(target) == record['sha256'] and target.stat().st_size == record['bytes'], name
print(json.dumps({'result': 'PASS', 'bound_files': len(files),
                  'manifest_sha256': digest(M), 'report_sha256': result['report_sha256']}))
