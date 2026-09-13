#!/usr/bin/env python3
"""One-time seal creation after the actual fresh compile and read-only preflight.

This is an executed evidence-authoring script, not a read-only verifier.
"""
import datetime
import hashlib
import json
from pathlib import Path

P = Path(__file__).resolve().parents[2]
E = P / 'verification/spectral-development'
OUTER = 'verification/spectral-development/EVIDENCE-MANIFEST.json'
assert not (P / OUTER).exists(), 'Do not overwrite a sealed evidence manifest.'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def read(p):
    return json.loads(p.read_text())

def write(p, value):
    p.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

validation = E / 'validation-3xi4xrva'
receipt = read(validation / 'command.json')
checks = read(validation / 'stdout.log')
assert receipt['exit'] == 0 and not (validation / 'stderr.log').read_bytes()
assert receipt['verifier_sha256'] == sha(E / 'verify_seal.py') == sha(validation / 'executed-verifier.py')
assert checks['status'] == 'KE04_SPECTRAL_CONTENT_PREFLIGHT_PASS'
attempts = ['attempt-qr384kbx', 'attempt-wzr6ev6d', 'attempt-k0z8w9ex', 'attempt-k2z1xc0b']
versions = {}
for name in attempts:
    a = E / name
    expected = read(a / 'source-before.json')['NLA/KE04/Spectral.lean']
    snapshot = a / 'inputs/NLA/KE04/Spectral.lean'
    assert sha(snapshot) == expected
    versions.setdefault(expected, []).append(str(snapshot.relative_to(P)))
source = P / 'NLA/KE04/Spectral.lean'
assert sha(source) == '64e8255697387e32e65cf591a0cb7dbf7986f471c82b4f1715c9a88a7650e20e'
final = E / attempts[-1]
audit = {'phase': 'bounded author spectral helper completion', 'checks': checks,
    'actual_preflight_command': str((validation / 'command.json').relative_to(P)),
    'actual_preflight_receipt_sha256': sha(validation / 'command.json'),
    'final_fresh_attempt': str(final.relative_to(P)),
    'final_actual_commands_sha256': sha(final / 'commands.json'),
    'final_source_snapshot_sha256': sha(final / 'inputs/NLA/KE04/Spectral.lean'),
    'final_inspector_snapshot_sha256': sha(final / 'inputs/verification/spectral-development/Inspect.lean'),
    'final_Lean_stdout_sha256': sha(final / 'compile-NLA-KE04-Spectral.stdout'),
    'final_inspection_stdout_sha256': sha(final / 'compile-Inspect.stdout'),
    'source_version_archives_by_exact_hash': versions,
    'checkpoint_preservation': {'exact_path': 'verification/spectral-development/CHECKPOINT-SEAL.json',
        'sha256': sha(E / 'CHECKPOINT-SEAL.json'), 'files': 110,
        'live_source_in_checkpoint_membership': False},
    'Linux_Comparator_execution': False, 'independent_final_mathematical_approval': False}
write(E / 'audit-result.json', audit)
report = P / 'reviews/spectral-development.md'
handoff = {'phase': 'complete assigned KE04 spectral helper implementation',
    'contributor': 'AI agent /root/ie05_statement_referee2',
    'source': {'path': 'NLA/KE04/Spectral.lean', 'sha256': sha(source)},
    'namespace': 'NLA.KE04._proved',
    'exact_frozen_contracts': {10: 'orderedSpectrum_semantics', 13: 'quadratic_semantics',
        14: 'spectral_gap_quadratic_psd', 17: 'psd_zero_form_iff_kernel'},
    'additional_API': 'quadratic_apply_eigenvector',
    'project_imports': {'NLA/KE04/Definitions.lean': sha(P / 'NLA/KE04/Definitions.lean')},
    'statement_freeze_sha256': sha(P / 'reviews/statement-freeze.json'),
    'accepted_gate_sha256': sha(P / 'verification/proof-start.json'),
    'final_fresh_attempt': str(final.relative_to(P)),
    'report_sha256': sha(report), 'audit_result_sha256': sha(E / 'audit-result.json'),
    'read_only_verifier': {'path': 'verification/spectral-development/verify_seal.py',
        'sha256': sha(E / 'verify_seal.py')},
    'exact_outer_path': OUTER,
    'scope_rule': 'Own complete module/report/evidence plus all1598 frozen inputs, freeze and gate; concurrent modules and unrelated projects are outside scope.',
    'whole_KE04_proof_complete': False, 'independent_final_mathematical_approval': False,
    'Linux_Comparator_execution': False, 'contributor_ineligible_as_independent_final_referee': True}
write(E / 'HANDOFF.json', handoff)
freeze = read(P / 'reviews/statement-freeze.json')
paths = set(freeze['files']) | {'reviews/statement-freeze.json', 'verification/proof-start.json',
    'NLA/KE04/Spectral.lean', 'reviews/spectral-development.md'}
paths |= {str(f.relative_to(P)) for f in E.rglob('*') if f.is_file()}
assert OUTER not in paths
files = {r: {'sha256': sha(P / r), 'bytes': (P / r).stat().st_size} for r in sorted(paths)}
for r, expected in freeze['files'].items():
    assert files[r]['sha256'] == expected, r
manifest = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope': handoff['scope_rule'], 'phase': handoff['phase'], 'files': files,
    'file_count': len(files), 'exact_self_exclusion': OUTER,
    'no_filename_based_hash_waivers': True,
    'historical_checkpoint_seal_preserved': True,
    'Linux_Comparator_execution': False, 'independent_final_mathematical_approval': False}
write(P / OUTER, manifest)
print(json.dumps({'outer_sha256': sha(P / OUTER), 'outer_files': len(files),
    'source_sha256': sha(source), 'report_sha256': sha(report),
    'handoff_sha256': sha(E / 'HANDOFF.json'), 'audit_result_sha256': sha(E / 'audit-result.json'),
    'read_only_verifier_sha256': sha(E / 'verify_seal.py')}, indent=2))
