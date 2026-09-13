#!/usr/bin/env python3
"""One-time author evidence seal; use verify_seal.py for read-only verification."""
from pathlib import Path
import datetime
import hashlib
import json

P = Path(__file__).resolve().parents[2]
E = P / 'verification/spectral-window-development'
OUTER = 'verification/spectral-window-development/EVIDENCE-MANIFEST.json'
assert not (P / OUTER).exists()

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def read(p):
    return json.loads(p.read_text())

def write(p, value):
    p.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

v = E / 'validation-i82h7cu_'
receipt, checks = read(v / 'command.json'), read(v / 'stdout.log')
assert receipt['exit'] == 0 and not (v / 'stderr.log').read_bytes()
assert sha(E / 'verify_seal.py') == receipt['verifier_sha256'] == sha(v / 'executed-verifier.py')
assert checks['status'] == 'KE04_SPECTRAL_WINDOW_PREFLIGHT_PASS'
source = P / 'NLA/KE04/SpectralWindow.lean'
assert sha(source) == 'c59a80ed6a6dff4e879fb6b8ca602a1d0946ef29b61ff400ffba0122bc86760f'
final = E / 'attempt-zq1v44eo'
versions = {}
for name in ['attempt-cmujju9q', 'attempt-k3h_4ob1', 'attempt-5sd34slq', 'attempt-zq1v44eo']:
    a = E / name
    expected = read(a / 'source-before.json')['NLA/KE04/SpectralWindow.lean']
    snapshot = a / 'inputs/NLA/KE04/SpectralWindow.lean'
    assert sha(snapshot) == expected
    versions.setdefault(expected, []).append(str(snapshot.relative_to(P)))
audit = {'phase': 'bounded author proof completion', 'checks': checks,
    'actual_preflight_command': str((v / 'command.json').relative_to(P)),
    'actual_preflight_command_sha256': sha(v / 'command.json'),
    'final_actual_commands_sha256': sha(final / 'commands.json'),
    'final_new_module_stdout_sha256': sha(final / 'compile-NLA-KE04-SpectralWindow.stdout'),
    'final_inspection_stdout_sha256': sha(final / 'compile-Inspect.stdout'),
    'source_version_archives_by_exact_hash': versions,
    'independent_final_mathematical_approval': False, 'Linux_Comparator_execution': False}
write(E / 'audit-result.json', audit)
prior_seals = read(final / 'imported-after.json')['seals']
handoff = {'phase': 'complete assigned contracts11and15',
    'contributor': 'AI agent /root/ie05_statement_referee2',
    'source': {'path': 'NLA/KE04/SpectralWindow.lean', 'sha256': sha(source)},
    'namespace': 'NLA.KE04._proved',
    'exact_frozen_contracts': {11: 'compression_basis_independent', 15: 'spectral_window_subspace'},
    'additional_API': 'orthonormal_span_form_nonpos',
    'project_imports': {r: sha(P / r) for r in ['NLA/KE04/Frames.lean', 'NLA/KE04/Spectral.lean']},
    'preserved_imported_seals': prior_seals,
    'statement_freeze_sha256': sha(P / 'reviews/statement-freeze.json'),
    'accepted_gate_sha256': sha(P / 'verification/proof-start.json'),
    'final_fresh_attempt': str(final.relative_to(P)),
    'complete_author_report': {'path': 'verification/spectral-window-development/HANDOFF.md',
        'sha256': sha(E / 'HANDOFF.md')},
    'audit_result_sha256': sha(E / 'audit-result.json'),
    'read_only_verifier': {'path': 'verification/spectral-window-development/verify_seal.py',
        'sha256': sha(E / 'verify_seal.py')},
    'exact_outer_path': OUTER,
    'scope_rule': 'Complete own source/evidence and explicit unchanged2245file imported seal union; concurrent project modules excluded.',
    'whole_KE04_proof_complete': False, 'independent_final_mathematical_approval': False,
    'Linux_Comparator_execution': False, 'contributor_ineligible_as_independent_final_referee': True}
write(E / 'HANDOFF.json', handoff)
prior = {}
for seal, expected in prior_seals.items():
    assert sha(P / seal) == expected
    prior[seal] = expected
    for r, d in read(P / seal)['files'].items():
        assert sha(P / r) == d['sha256']
        if r in prior:
            assert prior[r] == d['sha256']
        prior[r] = d['sha256']
assert len(prior) == 2245
paths = set(prior) | {'NLA/KE04/SpectralWindow.lean'}
paths |= {str(f.relative_to(P)) for f in E.rglob('*') if f.is_file()}
assert OUTER not in paths
files = {r: {'sha256': sha(P / r), 'bytes': (P / r).stat().st_size} for r in sorted(paths)}
write(P / OUTER, {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope': handoff['scope_rule'], 'phase': handoff['phase'], 'files': files,
    'file_count': len(files), 'exact_self_exclusion': OUTER,
    'no_filename_based_hash_waivers': True, 'all_historical_seals_preserved': True,
    'independent_final_mathematical_approval': False, 'Linux_Comparator_execution': False})
print(json.dumps({'outer_sha256': sha(P / OUTER), 'outer_files': len(files),
    'source_sha256': sha(source), 'report_sha256': sha(E / 'HANDOFF.md'),
    'handoff_sha256': sha(E / 'HANDOFF.json'), 'audit_result_sha256': sha(E / 'audit-result.json'),
    'read_only_verifier_sha256': sha(E / 'verify_seal.py')}, indent=2))
