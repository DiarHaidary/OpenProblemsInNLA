from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, subprocess

P = Path('/tmp/nla-lean-formalization/next-ie05-statements-draft/lean').resolve()
R = Path('/tmp/nla-lean-ra20-worktree')
ER = P / 'verification/final-review-root-acceptance'
E = ER / 'attempt-success'
G = P / 'verification/final-review-acceptance.json'
assert not E.exists() and not G.exists(), 'One-shot acceptance'
E.mkdir()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
load = lambda p: json.loads(p.read_text())
def save(p, x):
    p.write_text(json.dumps(x, indent=2) + '\n')

F = load(P / 'reviews/proof-freeze.json')
assert sha(P / 'reviews/proof-freeze.json') == '72d9a694d6c337937c6edd28ee632dc4a92464ac2dc7ba58ef98f5322405f251'
assert len(F['files']) == 1800 and len(F['source_files']) == 27
for rel, h in F['files'].items():
    q = P / rel
    assert q.is_file() and not q.is_symlink() and sha(q) == h, rel
    assert q.stat().st_size == F['file_sizes'][rel], rel
S = load(P / 'reviews/statement-freeze.json')
assert len(S['files']) == 733
for rel, h in S['files'].items():
    assert sha(P / rel) == h, rel
names = load(P / 'comparator.json')['theorem_names']
assert len(names) == 17
allowed = {'propext', 'Classical.choice', 'Quot.sound'}
reviews = []
for number, rh, mh, count in [
    (1, 'b17e5dc6ab73098183d1ecbe357d6aea51c0242d60c741dbfebdcf707c6eb828',
     '7c2d9cd5abfadf5cc6833b2e337e00be42f73f440678864c521c3a2151073d07', 2116),
    (2, '74b8ed57fc1a7594ba47f98b1cbce63a58bb515109fb4dd2dc033115c3aa23cb',
     'dea47f4f1e04bf12abf99b7b96e9abe5f0be57cb897253e3540105715dcde02d', 2010)]:
    report = P / f'reviews/final-referee-{number}.md'
    own = P / f'reviews/final-referee-{number}-evidence'
    outer = own / 'EVIDENCE-MANIFEST.json'
    assert sha(report) == rh and sha(outer) == mh
    m = load(outer)
    assert m['verdict'] == 'APPROVE'
    assert m['exact_self_exclusion'] == str(outer.relative_to(P))
    expected = set(F['files']) | {'reviews/proof-freeze.json', str(report.relative_to(P))}
    expected |= {str(q.relative_to(P)) for q in own.rglob('*') if q.is_file() and q != outer}
    assert set(m['files']) == expected and len(expected) == count
    for rel, r in m['files'].items():
        q = P / rel
        assert q.is_file() and not q.is_symlink() and sha(q) == r['sha256'], rel
        assert q.stat().st_size == r['bytes'], rel
    reviews.append({'number': number, 'report_sha256': rh, 'evidence_sha256': mh,
                    'bound_files': count, 'verdict': 'APPROVE'})

# Recheck the actual original Git objects in one batch, retaining the raw receipt.
keys = [F['base'] + ':' + rel for rel in F['source_files']]
cmd = ['git', 'cat-file', '--batch']
cp = subprocess.run(cmd, input=('\n'.join(keys) + '\n').encode(), cwd=R,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(E / 'original-git-batch.stdout').write_bytes(cp.stdout)
(E / 'original-git-batch.stderr').write_bytes(cp.stderr)
assert cp.returncode == 0 and not cp.stderr
pos = 0
originals = []
for rel, h in F['source_files'].items():
    stop = cp.stdout.index(b'\n', pos)
    oid, kind, size = cp.stdout[pos:stop].decode().split()
    assert kind == 'blob' and oid == F['source_git_blobs'][rel]
    pos = stop + 1
    data = cp.stdout[pos:pos + int(size)]
    assert hashlib.sha256(data).hexdigest() == h
    assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == oid
    assert (P / F['source_snapshot_directory'] / rel).read_bytes() == data
    pos += int(size)
    assert cp.stdout[pos:pos + 1] == b'\n'
    pos += 1
    originals.append({'path': rel, 'git_blob': oid, 'sha256': h, 'bytes': len(data)})
assert pos == len(cp.stdout)
save(E / 'original-git-command.json', {'command': cmd, 'cwd': str(R), 'input_keys': keys,
    'exit_code': 0, 'stdout_sha256': sha(E / 'original-git-batch.stdout'),
    'stderr_sha256': sha(E / 'original-git-batch.stderr'), 'matched_objects': originals})

# Independently walk the actual elaborated graph, rather than accept its summary.
e1 = P / 'reviews/final-referee-1-evidence'
env = load(e1 / 'inspection-001/run-003/actual-environment.json')
assert sha(e1 / 'inspection-001/run-003/actual-environment.json') == '39a0333759ecdd13f23fabd51312e98c7e2fab6c565dc14660b440c8d60248eb'
assert env['status'] == 'PASS' and env['contract_count'] == 17
assert [r['name'] for r in env['contracts']] == names
assert all(r['definitional_equality'] for r in env['contracts'])
graph = {r['name']: r for r in env['transitive_graph']}
assert len(graph) == env['transitive_count'] == 29597
assert len(env['source_seed_names']) == 157
assert all(not r['unsafe'] and not r['partial'] for r in graph.values())
assert all(r['name'] in allowed for r in graph.values() if r['kind'] == 'axiom')
for r in graph.values():
    assert set(r['type_references']) | set(r['body_references']) <= set(r['all_references'])
    assert set(r['all_references']) <= graph.keys()
todo = list(names)
seen = set()
while todo:
    name = todo.pop()
    if name in seen:
        continue
    seen.add(name)
    todo.extend(graph[name]['all_references'])
project = {n for n in seen if graph[n]['module'].startswith('NLA.IE05.')}
assert len(seen) == 29594 and len(project) == 181
assert env['project_declaration_count'] == 184
audit = load(e1 / 'audit-result.json')
assert audit['status'] == 'PASS' and len(audit['material_body_paths']) == 26
for p in audit['material_body_paths']:
    path = p['body_path']
    assert path[0] == p['from'] and path[-1] == p['to']
    for u, v in zip(path, path[1:]):
        assert v in graph[u]['body_references'], (u, v)
assert len(audit['source_kernel_assertions']) == 89
assert audit['additional_inspector_kernel_assertions'] == names
assert audit['total_executed_kernel_assertions_final_success'] == 106
commands1 = []
for d in sorted((e1 / 'attempt-001/commands').iterdir()):
    if not d.is_dir():
        continue
    c, r = load(d / 'command.json'), load(d / 'result.json')
    assert r['exit_code'] == 0
    for stream in ['stdout', 'stderr']:
        assert sha(d / stream) == r[stream + '_sha256']
    source = Path(c['argv'][-1]).resolve()
    assert source.is_relative_to(P) and sha(source) == F['files'][str(source.relative_to(P))]
    commands1.append({'source': str(source.relative_to(P)), 'exit_code': 0,
                      'stdout_sha256': r['stdout_sha256']})
assert len(commands1) == 13
assert load(e1 / 'inspection-001/run-003/result.json')['status'] == 'PASS'

# Recheck referee 2's successful raw source commands and actual inspected counts.
e2 = P / 'reviews/final-referee-2-evidence'
v2 = load(e2 / 'successful-build-validation/result.json')
assert v2['success'] and not v2['errors']
assert v2['Lean_commands'] == 14 and v2['exact_types'] == 17
r2 = load(e2 / 'attempt-gxrxb23r/result.json')
commands2 = [r for r in r2['commands'] if '-o' in r['command']]
assert len(commands2) == 14
axcount = 0
for r in commands2:
    assert r['exit_code'] == 0
    for stream in ['stdout', 'stderr']:
        assert sha(e2 / 'attempt-gxrxb23r' / r[stream]) == r[stream + '_sha256']
    text = (e2 / 'attempt-gxrxb23r' / r['stdout']).read_text()
    for _, axs in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", text):
        assert {s.strip() for s in axs.split(',') if s.strip()} <= allowed
        axcount += 1
    module = r['command'][-1]
    if module != 'Inspect.lean':
        assert sha(e2 / 'attempt-gxrxb23r/source' / module) == F['files'][module]
assert axcount == 106
inspect_command = next(r for r in commands2 if r['command'][-1] == 'Inspect.lean')
il = (e2 / 'attempt-gxrxb23r' / inspect_command['stdout']).read_text()
assert re.findall(r'^EXACT_TYPE (\S+):', il, re.M) == names
assert 'AUDIT_COMPLETE FINAL roots=1 closure=152 required=27' in il
assert 'AUDIT_COMPLETE ALL roots=17 closure=181 required=3' in il

gate = {'utc': datetime.now(timezone.utc).isoformat(),
    'gate': 'ACCEPT both independent final mathematical approvals; candidate packaging and actual Linux verification may proceed',
    'coordinator': '/root', 'coordinator_role': 'Proof contributor; not an independent final referee',
    'proof_freeze_sha256': sha(P / 'reviews/proof-freeze.json'),
    'statement_freeze_sha256': sha(P / 'reviews/statement-freeze.json'),
    'proof_inputs_preserved': 1800, 'statement_inputs_preserved': 733,
    'original_git_objects_preserved': 27, 'reviews': reviews,
    'configured_complete_target_exports': names,
    'root_review': 'Read both complete reports, actual independent inspectors, read-only seal logic, referee2 successful-build classifier, and actual full-target mathematical proof from the author assembly. Rehashed both exact referee scopes including every historical nested manifest and diagnostic; rechecked original Git objects, actual successful source/log bindings, exact type records and standard-three axiom reports. Independently traversed referee1 actual full dependency graph and all26 material body paths. No new Lean compilation is claimed by this gate.',
    'referee1_actual_source_commands': commands1,
    'referee1_export_closure': {'project': 181, 'all_declarations': 29594},
    'referee1_all_literal_source_closure': {'literal_sources': 157, 'project': 184, 'all_declarations': 29597},
    'referee2_actual_source_commands': 14, 'referee2_all_export_closure': 181,
    'referee2_final_closure': 152, 'referee2_final_material_dependencies': 27,
    'each_referee_explicit_kernel_assertions': 106,
    'scope': 'Negation of the complete original orthogonal GEPP growth extremizer conjecture at n=8 using its actual positive-diagonal Euclidean QR candidate, all admissible pivot paths, first-row tie convention and genuine bounded nonempty real supremum. Reduced64+204 integer obligations prove the required strict gap.',
    'independent_referees_requested_no_math_revision': True,
    'remaining': ['Explicit archive-aware live README/correspondence and Solution-default package',
                  'Truthful v0.4 formalization.yaml and independent candidate audit',
                  'Actual Ubuntu default-kernel and Comparator with real negative controls',
                  'Independent operational acceptance and reviewed canonical publication with an individual upstream main PR'],
    'canonical_status': 'Solved, unchanged', 'actual_linux_comparator': 'pending',
    'whole_problem_verified': False, 'count_increment_authorized': False}
(E / 'accept_ie05_final_reviews.py').write_bytes(Path(__file__).read_bytes())
save(G, gate)
inputs = [q for q in ER.rglob('*') if q.is_file()] + [G]
outer = ER / 'EVIDENCE-MANIFEST.json'
save(outer, {'exact_self_exclusion': str(outer.relative_to(P)),
    'scope': 'Coordinator final mathematical acceptance receipts only; both independent evidence seals remain unchanged',
    'files': {str(q.relative_to(P)): {'sha256': sha(q), 'bytes': q.stat().st_size} for q in inputs}})
print(json.dumps({'gate_sha256': sha(G), 'root_evidence_sha256': sha(outer),
    'proof_files': 1800, 'original_git_objects': 27, 'reviews': reviews}))
