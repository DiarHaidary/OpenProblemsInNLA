#!/usr/bin/env python3
"""Build RA20-specific v0.4 candidate metadata from accepted project identities."""
from pathlib import Path
import hashlib,json,yaml
D=Path(__file__).resolve().parent
P=Path('/tmp/nla-lean-ra20-worktree/randomized-and-low-rank-approximation/RA-20/lean')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
g=json.loads((P/'verification/final-review-acceptance.json').read_text())
assert sha(P/'verification/final-review-acceptance.json')=='a1c7ffebd2c0db8159b9861adf3663051b8e03346b776393553773d97e0abbbb'
names=json.loads((P/'comparator.json').read_text())['theorem_names']
base='https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/5830ed4fb06da0659414a3deb2a40ad327aca052/'
aff='Department of Computing and Mathematical Sciences, California Institute of Technology, Pasadena, California, USA'
scopes={
 'hollow_variety_semantics':'The actual complex hollow determinant is 2abc; membership in the original rank-at-most-two, three-diagonal-zero variety is equivalent to abc=0, and every original matrix has that hollow form.',
 'reduced_coordinate_ring':'An actual coordinate-preserving algebra equivalence takes the quotient by all polynomials vanishing on the original matrix variety to C[a,b,c]/(abc), with all nine matrix-coordinate images proved.',
 'algebraic_smooth_locus':'Actual point-prime membership in the algebraic smooth locus of the reduced matrix ring is equivalent to hollow form and exactly one zero off-diagonal coordinate; origin and axis intersections are excluded even if matrix rank is two.',
 'algebraic_tangent_space':'At every abc=0 point, including singular points, annihilation of derivatives of the entire original vanishing ideal is equivalent to symmetry, zero diagonal, and bc Z01 + ac Z02 + ab Z12 = 0, with no rank restriction on directions.',
 'full_frobenius_differential':'For every natural matrix order and every complex U,X,Z, the actual complex Frechet derivative of the full-entry squared distance equals 2 sum_ij (Xij-Uij) Zij; differentiability is proved.',
 'hollow_distance_semantics':'For arbitrary complex symmetric data, the full Frobenius bilinear objective restricts to the diagonal constant plus twice the three off-diagonal squared differences, without conjugation.',
 'generic_critical_locus':'For every symmetric complex datum with nonzero off-diagonal product, the entire genuine smooth critical set equals the injective range of its three component projections.',
 'component_hessians':'For every complex datum, even nonsymmetric, all three component charts have actual second complex Frechet derivative 4 sum_j h_j v_j and zero radical. No separate scheme-theoretic multiplicity result is exported.',
 'generic_data_intersection':'Every arbitrary ambient polynomial nonzero somewhere on symmetric complex data remains nonzero at some datum in the displayed generic set; the full six-dimensional symmetric data space and arbitrary diagonals are retained.',
 'generic_count_three':'Actual smooth critical-subtype cardinality is three on a nonempty principal Zariski-open subset of symmetric complex data.',
 'generic_count_not_four':'No nonempty principal Zariski-open subset of symmetric complex data can support a competing actual generic count four.',
 'not_criticalCountConjecture':'Unconditional negation of the complete original joint four-formula generic critical-count conjecture for all n>=3 and 1<=s<=min(4,n), by its allowed n=s=3 case. The other formulas are not separately settled.'}
assert set(names)=={'NLA.RA20.'+n for n in scopes}
def identity(path):return {'file':path,'sha256':sha(P/path)}
data={
 'version':'v0.4',
 'project':{'name':'RA-20: critical-point counts for symmetric rank-two approximation with diagonal zeros',
   'description':'Complete negative resolution of the original joint generic critical-count conjecture: the actual count at n=s=3 is three, whereas its formula predicts four.',
   'authors':['George Stepaniants'],'affiliations':{'George Stepaniants':aff},'responsible_maintainers':['George Stepaniants'],'license':'Apache-2.0'},
 'repository':{'role':'substantive-development'},
 'sources':[
  {'title':'RA-20 — Critical-point counts for symmetric rank-two approximation with diagonal zeros',
   'id':base+'randomized-and-low-rank-approximation/RA-20/README.md','type':'web-post',
   'location':'Complete retained original statement, all four formulas and their common parameter range',
   'relationship':'formalizes','author_endorsement':'not-contacted',
   'note':'All complex symmetric rank-at-most-two matrices with the prescribed diagonal zeros; generic smooth critical-point counting in the complex bilinear full-Frobenius metric. The full original conjunction is negated, not replaced by a weaker fixed-case target.'},
  {'title':'RA-20: A counterexample to the symmetric rank-two critical-point formula',
   'authors':['Codex automated maintainer audit'],'id':base+'randomized-and-low-rank-approximation/RA-20/solution.md',
   'type':'manuscript','location':'Proposition and complete proof, with the retained independent reconstruction in references/research-expansion-2026-09-11/ra20-resolution/',
   'relationship':'formalizes','author_endorsement':'n/a',
   'note':'The original negative-resolution mathematics remains attributed to the automated maintainer audit. The formal proof derives the actual reduced coordinate ring, smooth locus, entire-ideal tangent, genuine derivatives, generic-open intersection and actual cardinality. No external human author endorsement or mathematical priority is asserted.'},
  {'title':'Exact solutions in low-rank approximation with zeros','authors':['Kaie Kubjas','Luca Sodomaco','Elias Tsigaridas'],
   'id':'https://arxiv.org/abs/2010.15636v2','type':'preprint',
   'location':'Section 2.2 complex bilinear smooth critical-point convention, Section 2.3 full Frobenius distance, Conjecture 5.6 and Table 7 on printed p.21',
   'relationship':'background','author_endorsement':'not-contacted',
   'note':'Original conjecture and conventions. The source formula gives four at n=s=3. The negative resolution proves three independently of that assertion; no unproved critical-count theorem from this paper is a premise.'}],
 'related_formalizations':[
  {'id':'https://github.com/sgstepaniants/Forsythe/tree/8d1b0c0545a77b40245e84705aa7d273e6c81e62/lean-proof','relationship':'other',
   'note':'Pinned statement/proof, minimized computation, LeanCert kernel trust and Comparator reproduction patterns used by the shared campaign infrastructure. No Forsythe mathematical theorem or proof module is imported.'},
  {'id':'https://github.com/jaumededios/Schiffer/tree/2938e277969c329caf154e48a3d8823f3635c7f1','relationship':'other',
   'note':'Pinned exact mathematical statement/proof separation example. No Schiffer theorem or proof implementation is assumed.'}],
 'automation':{'methods':[{'method':'agent','framework':'OpenAI Codex',
   'tool_setup':'Multiple implementation agents; two independent statement reviews accepted before proof work; two fresh independent final mathematical referees with source, exact-type, actual-dependency, axiom and initially empty private-prefix compilation checks, accepted by the coordinator.',
   'prompting_notes':'Preserve all original complex symmetric matrix, rank, full-vanishing-ideal, point-prime smoothness, genuine Frechet derivative, bilinear full-Frobenius, nonempty generic-open and actual cardinality semantics. Prove the substantial geometric bridges. Eliminate interval work with exact algebra, localization and a fixed three-coordinate counterexample; retain all original universal formulas in the final negation.'}],
   'notes':'AI-assisted formalization requested by George Stepaniants. Implementers: /root/formal_review_standards (statements, Algebra, Tangent, Count, Proof, Solution); /root/leancert_examples (Smooth, Critical); /root/mf16_final_referee (Differential); /root (SmoothTransport, Generic), with Generic scoped inspection/sealing by /root/mf16_final_referee. None counts as an independent final mathematical referee. Final referees /root/ra20_final_referee1 and /root/ra20_final_referee2 are distinct from them. The first final referee subsequently authored these candidate documents, adding no independent mathematical or packaging approval. No external human review, official Tau Ceti endorsement, source-author endorsement or priority is claimed.'},
 'status':{'scope':'Complete twelve-export negative proof of the full original joint generic smooth critical-count conjecture, using its allowed n=s=3 case. Two independent statement approvals preceded implementation; two independent final mathematical approvals are sealed and accepted by the coordinator. Concrete candidate packaging review, actual non-root Ubuntu default-kernel/Comparator/control verification, independent operational acceptance and canonical publication remain pending. Canonical status remains Solved. Local macOS evidence does not yet promote it to Lean verified.',
   'sorry_count':0,'sorry_in_definitions':0,'axioms':['propext','Classical.choice','Quot.sound'],
   'main_results':[{'declaration':n,'file':'Solution.lean','sorry_count':0,'axioms':['propext','Classical.choice','Quot.sound'],
     'comparator_config':'comparator.json','literature_dependencies':[]} for n in names]},
 'toolchain':{'lean':'leanprover/lean4:v4.33.1','dependency_manifest':'lake-manifest.json',
   'dependencies':{x['name']:x['rev'] for x in json.loads((P/'lake-manifest.json').read_text())['packages']},
   'trust':'LeanCert #assert_trust kernel; standard foundational axioms only; no native execution or interval certificate'},
 'fidelity':{'divergences':'The full canonical target and all original assumptions, quantifiers, complex field and bilinear full-entry metric are retained. The informal Jacobian smoothness explanation is implemented through genuine localized algebraic smoothness, retractions and a square-zero lifting obstruction. The whole-ideal tangent and arbitrary generic-open intersection are proved. Supporting derivative/Hessian statements are generalized where stated. Only the full original conjunction is refuted; the remaining individual formulas and corrected values are not settled. The source abcLocalChart comment uses complete local ring for the ordinary localization: no adic completion or completeness theorem is claimed. Hessian nondegeneracy is exported, but no separate scheme-theoretic multiplicity theorem is formalized.'},
 'review':{'status':'agent-reviewed; coordinator-accepted; concrete-packaging-and-authoritative-Linux-verification-pending',
   'reviewers':[
    'OpenAI Codex agent /root: independent historical statement referee 1, subsequently a proof contributor and ineligible as an independent final mathematical referee',
    'OpenAI Codex agent /root/leancert_examples: independent historical statement referee 2, subsequently a proof contributor and ineligible as an independent final mathematical referee',
    'OpenAI Codex agent /root/ra20_final_referee1: independent final mathematical referee 1, subsequently candidate-document author; no additional mathematical or packaging approval',
    'OpenAI Codex agent /root/ra20_final_referee2: independent final mathematical referee 2'],
   'notes':'The accepted statement boundary binds 68 project inputs and 16 original source/policy files; the complete proof freeze binds 521 and those same 16 original identities at base 5830ed4fb06da0659414a3deb2a40ad327aca052. Author assembly and each final referee passed thirteen fresh source commands: eleven mathematical modules, a separate namespace-only admitted reference and inspector. Each successful set has 57 source plus twelve diagnostic printed standard-three axiom reports (69 total) and 61 source plus twelve diagnostic LeanCert kernel assertions. Referee 1 additionally audited 236 total project declarations, with 214 in the actual export closure and 39 material dependencies; referee 2 checked 214 closure declarations and 28 independently selected material dependencies. All twelve exact elaborated exports match the frozen contracts. Ten exact clean dependencies were reused read-only; no old target objects or copied caches supported those checks. All raw author/referee attempts and historical manifests remain retained. Reference admissions are isolated and excluded from the proved-development sorry count. The coordinator accepted both mathematical reviews before this candidate-document installation. No actual RA20 Linux success is asserted.',
   'statement_freeze':identity('reviews/statement-freeze.json'),
   'proof_freeze':identity('verification/proof-freeze.json'),
   'statement_gate':identity('verification/proof-start.json'),
   'statement_reports':[identity('reviews/statement-referee-1.md'),identity('reviews/statement-referee-2.md')],
   'proof_reports':[identity(r['report']) for r in g['reports']],
   'proof_report_evidence':{r['evidence']['file']:{'sha256':r['evidence']['sha256'],'bound_files':r['evidence']['bound_files']} for r in g['reports']},
   'coordinator_acceptance':{'status':'accepted',**identity('verification/final-review-acceptance.json'),
     'note':'Both full independent final mathematical reports accepted by the proof-contributing coordinator; this is not an additional independent review or a Linux result.'},
   'linux_verification':{'status':'pending','note':'No committed candidate revision or actual RA20 non-root Ubuntu Comparator, standalone default-kernel, sandbox/control result, or operational acceptance is claimed. A clean immutable candidate and independent concrete packaging review are required before the repository Linux workflow.'},
   'candidate_documents':{'preparer':'/root/ra20_final_referee1',
     'role':'Independent final mathematical referee 1, subsequently candidate-document author; no extra mathematical or packaging approval',
     'installation':'Candidate README and this metadata installed after the accepted mathematical gate, with the exact frozen README archived; concrete independent packaging review is pending.',
     'frozen_readme_sha256':'7eb951780e58ce518f0a400c90297020e7c6909ad9fd0c9c15b8036761a8bb50',
     'frozen_readme_archive':'verification/pre-candidate-README.md',
     'historical_inventory_mapping':'Only the exact README.md path when expecting SHA256 7eb951780e58ce518f0a400c90297020e7c6909ad9fd0c9c15b8036761a8bb50 maps to verification/pre-candidate-README.md. Every other prior path/hash remains unchanged, including both full final referee inventories.',
     'installation_evidence':'verification/linux-candidate-2026-09-13/HANDOFF.md','independent_packaging_review':'pending'},
   'standards':{'tau_ceti':'https://github.com/TauCetiProject/TauCetiReview/tree/afb424eda89e8ac96d9eb69f6a88972055a4cd1b/rubrics',
     'adaptation':'../../../docs/lean/REVIEW.md',
     'formalization_schema':'https://github.com/mathlib-initiative/formalization.yaml/blob/99c678e569c7c4c0772db297c5ddd5e4c9b6322e/schema/v0.4.schema.json',
     'local_schema':'../../../docs/lean/schema/v0.4.schema.json',
     'schema_sha256':'25ff6b25ca4511635aff4443cf20480c15e59dddf19591c730950b442ea54fce'}},
 'reproduction':{'local_development':{'cwd':'randomized-and-low-rank-approximation/RA-20/lean','command':'lake build Solution',
   'note':'Explicit Solution target is required because the unchanged historical defaultTargets contains Challenge. Candidate-document preparation performs no new Lean build.'},
   'authoritative_Linux':{'status':'pending','cwd':'repository root','host':'Non-root Ubuntu with the actual pinned harness prerequisites',
     'commands':['tools/lean/bootstrap.sh /tmp/nla-ra20-check','tools/lean/selftest.sh /tmp/nla-ra20-check',
       'tools/lean/verify.sh randomized-and-low-rank-approximation/RA-20/lean /tmp/nla-ra20-check'],
     'prerequisites_document':'../../../tools/lean/HARNESS.md','note':'Run only after independent concrete packaging review on the committed unchanged candidate; actual controls, default-kernel/Comparator results, independent operational acceptance and publication remain required.'}},
 'alignment':[{'declaration':n,'scope':scopes[n.removeprefix('NLA.RA20.')]} for n in names],
 'acknowledgements':'The Codex automated maintainer audit for the original negative-resolution mathematics, and Kubjas, Sodomaco and Tsigaridas for the original conjecture and geometric conventions. Mathlib contributors for actual matrix rank, reduced ideals and Nullstellensatz, point-prime localization and formal smoothness, complex Frechet calculus and cardinality APIs; LeanCert contributors for kernel trust auditing. The Schiffer/Forsythe examples and shared checker/exporter/sandbox tools retain their licenses and attribution. No unproved literature count theorem is assumed.'}
class Dumper(yaml.SafeDumper):
    def ignore_aliases(self,data):return True
(D/'formalization.yaml').write_text('# yaml-language-server: $schema=../../../docs/lean/schema/v0.4.schema.json\n'+yaml.dump(data,Dumper=Dumper,sort_keys=False,allow_unicode=True,width=105))
assert len(data['status']['main_results'])==12 and len(data['alignment'])==12
print('RA20_METADATA_WRITTEN: 12 exact exports, current accepted gate and pending Linux status')
