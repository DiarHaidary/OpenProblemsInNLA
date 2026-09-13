# IE-05 complete proof map

The implementation proves the negation of the original all-dimensional
orthogonal GEPP extremizer equality. The dimension-eight witness has strictly
greater growth than the prescribed positive-diagonal QR candidate, and belongs
to the genuinely bounded set used to define the real orthogonal-growth
supremum. No desired QR identity, elimination trajectory or supremum property
is supplied as an additional hypothesis.

This document records the author assembly. Two independent final mathematical
approvals and actual Linux default-kernel/Comparator verification remain
required before a Lean-verified status or publication. The older README and
Challenge comments retain their historical statement-only phase; the accepted
proof gate is `verification/proof-start.json`.

Formalization: George Stepaniants, Department of Computing and Mathematical
Sciences, California Institute of Technology, Pasadena, California, USA, with
substantial AI assistance. The preserved counterexample and integer data are
Stepaniants's submitted mathematics. The conjecture remains attributed to
John Peca-Medlin. The coordinator and `formal_review_standards` agent are proof
contributors; neither counts as an independent final referee. The separate
certificate/QR completion inspection is a mechanical handoff, not an additional
final mathematical approval.

## Original target and numerical strategy

`Definitions.lean` fixes actual real matrices, positive-diagonal QR via
normalized Euclidean Gram--Schmidt, row swaps and Schur updates, admissible
partial-pivoting paths, the first-available tie scan, and the maximum of the
actual entries at every active stage. The supremum includes every orthogonal
matrix and every admissible partial-pivoting path. All dimensions in the
original conjecture remain quantified.

The two exact integer constructions use the original tables. The witness
lower factor changes the one-based entry `(8,2)`, represented by `(7,1)` in
`Fin 8`. Diagonal Gram and LU certificates produce the actual normalized real
matrices and their complete trajectories. The candidate is proved equal to the
prescribed QR factor; its definition is not replaced by the integer formula.

Only the following bounds are needed:

* The 64 witness input inequalities imply
  `entryMax witnessQ ≤ 63 / sqrt 5272`.
* Its actual final pivot is `sqrt 5272`, so its growth is at least `5272 / 63`.
* One candidate input is `51 / sqrt 3286`.
* The 204 active candidate tail inequalities give an active maximum at most
  `sqrt 5462`, hence candidate squared growth at most `17948132 / 2601`.
* The exact squared gap is `117335164 / 1147041 > 0`.

The certificates use integer kernel decision and exact rational arithmetic.
All square-root transfers are symbolic. No square-root interval, subdivision,
witness intermediate-stage upper bound, extra QR table, or artificial numerical
certificate is introduced. The proof uses the exact matrix trajectories in the approved statement.

## Every final contract

All exports have prefix `NLA.IE05.` and are declared in `NLA/IE05/Proof.lean`.
`Solution.lean` imports only that complete implementation. It does not import
Challenge or an expected-type environment. The original 17 Challenge types and
the empty Comparator definition-exception list are unchanged.

| Export | Implementation and bridge |
| --- | --- |
| `entryMax_semantics` | `GEPP`: actual finite maximum, an attained absolute entry, and all-entry bound. |
| `schurStep_bound` | `GEPP`: actual row swap and admissible pivot give the factor-two active bound. |
| `gepp_growth_bound` | `GEPP`: induction over every actual active stage yields positivity, lower bound one, and the classical upper bound. |
| `firstPath_semantics` | `Pivot` and `GEPP`: active-submatrix injectivity prevents a zero pivot, and first-available uniqueness identifies the scan. |
| `orthogonalGrowthSet_bounded` | `GEPP`: actual orthogonal nonsingularity and admissibility give nonemptiness and uniform boundedness. |
| `candidate_positiveQR` | `QR`: actual normalized Gram--Schmidt of the prescribed lower matrix, with positive diagonal and uniqueness. |
| `scaledColumns_orthogonal` | `Scaling`: the real diagonal Gram identity and positive scales yield orthogonality. |
| `scaledLU_trajectory` | `LUTrajectory`: symbolic Schur elimination of a scaled unit-lower/upper factorization identifies every stage, including the zero terminal stage, and proves the tie scan. |
| `integer_factor_certificates` | `ExactCertificates`: both full integer Gram/LU identities, triangular structure, multipliers and strictly positive diagonals. |
| `integer_entry_certificates` | `ExactCertificates`: only the retained witness input, final pivot, candidate input and active-tail inequalities. |
| `canonical_integer_identification` | `IntegerQR` and `Witness`: generic positive QR reconstruction and uniqueness identify the original candidate and its actual scan path. |
| `witness_orthogonal_path` | `Witness`: real casts transfer the exact factor certificate; the generic LU proof establishes orthogonality and the actual admissible first path. |
| `bounded_growth_data` | `GrowthBounds` and `Growth`: symbolic square-root bounds applied to actual input and trajectory entries establish all five one-sided estimates. |
| `numerical_gap_positive` | `ExactCertificates`: exact rational equality and strict positivity. |
| `witness_strict_growth` | `Growth`: the rational squared gap and nonnegative growth give the strict comparison. |
| `supremum_strict_gap` | `Growth`: actual witness membership and `le_csSup` for the proved bounded set lift the strict comparison to the real supremum. |
| `orthogonalExtremizerConjecture` | `Growth`: specialize the original universal equality to dimension eight and contradict the strict supremum gap. |

## Trust, reuse and review

Every mathematical module uses the pinned Lean 4.33.1 environment with Mathlib
`0df444a360eaa60ab8c11dca51a86af692955474` and LeanCert
`621a43d7cf21f87872392a01e874f2f1dbddc926`. Explicit LeanCert kernel assertions
audit material theorems and every final export. The allowed foundational axioms
are `propext`, `Classical.choice`, and `Quot.sound`; no native-execution axiom,
custom axiom or admission supports the implementation.

The separate author inspector elaborates all 17 original signatures as
proof-free propositions and compares their actual Lean types with the final
exports. It traverses the actual project declaration types and bodies, audits
their transitive axioms and checks selected material dependencies. Expected
types are never imported by a solution theorem. This is an author mechanical
check, and does not substitute for the independent semantic reviews or the
later Linux Comparator execution.

The statement reviews inspected Schiffer and Forsythe for target/proof
separation and the pinned library APIs for reuse. This implementation uses the
actual Mathlib Gram--Schmidt, matrix inverse, finite maximum and real supremum
APIs; neither example repository is imported as a proof of IE-05. The NLA
adapter to Tau Ceti covers all ten relevant review angles while preserving
NLA's permanent target and ID requirements. No Tau Ceti service endorsement or
external human peer review is claimed.

All failed development attempts remain in their explicitly labelled evidence
directories. Recovery admissions in failed logs are not accepted proof
evidence. Historical seals retain their exact old memberships and hashes;
later additions do not authorize changing earlier inputs or omitting nested
manifests. Current independent reviews must assess the final frozen source
and perform their own fresh checks.
