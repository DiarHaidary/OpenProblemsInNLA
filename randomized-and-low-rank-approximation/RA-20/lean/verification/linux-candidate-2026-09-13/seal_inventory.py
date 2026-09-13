#!/usr/bin/env python3
"""One-shot author installation inventory seal, after successful preseal checks."""
from pathlib import Path
import datetime
import hashlib
import json
import os

E = Path(__file__).resolve().parent
P = E.parents[1]
R = P.parents[2]
SELF = E / 'EVIDENCE-MANIFEST.json'
assert not SELF.exists(), 'Never silently replace a historical seal'

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

baseline = json.loads((E / 'preflight.json').read_text())
proof = json.loads((P / 'verification/proof-freeze.json').read_text())
checks = json.loads((E / 'CHECKS.json').read_text())
validation = json.loads((E / 'VALIDATION.json').read_text())
assert validation['status'] == 'PRESEAL_INPUTS_PASS'
files = {p.resolve() for p in P.rglob('*') if p.is_file()}
files |= {(R / n).resolve() for n in proof['source_files']}
files |= {R / 'tools/lean/validate_manifest.py', R / 'tools/validate_problem_ids.py'}
assert SELF.resolve() not in files
own = [p for p in files if p.is_relative_to(E)]
out = {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status': 'AUTHOR_INSTALLATION_SEALED; independent packaging review pending',
    'author': '/root/ra20_final_referee1',
    'role': 'Prior independent final mathematical referee; now candidate-document author, adding no review approval',
    'base': proof['base'],
    'baseline_count': len(baseline['baseline']),
    'README_sha256': digest(P / 'README.md'),
    'YAML_sha256': digest(P / 'formalization.yaml'),
    'historical_mapping': {
        'exact_original_project_path': 'README.md',
        'only_expected_sha256': '7eb951780e58ce518f0a400c90297020e7c6909ad9fd0c9c15b8036761a8bb50',
        'exact_archive_project_path': 'verification/pre-candidate-README.md',
        'all_other_paths': 'Unchanged and checked at their original exact paths and hashes',
    },
    'file_count': len(files),
    'own_evidence_files_excluding_outer': len(own),
    'project_files_excluding_outer': sum(p.is_relative_to(P) for p in files),
    'live_original_and_check_tool_files': sum(not p.is_relative_to(P) for p in files),
    'original_sources': proof['source_files'],
    'original_source_git_blobs': proof['source_git_blobs'],
    'nested_historical_inventories': checks['all_prior_nested_manifests'],
    'inventory_rule': 'Every preinstallation project file, exact old README archive, current wrappers, all own evidence and nested manifests; all sixteen live original source inputs and actual schema/ID validator scripts. Paths relative to this manifest directory. Later files from a separate reviewer outside this directory are not part of this author seal.',
    'exact_self_exclusion': 'EVIDENCE-MANIFEST.json',
    'files': {os.path.relpath(p, E): {'sha256': digest(p), 'bytes': p.stat().st_size} for p in sorted(files)},
}
SELF.write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({'status': out['status'], 'files': len(files),
                  'own_evidence_files_excluding_outer': len(own),
                  'outer_sha256': digest(SELF)}))
