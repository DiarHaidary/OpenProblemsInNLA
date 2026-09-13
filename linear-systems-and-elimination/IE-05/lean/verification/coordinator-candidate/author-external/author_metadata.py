#!/usr/bin/env python3
"""Write candidate metadata after the accepted mathematical gate; no Lean changes."""
import hashlib
import json
from pathlib import Path
import shutil
import yaml

HERE = Path(__file__).resolve().parent
P = HERE / 'lean'
E = P / 'verification/candidate-package'
R = Path('/tmp/nla-lean-ra20-worktree')
base = '5830ed4fb06da0659414a3deb2a40ad327aca052'
url = 'https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/' + base + '/'
gate = P / 'verification/final-review-acceptance.json'
assert hashlib.sha256(gate.read_bytes()).hexdigest() == '6e1de72e81a0603066544133f7bb52a7217b31bd6f05372a8c1abe109ff03d61'
config = json.loads((P / 'comparator.json').read_text())
pins = {a['name']: a['rev'] for a in json.loads((P / 'lake-manifest.json').read_text())['packages']}
scopes = [
    'The actual finite maximum of absolute real matrix entries is nonnegative, dominates each entry and is attained in nonempty dimensions.',
    'Each actual admissible partial-pivoting Schur step increases the active maximum by at most two.',
    'Every admissible path on a nonempty matrix has a positive input maximum and growth between one and 2^(n-1).',
    'Nonsingularity gives the actual unique first-available-row path and exact agreement between the two trajectory definitions, including ties.',
    'The entire orthogonal growth set over all admissible paths is genuinely nonempty and bounded for every n>=2.',
    'The prescribed lower matrix has the actual normalized Euclidean Gram-Schmidt positive-diagonal QR factorization, which is unique for every n>=2.',
    'A diagonal real Gram identity with positive column scales yields actual real orthogonality.',
    'A scaled unit-lower/upper factorization with bounded multipliers and positive diagonals gives every actual Schur tail, the first-available no-swap path and terminal zero matrix.',
    'Both literal integer matrices satisfy the complete Gram/LU identities, triangular conditions, multiplier bounds and diagonal positivity.',
    'Only 64 witness input and 204 candidate active integer inequalities, a candidate input entry and witness final pivot are required.',
    'Positive QR uniqueness identifies the integer normalized candidate with the independently defined Euclidean Gram-Schmidt candidate and its actual scan path.',
    'The real witness is orthogonal and its no-swap path is the actual first-available admissible path.',
    'Five one-sided input/growth estimates hold in the implemented finite maximum and trajectory semantics.',
    'The exact rational squared gap is 117335164/1147041 and is strictly positive.',
    'The actual first-available GEPP growth of the dimension-eight witness strictly exceeds the candidate growth.',
    'Actual witness membership in the nonempty bounded orthogonal growth set gives a strict gap to its real supremum.',
    'The full original all-dimensional orthogonal GEPP extremizer equality is false, by dimension eight.'
]
assert len(scopes) == len(config['theorem_names']) == 17
metadata = {
    'version': 'v0.4',
    'project': {
        'name': 'IE-05: exact extremizers for partial pivoting on orthogonal matrices',
        'description': 'Complete negative resolution of the original universal orthogonal GEPP QR-extremizer equality, by an exact order-eight counterexample and a strict gap to the genuine real supremum.',
        'authors': ['George Stepaniants'],
        'affiliations': {'George Stepaniants': 'Department of Computing and Mathematical Sciences, California Institute of Technology, Pasadena, California, USA'},
        'responsible_maintainers': ['George Stepaniants'], 'license': 'Apache-2.0',
    },
    'repository': {
        'role': 'substantive-development',
        'note': 'Reviewable uncommitted candidate package. Exact mathematical sources match the accepted proof freeze. No candidate commit, upstream submission, Linux verification or publication is claimed by this metadata.'
    },
    'sources': [
        {'title': 'IE-05 — Exact extremizers for partial pivoting on orthogonal matrices',
         'contributors': [{'name': 'John Peca-Medlin', 'role': 'Original extremizer conjecture and cited element-growth analysis'}],
         'id': url + 'linear-systems-and-elimination/IE-05/README.md', 'type': 'web-post',
         'location': 'Complete retained Context and notation and Problem statement',
         'relationship': 'formalizes', 'author_endorsement': 'not-contacted',
         'note': 'The full n>=2 equality is negated. The supremum includes all orthogonal real matrices and every admissible partial-pivoting tie path; the prescribed positive-diagonal QR candidate uses the first available tied row.'},
        {'title': 'IE-05: An order-eight counterexample to the orthogonal extremizer conjecture',
         'authors': ['George Stepaniants'], 'id': url + 'linear-systems-and-elimination/IE-05/solution.md',
         'type': 'manuscript', 'location': 'Theorem and Sections 1–4; complete standalone solution.tex and original integer programs also retained',
         'relationship': 'formalizes', 'author_endorsement': 'participated',
         'note': 'George Stepaniants supplied the original counterexample and requested the substantially ChatGPT/Codex-assisted formalization. The witness changes one-based (8,2), zero-based (7,1), from -1 to 0. Only sufficient one-sided consequences of the original Gram/LU data are exported; the stronger exact growth equalities are not additional formal claims.'},
        {'title': 'Growth factors of orthogonal matrices and local behavior of Gaussian elimination with partial and complete pivoting',
         'authors': ['John Peca-Medlin'], 'id': 'https://arxiv.org/html/2308.16146v2', 'type': 'article',
         'location': 'Section 3.2 and Appendix B, as cited in the retained canonical source',
         'relationship': 'background', 'author_endorsement': 'not-contacted',
         'note': 'Original conjecture and cited element-growth analysis credit. Neither the paper nor an asymptotic-growth result is an unproved premise of the Lean proof; the separate asymptotic leading-constant question is not settled.'},
    ],
    'related_formalizations': [
        {'id': 'https://github.com/sgstepaniants/Forsythe/tree/8d1b0c0545a77b40245e84705aa7d273e6c81e62/lean-proof',
         'relationship': 'other', 'note': 'Pinned specification/proof separation and explicit LeanCert kernel-trust inspection examples. No Forsythe mathematical theorem or proof implementation is imported.'},
        {'id': 'https://github.com/jaumededios/Schiffer/tree/2938e277969c329caf154e48a3d8823f3635c7f1',
         'relationship': 'other', 'note': 'Pinned Challenge structural reference only. Its preserved metadata records UNLICENSED; no Schiffer mathematical implementation is incorporated into the IE-05 proof.'},
    ],
    'automation': {
        'methods': [{'method': 'agent', 'framework': 'OpenAI Codex',
                     'tool_setup': 'Independent statement reviews and an explicit gate preceded implementation. Two fresh independent final mathematical agents performed their own initially empty private-prefix source builds, actual 17-type and declaration-body/axiom inspection, primary-source fidelity review and exact integer/rational checks. The coordinator accepted both seals before packaging.',
                     'prompting_notes': 'Preserve the original full target, Euclidean QR and positive-sign uniqueness, every admissible tie path, actual first-available scan, zero-padded active trajectories with genuine nonzero pivots, finite maxima, bounded real supremum and witness membership. Reduce auxiliary arithmetic to 64 witness input plus 204 candidate active inequalities and the final pivot; introduce no premise containing the desired conclusion.'}],
        'notes': 'Substantial ChatGPT/Codex assistance at George Stepaniants’s request. The coordinator /root and /root/formal_review_standards are IE-05 proof contributors and are not independent final mathematical referees. Final mathematical referees /root/ie05_final_math_referee1 and /root/mf16_final_referee had no IE-05 implementation contribution when their reports were sealed. The first final referee subsequently authored this candidate package; that separate later role supplies no independent candidate or publication approval. The sealed earlier mathematical report remains unchanged. No external human review, official Tau Ceti endorsement or source-author priority claim is added.'
    },
    'status': {
        'scope': 'Complete 17-export negative proof of the full original universal orthogonal GEPP extremizer equality. Two independent final mathematical agent approvals and coordinator acceptance are recorded. Independent candidate packaging approval and authoritative Linux default-kernel/Comparator verification with real controls are pending. The canonical mathematical status remains Solved; no Lean-verified status or count change is asserted.',
        'sorry_count': 0, 'sorry_in_definitions': 0,
        'axioms': config['permitted_axioms'],
        'main_results': [{'declaration': name, 'file': 'NLA/IE05/Proof.lean', 'sorry_count': 0,
                          'axioms': config['permitted_axioms'], 'comparator_config': 'comparator.json',
                          'literature_dependencies': []} for name in config['theorem_names']],
        'canonical_status': 'Solved', 'whole_problem_verified': False,
        'actual_linux_comparator': 'pending', 'independent_packaging_approval': 'pending',
    },
    'toolchain': {'lean': 'leanprover/lean4:v4.33.1', 'dependency_manifest': 'lake-manifest.json',
                  'dependencies': pins,
                  'trust': 'Explicit LeanCert #assert_trust kernel on material results and final exports; exact integer decision and rational arithmetic with symbolic square-root transfer. Standard foundational axioms only, with no native trust, interval subdivision or admitted proof premise.'},
    'fidelity': {'divergences': 'All original target quantifiers, real field, orthogonality, positive QR sign convention, actual partial-pivoting trajectories, all admissible paths and genuine real supremum are retained. Generic supporting QR, scaling and LU results are proved. Auxiliary certificates establish sufficient one-sided growth estimates instead of all exact manuscript maxima and growth equalities. The true supremum and separate asymptotic leading-constant conjecture are not determined. Historical Challenge comments, proof-map phase prose, failed attempts and old wrappers are retained byte-for-byte; the live README and correspondence state the completed phase.'},
    'review': {
        'status': 'agent-reviewed; final-mathematical-approvals-coordinator-accepted; independent-packaging-and-actual-Linux-verification-pending',
        'reviewers': [
            'OpenAI Codex /root/ie05_statement_referee1: independent historical statement referee 1',
            'OpenAI Codex /root/ie05_statement_referee2: independent historical statement referee 2',
            'OpenAI Codex /root/ie05_final_math_referee1: independent final mathematical referee 1, subsequently candidate packaging author; no independent packaging approval',
            'OpenAI Codex /root/mf16_final_referee: independent final mathematical referee 2',
        ],
        'notes': 'The original 733-input statement freeze, 1,800-input proof freeze and all 27 original Git source identities are preserved. Both final mathematical seals are accepted by verification/final-review-acceptance.json. Each referee compiled the 12 final NLA modules and Solution directly from source with the pinned macOS Lean toolchain and read-only existing dependency objects, then compared all 17 actual elaborated types in a separate proof-free reference setup, traversed safe/nonpartial actual declaration type/body dependencies, and checked only the standard-three transitive axioms. Each recorded 106 successful explicit kernel assertions. Failed reviewer and coordinator attempts remain retained. These source checks are not an actual Linux Comparator/default-kernel sandbox run. The current package has 29 complete historical files inventories, explicit exact-path/hash wrapper archives, and seven small primary library source archives. Packaging checks confer no independent approval.',
        'final_math_acceptance': {'file': 'verification/final-review-acceptance.json',
                                  'sha256': hashlib.sha256(gate.read_bytes()).hexdigest()},
        'proof_freeze': {'file': 'reviews/proof-freeze.json', 'sha256': '72d9a694d6c337937c6edd28ee632dc4a92464ac2dc7ba58ef98f5322405f251'},
        'candidate_inventory': 'verification/candidate-inputs.json',
        'candidate_archive_map': 'verification/candidate-package/ARCHIVE-MAP.json',
    },
    'reproduction': {
        'local_development': {'cwd': 'linear-systems-and-elimination/IE-05/lean',
                              'command': 'lake build Solution',
                              'note': 'Solution is the candidate default target. Historical old lakefile.toml bytes selecting Challenge are archived. No new compilation was performed during packaging; unchanged mathematical sources have the accepted independent macOS checks.'},
        'package_integrity': {'commands': ['python3 verification/candidate-package/verify_inventory.py',
                                           'python3 verification/candidate-package/audit_metadata.py'],
                              'prerequisites': 'Python 3.9 or newer; the metadata audit also requires the pinned PyYAML and jsonschema requirements in tools/lean/requirements.txt.',
                              'note': 'Read-only package checks, not mathematical approval or a Lean runtime check.'},
        'authoritative_Linux': {'status': 'pending', 'cwd': 'repository root',
                                'host': 'Non-root Ubuntu with the actual pinned harness prerequisites',
                                'commands': ['tools/lean/bootstrap.sh /tmp/nla-ie05-check', 'tools/lean/selftest.sh /tmp/nla-ie05-check',
                                             'tools/lean/verify.sh linear-systems-and-elimination/IE-05/lean /tmp/nla-ie05-check'],
                                'prerequisites_document': '../../../tools/lean/HARNESS.md',
                                'note': 'Future reproduction from the independently approved, exact committed candidate. Actual default-kernel replay, separate-environment Comparator and both real negative-control suites must pass and be independently accepted before a canonical verification claim.'},
    },
    'alignment': [{'declaration': name, 'scope': scope} for name, scope in zip(config['theorem_names'], scopes)],
    'acknowledgements': 'George Stepaniants for the original counterexample and integer Gram/LU certificates; John Peca-Medlin for the original conjecture and cited element-growth analysis. Mathlib contributors for genuine Euclidean Gram-Schmidt, matrix algebra, finite maxima, real square roots and supremum APIs; LeanCert contributors for explicit kernel trust auditing. The Schiffer/Forsythe examples and preserved third-party sources retain their own attribution and license terms. The original counterexample and this formalization received substantial ChatGPT/Codex assistance.',
}
(P / 'formalization.yaml').write_text('# yaml-language-server: $schema=../../../docs/lean/schema/v0.4.schema.json\n' + yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False, width=100))
references = {}
for source, target in [
    ('docs/lean/schema/v0.4.schema.json', 'schema/v0.4.schema.json'),
    ('tools/lean/validate_manifest.py', 'schema/validate_manifest.py'),
    ('tools/lean/requirements.txt', 'schema/requirements.txt'),
]:
    dst = E / target
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(R / source, dst)
    b = dst.read_bytes()
    references[target] = {'source_repository_path': source, 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}
(E / 'schema/SOURCE-RECORDS.json').write_text(json.dumps(references, indent=2, sort_keys=True) + '\n')
shutil.copy2(R / 'tools/lean/LICENSE-APACHE-2.0', P / 'LICENSE')
shutil.copy2(Path(__file__), E / 'author_metadata.py')
print(json.dumps({'metadata_results': len(config['theorem_names']), 'schema_sha256': references['schema/v0.4.schema.json']['sha256'], 'actual_linux_comparator': 'pending'}))
