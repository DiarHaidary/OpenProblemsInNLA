# IE-05 source correspondence and implementation feasibility

This draft is based on immutable upstream commit
`5830ed4fb06da0659414a3deb2a40ad327aca052`. Source snapshots and Git-blob/SHA-256
identities are retained in `verification/original-source-inventory.json`.
No canonical page, problem number or existing solution is modified.

## Attribution and eligibility

The mathematical counterexample is by **George Stepaniants**, Department of
Computing and Mathematical Sciences, California Institute of Technology,
Pasadena, California, USA, with substantial ChatGPT/Codex assistance as disclosed
in the source. The original extremizer conjecture and cited element-growth
analysis are attributed to **John Peca-Medlin**. No claim is made that the older
orthogonal matrix family originated in that paper. No contact email is included.

The bounded current-upstream check found status **Solved**, no canonical IE-05
Lean project and no active campaign track. All-state upstream PR search returned
the historical mathematical submission #127 and grouped resolution #6; neither
is an IE-05 formalization. This is not an exhaustive search of private or
unidentifiably named forks. The exact query scope and result are in
`verification/eligibility.json`.

## Complete primary mathematical sources

- [Canonical target at the base](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/5830ed4fb06da0659414a3deb2a40ad327aca052/linear-systems-and-elimination/IE-05/README.md),
  **Context and notation**, **Problem statement**: exact active Schur growth,
  every admissible tie path, positive-diagonal QR and the universal real supremum.
- [Complete solution at the base](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/5830ed4fb06da0659414a3deb2a40ad327aca052/linear-systems-and-elimination/IE-05/solution.md),
  Theorem and §§1–4; the full generated `solution.tex` was also read.
- [Frozen informal proof](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/5830ed4fb06da0659414a3deb2a40ad327aca052/references/stepaniants-ie05-2026-09-11/full-proof.md)
  and [independent informal review](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/5830ed4fb06da0659414a3deb2a40ad327aca052/references/stepaniants-ie05-2026-09-11/independent-review.md).
  Their prior automated review is mathematical background, not an independent
  review of the new Lean statements.
- The three exact certificate programs (`integer_counterexample.py`,
  `verify_ie05.py`, `exact_matrix_review.py`) and both recovered-proof checkers,
  plus `verify_recovery_relation.py`, were inspected. Their values motivate
  finite obligations but are not imported as trusted Lean facts.

The full manuscript computes more than needed for the negation. Its integer
Gram/LU certificates and one-sided consequences are sufficient; this reduction
does not narrow the **original target**, only the auxiliary facts promised.

## Exact statement map

Every entry below is prefixed `NLA.IE05.` in `comparator.json`.

| Contract | Source and required semantic bridge |
|---|---|
| `entryMax_semantics` | Canonical max-entry norm; finite NNReal maximum must dominate every absolute real entry and be attained for nonempty dimensions. |
| `schurStep_bound` | Exact partial-pivot update; prove the elementary factor-two bound from the actual pivot inequality. |
| `gepp_growth_bound` | Repeated actual Schur bound, positive denominator and inclusion of stage zero; all admissible paths, all `n≥1`. |
| `firstPath_semantics` | Canonical first-available tie rule; derive nonzero pivots from actual determinant nonzero, trajectory agreement and uniqueness. |
| `orthogonalGrowthSet_bounded` | Genuine real-supremum preconditions from the identity and the universal GEPP bound. These are conclusions, never premises in the conjecture. |
| `candidate_positiveQR` | Canonical `L_n`; true normalized L2 Gram–Schmidt, its factorization and positive diagonal, and uniqueness for every `n≥2`. |
| `scaledColumns_orthogonal` | Solution §1; actual diagonal Gram identity plus positive scales yields actual matrix orthogonality. |
| `scaledLU_trajectory` | Solution §2; generic finite tail-sum algebra gives the exact Schur stages and first-available no-exchange path. |
| `integer_factor_certificates` | Solution §§1,4; complete literal integer Gram, LU, triangular, multiplier and positivity facts for both matrices. |
| `integer_entry_certificates` | Reduced finite inequalities from §§3,4: 64 witness input bounds, 204 candidate active bounds, one candidate input entry and the witness final pivot. |
| `canonical_integer_identification` | Solution §4; connect the integer candidate to the exact positive-diagonal QR object. |
| `witness_orthogonal_path` | Solution §§1,2; actual real orthogonality and exact stipulated, admissible pivot path. |
| `bounded_growth_data` | One-sided consequences sufficient for the full theorem; stronger manuscript equalities are not exported. |
| `numerical_gap_positive` | Solution §4's exact positive rational squared gap. |
| `witness_strict_growth` | Theorem's strict comparison, with actual implemented growth/path objects. |
| `supremum_strict_gap` | Genuine `sSup` comparison using established boundedness and witness membership. |
| `orthogonalExtremizerConjecture` | Negates the complete canonical universal equality, by dimension eight. |

## Actual pinned APIs and proof plan

The project pins Lean `v4.33.1`, Mathlib
`0df444a360eaa60ab8c11dca51a86af692955474` and LeanCert
`621a43d7cf21f87872392a01e874f2f1dbddc926`. All ten transitive packages are pinned
in `lake-manifest.json`; no fresh dependency download or Lake build is performed.

- `Mathlib/Analysis/InnerProductSpace/GramSchmidtOrtho.lean` defines
  `InnerProductSpace.gramSchmidtNormed` as inverse actual norm times the
  orthogonalized vector. `gramSchmidtNormed_orthonormal`, `gramSchmidt_ne_zero`,
  `gramSchmidt_inv_triangular` and the finite-span lemmas supply the genuine QR
  route. `euclideanColumns` explicitly uses `EuclideanSpace ℝ (Fin n)`.
  The candidate's independent columns follow from the unit triangular input's
  determinant; positive diagonal follows from the norm of each nonzero residual.
  Uniqueness requires proving an upper triangular orthogonal change of basis
  with positive diagonal is identity. It is an explicit obligation, not a cited
  unsupported QR routine.
- `Matrix.linearIndependent_cols_of_det_ne_zero`, `det_mul`, `det_transpose`,
  triangular determinant lemmas and row-addition determinant invariance are
  available in actual determinant/triangular modules. The Schur complement
  file supplies `det_fromBlocks₁₁` and genuine block factorization identities.
  These support a shrinking active-index or block-matrix proof that nonsingular
  inputs retain a nonzero active pivot. The padded full matrix has zero rows
  after elimination and is **not** itself nonsingular; any such induction must
  restrict to the active block. No GEPP theorem was found that bypasses this.
- `Finset.le_sup`, `Finset.sup_le`, real/NNReal norm coercions and finite maxima
  give exact entrywise semantics. The factor-two induction is scalar triangle
  inequality and `|multiplier|≤1`, not an operator norm theorem.
- `Real.sqrt_pos`, `Real.sq_sqrt` and exact field/ring arithmetic handle the
  positive column scalings. The integer tail sums should be collected before
  introducing roots; they need not be evaluated as hundreds of real radicals.
- `le_csSup` requires `BddAbove`; `csSup_le` requires nonemptiness. The draft
  visibly includes both prerequisites as results about the actual set.
- `LeanCert.Tactic.Verification` is used for definition-only trust inspection.
  The eventual proof may use `LeanCert.Tactic.IntervalAuto.PointIneq` for the
  one retained final rational positivity certificate with explicit kernel trust.
  The source checker, if used, must occur in the actual final dependency chain.

These are inspected APIs and a proposed route, **not a claim that the required
universal bridges are already implemented**. They are expected to be more work
than the finite arithmetic. If a bridge proves obstructed, the target may not
be weakened to avoid it.

## Reuse and review protocol

The inspected [Schiffer Challenge at its campaign pin](https://github.com/jaumededios/Schiffer/blob/2938e277969c329caf154e48a3d8823f3635c7f1/Schiffer/Challenge.lean)
illustrates a separately auditable mathematical boundary. The inspected
[Forsythe Challenge](https://github.com/sgstepaniants/Forsythe/blob/8d1b0c0545a77b40245e84705aa7d273e6c81e62/lean-proof/Challenge.lean)
and `CheckedMultivariateBound.lean` illustrate independent specification/proof
environments and explicit retained checker soundness. Forsythe's Lean project
and LeanCert are Apache 2.0. The inspected Schiffer metadata says `UNLICENSED`,
so it is used only as a structural reference. This draft copies no mathematical
implementation from them, and does not claim their numerical methods or prior checks as IE-05
evidence. Its project skeleton and standard-three comparator configuration use
the existing NLA campaign pattern.

The repository's `docs/lean/REVIEW.md` adapts Tau Ceti at
`afb424eda89e8ac96d9eb69f6a88972055a4cd1b`. Required independent reviews must
scrutinize all target quantifiers, arbitrary tie paths, real norm instances,
zero/empty cases, QR sign convention, genuine supremum preconditions, and
proof obligations hidden in definitions. Correctness, scope, proof quality,
reuse, generality, API, naming, placement, documentation and attribution all
apply within this scope. No Tau Ceti service endorsement is claimed.

Comparator will compare the exact theorem types and statement definitions in
separate environments, then replay the actual proofs with only `propext`,
`Classical.choice`, `Quot.sound`. It does not establish English-to-Lean fidelity.
`definition_names` is empty: there are no definition exceptions. At this stage
there is no `Solution.lean`, so no Comparator run or complete theorem can pass.
Actual v0.4 `formalization.yaml` will be added at the appropriate reviewed
candidate stage; no verification manifest is fabricated now.

The coordinating root suggested the optional further one-sided numerical
reduction. That contribution is recorded transparently. No statement approval,
proof gate, independent final review, or Linux verification has occurred for
this draft.
