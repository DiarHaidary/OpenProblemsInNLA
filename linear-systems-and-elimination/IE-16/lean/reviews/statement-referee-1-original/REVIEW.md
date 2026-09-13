# IE-16 independent statement referee 1 — original boundary

**REQUEST CHANGES before proof implementation.** The twelve original numerical
propositions are consistent with the complete Holden proof and retain the
intended complex polynomial domain. Make the attained-minimum interpretation
and positive ratio denominator explicit before approving the statement boundary.
No false numerical assertion or lost universal quantifier was found.

Reviewer: `/root/is02_cleanup_referee`, independent Codex AI agent, 13 September
2026. I did not author or edit IE-16. This statement review is not human peer
review, an official Tau Ceti run, or formal verification. No Lean, Lake, Git,
network or heavy computation was launched: the coordinator expressly prohibited
new compilation because an unrelated Lean job had exhausted machine memory.

## Three required contracts

The canonical M is a minimum over feasible complex polynomials. The current M
is `sInf` of their objective values. Require its attained-minimum interpretation
at all inputs used by this counterexample, rather than leaving that bridge
implicit. Add these signatures, their properties to `ExplicitCertificate`, and
the corresponding numerical-target, Comparator and YAML entries:

```lean
theorem full_minimum_isLeast :
    IsLeast (feasibleValues explicitL 4) (M explicitL 4)

theorem every_five_point_subset_minimum_isLeast :
    ∀ S : Finset ℂ, S ∈ subsetFamily explicitL 4 →
      IsLeast (feasibleValues S 4) (M S 4)

theorem subset_max_positive : 0 < subsetMax explicitL 4
```

`IsLeast` supplies both membership in the set of feasible objective values
(an actual attaining complex polynomial) and the lower-bound property
(global optimality). The specified full-set witness supplies the first
instance; the manuscript's Lagrange interpolation construction supplies each
five-point instance. Positive subsetMax excludes zero division and its
empty-family/default-zero branch. Although positivity could follow later from
the positive full value and ratio theorem, it should be visible before proof.

Preserve all twelve existing contracts and the original target. The corrected
boundary should have fifteen deliberate placeholders. A general all-input
attainment theorem is unnecessary for this negative resolution: attainment on
the nine-point set and all its five-point subsets identifies every canonical
minimum used to refute the universal inequality. No stronger amplification
formalization is required.

## Scope and mathematical correspondence

I read the entire supplied canonical README, complete Holden manuscript,
submission explanation, verifier, certificate, Definitions, all twelve Challenge
signatures, numerical/source map, metadata, Comparator and existing raw logs.
The source snapshot is labeled upstream commit
`b73cd1804e40e0d101294eedb156984f0d62b4a6`. All six copied source SHA-256 hashes
and all twenty then-current statement-inventory hashes matched on my initial
independent check. I did not retrieve that commit or check its Git tree under
the task's no-Git/no-network restriction; snapshot provenance is supplied, not
an independently claimed upstream checkout audit.

`Poly` is actual `Polynomial ℂ`; coefficients and evaluations are arbitrary
complex values. `natDegree ≤ k` agrees with ordinary bounded degree, as the
pinned Mathlib `natDegree_le_iff_degree_le` source confirms. Normalization is
actual `p.eval 0 = 1`; it excludes the zero polynomial. The constant-one
polynomial makes the feasible domain nonempty for every natural k. The unused
L argument in feasibility is harmless. The objective is the true finite
maximum of complex norms, as Mathlib's `sup'_le_iff` and `le_sup'` confirm.
Every objective is nonnegative, so the real infimum is taken over a nonempty
set bounded below by zero. It does not use an undefined-infimum fallback.
The requested IsLeast contracts expose attainment at the relevant instances.

The subset family is the complete powerset filtered by cardinality k+1, not a
certificate list or a single pattern. Finset distinctness and explicit exclusion
of zero match the source's admissibility. The universal target retains all
n >= 3, all n-point nonzero complex sets and every 1 <= k <= n-2. Natural
subtraction causes no issue when n >= 3. The factor is actual `4 / Real.pi`.
There is no restriction to real/rational polynomials, root-of-unity competitors,
exact degree k, or selected subsets. The unconditional final negation at
n=9 and k=4 suffices to disprove the complete original statement.

The witness uses exactly -1/2 + sqrt(3)/2 * I, epsilon=1/1000, and all nine
Fin 3 × Fin 3 pairs. Cardinality and nonzero nodes are obligations, not assumed
injectivity. Same-cluster distances are sqrt(3) epsilon; cross-cluster distances
are at least sqrt(3)-2 epsilon; all node norms are at least 1-epsilon. These
positive bounds establish every interpolation denominator is nonzero.
The polynomial 1-((1+epsilon)/D) X^3 has permissible degree three at k=4.
Its exact claimed norm and full optimum are
3003003000/1001003001001. Rotation/conjugation averaging covers all feasible
complex polynomials before the source's real scalar quadratic minimization.
The source also provides positive weighted orthogonality as an alternative
exact global-optimality argument; the four moment identities must be proved,
not imported as a certificate hypothesis.

Every five-point subset has, up to permutation, occupancy (2,2,1), (3,1,1),
or (3,2,0). The first profile uses four Lagrange contributions and the latter
two use the three points of a full cluster. Lagrange interpolation of complex
values aligned with conjugate cardinal weights constructs a normalized
polynomial of degree at most four attaining the reciprocal Lagrange norm.
This is the natural finite proof route for the requested subset IsLeast
contracts and needs no general compactness argument.

The numerical scales agree exactly:
(299/100000)/(23/10000)=13/10. I checked the coarse rational upper bound
2259009004/996005996001 < 23/10000 and the exact full-set rational value.
I also made a small source-data audit: nine rational Q(omega) coordinate pairs
are distinct and nonzero; the JSON includes exactly all 126 five-label subsets,
with occupancy counts 81,27,18; and all 630 squared Lagrange weights match my
independent rational recomputation. These checks are supporting source-data
checks, not Lean proofs or a substitute for quantification over actual subsets.

The π comparison uses Real.pi, not decimal data. Mathlib's inspected
`Real.pi_gt_d2 : 3.14 < π` gives 31/10 < π and then 4/π < 13/10 with exact
arithmetic, avoiding unnecessary new interval computation. Source excerpts and
hashes for polynomial degree/evaluation, finite suprema, Lagrange interpolation,
IsLeast, compact minimization and π bounds are retained in
MATHLIB-API-INSPECTION.json. No dependency objects were rebuilt or inspected by
executing Lean.

## Existing evidence and documentation limits

The old Definitions log shows one unused-binder warning. The old Challenge log
shows twelve intentional sorry warnings. Both retained status files report
zero exit status. These are the author's existing logs, not my independent
elaboration or an actual-types/axioms inspection. Definitions has no sorry;
there is no Solution/proof import. Metadata truthfully reports the twelve
placeholders and sorryAx. Comparator covers the same twelve public contracts.

The historical command record uses `lake env lean` for Definitions and explicit
LEAN_PATH for Challenge. Therefore do not describe that historical run as
having used no Lake invocation. No dependency build is recorded. The pin log
lists manifest revisions; it does not independently compare all ten current
Git heads and clean tracked trees. I did not perform Git checks in this task.
Future local runs require coordinator clearance and bounded_lean.py. None of
this evidence is Linux Comparator or final proof verification.

Two small documentation corrections should accompany the required update:
SOURCE_HASHES.json contains SHA-256 content hashes, not Git blob object IDs;
and Definitions itself contains no deliberate placeholders. Original resolution
credit remains with Sidney Holden. George Stepaniants's formalization credit
includes Computing and Mathematical Sciences and Caltech without an email.

## Historical immutable boundary

- Definitions: `7f232bb361e6e81db9460b88dc6ed2b990c8148d29d5f0a4fe92be7127ec57b9`
- Challenge: `5dd745c5d0ba7f1aa7652bdc163ca8d686b5d548b94c9d28b0cfbeaf5f73b590`
- Numerical targets: `41072a032fcb3647c6d3f68ffdc909b06a698a92d646c051a993c234caf853d5`
- Comparator: `b4cdecf0576aabcf0d78e1a6fdb0ea1c4076b4d84b6c064a968a78019192df79`
- Canonical README: `bc4ac8591a0dd4fc3533ad278741c335b43bb1677e4148340cb0b25f2938558f`
- Holden manuscript: `e0b8de10f215fa216541985f5602787995a54d9f6908bd17095f8be942ce2390`

The author amended the live source while this report was being finalized.
My hash guard caught that change. The old Definitions and Challenge in
old-boundary-reconstructed/ were reconstructed by deleting exactly the three
new contracts/certificate fields, then required to match the old hashes above
before being saved. The reconstruction note makes this chronology explicit;
it is not presented as a snapshot captured before mutation.

This report remains REQUEST CHANGES for the original twelve-contract boundary.
Any approval of the amended fifteen-contract boundary belongs in a separate
report. EVIDENCE-MANIFEST.json binds portable relative-path hashes of this
report and compact records; no compiled objects or caches are included.
