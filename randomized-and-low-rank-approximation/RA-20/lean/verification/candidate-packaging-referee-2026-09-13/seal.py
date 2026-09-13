#!/usr/bin/env python3
"""One-shot seal of independent packaging evidence; never overwrites an outer seal."""
from pathlib import Path
import datetime
import hashlib
import json
import os
from verify_inventory import A, E, G, P, REPORT, SELF, load, sha, verify

assert not SELF.exists(), 'The independent packaging seal already exists.'
assert not (E / 'FINAL.json').exists(), 'The final handoff already exists.'
final = {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'reviewer': '/root/ra20_final_referee2',
    'verdict': 'APPROVE: candidate packaging only',
    'report': str(REPORT.relative_to(P)),
    'report_sha256': sha(REPORT),
    'checks': 'RESULT.json',
    'checks_sha256': sha(E / 'RESULT.json'),
    'installer_manifest_sha256': sha(A / 'EVIDENCE-MANIFEST.json'),
    'README_sha256': sha(P / 'README.md'),
    'YAML_sha256': sha(P / 'formalization.yaml'),
    'command_receipts': 21,
    'read_only_checks': 'schema, two permanent-ID validators, canonical diff, complete inventory, live/snapshot/original Git identities, concrete metadata and reproduction alignment',
    'reviewer_diagnostics': 'One initial combined-link-count assertion failed, retained and corrected without candidate changes; sixteen previously successful immutable Git receipts are preserved and verified on resume.',
    'new_mathematical_approval': False,
    'new_Lean_builds': 0,
    'actual_Linux_Comparator_default_kernel_controls': 'pending; not executed',
    'operational_acceptance': 'pending',
    'canonical_status': 'Solved, unchanged',
    'publication': 'pending',
    'sole_write_scope': [str(REPORT.relative_to(P)),str(E.relative_to(P)) + '/']
}
(E / 'FINAL.json').write_text(json.dumps(final, indent=2) + '\n')
author = load(A / 'EVIDENCE-MANIFEST.json')
author_bound = {(A / n).resolve() for n in author['files']}
own = {p.resolve() for p in E.rglob('*') if p.is_file() and p.resolve() != SELF}
files = author_bound | {A / 'EVIDENCE-MANIFEST.json', REPORT} | own
files |= {(G / n).resolve() for n in load(E / 'snapshots.json')}
assert SELF not in files
# At the sealing instant the entire project is accounted for, with no general
# directory, basename or historical-manifest exclusions.
assert {p.resolve() for p in P.rglob('*') if p.is_file()} == {p for p in files if p.is_relative_to(P)}
manifest = {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'reviewer': '/root/ra20_final_referee2',
    'verdict': 'APPROVE: candidate packaging only',
    'base': '5830ed4fb06da0659414a3deb2a40ad327aca052',
    'file_count': len(files),
    'own_evidence_files_excluding_outer': len(own),
    'installer_bound_inputs': 1010,
    'installer_outer_manifest_itself_bound': True,
    'complete_current_project_membership_at_seal': True,
    'exact_self_exclusion': 'EVIDENCE-MANIFEST.json',
    'inventory_rule': 'All installer-bound files, its exact outer manifest, all additional actual tool inputs recorded by snapshots.json, this independent report and every own evidence file. Later separate acceptance/publication artifacts outside this evidence directory are outside this fixed seal. No nested manifest is excluded.',
    'historical_mapping': {
        'exact_original_project_path': 'README.md',
        'only_expected_sha256': '7eb951780e58ce518f0a400c90297020e7c6909ad9fd0c9c15b8036761a8bb50',
        'exact_archive_project_path': 'verification/pre-candidate-README.md'
    },
    'files': {os.path.relpath(p,E): {'sha256':sha(p), 'bytes':p.stat().st_size} for p in sorted(files)}
}
checked = verify(manifest)
with SELF.open('x') as f:
    f.write(json.dumps(manifest, indent=2) + '\n')
checked = verify()
checked.update(manifest_sha256=sha(SELF), report_sha256=sha(REPORT),
               result_sha256=sha(E/'RESULT.json'), final_sha256=sha(E/'FINAL.json'))
print(json.dumps(checked, indent=2))
