# Independent review of PR #232: IE-05 Lean verification

**Verdict: PASS for mathematical statement fidelity, proof correspondence and the submitted canonical PDF.** No mathematical blocker was found. One historical-status clarification is recommended on the canonical page, outside the immutable Lean evidence package. Final merge also requires the coordinator's separate source-preservation, dependency and GitHub CI authentication checks.

- Reviewed PR head: `5ce3e36cacbebcafda267eb6a9f2a42c461b189b`.
- Published comparison base: `50838e37dd793830e2cecd1055cfc7e0349490f1`.
- Read-only worktree: `/private/tmp/nla-audit-232`.
- Review date: 2026-09-13.
- Reviewer: independent Codex agent `/root/review_ie05_232`; no contribution to the submitted mathematical implementation.
- Evidence: independently authored `nla-pr232-independent-exact-checks.py` and its `nla-pr232-independent-exact-checks.json` output. The JSON binds the active module and PDF hashes.

## Directly inspected material and review boundary

I read the complete actual project source: `Definitions`, `Pivot`, `GEPP`, `Scaling`, `QR`, `IntegerQR`, `LUTrajectory`, `ExactCertificates`, `Witness`, `GrowthBounds`, `Growth`, `Proof`, and the one-line `Solution` entry point. These are the entire 13-file local import closure reached from `Solution`; historical copies were not substituted for active files. I separately read every Challenge contract, the Comparator selection, Lake configuration, formalization metadata, source correspondence, the retained informal solution, canonical README/TeX changes and the RESOLVED insertion. I inspected the relevant preserved primary Mathlib Gram-Schmidt and conditional-supremum implementations and the LeanCert trust interface.

This review does not claim a new Lean compilation, dependency-byte authentication or remote artifact replay. Those are separately assigned to the coordinator. In particular, submitted referee reports and archived success summaries did not substitute for reading the mathematical implementation and independently checking its arithmetic.

`Solution` imports `NLA.IE05.Proof`, which imports `Growth`; the latter reaches both the witness/QR/LU branch and GEPP/bounds branch. Every project import was resolved from the actual worktree. None reaches `Challenge`, and the only external import families are Mathlib and LeanCert. The active-source scan, after stripping comments, found no `sorry`, custom `axiom`, `native_decide`, `unsafe`, `partial`, `run_elab` or `implemented_by` construct. `Challenge` intentionally has 17 reference holes in a separate environment. All 17 final export signatures match their Challenge signatures textually after whitespace/comment normalization; the configured order and names match exactly. Mathematical implementations are under distinct proved/helper names, so no Challenge theorem supplies its own proof.

## Original target and definition semantics

The canonical original target is retained: the equality between the supremum over real orthogonal matrices and all admissible partial-pivoting paths, and the first-available-row growth of the positive-diagonal QR factor of the prescribed lower matrix, for every dimension at least two. The terminal theorem negates this complete universal statement by dimension eight. It does not replace the target by one rational subfamily or assume an extremal/growth bound as a premise.

The literature attribution and distinction between the exact equality and a separate asymptotic conjecture agree with [Peca-Medlin's primary manuscript](https://arxiv.org/html/2308.16146v2): Section 1.2 specifies the relevant elimination and positive-QR conventions; Section 3.1 describes the lower-matrix family; Section 3.2 discusses the asymptotic leading constant; Appendix B explicitly discusses the exact candidate equality. No assertion of the paper is an unproved premise in the Lean proof.

`Orthogonal A` is the actual real matrix identity `A.transpose * A = 1`. The square finite matrix condition supplies genuine orthogonality, with no hidden pivot assumptions. `euclideanColumns` uses `EuclideanSpace` via `WithLp.toLp 2`; therefore the norm in Gram-Schmidt is Euclidean, not the coordinate supremum norm. The prescribed matrix has diagonal one, strict-lower entries minus one and zero strict-upper entries. `normalizedQRQ` is actual normalized increasing-index Gram-Schmidt. Its positive QR existence and uniqueness are proved generically before the integer candidate is identified with it.

`rowSwap` swaps only current rows. `schurStep` computes the actual pivot-row quotient update on the next trailing block and zeroes coordinates outside it. `AdmissiblePivot` requires an active row, a nonzero pivot and maximal column magnitude; `FirstAvailablePivot` additionally requires the least current row among all ties. The explicit scan visits ascending rows and replaces a row only on strict improvement. Its specification is proved through first-occurring list argmax, and path equality is proved by induction. Nonsingularity is maintained as injectivity on vectors supported in the active block, avoiding an invalid assertion that the padded full matrix remains nonsingular.

The entry maxima are genuine finite suprema of nonnegative absolute real entries. The growth numerator includes exactly the input and active stages zero through n−1; it does not omit the input or include a spurious terminal stage. Denominator positivity follows from admissibility. The growth set ranges over every orthogonal matrix and every admissible path. It is proved nonempty through the identity matrix and bounded through the all-path factor-two Schur estimate, giving growth in [1, 2^(n−1)]. `orthogonalGrowthSup` is the genuine real `sSup`; the final comparison invokes `le_csSup` with the independently proved upper boundedness and actual witness membership.

## Coverage of all 17 selected exports

| Exports | Mathematical review |
|---|---|
| `entryMax_semantics`, `schurStep_bound`, `gepp_growth_bound` | Finite maximum is attained in positive dimension; row-swap active entries and multiplier magnitude ≤1 give the factor-two estimate; induction and the positive input maximum give the all-path classical growth bound. |
| `firstPath_semantics` | Actual scan maximality/minimality, supported-vector injectivity, nonzero pivot existence, Schur preservation and trajectory/path uniqueness are proved. |
| `orthogonalGrowthSet_bounded` | Identity membership proves nonemptiness; the previously proved all-path bound applies to every set member. |
| `candidate_positiveQR` | Determinant of the prescribed lower matrix is one. Gram-Schmidt orthonormality, upper triangularity, positive diagonal and factor recovery are derived, and induction on columns proves uniqueness in every required dimension. |
| `scaledColumns_orthogonal` | Positive diagonal Gram data transfer by real square-root algebra to the actual orthogonality identity. |
| `scaledLU_trajectory` | Tail splitting exactly cancels the eliminated lower-factor contribution; multiplier bounds give the first-available diagonal pivot. The actual no-swap recurrence, scan identity and terminal zero tail follow. |
| `integer_factor_certificates`, `integer_entry_certificates` | The literal 8×8 integer Gram/LU identities, positivity, triangularity, 64 witness input inequalities, 204 candidate active inequalities and final pivot are kernel-decision obligations. Independently replayed below. |
| `canonical_integer_identification`, `witness_orthogonal_path` | Exact real casts preserve the integer identities. The generic positive QR bridge identifies the candidate; the scaled-LU proof supplies both real no-swap paths and the witness's admissibility/orthogonality. |
| `bounded_growth_data`, `numerical_gap_positive` | Positive square-root denominators transfer the integer inequalities to sufficient one-sided growth estimates. The exact positive rational gap is correctly calculated. |
| `witness_strict_growth`, `supremum_strict_gap`, `orthogonalExtremizerConjecture` | The squared estimates and nonnegativity imply strict first-path growth comparison; actual set membership gives the strict real-supremum gap; dimension eight contradicts the universal equality. |

The one-sided formal bounds suffice for the complete negative target. Neither all exact intermediate witness maxima nor the stronger exact growth equalities are misrepresented as additional Lean exports. The original informal manuscript retains its stronger equality claim, which the independent exact replay also confirms. The true orthogonal supremum and separate asymptotic leading constant remain outside scope. Original problem number, path, historical ratings and Peca-Medlin/Stepaniants credit are preserved in the reviewed display changes.

## Independent arithmetic replay

I wrote a new Python standard-library checker that parses the active Lean integer literals and uses integers and `fractions.Fraction`; it imports or executes no supplied certificate program. It reconstructs each lower matrix from the original target and the single `(8,2)` modification, checks both full Gram identities and both LU identities, all positive diagonals and upper triangularity, then performs direct exact elimination on each integer-column matrix. Fixed positive column scaling cancels in pivot comparisons and elimination multipliers.

All 408 active entries across the two executions match the independently computed factor tails. Every stage's complete tie list includes the diagonal as its first available row. Both terminal padded states are zero. All 64 required witness input inequalities and all 204 required candidate active inequalities pass. The checker additionally recovers every exact manuscript stage maximum and both exact squared growth factors:

- Witness: `(5272/63)^2`.
- Candidate: `17948132/2601`.
- Positive squared gap: `117335164/1147041`.

The checker exits successfully and records all stage maxima, tie lists and module SHA-256 hashes in its JSON result. These computations are independent corroboration of the mathematical certificates, not additional assumptions in the formal proof.

## Canonical display and historical documentation

Using the PDF skill in read-only mode, I rendered and visually inspected **both pages** of the submitted canonical `linear-systems-and-elimination/IE-05/problem.pdf`. The title, Lean verified status, credit, exact comparison, original statement, references and historical checks are legible and consistent with the README/TeX. There is no clipped text, broken mathematics, overlap or missing content.

There is a minor current-versus-historical documentation ambiguity: `lean/SourceCorrespondence.md:8` says the canonical status remains Solved, line 112 says Linux replay remains pending, and lines 130–149 describe a future publication gate. The current `lean/README.md` and metadata otherwise correctly report accepted publication. The correspondence is an immutable candidate member (`verification/candidate-inputs.json:96`, `verification/publication-inputs.json:93`), and `verify_publication.py:57–59` requires its exact bytes. It should not be edited in place merely to update status.

Recommended minimal correction outside that sealed package, after the canonical verification-archive paragraph: “The [source correspondence](lean/SourceCorrespondence.md) is preserved from the earlier candidate phase; its ‘Solved’ status and pending-Linux wording are historical and superseded by this verification record.” This resolves the ambiguity while keeping every candidate/referee inventory reproducible. Any resulting canonical PDF regeneration should receive a fresh visual check. This editorial clarification does not affect the mathematical PASS.

**Integration follow-up:** I read the corrected canonical README in `/private/tmp/nla-integration-232-233` and confirmed that the coordinator applied this historical-phase clarification in the intended location. The coordinator reports preserving the entire Lean package and visually accepting both regenerated PDF pages. The regenerated PDF has two pages and SHA-256 `053033ff1a12fc882badfc0cc41668e37c64f189dabda3e4a2b0902432e9d9e4`, which I independently checked. The editorial issue is addressed; there is no remaining requested source correction from this review.
