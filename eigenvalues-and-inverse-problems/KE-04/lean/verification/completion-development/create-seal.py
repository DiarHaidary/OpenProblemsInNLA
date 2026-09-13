#!/usr/bin/env python3
"""One-time completion evidence seal; use verify_seal.py for read-only checks."""
from pathlib import Path
import datetime
import hashlib
import json

P = Path(__file__).resolve().parents[2]
E = P / 'verification/completion-development'
OUTER = 'verification/completion-development/EVIDENCE-MANIFEST.json'
assert not (P / OUTER).exists()

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def read(p):
    return json.loads(p.read_text())

def write(p, value):
    p.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

v = E / 'validation-tyefblp0'
receipt, checks = read(v / 'command.json'), read(v / 'stdout.log')
assert receipt['exit'] == 0 and not (v / 'stderr.log').read_bytes()
assert sha(E / 'verify_seal.py') == receipt['verifier_sha256'] == sha(v / 'executed-verifier.py')
assert checks['status'] == 'KE04_COMPLETION_PREFLIGHT_PASS'
source = P / 'NLA/KE04/Completion.lean'
assert sha(source) == '4014011a7c6435c362ce4cf304aed8d7a8ad2e32ffb03448fbf43223c59a3f97'
final = E / 'attempt-700n3s8e'
versions = {}
for name in ['attempt-c7o2c3cd', 'attempt-700n3s8e']:
    a = E / name
    expected = read(a / 'source-before.json')['NLA/KE04/Completion.lean']
    snapshot = a / 'inputs/NLA/KE04/Completion.lean'
    assert sha(snapshot) == expected == sha(source)
    versions.setdefault(expected, []).append(str(snapshot.relative_to(P)))
audit = {'phase': 'complete frozen target author assembly', 'checks': checks,
    'actual_preflight_command': str((v / 'command.json').relative_to(P)),
    'actual_preflight_command_sha256': sha(v / 'command.json'),
    'final_actual_commands_sha256': sha(final / 'commands.json'),
    'final_new_module_stdout_sha256': sha(final / 'compile-NLA-KE04-Completion.stdout'),
    'final_inspection_stdout_sha256': sha(final / 'compile-Inspect.stdout'),
    'source_version_archives_by_exact_hash': versions,
    'independent_final_mathematical_approval': False, 'Linux_Comparator_execution': False}
write(E / 'audit-result.json', audit)
binding = read(E / 'imported-helper-checks/after.json')
assert binding == read(E / 'imported-helper-checks/before.json')
assert binding['file_count'] == 3047
handoff = {'phase': 'complete exact frozen contracts22and24',
    'contributor': 'AI agent /root/ie05_statement_referee2',
    'source': {'path': 'NLA/KE04/Completion.lean', 'sha256': sha(source)},
    'namespace': 'NLA.KE04._proved',
    'exact_frozen_contracts': {22: 'strictIntervalOccupancy', 24: 'blockLanczosConjecture'},
    'additional_API': 'psd_form_nonneg',
    'explicit_project_imports': ['NLA.KE04.SpectralWindow', 'NLA.KE04.Transport',
        'NLA.KE04.Intersection', 'NLA.KE04.Nonannihilation'],
    'transitive_project_source_pins': {'NLA/KE04/' + n + '.lean': sha(P / ('NLA/KE04/' + n + '.lean'))
        for n in ['Definitions', 'Krylov', 'Frames', 'Spectral', 'SpectralWindow',
            'Transport', 'Intersection', 'Nonannihilation']},
    'preserved_imported_seals': binding['seals'],
    'statement_freeze_sha256': sha(P / 'reviews/statement-freeze.json'),
    'accepted_gate_sha256': sha(P / 'verification/proof-start.json'),
    'final_fresh_attempt': str(final.relative_to(P)),
    'complete_author_report': {'path': 'verification/completion-development/HANDOFF.md',
        'sha256': sha(E / 'HANDOFF.md')},
    'audit_result_sha256': sha(E / 'audit-result.json'),
    'read_only_verifier': {'path': 'verification/completion-development/verify_seal.py',
        'sha256': sha(E / 'verify_seal.py')},
    'exact_outer_path': OUTER,
    'scope_rule': 'Complete own Completion module/evidence plus exact unchanged3047file imported helper union; concurrent final wrappers excluded.',
    'remaining_gates': ['coordinator final24export wrappers', 'independent final mathematical reviews',
        'actual Linux/default-kernel/Comparator controls', 'publication'],
    'independent_final_mathematical_approval': False, 'Linux_Comparator_execution': False,
    'contributor_ineligible_as_independent_final_referee': True}
write(E / 'HANDOFF.json', handoff)
prior = binding['files']
for r, expected in prior.items():
    assert sha(P / r) == expected
paths = set(prior) | {'NLA/KE04/Completion.lean'}
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
