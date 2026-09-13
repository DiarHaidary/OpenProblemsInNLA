from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,re
P=Path('/tmp/nla-lean-formalization/next-ra-statements-draft/RA-20/lean');D=P/'reviews/statement-referee-1-evidence';report=P/'reviews/statement-referee-1.md';assert not report.exists();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();F=json.loads((P/'reviews/statement-freeze.json').read_text());res=json.loads((D/'result.json').read_text());assert res['status'].startswith('PASS') and len(res['commands'])==3
for c in res['commands']:assert c['exit_code']==0 and sha(D/c['log'])==c['log_sha256']
for r,h in F['files'].items():assert sha(P/r)==h,r
assert len(F['files'])==68 and len(F['source_files'])==16
assert not (P/'Solution.lean').exists() and not list((P/'NLA').rglob('Proof.lean'))
report.write_text('''# RA-20 independent statement review 1

**APPROVE the exact frozen statements for proof implementation, subject to the separate two-review coordinator gate.** No existing theorem is proved or marked Lean verified by this review.

Reviewer `/root`, 13 September 2026. I did not author or edit RA-20's definitions, mathematical/numerical contracts or proof. My prior work on other campaign problems does not supply an RA-20 approval. Statement author `/root/formal_review_standards` is distinct from both assigned statement referees. A later implementation contribution would make me ineligible as an independent final mathematical referee.

## Exact target and definitions

I read the complete canonical original statement, complete Markdown/TeX resolution, original independent informal audit and numerical record, all149 lines of Definitions, all12 Challenge contracts, NUMERICAL_TARGETS, SourceCorrespondence, README and the applicable repository review policy. The frozen boundary is reviews/statement-freeze.json SHA256 6bd2bbf4a6d787fd4e0c5c8b19aad74dac73b7e79c9552e537544136a4812aa8: 68 project inputs and16 original source/policy Git files, all independently rehashed against the actual source objects.

The canonical target is the joint four-formula generic smooth critical-point assertion over complex symmetric rank-at-most-two matrices with the first s diagonal entries zero, for every n>=3 and1<=s<=min(4,n). Definitions retains all four formulas and that full range. Natural subtraction is harmless in precisely that range. The allowed n=s=3 specialization predicts4; the proposed complete negation does not replace the target by an isolated fixed-order theorem.

`variety` uses actual Matrix.IsSymm and Matrix.rank. The reduced ring is the quotient by every polynomial vanishing on the actual point set. `SmoothPoint` requires a genuine point prime mapping to the evaluation prime and membership in actual `Algebra.smoothLocus`; it is not defined as the rank-two stratum or ExactlyOneZero. The independently printed library definition is formal smoothness of the coordinate ring localized at that prime. For this finite-type reduced complex affine variety this is the appropriate algebraic smoothness notion. The coordinate-preserving quotient-ring isomorphism and smoothness equivalence remain explicit theorem obligations, not assumptions in the final target.

`TangentVector` annihilates differentials of the entire reduced ideal. Its contract includes singular intersections and imposes the symmetry/zero-diagonal linear constraints; it does not omit extra ideal equations. `SmoothCriticalPoint` differentiates the actual full-entry distance in actual complex Fréchet calculus. All off-diagonal entries are counted twice on symmetric matrices; there is no complex conjugation or Hermitian norm. The full-distance derivative contract prevents reliance on fderiv's nondifferentiability fallback. The objective is polynomial, so ordinary differentiability is available to a future proof.

`HasCriticalCount` uses Cardinal.mk of the actual critical set, avoiding any finite-count default for infinite sets. The exceptional polynomial may be arbitrary but must be nonzero at some symmetric datum. Thus genericity is a genuine nonempty principal open subset of the full symmetric data space. This formulation is equivalent to holding off a proper algebraic exceptional set: one nonzero defining polynomial supplies a contained principal open; conversely its zero set is proper. The separate intersection contract prevents silently replacing an unknown generic set by the source's chosen one.

## Counterexample obligations and boundary checks

The matrix/determinant contract correctly identifies det(hollow(a,b,c))=2abc and rank<=2 exactly with abc=0. The reduced ring and actual smooth-locus bridges require proving that only points lying on exactly one plane are smooth; rank-two axis points remain singular. The tangent contract has the correct gradient coefficients bc,ac,ab, including intersections. The full metric has coefficient2 on each off-diagonal square; each component Hessian is4I and is stated using actual second derivatives with zero kernel.

For nonzero off-diagonal data alpha,beta,gamma, the three proposed points are distinct and each has exactly one zero coordinate. Informally differentiating the two free coordinates on a component gives precisely its projected datum. The arbitrary diagonal data only add a constant. This is a sanity check of the stated contracts, not a formal proof of their geometric obligations. All critical points must still be exhausted, generic-open intersection proved, and actual finite cardinality established. Neither one rational sample nor a chosen three-element list is defined to be the critical set. The generic count three and impossibility of generic count four then suffice to negate the original conjunction; other parameter formulas and corrected sequences are not claimed.

I directly opened the primary [author paper](https://arxiv.org/pdf/2010.15636v2), checking its distance/genericity conventions and Conjecture5.6/Table7 on printed page21. Those records support the retained source convention and formula, while the exact formal target is the repository's canonical statement. The first HTML fetch failed; the PDF fetch succeeded. No external theorem about this particular critical count is assumed.

## Actual independent checks and trust

My three fresh direct-source commands compiled Definitions, the isolated twelve-hole Challenge and an independently written definition inspector. All succeeded without correction. The inspector printed the actual target, genericity, smoothness, tangent, differential/cardinal definitions and library APIs; checked actual finite-dimensional complex matrix and algebraically closed field instances; and reduced the relevant predicted counts to(4,7,4,28). Ten explicit LeanCert kernel assertions passed: nine definitions have exactly the standard three axioms, and predictedCount is axiom-free. Only the twelve deliberate reference holes warned, solely in Challenge. The inspector imports Definitions and LeanCert verification, not Challenge. No theorem implementation was supplied.

The prefix was initially empty. Ten exact dependency revisions were reused read-only from the pinned MI22 cache and checked clean both before and after. No prior target object, Lake invocation, download or dependency rebuild was used. This is local macOS statement review, not actual Linux Comparator or proof acceptance. Lean4.33.1, Mathlib0df444a360eaa60ab8c11dca51a86af692955474 and LeanCert621a43d7cf21f87872392a01e874f2f1dbddc926 remain unchanged. Exact algebra requires no numerical interval certificate; future proof exports still require material kernel-trust/axiom checks and authoritative Linux default-kernel/Comparator controls.

All68 frozen inputs and16 original source identities remain unchanged. The small root-owned compiled objects were recorded and removed after completion; no shared cache or source was changed. Complete source snapshots, commands, actual output and hashes are retained in the adjacent evidence directory.

## Disposition and attribution

No semantic correction requested. Genuine quotient/localization smoothness and full-ideal tangent identification are substantial outstanding proof work and must not be weakened if implementation is difficult. Future proof code needs two independent final mathematical referees who are not contributors, full Linux verification and truthful v0.4 metadata before any status promotion. This review supplies one independent statement approval only.

George Stepaniants receives formalization credit with Department of Computing and Mathematical Sciences, California Institute of Technology, Pasadena, California, USA, without email. The original Codex maintainer audit's mathematical provenance and Kubjas–Sodomaco–Tsigaridas question attribution remain intact. No external human review, official Tau Ceti endorsement or mathematical priority is claimed.
''')
# Normalize readable count/reference spacing in this new report only.
s=report.read_text()
for a,b in {'all149':'all 149','all12':'all 12','and16':'and 16','and1<=':'and 1<=','predicts4':'predicts 4','coefficient2':'coefficient 2','is4I':'is 4I','Conjecture5.6/Table7':'Conjecture 5.6/Table 7','page21':'page 21','to(4,7,4,28)':'to (4, 7, 4, 28)','Lean4.33.1':'Lean 4.33.1','Mathlib0df':'Mathlib 0df','LeanCert621':'LeanCert 621','All68':'All 68'}.items():s=s.replace(a,b)
report.write_text(s)
prefix=Path(res['prefix']);deleted=[]
for row in res['generated_objects']:
 f=prefix/row['path'];assert sha(f)==row['sha256'] and f.stat().st_size==row['bytes'];assert f.suffix in ['.olean','.ilean'];f.unlink();deleted.append(row)
(D/'cleanup.json').write_text(json.dumps({'scope':'Only own completed target-prefix .olean/.ilean objects removed after matching recorded hashes','objects':deleted,'bytes':sum(x['bytes'] for x in deleted),'shared_cache_touched':False},indent=2)+'\n')
(D/'seal.py').write_bytes(Path(__file__).read_bytes());outer=D/'EVIDENCE-MANIFEST.json';files={str(f.relative_to(D)):dict(sha256=sha(f),bytes=f.stat().st_size) for f in sorted(D.rglob('*')) if f.is_file() and f!=outer};files['../statement-referee-1.md']={'sha256':sha(report),'bytes':report.stat().st_size};outer.write_text(json.dumps({'reviewer':'/root','files':files,'file_count':len(files),'inventory_rule':'All actual evidence recursively plus adjacent report; exact outer self-exclusion only'},indent=2)+'\n');print(json.dumps({'report_sha256':sha(report),'outer_sha256':sha(outer),'bound_files':len(files),'fresh_commands':3,'kernel_assertions':10,'standard_three_reports':9,'axiom_free_reports':1},indent=2))
