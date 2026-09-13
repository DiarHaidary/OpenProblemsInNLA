#!/usr/bin/env python3
"""Read retained Frames author evidence; write only the scoped audit result."""
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


def record(p):
    return {'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size}


def check(p, r):
    assert p.is_file() and not p.is_symlink(), str(p)
    assert record(p) == r, str(p)


assert record(P / 'reviews/statement-freeze.json')['sha256'] == '85d583c12fbbf1361cd128f7e98c359dd8990d3886ecfb9e8aed7c79793c305e'
assert record(P / 'verification/proof-start.json')['sha256'] == '5e7cfd64709f436c684698fdb0c4adb5cc3f3e50f8945aa5fffdf70ec22fe624'
F = json.loads((P / 'reviews/statement-freeze.json').read_text())
assert len(F['files']) == 1598
for rel, h in F['files'].items():
    assert record(P / rel)['sha256'] == h, rel
inventory = json.loads((P / 'verification/original-source-inventory.json').read_text())
originals = {}
for rel, h in F['source_files'].items():
    item = inventory['files'][rel]
    b = (P / rel).read_bytes()
    assert hashlib.sha256(b).hexdigest() == h == item['sha256']
    ref = item['commit'] + ':' + item['upstream_path']
    blob = subprocess.check_output(['git', '-C', GIT, 'rev-parse', ref], text=True).strip()
    assert blob == item['git_blob'] == F['source_git_blobs'][rel]
    assert subprocess.check_output(['git', '-C', GIT, 'show', ref]) == b
    originals[rel] = {'sha256': h, 'bytes': len(b), 'git_blob': blob,
        'commit': item['commit'], 'upstream_path': item['upstream_path']}
assert len(originals) == 17
selected = json.loads((E / 'latest.json').read_text())
A = E / selected['attempt']
assert record(A / 'result.json')['sha256'] == selected['result_sha256']
R = json.loads((A / 'result.json').read_text())
assert R['pass'] and R['fresh'] and R['inspect'] and R['source_unchanged']
assert len(R['commands']) == 3
assert not R['independent_review'] and not R['actual_linux_comparator']
for rel, r in R['inputs'].items():
    check(P / rel, r)
    check(A / 'source' / rel, r)
logs = {}
for c in R['commands']:
    assert c['exit_code'] == 0
    assert record(A / c['log'])['sha256'] == c['log_sha256']
    s = (A / c['log']).read_text()
    assert not re.search(r'^.*:\d+:\d+: error', s, re.M)
    logs[c['source']] = s
assert R['pins_before'] == R['pins_after'] and len(R['pins_after']) == 10
pins = {p['name']: p['rev'] for p in json.loads((P / 'lake-manifest.json').read_text())['packages']}
for pin in R['pins_after']:
    q = PACKAGES / pin['name']
    assert pin['rev'] == pins[pin['name']]
    assert subprocess.check_output(['git', '-C', str(q), 'rev-parse', 'HEAD'], text=True).strip() == pin['rev']
    assert not subprocess.check_output(['git', '-C', str(q), 'status', '--porcelain', '--untracked-files=no'], text=True)
    assert (q / '.lake/build/lib/lean').is_dir() == pin['object_directory_present']
assert sum(p['object_directory_present'] for p in R['pins_after']) == 9

X = json.loads((E / 'expected-type-extraction.json').read_text())
assert X['inspector_sha256'] == record(E / 'Inspect.lean')['sha256']
assert X['frozen_challenge_sha256'] == record(P / 'Challenge.lean')['sha256']
for name, header in X['headers'].items():
    actual_header = re.search(r'^theorem ' + name + r'\b(.*?) := by sorry$', (P / 'Challenge.lean').read_text(), re.M | re.S).group(1)
    assert actual_header == header
I = logs['verification/frames-development/Inspect.lean']
assert len(re.findall(r'^EXACT_FROZEN_TYPE ', I, re.M)) == len(X['headers']) == 5
edges = re.findall(r'^PROJECT_EDGE ([^:]+):', I, re.M)
axioms = re.findall(r'^ACTUAL_AXIOMS ([^:]+): \[([^\]]*)\]', I, re.M)
retained = re.findall(r'^RETAINED_DEPENDENCY (.+)$', I, re.M)
assert len(edges) == len(set(edges)) == len(axioms) == 38
assert set(edges) == {n for n, _ in axioms}
assert set(X['actual_roots']) <= set(edges) and len(X['actual_roots']) == 19
assert retained == X['required_dependencies'] and len(retained) == 34
assert 'PROJECT_COUNTS declarations=38, required=34' in I
for _, items in axioms:
    assert set(filter(None, items.split(', '))) <= ALLOWED
reports = {}
warnings = {}
for rel, log in logs.items():
    printed = re.findall(r"^'([^']+)' depends on axioms: \[([^\]]*)\]$", log, re.M)
    for _, items in printed:
        assert set(filter(None, items.split(', '))) == ALLOWED
    reports[rel] = len(printed)
    assert len(re.findall(r'^#assert_trust kernel ', (P / rel).read_text(), re.M)) == len(printed)
    warnings[rel] = re.findall(r'^.*:\d+:\d+: warning: (.*)$', log, re.M)
assert list(reports.values()) == [0, 8, 19]
assert not warnings['NLA/KE04/Definitions.lean'] and not warnings['NLA/KE04/Frames.lean']
assert warnings['verification/frames-development/Inspect.lean'] == [
    'Variable name `hfull` is not explicitly referenced.',
    'Variable name `hQ` is not explicitly referenced.',
    'Variable name `hA` is not explicitly referenced.',
    'Variable name `hQ` is not explicitly referenced.']
S = (P / 'NLA/KE04/Frames.lean').read_text()
assert record(P / 'NLA/KE04/Frames.lean')['sha256'] == 'bfea6b02091db4e999c2c870b4b1f238cb546ad84df010c7d5431fe82904db0b'
code = re.sub(r'/\-.*?\-/', '', S, flags=re.S)
code = re.sub(r'--[^\n]*', '', code)
assert not re.search(r'\b(sorry|admit|axiom|native_decide|unsafe|partial)\b', code)
assert not re.search(r'^import .*Challenge', code, re.M)
assert re.findall(r'^import NLA\.(.+)$', code, re.M) == ['KE04.Definitions']
assert len(re.findall(r'^theorem ', code, re.M)) == 19
api = json.loads((E / 'api-source-manifest.json').read_text())
for rel, item in api['files'].items():
    check(P / rel, {k: item[k] for k in ['sha256', 'bytes']})
    q = PACKAGES / item['package']
    assert (q / item['upstream_path']).read_bytes() == (P / rel).read_bytes()
    assert subprocess.check_output(['git', '-C', str(q), 'cat-file', 'blob', item['git_blob']]) == (P / rel).read_bytes()
attempts = {}
for a in sorted(E.glob('attempt-*')):
    r = json.loads((a / 'result.json').read_text())
    assert r['fresh'] and r['own_object_cleanup']['removed'] and not Path(r['prefix']).exists()
    assert r['pins_before'] == r['pins_after'] == R['pins_after']
    assert r['frozen_inputs_before'] == r['frozen_inputs_after'] == 1598
    for rel, item in r['inputs'].items():
        check(a / 'source' / rel, item)
    for c in r['commands']:
        assert record(a / c['log'])['sha256'] == c['log_sha256']
    attempts[a.name] = {'pass': r['pass'], 'result': record(a / 'result.json'),
        'commands': [{'source': c['source'], 'exit_code': c['exit_code']} for c in r['commands']],
        'removed_own_objects': len(r['own_object_cleanup']['objects']),
        'removed_logical_bytes': sum(o['bytes'] for o in r['own_object_cleanup']['objects'].values())}
assert len(attempts) == 3
out = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'pass': True,
    'scope': 'KE04 Frames author helper validation; concurrent Krylov/Spectral and full proof excluded',
    'source': record(P / 'NLA/KE04/Frames.lean'), 'selected_attempt': A.name,
    'selected_result': record(A / 'result.json'), 'platform': R['platform'], 'toolchain': R['toolchain'],
    'fresh_commands': 3, 'total_seconds': sum(c['seconds'] for c in R['commands']),
    'exact_contracts': list(X['headers']), 'actual_roots': X['actual_roots'],
    'actual_project_declarations': len(edges), 'retained_dependencies': retained,
    'kernel_assertions': sum(reports.values()), 'standard_three_reports': reports,
    'warnings': warnings, 'preserved_statement_inputs': len(F['files']), 'originals': originals,
    'clean_pins': R['pins_after'], 'readonly_object_directories': 9,
    'primary_API_sources': api['files'], 'attempts': attempts,
    'independent_review': False, 'actual_linux_comparator': False,
    'proof_status_metadata_git_canonical_changes': False}
(E / 'audit-result.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({k: out[k] for k in ['pass', 'fresh_commands', 'total_seconds',
    'actual_project_declarations', 'kernel_assertions', 'preserved_statement_inputs']}))
