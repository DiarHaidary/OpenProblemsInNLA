"""Accept author assembly, copy its immutable bytes, and freeze for fresh referees.
No proof build, dependency mutation, Git mutation or final verification claim.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, shutil, subprocess

S = Path('/tmp/nla-lean-formalization/next-ra-statements-draft/RA-20/lean')
R = Path('/tmp/nla-lean-ra20-worktree')
P = R/'randomized-and-low-rank-approximation/RA-20/lean'
BASE = '5830ed4fb06da0659414a3deb2a40ad327aca052'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
load = lambda p: json.loads(Path(p).read_text())
git = lambda *args: subprocess.check_output(['git', *args], cwd=R)
assert git('rev-parse', 'HEAD').decode().strip() == BASE
assert git('branch', '--show-current').decode().strip() == 'codex/lean-ra20-hollow-critical-count'
assert not git('status', '--porcelain').strip()
assert not P.exists()
assert '**Status:** Solved' in (P.parent/'README.md').read_text()
assert len(load(R/'problem_ids.json')) == 217
alternates_path = Path(git('rev-parse', '--git-path', 'objects/info/alternates').decode().strip())
if not alternates_path.is_absolute(): alternates_path = R/alternates_path
assert alternates_path.is_file() and alternates_path.read_text().strip()

F = load(S/'reviews/statement-freeze.json')
assert sha(S/'reviews/statement-freeze.json') == '6bd2bbf4a6d787fd4e0c5c8b19aad74dac73b7e79c9552e537544136a4812aa8'
assert sha(S/'verification/proof-start.json') == '9fe55d622e50390cb3ed439989b9393455fa48eb50d42d84fb33c20fd8c883f3'
assert len(F['files']) == 68 and len(F['source_files']) == 16
for rel, digest in F['files'].items(): assert sha(S/rel) == digest, rel
for rel, digest in F['source_files'].items():
    data = git('show', BASE+':'+rel)
    assert hashlib.sha256(data).hexdigest() == digest, rel
    assert sha(S/'verification/original-sources'/rel) == digest
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == F['source_git_blobs'][rel]
E = S/'verification/conclusion-development'
assert sha(E/'EVIDENCE-MANIFEST.json') == '08a46ab6aac719684b7376b1e92717e25a3bc8fa5aa2a54429a0c6d4b86466ab'
assert sha(E/'HANDOFF.md') == '497de9a07c5d2f4e54029632272dbe40536b05cb82ffc8582de8f7dd4a2acc67'
assert sha(E/'validation.json') == '273534b9b1a4c3fe89daa2d542b9ea25621268b090db8a1940b2cd3d20bdd5e8'
seal_output = subprocess.check_output(['python3', str(E/'verify_seal.py')], cwd=S)
seal = json.loads(seal_output)
assert seal['status'] == 'PASS' and seal['bound_files'] == 513 and seal['prior_manifests'] == 7
assert sha(S/'PROOF_MAP.md') == '9a1ed03e395a26fd4e3557623caa0bef892a4cd1c0cbc64dd097e5635eda917c'
assert sha(S/'reviews/proof-completion.md') == '56764086d6f4a4faec342a33a890aaa3fd7ba4882a8447e2e5bcdf30c953f3b5'

V = load(E/'validation.json')
results = []
standard = {'propext', 'Classical.choice', 'Quot.sound'}
source_reports = diagnostic_reports = 0
for d in sorted(E.glob('attempt-*')):
    rec = load(d/'result.json')
    source = S/rec['source']
    snapshot = d/source.name
    assert sha(snapshot) == rec['sha256']
    text = (d/'lean.log').read_text()
    if rec['exit_code'] == 0:
        assert sha(source) == rec['sha256'], rec['source']
        assert not re.search(r'^.*error:', text, re.M), str(d)
        rows = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", text)
        for name, axioms in rows:
            assert {a.strip() for a in axioms.split(',') if a.strip()} == standard, name
        if rec['source'].startswith('verification/'):
            diagnostic_reports += len(rows)
        else:
            source_reports += len(rows)
    results.append({'attempt': d.name, 'source': rec['source'], 'source_sha256': rec['sha256'],
                    'exit_code': rec['exit_code'], 'result_sha256': sha(d/'result.json'),
                    'log_sha256': sha(d/'lean.log')})
assert len(results) == 14 and sum(r['exit_code'] == 0 for r in results) == 13
assert source_reports == 57 and diagnostic_reports == 12
for rel, data in V['math_sources'].items():
    assert sha(S/rel) == data['sha256'] and (S/rel).stat().st_size == data['bytes']
    matches = [r for r in results if r['source'] == rel and r['exit_code'] == 0]
    assert len(matches) == 1
    assert matches[0]['result_sha256'] == data['successful_result_sha256']
    assert matches[0]['log_sha256'] == data['log_sha256']
assert len(V['math_sources']) == 11
last = load(E/'latest.json')
assert last['source'] == 'verification/conclusion-development/Inspect.lean' and last['exit_code'] == 0
inspector = (E/'attempt-014/lean.log').read_text()
exports = load(S/'comparator.json')['theorem_names']
assert len(exports) == 12
assert re.findall(r'^EXACT_FROZEN_TYPE ([^:]+):', inspector, re.M) == exports
actual_axioms = re.findall(r'^ACTUAL_AXIOMS ([^:]+):\s*\[([^\]]*)\]', inspector, re.M)
assert len(actual_axioms) == 214
for name, axioms in actual_axioms:
    assert {a.strip() for a in axioms.split(',') if a.strip()} <= standard, name
assert len(re.findall(r'^RETAINED_DEPENDENCY ', inspector, re.M)) == 39
assert 'PROJECT_COUNTS declarations=214, required=39' in inspector

pins = load(S/'lake-manifest.json')['packages']
cache = Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
assert len(pins) == 10
for pin in pins:
    repo = cache/pin['name']
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip() == pin['rev']
    assert not subprocess.check_output(['git','status','--porcelain'],cwd=repo)

prior = {}
for f in sorted(S.rglob('*')):
    assert not f.is_symlink(), f
    if f.is_file():
        assert f.suffix not in ['.olean', '.ilean', '.pyc'], f
        prior[str(f.relative_to(S))] = sha(f)
assert 'verification/proof-freeze.json' not in prior
shutil.copytree(S, P, copy_function=shutil.copy2)
actual = {str(f.relative_to(P)):sha(f) for f in P.rglob('*') if f.is_file()}
assert actual == prior
for rel, digest in prior.items(): assert sha(S/rel) == digest, rel

O = P/'verification/root-proof-acceptance-2026-09-13'
O.mkdir()
(O/'author-seal-check.json').write_bytes(seal_output)
(O/'copy-and-acceptance.json').write_text(json.dumps({
    'utc': datetime.now(timezone.utc).isoformat(), 'status': 'Author assembly accepted; frozen package authorized for two fresh independent final mathematical referees',
    'source_workspace': str(S), 'destination': str(P), 'base': BASE,
    'Git_storage': 'Independent sparse clone with a read-only shared object alternate to the existing local repository. No Git or shared-cache mutation during this copy/freeze. Standalone published verification uses normal Git checkouts.',
    'Git_alternates_file_sha256': sha(alternates_path),
    'all_copied_files': prior, 'source_workspace_preserved': True,
    'statement_inputs_unchanged': 68, 'original_source_Git_blobs': 16,
    'scoped_author_assembly_inventory_files': 513, 'all_seven_helper_seals_preserved': True,
    'actual_successful_author_commands': 13, 'retained_failed_author_commands': 1,
    'actual_source_axiom_reports': 57, 'actual_diagnostic_axiom_reports': 12,
    'actual_source_kernel_assertions': 61, 'actual_diagnostic_kernel_assertions': 12,
    'actual_elaborated_export_types': 12, 'actual_safe_project_declarations': 214,
    'required_material_dependencies': 39, 'author_attempts': results,
    'formalization_author': 'George Stepaniants',
    'affiliation': 'Department of Computing and Mathematical Sciences, California Institute of Technology, Pasadena, California, USA',
    'mathematical_resolution_author': 'Codex automated maintainer audit',
    'conjecture_authors': 'Kubjas, Sodomaco and Tsigaridas',
    'proof_contributors_ineligible_for_independent_final_review': ['/root', '/root/formal_review_standards', '/root/leancert_examples', '/root/mf16_final_referee'],
    'review_reading_scope': 'Root read all scoped helper and assembly handoffs, the full proof map/completion, and final Count/Critical source. It separately inspected exact actual type output, all actual axiom/dependency reports and complete source/hash/attempt binding. This coordinator check is not an independent final mathematical approval or new Lean build.',
    'unfrozen_prose_clarification': 'Before this freeze, root clarified the proof-map table to say exactly one hollow coordinate is zero; no mathematical source or prior seal changed.',
    'current_canonical_status': 'Solved, unchanged',
    'linux_Comparator_status': 'not run; not claimed',
    'formalization_yaml_status': 'not yet authored; required truthful candidate wrapper after final reviews',
    'remaining_gates': ['Two independent final mathematical referees', 'Candidate metadata and packaging review', 'Actual Ubuntu Comparator/default-kernel/control execution', 'Independent operational acceptance', 'Reviewed publication and separate upstream main PR'],
}, indent=2)+'\n')
(O/'freeze.py').write_bytes(Path(__file__).read_bytes())
own = {str(f.relative_to(O)):{'sha256':sha(f),'bytes':f.stat().st_size} for f in sorted(O.rglob('*')) if f.is_file()}
(O/'EVIDENCE-MANIFEST.json').write_text(json.dumps({'files':own,'file_count':len(own),'exact_self_exclusion':'EVIDENCE-MANIFEST.json','inventory_rule':'All own files; only the exact outer self path is excluded'},indent=2)+'\n')

all_files = {str(f.relative_to(P)):sha(f) for f in sorted(P.rglob('*')) if f.is_file()}
freeze = {'utc':datetime.now(timezone.utc).isoformat(), 'scope':'Complete RA20 twelve-export author proof and all existing evidence, frozen before two independent final mathematical reviews',
    'base':BASE, 'files':all_files, 'source_files':F['source_files'], 'source_git_blobs':F['source_git_blobs'],
    'statement_freeze_sha256':sha(P/'reviews/statement-freeze.json'),
    'proof_start_sha256':sha(P/'verification/proof-start.json'),
    'solution_sha256':sha(P/'Solution.lean'), 'proof_sha256':sha(P/'NLA/RA20/Proof.lean'),
    'proof_completion_sha256':sha(P/'reviews/proof-completion.md'),
    'coordinator_acceptance_sha256':sha(O/'copy-and-acceptance.json'),
    'exact_self_exclusion':'verification/proof-freeze.json',
    'inventory_rule':'Every existing project file, including every nested manifest and diagnostic; exclude only this exact freeze file itself',
    'independent_final_reviews':'pending', 'actual_Ubuntu_Comparator':'pending'}
(P/'verification/proof-freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
receipt = {'project':str(P),'base':BASE,'copied_files':len(prior),'frozen_files':len(all_files),
    'proof_freeze_sha256':sha(P/'verification/proof-freeze.json'),
    'root_acceptance_sha256':sha(O/'copy-and-acceptance.json'),
    'solution_sha256':sha(P/'Solution.lean'),'status':'Ready for two fresh independent final referees; not yet Lean verified'}
Path('/tmp/nla-lean-formalization/RA-20-complete-proof-freeze.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
