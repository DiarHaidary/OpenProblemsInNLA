"""One-shot coordinator acceptance of the two sealed KE-04 statement reviews."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess, sys, tempfile

P = Path('/tmp/nla-lean-formalization/next-ke04-statements-draft/lean').resolve()
V = P / 'reviews/statement-referee-2-evidence'
O = P / 'verification/statement-acceptance'
F = P / 'reviews/statement-freeze.json'
G = P / 'verification/proof-start.json'
sha = lambda b: hashlib.sha256(b).hexdigest()
ident = lambda p: {'sha256': sha(p.read_bytes()), 'bytes': p.stat().st_size}
load = lambda p: json.loads(p.read_text())
def save(p, data):
    p.write_text(json.dumps(data, indent=2) + '\n')

assert not any(p.exists() for p in [O, F, G, P/'Solution.lean', P/'NLA/KE04/Proof.lean'])
anchors = {
    'NLA/KE04/Definitions.lean': 'ae1baccc0cb622f83103eff8bb4a5efe4cd9a3bae4822ccca38da29554ae9ca4',
    'Challenge.lean': 'a27de227d483072e395b6658a97cbf31296503c7fab36e5f9dbf248b2efa299e',
    'NUMERICAL_TARGETS.md': 'ad963526a371cdfee8eaaf179674d5cabd2a1d5a9ae5b123c96ac2f2b4271c47',
    'SourceCorrespondence.md': '399f28847f52a6c5ff309a25b9501c0c6d4bd5a76892de2f5adaa9c25fe80a00',
    'comparator.json': 'c0c7086cb81abe8f422762d0db2cc55419828f08ba80d33f9157cb3f396a8b8e',
    'STATEMENT-HANDOFF.md': 'f46ec1cb54a9eed22dd7fc2cf640531be64b2ec86d48251d09075a64e94fa8a9',
    'DRAFT-INVENTORY.json': 'e82c391cc2d8d3ad1ee12e4f19266e2495e469e4b39272d31697a2e4a873a9fa',
    'reviews/statement-referee-1.md': 'a685c8098738d02f66adf58816ad7b979f21f85c91c7881c1e90c7a1b732dcb7',
    'reviews/statement-referee-1-evidence/EVIDENCE-MANIFEST.json': 'f3bbf77a6dcc4abf108ceb068393f6e90fdde9abff5e306f1b05dcd4c4064dd6',
    'reviews/statement-referee-1-evidence/attempt-nglj5yvu/result.json': '6ac17ee119a2f1f364dab0c2a095a9555e7ea04f35e7682fe469bc97e1b1d1bf',
    'reviews/statement-referee-2.md': '8aacde7c1c8606d0c3cac710c726411a4fdb17a59f27c622f78a5b42e4dfe63e',
    'reviews/statement-referee-2-evidence/EVIDENCE-MANIFEST.json': 'abf7360791a312f8366a3b78fd6b08302e8884c43bec5f6bc430d5a802084c94',
    'reviews/statement-referee-2-evidence/attempt-o6p9csbt/result.json': '5ac8999d0a5ddf045460d136919756fd10b20090496e45ed5f599d1ccf1fbf29',
    'reviews/statement-referee-2-evidence/source-audit/result.json': 'afeb955dbbb8d13db21f4e0b6e5d9822f841b19bcb97d6e0c5aae48862be9d98',
}
for rel, expected in anchors.items():
    assert ident(P/rel)['sha256'] == expected, rel
before = {str(p.relative_to(P)): ident(p) for p in sorted(P.rglob('*')) if p.is_file()}
assert len(before) == 1598
sealed = load(V/'EVIDENCE-MANIFEST.json')
assert sealed['excluded_paths'] == ['reviews/statement-referee-2-evidence/EVIDENCE-MANIFEST.json']
assert set(before) == set(sealed['files']) | set(sealed['excluded_paths'])
assert all(before[n] == row for n,row in sealed['files'].items())

R = Path(tempfile.mkdtemp(prefix='ke04-root-statement-gate-', dir='/tmp/nla-lean-formalization')).resolve()
(R/'executed-authorize_ke04_proof.py').write_bytes(Path(__file__).read_bytes())
commands = []
def run(argv, cwd=P, inp=None):
    idx = len(commands)
    c = subprocess.run(argv, cwd=cwd, input=inp, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    names = {stream: f'{idx:02d}.{stream}' for stream in ['stdout','stderr']}
    for stream, name in names.items():
        (R/name).write_bytes(getattr(c,stream))
    row = {'argv':argv, 'cwd':str(cwd), 'exit_code':c.returncode, **names,
           'stdout_sha256':sha(c.stdout), 'stderr_sha256':sha(c.stderr)}
    if inp is not None:
        (R/f'{idx:02d}.stdin').write_bytes(inp)
        row.update(stdin=f'{idx:02d}.stdin', stdin_sha256=sha(inp))
    commands.append(row); save(R/'commands.json',commands)
    assert c.returncode == 0, f'Coordinator read-only command failed; retained at {R}'
    return c.stdout

checked = json.loads(run([sys.executable,'-B',str(V/'verify_inventory.py'),'--strict']))
assert checked['status'] == 'PASS' and checked['strict_current_membership'] and checked['sealed_files'] == 1597
ref1 = load(P/'reviews/statement-referee-1-evidence/RESULT.json')
assert ref1['verdict'] == 'APPROVE' and ref1['contracts'] == 24 and ref1['kernel_trust_commands'] == 27
assert ref1['independently_compiled_modules'] == 4 and ref1['definition_closure'] == 33
ref2 = load(V/'attempt-o6p9csbt/result.json')
assert ref2['success'] and not ref2['errors'] and ref2['own_private_prefix_removed']
cfg = load(P/'comparator.json'); contracts = cfg['theorem_names']
assert len(contracts) == 24 and len(set(contracts)) == 24 and set(contracts) == set(ref2['target_names'])
assert cfg['definition_names'] == [] and set(cfg['permitted_axioms']) == {'propext','Classical.choice','Quot.sound'}
assert all(set(a) <= set(cfg['permitted_axioms']) for a in ref2['definition_axioms'].values())

originals = load(P/'verification/original-source-inventory.json')
assert originals['source_count'] == len(originals['files']) == 17
rows = list(originals['files'].items())
queries = ''.join(row['commit']+':'+row['upstream_path']+'\n' for _,row in rows).encode()
raw = run(['git','-C','/tmp/nla-lean-ra20-worktree','cat-file','--batch'], inp=queries)
pos = 0
for rel,row in rows:
    end = raw.index(b'\n',pos); obj,kind,n = raw[pos:end].decode().split(); n=int(n)
    content = raw[end+1:end+1+n]; assert raw[end+1+n:end+2+n] == b'\n'
    pos = end+2+n
    assert kind == 'blob' and obj == row['git_blob']
    assert content == (P/rel).read_bytes() and len(content) == row['bytes'] and sha(content) == row['sha256'], rel
assert pos == len(raw)
deps = Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
assert len(ref2['before_dependencies']) == 10
for dep in ref2['before_dependencies']:
    loc = deps/dep['name']
    assert run(['git','rev-parse','HEAD'],loc).decode().strip() == dep['revision']
    assert run(['git','status','--porcelain','--untracked-files=no'],loc) == b''
assert {str(p.relative_to(P)):ident(p) for p in P.rglob('*') if p.is_file()} == before

utc = datetime.now(timezone.utc).isoformat()
frozen = {
    'utc':utc, 'scope':'All 1598 complete pre-implementation KE-04 statement and review files; all 24 full-target contracts',
    'base':originals['base'], 'files':{n:r['sha256'] for n,r in before.items()},
    'file_sizes':{n:r['bytes'] for n,r in before.items()},
    'source_files':{n:r['sha256'] for n,r in originals['files'].items()},
    'source_git_blobs':{n:r['git_blob'] for n,r in originals['files'].items()},
    'independent_statement_referees':['/root/ra20_final_referee2','/root/mf16_final_referee'],
    'reviewed_anchor_hashes':anchors, 'configured_contracts':contracts,
    'definitions_sha256':ident(P/'NLA/KE04/Definitions.lean')['sha256'],
    'challenge_sha256':ident(P/'Challenge.lean')['sha256'],
    'exact_self_exclusion':'reviews/statement-freeze.json',
    'inventory_rule':'Every input existing before this freeze, including every nested inventory. Later gate and proof files are separate additions.'}
save(F,frozen)
O.mkdir()
for source in R.iterdir():
    assert source.is_file() and not source.is_symlink()
    (O/source.name).write_bytes(source.read_bytes())
acceptance = {
    'utc':utc, 'status':'Both independent statement approvals accepted by the coordinator',
    'root_role':'Statement-design contributor and proof coordinator; not an independent referee',
    'root_read_complete_original_target_source_proof_definitions_24_contracts_numerical_strategy_correspondence_both_reports_and_inspectors':True,
    'root_semantic_judgment':'Complete original all-dimensional symmetric block-Lanczos claim, arbitrary orthonormal Krylov bases, true ordered Ritz values with multiplicities, both strict endpoints and no hidden gap or nonannihilation premise.',
    'statement_freeze_sha256':ident(F)['sha256'], 'frozen_inputs':1598, 'original_Git_sources':17,
    'read_only_referee2_strict_verifier_executed':True, 'read_only_coordinator_commands':len(commands),
    'fresh_original_git_batch_checked':17, 'fresh_clean_dependency_pins_checked':10,
    'per_referee_actual_Lean_modules':4, 'per_referee_definition_kernel_assertions':27,
    'per_referee_safe_definition_closure':33, 'per_referee_exact_target_types':24,
    'new_coordinator_Lean_compile':False, 'reviewed_anchors':anchors,
    'historical_scope':'The first reviewer full-tree check passed before second-review additions; all 1468 old files remain byte-identical in the second seal. Do not rerun historical strict whole-tree checks against later proof additions.',
    'failures_preserved':'All original author and first-reviewer diagnostics remain in the frozen tree. Their lost historical object-result fields are not reconstructed or substituted for either successful fresh independent review.'}
save(O/'ROOT-ACCEPTANCE.json',acceptance)
outer = O/'EVIDENCE-MANIFEST.json'
bound = {str(p.relative_to(O)):ident(p) for p in sorted(O.rglob('*')) if p.is_file()}
bound['../../reviews/statement-freeze.json'] = ident(F)
save(outer,{'scope':'Every own coordinator artifact and exact full statement freeze; only this own outer self is excluded','excluded_paths':['EVIDENCE-MANIFEST.json'],'files':bound})
gate = {
    'utc':utc, 'problem':'KE-04', 'proof_authorized':True,
    'statement_freeze_sha256':ident(F)['sha256'], 'coordinator_acceptance_sha256':ident(O/'ROOT-ACCEPTANCE.json')['sha256'],
    'coordinator_evidence_sha256':ident(outer)['sha256'], 'independent_statement_approvals':2,
    'contracts':contracts,
    'complete_original_target':'BlockLanczosConjecture for all real symmetric matrices, full-column-rank starting blocks and largest full iterations, all independent Krylov bases and original strict interval indices; prove the stronger FullPrefixBlockLanczosClaim and its implication.',
    'boundary_rule':'Do not change any frozen definitions, quantifiers, numerical statements or contract types without reopening independent statement review.',
    'numerical_strategy':'Use exact finite-dimensional linear algebra, genuine spectral theorem and monic quadratic nonannihilation. No interval computation is required. LeanCert explicit kernel-trust assertions remain mandatory for material lemmas and exports.',
    'forbidden_shortcuts':['No admitted proof or extra axiom','No native execution axiom','No Challenge import in proof or Solution','No assumed basis compatibility, spectrum separation, PSD bridge or nonannihilation'],
    'independent_final_mathematical_reviews':'Two required on the complete frozen proof; proof contributors cannot count as independent final reviewers.',
    'actual_Linux_Comparator_default_kernel_controls':'Required later; not yet run for this problem',
    'canonical_status':'Solved, unchanged', 'fully_verified':False}
save(G,gate)
receipt = {'problem':'KE-04','proof_authorized':True,'frozen_inputs':1598,'original_sources':17,
           'statement_freeze_sha256':ident(F)['sha256'],'proof_start_sha256':ident(G)['sha256'],
           'root_acceptance_sha256':ident(O/'ROOT-ACCEPTANCE.json')['sha256'],'root_evidence_sha256':ident(outer)['sha256'],
           'independent_statement_approvals':2,'contracts':24,'actual_read_only_coordinator_commands':len(commands),
           'canonical_status':'Solved, unchanged','fully_verified':False}
save(Path('/tmp/nla-lean-formalization/KE-04-proof-start.json'),receipt)
print(json.dumps(receipt,indent=2))
