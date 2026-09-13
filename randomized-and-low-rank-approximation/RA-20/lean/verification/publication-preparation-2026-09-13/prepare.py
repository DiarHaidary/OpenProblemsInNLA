#!/usr/bin/env python3
"""Install concrete RA20 publication documents after the accepted Linux gate."""
from pathlib import Path
import hashlib,json,shutil,yaml
D=Path(__file__).resolve().parent
R=Path('/tmp/nla-lean-ra20-worktree').resolve()
P=R/'randomized-and-low-rank-approximation/RA-20/lean'
E=P/'verification/publication-preparation-2026-09-13'
C='43603b173beb294c2588d83f936a8a96246fd5f0'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
b=json.loads((D/'PREFLIGHT.json').read_text())
assert b['status']=='PUBLICATION_PREAUTHOR_GATE_PASS' and not E.exists()
for n,v in b['project_baseline'].items():assert sha(P/n)==v['sha256'],n
for n,v in b['other_publication_inputs'].items():assert sha(R/n)==v['sha256'],n
assert json.loads((D/'artifact-operation-result.json').read_text())['exit_code']==0
E.mkdir()
for q in D.iterdir():
 if q.is_file():shutil.copyfile(q,E/q.name)
archives=[]
for n,label in [('README.md','candidate-README.md'),('formalization.yaml','candidate-formalization.yaml')]:
 q=E/'archive'/label;q.parent.mkdir(exist_ok=True);shutil.copyfile(P/n,q)
 archives.append({'original_repository_path':str((P/n).relative_to(R)),'expected_sha256':sha(q),'archive_project_path':str(q.relative_to(P))})
for n,v in b['other_publication_inputs'].items():
 q=E/'archive/repository'/n;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/n,q)
 archives.append({'original_repository_path':n,'expected_sha256':v['sha256'],'archive_project_path':str(q.relative_to(P))})
(E/'ARCHIVES.json').write_text(json.dumps({'rule':'Map only the exact original repository path together with its exact expected prepublication SHA256; preserve all other paths/hashes. The earlier old README mapping remains separately valid.','archives':archives},indent=2)+'\n')

readme=(P/'README.md').read_text()
start=readme.index('Formalization author:')
readme='''# RA-20 Lean proof and accepted verification

The complete twelve-export proof **refutes the original joint critical-count
conjecture**: the genuine generic count at the allowed parameters `n=s=3` is
three, whereas its formula predicts four. Two independent final mathematical
reviews, independent candidate packaging and operational reviews, and the
[coordinator's accepted Linux verification](verification/root-linux-acceptance-2026-09-13/ROOT-ACCEPTANCE.json)
support **Lean verified** status. This publication is prepared for a separate
independent publication review; its new upstream pull request is still pending.

'''+readme[start:]
readme=readme.replace('## Statements, reviews and retained evidence','## Reviewed evidence')
old='''The accepted [final-review gate](verification/final-review-acceptance.json)
has SHA-256 `a1c7ffebd2c0db8159b9861adf3663051b8e03346b776393553773d97e0abbbb`.
This documentation was subsequently prepared by `/root/ra20_final_referee1`.
That document-author role adds no independent mathematical or packaging
approval. A different reviewer must inspect this concrete installation before
a candidate commit and Linux run. No candidate Git revision or Linux run is
asserted at this stage.
'''
new='''The accepted [final-review gate](verification/final-review-acceptance.json)
has SHA-256 `a1c7ffebd2c0db8159b9861adf3663051b8e03346b776393553773d97e0abbbb`.
The [independent candidate packaging review](reviews/candidate-packaging-referee-2026-09-13.md)
preceded the committed candidate. `/root/ra20_final_referee1` subsequently
authored the candidate and publication documents; that author role adds no
independent approval of its own packaging or publication.

## Actual Ubuntu verification - 13 September 2026

[Immutable proof revision](https://github.com/sgstepaniants/OpenProblemsInNLA/tree/43603b173beb294c2588d83f936a8a96246fd5f0/randomized-and-low-rank-approximation/RA-20/lean)
`43603b173beb294c2588d83f936a8a96246fd5f0` passed
[run 34743832047](https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34743832047),
attempt 1, on non-root Ubuntu 24.04. All 17 workflow jobs succeeded, including
the RA-20 job and separate checker-controls job. The actual default Lean kernel
replayed the exported solution, and the real Comparator matched all twelve
frozen contracts with no definition exceptions. This catalog ran that Linux
workflow and reviewed its original artifacts; no local macOS Comparator
execution is claimed.

The actual source build passed **61 LeanCert kernel assertions** and printed
**57 axiom reports covering 45 distinct declaration names**. Every report
contains only `propext`, `Classical.choice`, and `Quot.sound`. The additional
twelve diagnostic prints in each earlier local review account for its 69
reports and are not part of the authoritative source run. Challenge's
deliberate reference admissions are isolated from Solution.

Both the standalone checker and RA-20 preproof controls passed: two sandbox
modes, four unsupported-option rejections, three raw default-kernel controls,
five Comparator fixtures and two forbidden-axiom controls. The invalid proof,
quotient mismatch, statement/kind/helper mismatch, `sorry` and native-execution
fixtures fail at their intended gates. In the nested-namespace check, bwrap
ran but UID-map setup was denied before the inner write; no executed inner
write syscall is claimed. The original control and isolation logs are retained.

The fresh project compiled the proof using all ten pinned dependencies and
**8,690 official matching Mathlib cache files**. This was not a from-source
rebuild of all Mathlib. The toolchain, dependency objects, trusted Challenge,
exporter, default kernel and checker infrastructure remain the disclosed trust
boundary. Exact algebra removes numerical interval computations.

The [independent operational report](reviews/linux-operational-referee-2026-09-13.md)
and [complete original runtime evidence](verification/linux-run-2026-09-13/runtime-verification.json)
bind all **1,092 candidate Git inputs**, every artifact and all source/line
axiom records. The operational seal has 1,589 entries. The coordinator rechecked
and accepted it in the [root acceptance](verification/root-linux-acceptance-2026-09-13/ROOT-ACCEPTANCE.json),
SHA-256 `a2c3a74eb858edb859d34d8bd2985dc54710e31816412d285c32a547e080e57e`;
its complete seal binds 1,604 files. These are accepted mechanical verification
results, not an additional independent mathematical approval.
'''
assert old in readme;readme=readme.replace(old,new)
old='''The [candidate installation record](verification/linux-candidate-2026-09-13/HANDOFF.md)
and its verifier preserve the complete prior inventory through that one
archived README; historical manifests bind their original version.
'''
new='''The [candidate installation record](verification/linux-candidate-2026-09-13/HANDOFF.md)
is a dated record. The exact checked candidate
[README](verification/publication-preparation-2026-09-13/archive/candidate-README.md)
and [metadata](verification/publication-preparation-2026-09-13/archive/candidate-formalization.yaml)
are now archived at their original SHA-256 values. The
[publication handoff and read-only verifier](verification/publication-preparation-2026-09-13/HANDOFF.md)
check every historical manifest with strict exact-path plus expected-hash
archive mappings, including both old README versions and the canonical page.
No proof, frozen statement, dependency pin or previous review/evidence file
was changed for publication. Older pending-phase notices are superseded by the
accepted gates and this current documentation.
'''
assert old in readme;readme=readme.replace(old,new)
readme=readme.replace('the retained fresh direct-source reviewer logs describe','the retained fresh direct-source reviewer logs describe')
readme=readme.replace('''After independent packaging review and a clean committed candidate, run the
authoritative commands **from the repository root on non-root Ubuntu**, with
the [Linux prerequisites and isolation](../../../tools/lean/HARNESS.md) ready:''','''To reproduce the accepted run, use a clean checkout of immutable revision
`43603b173beb294c2588d83f936a8a96246fd5f0`. Run the authoritative commands
**from the repository root on non-root Ubuntu**, with the
[Linux prerequisites and isolation](../../../tools/lean/HARNESS.md) ready:''')
old='''These commands are **pending**, not a report of execution. They must use the
actual pinned exporter/default kernel and [Lean Comparator](https://github.com/leanprover/comparator),
real isolation and the complete rejection/control suite. Independent
operational review and reviewed canonical Markdown/TeX/PDF/index changes must
follow before any `Lean verified` status or upstream publication claim.
'''
new='''These are the repository commands whose actual Linux workflow result is
recorded above. They use the pinned exporter/default kernel and
[Lean Comparator](https://github.com/leanprover/comparator), real isolation and
the complete rejection/control suite. The concrete canonical Markdown/TeX/PDF,
metadata and indexes receive a separate publication review before the new
individual pull request to upstream main. No upstream acceptance is claimed.
'''
assert old in readme;readme=readme.replace(old,new)
(P/'README.md').write_text(readme)

metadata=yaml.safe_load((P/'formalization.yaml').read_text())
metadata['repository']['revision']=C
metadata['repository']['note']='Immutable proof and Linux-checked candidate revision; current publication wrappers archive its exact metadata and README. No final publication commit or upstream acceptance is asserted.'
metadata['status']['scope']='Complete twelve-export negative proof of the full original joint generic smooth critical-count conjecture, using its allowed n=s=3 case. Two independent statement approvals preceded implementation; two final mathematical approvals, independent candidate packaging, and actual Ubuntu default-kernel/Comparator/control verification were accepted by the coordinator. Canonical Lean verified publication is prepared for a separate independent publication review; the new upstream main pull request remains pending.'
metadata['review']['status']='agent-reviewed; mathematical-packaging-operational-reviews-accepted; actual-Linux-kernel-and-Comparator-pass; independent-publication-review-pending'
metadata['review']['reviewers'].append('OpenAI Codex agent /root/ra20_final_referee2: independent candidate-packaging and actual Linux operational reviewer; these mechanical audits add no extra mathematical approval')
metadata['review']['notes'] += ' Actual Ubuntu run 34743832047 for immutable revision '+C+' passed all 17 workflow jobs. Its source build passed 61 LeanCert kernel assertions and printed 57 standard-three axiom occurrences for 45 distinct names; historical local diagnostic prints are separate. Both actual control suites passed. All 1092 candidate inputs match the receipt. Official matching Mathlib cache decompressed 8690 files across the ten pinned dependencies; no full from-source dependency rebuild is claimed. The coordinator accepted the independently audited operational result before publication preparation.'
metadata['review']['linux_verification']={
 'status':'passed; independently operationally audited and coordinator accepted',
 'candidate_revision':C,'date':'2026-09-13','run':'https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34743832047',
 'run_attempt':1,'successful_jobs':17,'host':'Non-root Ubuntu 24.04, sandbox UID 1001',
 'actual_default_kernel':'pass','actual_Comparator':'pass, twelve exports, no definition exceptions',
 'actual_control_suites':'pass, standalone checker and RA20 preproof',
 'source_kernel_assertions':61,'source_printed_axiom_occurrences':57,'source_distinct_printed_names':45,
 'candidate_inputs':1092,'official_matching_dependency_cache_files':8690,
 'dependency_scope':'Fresh project proof compilation against ten exact dependency revisions and official matching Mathlib cache; not a from-source rebuild of all Mathlib',
 'operational_report':{'file':'reviews/linux-operational-referee-2026-09-13.md','sha256':'7f7532bbc01533d0c35fe0ac3aece0ff66cb43c1444e41275db0784cee6b8ae7'},
 'complete_operational_inventory':{'file':'verification/linux-run-2026-09-13/EVIDENCE-MANIFEST.json','sha256':'89b3cd2aa8c47835be4531cca85561a70aee7f20be6e9f3bcdaaa48d23812dcd','bound_files':1589},
 'root_acceptance':{'file':'verification/root-linux-acceptance-2026-09-13/ROOT-ACCEPTANCE.json','sha256':'a2c3a74eb858edb859d34d8bd2985dc54710e31816412d285c32a547e080e57e'},
 'root_complete_inventory':{'file':'verification/root-linux-acceptance-2026-09-13/EVIDENCE-MANIFEST.json','sha256':'40d68224c966fc5114995418bf47ee2fc38f3ebbacc50536cae3b1c9d98ca0b8','bound_files':1604},
 'scope_note':'This catalog ran the GitHub Linux workflow and reviewed its original artifacts; no local macOS Comparator execution or new Linux execution during publication preparation is claimed. In the nested-namespace control, bwrap ran but UID-map setup was denied before the inner write.'}
metadata['review']['candidate_documents']['independent_packaging_review']='passed and coordinator accepted before candidate commit and actual Linux run'
metadata['review']['candidate_documents']['installation']='Historical candidate wrapper installation; exact checked bytes now archived in publication-preparation-2026-09-13/archive. All earlier seals remain unchanged.'
metadata['review']['publication']={
 'author':'/root/ra20_final_referee1','role':'Previously independent final mathematical referee 1, then candidate-document and publication author; no independent approval of own publication',
 'status':'prepared for separate independent publication review; no new publication commit, push or PR yet',
 'candidate_README_archive':'verification/publication-preparation-2026-09-13/archive/candidate-README.md',
 'candidate_README_sha256':'83e19faf1bf25a9748de40da3193cfd68690100923a50379553e288c45b5e8bc',
 'candidate_YAML_archive':'verification/publication-preparation-2026-09-13/archive/candidate-formalization.yaml',
 'candidate_YAML_sha256':'bec9d851e204464fa2d3e29033d5958034665d51c3554d2043f1470bfafd4197',
 'preservation':'Every historical inventory is checked by exact original path and expected hash. The original old-README mapping remains, and exact candidate README/YAML and canonical-page archives preserve later expected versions. No proof, frozen statement, pin or prior evidence is edited.',
 'handoff':'verification/publication-preparation-2026-09-13/HANDOFF.md'}
metadata['reproduction']['authoritative_Linux']['status']='Actual run passed and operational acceptance recorded; commands reproduce the immutable candidate'
metadata['reproduction']['authoritative_Linux']['candidate_revision']=C
metadata['reproduction']['authoritative_Linux']['note']='From a clean checkout of the exact candidate on non-root Ubuntu. Both real control suites, statement Comparator and default-kernel replay passed in the recorded original workflow; independent publication review and upstream submission remain separate.'
class Dumper(yaml.SafeDumper):
 def ignore_aliases(self,data):return True
(P/'formalization.yaml').write_text('# yaml-language-server: $schema=../../../docs/lean/schema/v0.4.schema.json\n'+yaml.dump(metadata,Dumper=Dumper,allow_unicode=True,sort_keys=False,width=104))

canonical=(P.parent/'README.md').read_text()
canonical=canonical.replace('**Status:** Solved  \n**Last checked:** 2026-09-11','**Status:** Lean verified  \n**Last checked:** 2026-09-13')
canonical=canonical.replace('It is automated-agent verification, not external human peer review or formal certification.','That dated audit was automated-agent review. The separate Lean verification below certifies the complete original negative target; external human peer review is not claimed.')
section='''## Lean proof and verification evidence - 2026-09-13

**Formalization:** George Stepaniants, Department of Computing and Mathematical Sciences, California Institute of Technology, Pasadena, California, USA, with AI-agent assistance. The **Codex automated maintainer audit** retains credit for the original negative resolution; Kubjas, Sodomaco and Tsigaridas retain credit for the conjecture.

The [proof at immutable revision 43603b17](https://github.com/sgstepaniants/OpenProblemsInNLA/blob/43603b173beb294c2588d83f936a8a96246fd5f0/randomized-and-low-rank-approximation/RA-20/lean/Solution.lean) proves `NLA.RA20.not_criticalCountConjecture`: the full original four-formula conjecture is false, since the genuine generic count at $`n=s=3`$ is three, not its predicted four. The original complex field, symmetry, rank bound, zero-diagonal constraints, bilinear full-Frobenius metric and all quantifiers remain. The other formulas are not separately settled.

All twelve checked exports have namespace `NLA.RA20`:

- `hollow_variety_semantics`; `reduced_coordinate_ring`.
- `algebraic_smooth_locus`; `algebraic_tangent_space`.
- `full_frobenius_differential`; `hollow_distance_semantics`.
- `generic_critical_locus`; `component_hessians`.
- `generic_data_intersection`; `generic_count_three`.
- `generic_count_not_four`; `not_criticalCountConjecture`.

The definitions use the actual reduced coordinate ring modulo the **entire vanishing ideal**, its genuine algebraic smooth locus and whole-ideal tangent space, actual complex derivatives, and the cardinality of the full smooth critical-point subtype. Arbitrary nonempty generic opens are compared on the complete symmetric data space. Every bridge and every premise needed to refute the target is proved, with no new unproved literature assumption. The [proof map](lean/PROOF_MAP.md), [exact contracts and metadata](lean/formalization.yaml), and [detailed proof scope](lean/README.md) identify the correspondence. Exact algebra eliminates interval computations; LeanCert audits kernel trust. The source comment describing a complete local ring denotes ordinary `Localization.AtPrime`, not an adic completion. Hessian nondegeneracy is proved; no separate scheme-theoretic multiplicity theorem is claimed.

Two independent statement reviews preceded implementation; two independent final mathematical reviews and independent packaging review passed. This catalog ran [Ubuntu workflow 34743832047](https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34743832047) on 13 September 2026 and reviewed its original artifacts. The real Comparator matched all twelve exports without definition holes, and Lean's default kernel replayed the solution. All **61 LeanCert kernel assertions** passed; **57 source axiom reports, covering 45 distinct names**, contain only `propext`, `Classical.choice` and `Quot.sound`. Both real control suites passed as a non-root user, including invalid-proof, statement-mismatch, quotient and forbidden-axiom rejection. All 17 workflow jobs succeeded. The [independent operational report](lean/reviews/linux-operational-referee-2026-09-13.md), [original successful log and artifacts](lean/verification/linux-run-2026-09-13/runtime-verification.json), and [coordinator acceptance](lean/verification/root-linux-acceptance-2026-09-13/ROOT-ACCEPTANCE.json) bind all 1,092 candidate inputs. Local macOS development checks are separate.

The checked toolchain is **Lean 4.33.1**. Dependency revisions are:

- Mathlib: `0df444a360eaa60ab8c11dca51a86af692955474`.
- LeanCert: `621a43d7cf21f87872392a01e874f2f1dbddc926`.

The [Lake manifest](lean/lake-manifest.json) pins all ten dependencies. The fresh proof build used 8,690 official matching Mathlib cache files, rather than rebuilding all dependencies from source. To reproduce from a clean checkout of revision `43603b173beb294c2588d83f936a8a96246fd5f0`, use a non-root Linux host with the [documented prerequisites](../../tools/lean/HARNESS.md) and run from the repository root:

```
tools/lean/bootstrap.sh /tmp/nla-ra20-check
tools/lean/selftest.sh /tmp/nla-ra20-check
tools/lean/verify.sh \\
  randomized-and-low-rank-approximation/RA-20/lean \\
  /tmp/nla-ra20-check
```

These commands run the actual controls, Comparator, permitted-axiom checks and default-kernel replay. A local `lake build Solution` is a separate development check; the historical default build target is Challenge. All original statement and source material below remains unchanged.

'''
assert canonical.count('## Statement\n')==1
canonical=canonical.replace('## Statement\n',section+'## Statement\n')
original=(E/'archive/repository/randomized-and-low-rank-approximation/RA-20/README.md').read_text()
assert canonical[canonical.index('## Statement\n'):]==original[original.index('## Statement\n'):]
(P.parent/'README.md').write_text(canonical)

resolved=(R/'RESOLVED.md').read_text()
old='The ID and canonical path are retained; verification is by automated agents, not external human peer review or formal certification.'
assert old in resolved
new='The ID and canonical path are retained; that original audit was by automated agents. The separate full-target Lean verification below supersedes its informal-only status; external human peer review is not claimed.'
resolved=resolved.replace(old,new,1)
note='''

**Lean verified - 2026-09-13. Lean formalization:** George Stepaniants, Department of Computing and Mathematical Sciences, California Institute of Technology, Pasadena, California, USA, with AI-agent assistance. Original negative-resolution credit remains with the Codex automated maintainer audit, and original conjecture credit with Kubjas, Sodomaco and Tsigaridas. The [twelve exported theorems](https://github.com/sgstepaniants/OpenProblemsInNLA/blob/43603b173beb294c2588d83f936a8a96246fd5f0/randomized-and-low-rank-approximation/RA-20/lean/Solution.lean) prove the actual reduced-ring, smooth-locus, tangent, derivative and generic-cardinality bridges and negate the complete original four-formula conjecture at its allowed case n=s=3. [Ubuntu run 34743832047](https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34743832047) matched every frozen export and replayed the solution through Lean's default kernel, with 61 LeanCert kernel assertions and 57 source reports allowing only the standard three axioms. The [canonical proof and verification evidence](randomized-and-low-rank-approximation/RA-20/README.md#lean-proof-and-verification-evidence---2026-09-13) gives immutable sources, pins, commands, two independent mathematical reviews and the accepted operational audit. The other individual formulas and a separate scheme-multiplicity theorem remain outside the claims.
'''
start=resolved.index('### RA-20 - ');end=resolved.index('\n### ',start+1)
resolved=resolved[:end]+note+resolved[end:]
(R/'RESOLVED.md').write_text(resolved)
print(json.dumps({'status':'PUBLICATION_TEXT_INSTALLED; canonical PDF and author validation pending','archives':len(archives),'README_sha256':sha(P/'README.md'),'YAML_sha256':sha(P/'formalization.yaml'),'canonical_README_sha256':sha(P.parent/'README.md'),'independent_publication_review':'pending'}))
