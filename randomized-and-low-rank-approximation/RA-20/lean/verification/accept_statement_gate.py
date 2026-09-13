from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess

P=Path('/tmp/nla-lean-formalization/next-ra-statements-draft/RA-20/lean')
R=Path('/tmp/nla-lean-ra09-worktree')
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def bound(f, base=None, complete_internal=False):
    d=json.loads(f.read_text());base=base or f.parent
    for r,v in d['files'].items():
        p=base/r;want=v if isinstance(v,str) else v['sha256']
        assert h(p)==want,(f,r)
        if isinstance(v,dict) and 'bytes' in v:assert p.stat().st_size==v['bytes']
    if complete_internal:
        actual={str(p.relative_to(base)) for p in base.rglob('*') if p.is_file() and p!=f}
        internal={r for r in d['files'] if not r.startswith('../')}
        assert actual==internal,(f,actual-internal,internal-actual)
    return dict(path=str(f.relative_to(P)),sha256=h(f),bound_files=len(d['files']))

F=P/'reviews/statement-freeze.json';f=json.loads(F.read_text())
assert h(F)=='6bd2bbf4a6d787fd4e0c5c8b19aad74dac73b7e79c9552e537544136a4812aa8'
for r,v in f['files'].items():assert h(P/r)==v,r
for r,v in f['source_files'].items():
    snapshot=P/'verification/original-sources'/r
    blob=subprocess.check_output(['git','show',f['base']+':'+r],cwd=R)
    assert hashlib.sha256(blob).hexdigest()==v==h(snapshot),r
    assert subprocess.check_output(['git','rev-parse',f['base']+':'+r],cwd=R,text=True).strip()==f['source_git_blobs'][r]
assert not (P/'Solution.lean').exists()
assert list((P/'NLA/RA20').glob('*.lean'))==[P/'NLA/RA20/Definitions.lean']
package=bound(P/'reviews/statement-package-manifest.json',P)
reviews=[]
for n,who,expected,commands,kernel,standard in [
    (1,'/root','bf0f1decd2e67f6230e9655f4c669be9c868001c8259b4fd2461b8cf90988904',3,10,9),
    (2,'/root/leancert_examples','542cfa5fb183aa7bfa4b79ad9ab1c16bb32b77e713e10414d4c8bae50c0873a2',3,20,19)]:
    report=P/f'reviews/statement-referee-{n}.md';assert h(report)==expected
    manifest=bound(P/f'reviews/statement-referee-{n}-evidence/EVIDENCE-MANIFEST.json',complete_internal=True)
    reviews.append(dict(reviewer=who,report=str(report.relative_to(P)),sha256=h(report),evidence=manifest,successful_direct_source_commands=commands,explicit_kernel_definition_checks=kernel,standard_three_reports=standard,axiom_free_reports=1,mathematical_revision_requested=False))

gate=dict(utc=datetime.now(timezone.utc).isoformat(),phase='PROOF IMPLEMENTATION AUTHORIZED after two accepted independent statement approvals',coordinator='/root',statement_author='/root/formal_review_standards',independent_statement_reviewers=['/root','/root/leancert_examples'],statement_freeze_sha256=h(F),preserved_statement_inputs=len(f['files']),preserved_original_source_Git_blobs=len(f['source_files']),original_author_package=package,reports=reviews,root_review='Complete source and exact target, all definitions and twelve contracts, numerical plan, both complete independent reports and primary geometric conventions reviewed. Root independently elaborated the statements and actual semantic library definitions. Full retained TeX and exact numerical record also read. All frozen and original Git bytes and complete referee inventories rehashed before this gate.',obligations='Prove all twelve exact contracts and negate the complete original four-formula target. Keep the complex symmetric rank-at-most-two variety, all-vanishing-ideal reduced coordinate ring, actual algebraic smooth locus, tangent space of the entire ideal, actual complex derivatives of the full Frobenius bilinear objective, nonvacuous generic principal opens and cardinal counting. Prove the reduced-ring, smooth/non-smooth and genericity bridges without hypotheses assuming their conclusions.',numerical_scope='Pure exact algebra, localization, calculus and finite cardinality. Actual LeanCert kernel trust/dependency assertions; no artificial interval or numerical certificate.',proof_absent_at_gate=True,workspace='Continue in this isolated /tmp project using original Git-bound snapshots and read-only shared dependencies; install into an isolated Git branch before candidate submission. No full dependency copy.',canonical_status='Solved, unchanged',proof_gate_open=True,final_independent_reviews_Linux_and_publication='pending')
G=P/'verification/proof-start.json';assert not G.exists();G.write_text(json.dumps(gate,indent=2)+'\n')
roles=dict(utc=datetime.now(timezone.utc).isoformat(),gate_sha256=h(G),owners={'/root/formal_review_standards':['NLA/RA20/Algebra.lean: matrix/variety semantics and reduced coordinate ring; main integration after current publication reviews'], '/root/leancert_examples':['NLA/RA20/Smooth.lean: genuine algebraic smooth and nonsmooth locus, coordinate-ring localization bridge'], '/root/mf16_final_referee':['NLA/RA20/Differential.lean: full Frobenius derivative, hollow metric, chart second derivatives and nondegeneracy'], '/root':['coordination, packaging; further mathematical module ownership must be recorded before edits']},no_frozen_definition_or_contract_edits=True,disclosure='Statement reviewers who implement are ineligible as independent final mathematical referees. Two fresh final referees will be assigned after completion.',shared_cache='MI-22 exact ten-package sources and artifacts are read-only; own fresh prefixes only, no download or dependency mutation.',unassigned=['entire-ideal tangent equivalence','generic data intersection','critical-set exhaustion/cardinality and final wrappers'])
A=P/'verification/implementation-roles.json';assert not A.exists();A.write_text(json.dumps(roles,indent=2)+'\n')
(P/'verification/accept_statement_gate.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps({'gate':h(G),'roles':h(A),'statement_inputs':len(f['files']),'source_inputs':len(f['source_files']),'reviews':reviews},indent=2))
