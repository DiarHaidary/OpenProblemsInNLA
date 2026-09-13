from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess, sys, tempfile

P = Path('/tmp/nla-lean-formalization/next-ie05-statements-draft/lean')
E = P / 'verification/statement-gate-preflight'
O = P / 'verification/statement-acceptance'
F = P / 'reviews/statement-freeze.json'
G = P / 'verification/proof-start.json'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
identity = lambda p: {'sha256': sha(p), 'bytes': p.stat().st_size}
assert not any(p.exists() for p in [O, F, G, P / 'Solution.lean', P / 'NLA/IE05/Proof.lean'])
anchors = {
    'reviews/statement-referee-1.md': '13aa3e9b73c1fde94d2b45c4ec327a44b0e4470c685fa58478526a122cb25c10',
    'reviews/statement-referee-1-evidence/outer-manifest.json': '26f09fc4bff996802f57dea898de457d4105d0454e1700288da96f578222561b',
    'reviews/statement-referee-2.md': 'd5b204c4bcc727e52c52c60855e5a393debdba5bc5a2d5567c1c715e5de18730',
    'reviews/statement-referee-2-evidence/EVIDENCE-SEAL.json': 'f21212db9edcfba43dccbf92bb1eb75fea56b63fc464fa636abb756aa81c7a52',
    'verification/statement-gate-preflight/EVIDENCE-SEAL.json': '7f012a16fa8d947511176a634b28d63ebdfc4331f48532b16e513284e397f6c3',
    'verification/statement-gate-preflight/preflight-result.json': '4c9c522155833039463c16e2d46f2215753635bbc2eab158f5419cc64b8be6ae',
    'verification/statement-gate-preflight/proposed-input-binding.json': 'ef6165de5d5129ed19871e0cb1000ece1f50040c2453e9937a71f1d58e82cfe0',
    'verification/statement-gate-preflight/verify_preflight.py': '26b3081d0e59e2b99dd7c3cc2c4f22a35d81eab717442f934d802f2c34cc6e85',
    'NLA/IE05/Definitions.lean': 'aa9a18994bb8d1889af8b30290cb71846af5424436d720afaf15a54184164dfa',
    'Challenge.lean': '0ccd5424f990587b1bb7170c674cba4645d9427286c916e2e19387234ccf250e',
}
for rel, expected in anchors.items():
    assert sha(P / rel) == expected, rel
seal = json.loads((E / 'EVIDENCE-SEAL.json').read_text())
assert seal['excluded_paths'] == ['verification/statement-gate-preflight/EVIDENCE-SEAL.json']
members = {str(p.relative_to(P)): identity(p) for p in E.rglob('*') if p.is_file() and p != E / 'EVIDENCE-SEAL.json'}
assert members == seal['files'] and len(members) == 14
binding = json.loads((E / 'proposed-input-binding.json').read_text())
assert len(binding['files']) == 718
for rel, expected in binding['files'].items():
    assert identity(P / rel) == expected, rel
before = {str(p.relative_to(P)): identity(p) for p in sorted(P.rglob('*')) if p.is_file()}
assert len(before) == 733
assert set(before) == set(binding['files']) | set(members) | {'verification/statement-gate-preflight/EVIDENCE-SEAL.json'}

# Run the inspected, read-only full check before adding any gate artifact.
# Its strict pre-implementation tree check is historical after this gate.
run_dir = Path(tempfile.mkdtemp(prefix='ie05-root-statement-gate-', dir='/tmp/nla-lean-formalization'))
argv = [sys.executable, '-B', str(E / 'verify_preflight.py')]
(run_dir / 'command.json').write_text(json.dumps({'argv': argv, 'cwd': str(P)}, indent=2) + '\n')
(run_dir / 'authorize_ie05_proof.py').write_bytes(Path(__file__).read_bytes())
result = subprocess.run(argv, cwd=P, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'),
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(run_dir / 'stdout.json').write_bytes(result.stdout)
(run_dir / 'stderr.log').write_bytes(result.stderr)
(run_dir / 'exit.json').write_text(json.dumps({'returncode': result.returncode}) + '\n')
assert result.returncode == 0, 'Full preflight failed; actual result retained at ' + str(run_dir)
checked = json.loads(result.stdout)
assert checked['pass'] and checked['stage'] == 'complete'
assert checked['checked_reviewed_input_count'] == 718 and len(checked['actual_commands']) == 85
assert len(checked['configured_types']) == 17 and len(checked['actual_definition_axioms']) == 41
contracts = json.loads((P / 'comparator.json').read_text())['theorem_names']
assert contracts == ['NLA.IE05.' + name for name in checked['configured_types']]
assert {str(p.relative_to(P)): identity(p) for p in P.rglob('*') if p.is_file()} == before
originals = json.loads((P / 'verification/original-source-inventory.json').read_text())
assert len(originals['files']) == 27
utc = datetime.now(timezone.utc).isoformat()
frozen = {
    'utc': utc, 'scope': 'Complete IE-05 pre-implementation statement and review inputs; all 17 original-target contracts',
    'base': originals['base'], 'files': {k: v['sha256'] for k, v in before.items()},
    'file_sizes': {k: v['bytes'] for k, v in before.items()},
    'source_files': {k: v['sha256'] for k, v in originals['files'].items()},
    'source_git_blobs': {k: v['git_blob'] for k, v in originals['files'].items()},
    'source_snapshot_directory': 'verification/original-sources',
    'independent_statement_referees': ['/root/ie05_statement_referee1', '/root/ie05_statement_referee2'],
    'reviewed_anchor_hashes': anchors, 'definitions_sha256': sha(P / 'NLA/IE05/Definitions.lean'),
    'challenge_sha256': sha(P / 'Challenge.lean'), 'configured_contracts': contracts,
    'exact_self_exclusion': 'reviews/statement-freeze.json',
    'inventory_rule': 'All 733 project inputs existing immediately before this freeze; no nested manifest exclusions. Later coordinator gate and proof files are separate additions.'}
F.write_text(json.dumps(frozen, indent=2) + '\n')
O.mkdir()
for source in run_dir.iterdir():
    (O / source.name).write_bytes(source.read_bytes())
acceptance = {
    'utc': utc, 'status': 'Both independent statement approvals accepted by the coordinator',
    'root_read_complete_reports_statements_numerical_targets_correspondence_preflight_source': True,
    'root_role': 'Statement numerical-design contributor and prospective proof contributor; not an independent statement referee',
    'statement_freeze_sha256': sha(F), 'frozen_inputs': 733, 'original_Git_sources': 27,
    'read_only_preflight_reexecuted': True, 'actual_read_only_commands': 85,
    'configured_contracts': 17, 'definition_kernel_trust_reports': 41,
    'full_preflight_output_sha256': sha(O / 'stdout.json'),
    'reviewed_anchors': anchors, 'new_Lean_compile': False,
    'historical_driver_note': 'The prior one-shot author/reviewer/preflight tree checks retain their pre-implementation scopes; inspect their snapshots and manifests after later proof additions instead of rerunning them against an expanded live tree.'}
(O / 'ROOT-ACCEPTANCE.json').write_text(json.dumps(acceptance, indent=2) + '\n')
outer = O / 'EVIDENCE-MANIFEST.json'
bound = {str(p.relative_to(O)): identity(p) for p in O.rglob('*') if p.is_file()}
bound['../../reviews/statement-freeze.json'] = identity(F)
outer.write_text(json.dumps({'scope': 'Every own acceptance artifact and the complete statement freeze; only exact own outer self excluded', 'files': bound}, indent=2) + '\n')
gate = {
    'utc': utc, 'problem': 'IE-05', 'proof_authorized': True,
    'statement_freeze_sha256': sha(F), 'coordinator_acceptance_sha256': sha(O / 'ROOT-ACCEPTANCE.json'),
    'coordinator_evidence_sha256': sha(outer), 'independent_statement_approvals': 2,
    'complete_original_target': 'Negation of the full all-dimensional orthogonal GEPP extremizer equality, with actual QR, all admissible tie paths and real supremum',
    'contracts': contracts,
    'boundary_rule': 'Do not alter the frozen Definitions, Challenge, data, quantifiers or contract types without reopening independent statement review.',
    'numerical_strategy': 'Prove the reduced integer and rational facts by exact kernel-checked arithmetic, then transfer via actual square-root bounds and GEPP semantics. Use LeanCert explicit kernel trust audits on material lemmas and exports. No artificial interval or singleton certificate is needed or planned.',
    'retained_computations': {'witness_input_bounds': 64, 'candidate_active_bounds': 204, 'positive_squared_gap': '117335164/1147041'},
    'forbidden_shortcuts': ['No admitted proof or extra axiom', 'No native execution axiom', 'No imported Challenge or reference environment in Solution', 'No assumed QR, nonsingular-elimination, trajectory or supremum bridge'],
    'independent_final_mathematical_reviews': 'Required after complete frozen proof; proof contributors cannot count',
    'actual_Linux_Comparator_default_kernel_controls': 'Required later and not run',
    'canonical_status': 'Solved, unchanged', 'fully_verified': False}
G.write_text(json.dumps(gate, indent=2) + '\n')
receipt = {'problem': 'IE-05', 'proof_authorized': True, 'frozen_inputs': 733, 'original_sources': 27,
           'statement_freeze_sha256': sha(F), 'proof_start_sha256': sha(G),
           'root_acceptance_sha256': sha(O / 'ROOT-ACCEPTANCE.json'), 'root_evidence_sha256': sha(outer),
           'independent_statement_approvals': 2, 'contracts': 17, 'canonical_status': 'Solved, unchanged',
           'fully_verified': False}
Path('/tmp/nla-lean-formalization/IE-05-proof-start.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
