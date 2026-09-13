"""Seal the complete author proof before independent final mathematical review.

One-shot coordinator receipt; never mutates a mathematical source or prior seal.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, re, subprocess, sys, tempfile

P = Path('/tmp/nla-lean-formalization/next-ke04-statements-draft/lean').resolve()
O = P / 'verification/assembly-handoff'
F = P / 'reviews/proof-freeze.json'
A = P / 'verification/assembly-development/attempt-zus_4k08'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ident = lambda p: {'sha256': sha(p), 'bytes': p.stat().st_size}
load = lambda p: json.loads(p.read_text())
def save(p, data): p.write_text(json.dumps(data, indent=2) + '\n')
def inventory(root):
    out = {}
    for q in sorted(root.rglob('*')):
        assert not q.is_symlink(), str(q)
        if q.is_file(): out[str(q.relative_to(root))] = ident(q)
    return out

assert not O.exists() and not F.exists(), 'One-shot freeze already exists'
assert not any(q.name.startswith('final-referee-') for q in (P / 'reviews').iterdir())
anchors = {
    'reviews/statement-freeze.json': '85d583c12fbbf1361cd128f7e98c359dd8990d3886ecfb9e8aed7c79793c305e',
    'verification/proof-start.json': '5e7cfd64709f436c684698fdb0c4adb5cc3f3e50f8945aa5fffdf70ec22fe624',
    'NLA/KE04/Definitions.lean': 'ae1baccc0cb622f83103eff8bb4a5efe4cd9a3bae4822ccca38da29554ae9ca4',
    'Challenge.lean': 'a27de227d483072e395b6658a97cbf31296503c7fab36e5f9dbf248b2efa299e',
    'NLA/KE04/Proof.lean': 'f3920f297fdd8de840e88cad46322ce69ddcfd106b6dec51dd92fc386ccc76da',
    'Solution.lean': '4bd85171d2284ab4ef1bcb914d1eae2763d3e5f6a279b120aec2709b0628bf13',
    'verification/krylov-root-development/EVIDENCE-MANIFEST.json': 'd0077d6e4f751a13404ebee91f60a2c9965ad22e5030983e66412746acb69407',
    'verification/frames-development/EVIDENCE-MANIFEST.json': '73770debb7678e443032c5f30e77ef82365cd32b81d24bba161990e2ac7f8db8',
    'verification/spectral-development/EVIDENCE-MANIFEST.json': '27a8328c569a17db1e6cf671a0a79034e3ce9eb2dc85c4640d13be7624191ca2',
    'verification/spectral-window-development/EVIDENCE-MANIFEST.json': '2fecf0e58267ebab396ccc9a4691fb1e41a751fe6e23e98c89a2842af01a269c',
    'verification/transport-intersection-handoff/EVIDENCE-MANIFEST.json': 'b3232d8adb072dc44447a2a1f6f806f709bc55b4201b85d680d557645d9d72e8',
    'verification/nonannihilation-development/EVIDENCE-MANIFEST.json': 'd57bb205a29e51eefa1e1d67f662f052875a58961c750f6930028408251def68',
    'verification/completion-development/EVIDENCE-MANIFEST.json': 'bc6e2192403d72e8a136acbd6bef181633668beaaabecf6c9acf67a3ec272ca5',
}
for n, h in anchors.items(): assert sha(P/n) == h, n
initial = inventory(P)
old = load(P/'reviews/statement-freeze.json')
assert len(old['files']) == 1598
for n, h in old['files'].items():
    assert sha(P/n) == h and (P/n).stat().st_size == old['file_sizes'][n], n
R = Path(tempfile.mkdtemp(prefix='ke04-root-proof-freeze-', dir='/tmp/nla-lean-formalization')).resolve()
(R/'executed-freeze.py').write_bytes(Path(__file__).read_bytes())
commands = []
def run(label, argv, inp=None):
    c = subprocess.run(argv, cwd=P, input=inp,
        env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0'),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    row = {'label': label, 'argv': argv, 'cwd': str(P), 'exit_code': c.returncode}
    for s in ['stdout', 'stderr']:
        q = R/(label+'.'+s); q.write_bytes(getattr(c, s)); row[s+'_sha256'] = sha(q)
    if inp is not None:
        (R/(label+'.stdin')).write_bytes(inp); row['stdin_sha256'] = sha(R/(label+'.stdin'))
    commands.append(row); save(R/'commands.json', commands)
    assert c.returncode == 0, (label, str(R))
    return c.stdout

helper_checks = [
    ('krylov', 'krylov-root-development/verify_seal.py', []),
    ('frames', 'frames-development/verify_seal.py', []),
    ('spectral', 'spectral-development/verify_seal.py', []),
    ('spectral-window', 'spectral-window-development/verify_seal.py', []),
    ('transport-intersection', 'transport-intersection-handoff/verify_seal.py', []),
    ('nonannihilation', 'nonannihilation-development/seal.py', ['--verify']),
    ('completion', 'completion-development/verify_seal.py', []),
]
for label, rel, args in helper_checks:
    run(label+'-read-only-seal', [sys.executable, '-B', str(P/'verification'/rel), *args])
original = load(P/'verification/original-source-inventory.json')
rows = list(original['files'].items()); assert len(rows) == 17
query = ''.join(r['commit']+':'+r['upstream_path']+'\n' for _, r in rows).encode()
raw = run('original-17-git-blobs', ['git', '-C', '/tmp/nla-lean-ra20-worktree', 'cat-file', '--batch'], query)
pos = 0
for path, r in rows:
    end = raw.index(b'\n', pos); obj, kind, ns = raw[pos:end].decode().split(); size = int(ns)
    data = raw[end+1:end+1+size]; pos = end+2+size
    assert kind == 'blob' and obj == r['git_blob'] and raw[pos-1:pos] == b'\n'
    assert data == (P/path).read_bytes() and ident(P/path) == {k:r[k] for k in ['sha256', 'bytes']}, path
assert pos == len(raw)

d = load(A/'result.json')
assert d['success'] and not d['errors'] and d['final_requested'] and d['fresh_empty_prefix']
assert d['own_prefix_removed'] and not Path(d['private_prefix']).exists()
assert len(d['objects']) == 12 and len(d['commands']) == 13
assert d['before_dependencies'] == d['after_dependencies'] and len(d['before_dependencies']) == 10
for stage in ['before_dependencies', 'after_dependencies']:
    for r in d[stage]:
        assert len(r['checks']) == 2
        assert all(c['exit_code'] == 0 and not c['stderr'] for c in r['checks'])
        assert r['checks'][0]['stdout'].strip() == r['expected_revision']
        assert r['checks'][1]['stdout'] == ''
for n, r in d['inputs'].items():
    assert ident(A/'source'/n) == r, n
    if n != 'Inspect.lean': assert ident(P/n) == r, n
logs = []
for c in d['commands']:
    assert c['exit_code'] == 0
    for s in ['stdout', 'stderr']: assert sha(A/c[s]) == c[s+'_sha256']
    logs.append((A/c['stdout']).read_text())
assert d['final_inspection_counts'] == ['24', '147', '37']
configured = load(P/'comparator.json')['theorem_names']; assert len(configured) == 24
log = (A/'Inspect.stdout').read_text()
assert re.findall(r'EXACT_CONTRACT (\S+):', log) == configured
assert 'FINAL_COUNTS contracts=24, closure=147, material=37' in log
axioms = []
for text in logs:
    for name, values in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", text, re.S):
        names = [s.strip() for s in values.split(',') if s.strip()]
        assert set(names) <= {'propext', 'Classical.choice', 'Quot.sound'}, (name, names)
        axioms.append({'name': name, 'axioms': names})
assert len(axioms) == 101
live_modules = sorted((P/'NLA/KE04').glob('*.lean')); assert len(live_modules) == 10
assert sum(len(re.findall(r'^#assert_trust kernel ', q.read_text(), re.M)) for q in live_modules) == 77
assert len(re.findall(r'^#assert_trust kernel ', (A/'source/Inspect.lean').read_text(), re.M)) == 24
warnings = [line for text in logs for line in text.splitlines()
    if re.match(r'^.+\.lean:\d+:\d+: warning:', line)]
assert len(warnings) == 38 and sum('Krylov.lean:107:25: warning:' in w for w in warnings) == 1
assert all('Inspect.lean:' in w or 'Krylov.lean:107:25:' in w for w in warnings)
extraction = load(P/'verification/assembly-development/export-extraction.json')
assert extraction['challenge_sha256'] == sha(P/'Challenge.lean')
assert extraction['proof_sha256'] == sha(P/'NLA/KE04/Proof.lean')
assert ['NLA.KE04.'+r['name'] for r in extraction['contracts']] == configured
challenge = (P/'Challenge.lean').read_text(); proof = (P/'NLA/KE04/Proof.lean').read_text()
for r in extraction['contracts']:
    head = 'theorem '+r['name']+r['frozen_signature']
    assert head in challenge and head in proof, r['name']
    assert '  exact '+r['implementation'] in proof, r['name']
assert inventory(P) == initial, 'A pre-review file changed during coordinator checks'

O.mkdir()
for q in R.iterdir():
    assert q.is_file() and not q.is_symlink(); (O/q.name).write_bytes(q.read_bytes())
prior = Path('/tmp/nla-lean-formalization/ke04-root-proof-freeze-1osyqny2')
if prior != R:
    (O/'initial-coordinator-diagnostic').mkdir()
    for q in prior.iterdir():
        assert q.is_file() and not q.is_symlink()
        (O/'initial-coordinator-diagnostic'/q.name).write_bytes(q.read_bytes())
save(O/'actual-axioms.json', axioms)
utc = datetime.now(timezone.utc).isoformat()
accept = {
    'utc': utc, 'phase': 'Complete author proof accepted for two independent final mathematical reviews',
    'root_role': 'Proof contributor and coordinator, not independent mathematical referee',
    'root_read_all_mathematical_sources_Proof_map_and_actual_inspectors': True,
    'root_read_only_helper_seals': [row[0] for row in helper_checks],
    'frozen_statement_inputs_unchanged': 1598, 'fresh_original_Git_blobs': 17,
    'final_fresh_attempt': str(A.relative_to(P)), 'final_attempt_sha256': sha(A/'result.json'),
    'source_and_inspector_commands': 12, 'dependency_pin_commands': 40, 'version_commands': 1,
    'exact_public_types': 24, 'actual_project_closure': 147, 'required_material_dependencies': 37,
    'source_kernel_assertions': 77, 'inspector_kernel_assertions': 24, 'actual_axiom_reports': 101,
    'inherited_Krylov_source_warnings': 1, 'expected_proposition_unused_binder_warnings': 37,
    'fresh_objects_hashed_then_removed': 12, 'own_prefix_absent': True,
    'source_proof_sha256': sha(P/'NLA/KE04/Proof.lean'), 'proof_map_sha256': sha(P/'PROOF-MAP.md'),
    'reviewed_anchors': anchors,
    'historical_diagnostics': 'Earlier helper compilation/API failures and metadata-only diagnostics remain sealed. The whole-author build passed on its first attempt. The first coordinator seal assumed a warning count and counted hint lines; its preserved diagnostic was corrected to the actual 38 warning headers (1 inherited source, 37 expected-Prop binders). No mathematical source changed and this freeze command performs no Lean rebuild.',
    'independent_final_approvals': 0, 'fully_verified': False, 'actual_Linux_Comparator': False,
    'complete_target': 'All 24 original contracts including BlockLanczosConjecture via FullPrefixBlockLanczosClaim, on genuine matrices, Krylov spans, compressions and spectra.',
}
save(O/'ROOT-ASSEMBLY-ACCEPTANCE.json', accept)
outer = O/'EVIDENCE-MANIFEST.json'
members = {str(q.relative_to(P)): ident(q) for q in sorted(O.rglob('*')) if q.is_file()}
for n in ['PROOF-MAP.md', *anchors]: members[n] = ident(P/n)
save(outer, {'scope': 'Every own coordinator assembly artifact and exact named anchors; full project is in subsequent proof freeze.',
    'exact_self_exclusion': str(outer.relative_to(P)), 'files': members})
all_files = inventory(P)
freeze = {
    'utc': utc, 'phase': 'Complete KE04 proof before independent final mathematical review', 'base': original['base'],
    'files': {n:r['sha256'] for n,r in all_files.items()}, 'file_sizes': {n:r['bytes'] for n,r in all_files.items()},
    'source_files': {r['upstream_path']:r['sha256'] for _,r in rows},
    'source_git_blobs': {r['upstream_path']:r['git_blob'] for _,r in rows},
    'source_snapshot_directory': 'verification/original-sources',
    'frozen_statement_sha256': sha(P/'reviews/statement-freeze.json'),
    'proof_start_sha256': sha(P/'verification/proof-start.json'),
    'root_assembly_acceptance_sha256': sha(O/'ROOT-ASSEMBLY-ACCEPTANCE.json'),
    'root_assembly_evidence_sha256': sha(outer), 'final_author_source_attempt_sha256': sha(A/'result.json'),
    'configured_contracts': configured, 'exact_self_exclusion': str(F.relative_to(P)),
    'inventory_rule': 'Every project file before independent final reviews; exact own outer self-exclusion only. Includes every historical source snapshot, seal and failed diagnostic. Later reviews and packaging are separate additions.',
    'status': 'Ready for two independent final mathematical reviews; not Lean verified',
    'known_metadata_phase': 'Historical Lake default is Challenge. Actual author checks explicitly built Solution. Candidate packaging must select Solution by default and archive the old exact wrapper.',
}
save(F, freeze)
assert inventory(P) == dict(all_files, **{str(F.relative_to(P)):ident(F)})
receipt = {'problem':'KE-04', 'complete_author_proof':True, 'fully_verified':False,
    'frozen_project_inputs':len(all_files), 'original_Git_sources':17, 'proof_freeze_sha256':sha(F),
    'root_assembly_acceptance_sha256':sha(O/'ROOT-ASSEMBLY-ACCEPTANCE.json'),
    'root_assembly_evidence_sha256':sha(outer), 'final_author_attempt_sha256':sha(A/'result.json'),
    'exact_exports':24, 'actual_project_closure':147, 'actual_axiom_reports':101,
    'source_modules':{str(q.relative_to(P)):sha(q) for q in live_modules},
    'Solution_sha256':sha(P/'Solution.lean'), 'PROOF_MAP_sha256':sha(P/'PROOF-MAP.md')}
save(Path('/tmp/nla-lean-formalization/KE-04-final-proof-freeze.json'), receipt)
print(json.dumps(receipt, indent=2))
