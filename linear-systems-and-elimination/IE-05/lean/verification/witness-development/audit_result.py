#!/usr/bin/env python3
"""Audit retained Witness author checks; write only this scope's result JSON."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess

E = Path(__file__).resolve().parent
P = E.parents[1]
PACKAGES = Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
GIT = '/tmp/nla-lean-ra20-worktree'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def record(p):
    return {'sha256': sha(p), 'bytes': p.stat().st_size}


def checked_record(p, r):
    assert p.is_file() and not p.is_symlink(), str(p)
    assert record(p) == r, str(p)


freeze_path = P / 'reviews/statement-freeze.json'
assert sha(freeze_path) == 'bd329885eb323bd4f3fd40879649b56c201918d8c2bd6f63fbd0e86f48ca770c'
F = json.loads(freeze_path.read_text())
assert len(F['files']) == 733
for rel, h in F['files'].items():
    assert sha(P / rel) == h, rel
originals = {}
for rel, h in F['source_files'].items():
    b = (P / F['source_snapshot_directory'] / rel).read_bytes()
    assert hashlib.sha256(b).hexdigest() == h, rel
    ref = F['base'] + ':' + rel
    blob = subprocess.check_output(['git', '-C', GIT, 'rev-parse', ref], text=True).strip()
    assert blob == F['source_git_blobs'][rel], rel
    assert subprocess.check_output(['git', '-C', GIT, 'show', ref]) == b, rel
    originals[rel] = {'sha256': h, 'git_blob': blob, 'bytes': len(b)}
assert len(originals) == 27
gate = P / 'verification/proof-start.json'
assert sha(gate) == '2a8e4b4029a6ba005856c9ec56178cc7fefc8b8b16e945df27599ce471c95726'
ownership = json.loads((E / 'gate-and-ownership.json').read_text())
for rel, h in ownership['immutable_imports'].items():
    assert sha(P / rel) == h, rel

selected = json.loads((E / 'latest.json').read_text())
A = E / selected['attempt']
assert sha(A / 'result.json') == selected['result_sha256']
R = json.loads((A / 'result.json').read_text())
assert R['pass'] and R['fresh'] and R['inspect'] and R['source_unchanged']
assert not R['independent_review'] and not R['actual_linux_comparator']
assert len(R['commands']) == 9 and not R['reused_own_immutable_dependency_objects']
assert R['immutable_imports'] == ownership['immutable_imports']
assert R['frozen_inputs_before'] == R['frozen_inputs_after'] == 733
for rel, r in R['inputs'].items():
    checked_record(P / rel, r)
    checked_record(A / 'source' / rel, r)
logs = {}
for c in R['commands']:
    assert c['exit_code'] == 0
    assert sha(A / c['log']) == c['log_sha256']
    s = (A / c['log']).read_text()
    assert not re.search(r'^.*:\d+:\d+: (?:error|warning):', s, re.M)
    logs[c['source']] = s

assert R['pins_before'] == R['pins_after'] and len(R['pins_after']) == 10
manifest = json.loads((P / 'lake-manifest.json').read_text())
expected_pins = {v['name']: v['rev'] for v in manifest['packages']}
for pin in R['pins_after']:
    q = PACKAGES / pin['name']
    assert pin['rev'] == expected_pins[pin['name']]
    assert subprocess.check_output(['git', '-C', str(q), 'rev-parse', 'HEAD'], text=True).strip() == pin['rev']
    assert not subprocess.check_output(['git', '-C', str(q), 'status', '--porcelain', '--untracked-files=no'], text=True)
    assert (q / '.lake/build/lib/lean').is_dir() == pin['object_directory_present']
assert sum(p['object_directory_present'] for p in R['pins_after']) == 9

I = logs['verification/witness-development/Inspect.lean']
X = json.loads((E / 'expected-type-extraction.json').read_text())
assert X['inspector_sha256'] == sha(E / 'Inspect.lean')
assert X['frozen_challenge_sha256'] == sha(P / 'Challenge.lean')
for name, header in X['headers'].items():
    match = re.search(r'^theorem ' + re.escape(name) + r'\b(.*?) := by sorry$', (P / 'Challenge.lean').read_text(), re.M | re.S)
    assert match and match.group(1) == header, name
assert len(X['headers']) == len(re.findall(r'^EXACT_FROZEN_TYPE ', I, re.M)) == 2
assert len(X['actual_roots']) == 15
edges = re.findall(r'^PROJECT_EDGE ([^:]+):', I, re.M)
axioms = re.findall(r'^ACTUAL_AXIOMS ([^:]+): \[([^\]]*)\]', I, re.M)
retained = re.findall(r'^RETAINED_DEPENDENCY (.+)$', I, re.M)
assert len(edges) == len(set(edges)) == len(axioms) == 93
assert set(edges) == {n for n, _ in axioms}
assert set(X['actual_roots']) <= set(edges)
assert retained == X['required_dependencies'] and len(retained) == 56
assert 'PROJECT_COUNTS declarations=93, required=56' in I
for _, items in axioms:
    assert set(filter(None, items.split(', '))) <= ALLOWED
reports = {}
kernel_checks = {}
for rel, log in logs.items():
    printed = re.findall(r"^'([^']+)' depends on axioms: \[([^\]]*)\]$", log, re.M)
    for _, items in printed:
        assert set(filter(None, items.split(', '))) == ALLOWED
    reports[rel] = len(printed)
    source = (P / rel).read_text()
    kernel_checks[rel] = len(re.findall(r'^#assert_trust kernel ', source, re.M))
assert list(reports.values()) == [0, 1, 15, 1, 5, 9, 3, 11, 15]
assert reports == kernel_checks and sum(reports.values()) == 60
S = (P / 'NLA/IE05/Witness.lean').read_text()
assert sha(P / 'NLA/IE05/Witness.lean') == '4fa2cfeef00d80f28475bf221082a786f2b035f1e77e47b1bfd70bc13f2e57b6'
code = re.sub(r'/\-.*?\-/', '', S, flags=re.S)
code = re.sub(r'--[^\n]*', '', code)
assert not re.search(r'\b(sorry|admit|axiom|native_decide|unsafe|partial)\b', code)
assert not re.search(r'^import .*Challenge', code, re.M)
assert len(re.findall(r'^theorem ', code, re.M)) == 15

prior = []
prior_manifests = [
    ('gepp-development', P, 150, 'f3854e99028561510756f6c58d024841d2e8cab4ce8d9315d45ac4b25eebd0d1'),
    ('lu-development', P, 68, '9333e7615283fa9067b571a60f22488c884c435444d0f7a9221d8090ec5412a2'),
    ('qr-scaling-handoff', P / 'verification/qr-scaling-handoff', 847, 'b328744f06c3af7d3ae119ba28dc6d5a078ed79675d3e89fe888b6000c2f58c6'),
    ('exactcert-diagnostic-referee', P, 54, '74d46f48c5d0a3b70da7925065b3a7c34fd7306d7a46120aee8a750bc8442420'),
]
for name, base, count, digest in prior_manifests:
    path = P / 'verification' / name / 'EVIDENCE-MANIFEST.json'
    assert sha(path) == digest
    M = json.loads(path.read_text())
    assert len(M['files']) == count
    for rel, r in M['files'].items():
        checked_record(base / rel, r)
    prior.append({'manifest': str(path.relative_to(P)), **record(path), 'verified_bound_files': count})

attempts = {}
prefixes = set()
for a in sorted(E.glob('attempt-*')):
    r = json.loads((a / 'result.json').read_text())
    prefixes.add(r['prefix'])
    for rel, input_record in r['inputs'].items():
        checked_record(a / 'source' / rel, input_record)
    for c in r['commands']:
        assert sha(a / c['log']) == c['log_sha256']
    assert r['pins_before'] == r['pins_after'] == R['pins_after']
    assert r['immutable_imports'] == R['immutable_imports']
    assert r['frozen_inputs_before'] == r['frozen_inputs_after'] == 733
    attempts[a.name] = {'pass': r['pass'], 'result': record(a / 'result.json'),
        'commands': [{'source': c['source'], 'exit_code': c['exit_code']} for c in r['commands']],
        'reused_own_immutable_dependency_objects': len(r['reused_own_immutable_dependency_objects'])}
assert len(attempts) == 5
cleanup = [R['prior_own_prefix_cleanup'], R['own_prefix_cleanup']]
assert {c['prefix'] for c in cleanup} == prefixes
for c in cleanup:
    assert c['removed'] and not Path(c['prefix']).exists()
    assert all(rel.endswith(('.olean', '.ilean')) for rel in c['objects'])
assert R['own_generated_objects_before_exit'] == R['own_prefix_cleanup']['objects']
assert json.loads((E / 'development-state.json').read_text()) == {}
assert [len(c['objects']) for c in cleanup] == [16, 18]

out = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'pass': True,
    'scope': 'IE05 Witness scoped author validation; excludes concurrent Growth/GrowthBounds and complete-project claims',
    'source': record(P / 'NLA/IE05/Witness.lean'), 'selected_attempt': A.name,
    'selected_result': record(A / 'result.json'), 'platform': R['platform'], 'toolchain': R['toolchain'],
    'fresh_source_commands': len(R['commands']), 'total_seconds': sum(c['seconds'] for c in R['commands']),
    'exact_contracts': list(X['headers']), 'explicit_witness_roots': X['actual_roots'],
    'safe_actual_project_declarations': len(edges), 'material_dependencies': retained,
    'kernel_assertions': sum(kernel_checks.values()), 'standard_three_reports': reports,
    'warnings': 0, 'preserved_statement_files': len(F['files']), 'originals': originals,
    'immutable_imports': R['immutable_imports'], 'prior_complete_handoffs': prior,
    'clean_pins': R['pins_after'], 'dependency_object_directories': 9, 'attempts': attempts,
    'own_object_cleanup': [{'prefix': c['prefix'], 'objects': len(c['objects']),
        'logical_bytes': sum(v['bytes'] for v in c['objects'].values()), 'removed': True} for c in cleanup],
    'independent_review': False, 'actual_linux_comparator': False,
    'canonical_status_or_git_changes': False}
(E / 'audit-result.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({k: out[k] for k in ['pass', 'selected_attempt', 'fresh_source_commands', 'total_seconds',
    'safe_actual_project_declarations', 'kernel_assertions', 'warnings', 'preserved_statement_files']}))
