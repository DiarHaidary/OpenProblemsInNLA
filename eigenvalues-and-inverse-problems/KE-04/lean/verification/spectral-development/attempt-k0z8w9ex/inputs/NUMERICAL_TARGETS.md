# KE-04 statement boundary

This is a statement-only draft of the complete affirmative KE-04 resolution. It
contains no numerical experiment, interval certificate, proof implementation, or
claim of formal verification. All constants below are exact structural integers.

The permanent target is
`eigenvalues-and-inverse-problems/KE-04/README.md` at upstream commit
`5830ed4fb06da0659414a3deb2a40ad327aca052`. The complete source proof is Matthew J.
Colbrook's `solution.md` and its `solution.tex`, at that same commit. Exact bytes,
original submission, original target and prior informal review are retained under
`verification/`; `original-source-inventory.json` binds their Git blobs and SHA-256.
The coordinator's source note and the prior informal review are not statement
approvals for this draft.

## Complete target and domains

For every pair of natural dimensions `n,p`, every real `n × n` symmetric matrix
`A`, and every real `n × p` matrix `V` with linearly independent columns, define

\[
K_\ell=\operatorname{span}\{A^r V e_c:0\le r<\ell,\ 0\le c<p\}.
\]

For any `s` satisfying `dim K_s = s*p`, and for every `1 ≤ k < j ≤ s`, independently
choose any orthonormal column bases `Qk` and `Qj` of `K_k` and `K_j`. Let the ordered
eigenvalues of `Qellᵀ A Qell` be
`θ₁^(ell) ≤ … ≤ θ_(ell*p)^(ell)`, with their algebraic multiplicities. For every
`1 ≤ i ≤ (k-1)*p`, the conclusion is

\[
\exists r\in\{1,\ldots,jp\},\qquad
\theta_i^{(k)}<\theta_r^{(j)}<\theta_{i+p}^{(k)}.
\]

`strictIntervalOccupancy : FullPrefixBlockLanczosClaim` states this full-prefix
version, exactly as the source proof's theorem. `blockLanczosConjecture :
BlockLanczosConjecture` states the canonical original convention in which `s` is
the largest index with full block dimension. `fullPrefix_implies_canonical`
explicitly requires proving that the stronger version implies that original
target. The final target does not take either occupancy or polynomial
nonannihilation as an additional hypothesis.

The dimensions are not capped, the matrices are not rational-only, and no bound on
their entries, norm, spectrum, or conditioning is imposed. No positivity,
invertibility of `A`, simple spectrum, distinct endpoints, or compatibility of
bases between iterations is assumed. There is no probability law or
floating-point model; this is the source's exact real arithmetic statement.

## Exact objects and indexing

`Vec n` is Mathlib's `EuclideanSpace ℝ (Fin n)`, with its actual L2 inner product.
`act` is `Matrix.toEuclideanLin`, not an uninterpreted action. `FullColumnRank`
is actual `LinearIndependent` for the starting columns. `krylovColumns` has index
`Fin ell × Fin p`; `krylov` is the actual span of those columns, and
`krylovCombination` is Mathlib's finite linear-combination map. Range, coefficient
uniqueness, nesting, one-power propagation, and dimension/independence equivalence
are separate obligations.

`FullBlockDimension A V ell` means only `Module.finrank ℝ (krylov A V ell) = ell*p`.
`fullBlockDimension_prefix` must derive all previous full dimensions from the
single condition at `s`. `IsKrylovBasis` contains exactly `QᵀQ=I` and equality of
column space with `K_ell`; `krylovBasis_exists` must prove an appropriate basis
exists, so the universal basis quantification is not supported merely by a
possibly empty custom type. `frameProjection_semantics` and
`compression_semantics` relate `Q Qᵀ` and `Qᵀ A Q` to the actual orthogonal
projection and the compressed operator on the subspace.

The spectrum uses Mathlib's genuine self-adjoint spectral theorem, not a proposed
list of eigenvalues accompanied by desired properties. Its decreasing ordered
`LinearMap.IsSymmetric.eigenvalues` is reversed using `Fin.rev`, and its matching
orthonormal eigenbasis is reindexed by the same involution. The explicit
`orderedSpectrum_semantics` obligation includes monotonicity, the eigenvector
equations, and equality with the characteristic-root **multiset**, not merely
equality of sets of distinct values. `compression_basis_independent` requires
orthogonal similarity, equal characteristic polynomials, and equality of the
whole ordered eigenvalue functions for arbitrary equal-span orthonormal frames.

Natural `i` in the target is one-based. Lean's endpoints are `i-1` and `i+p-1`,
and the later witness is `r : Fin (j*p)`. The total helper `eigenvalueAt` has an
out-of-range value of zero; `interval_index_validity` proves that neither endpoint
can use that branch in any admissible target case. It also derives `k ≥ 2` and
`p > 0` from the admissible index bounds. Both inequalities in the target are
strict; there is no endpoint inclusion or non-strict substitute.

For `p=0`, every block Krylov space has dimension zero and there is no largest
full-dimension index. Accordingly `lastFullBlockIteration_exists` has the necessary
hypothesis `0 < p`. It also uses the source full rank of `V` to obtain `s ≥ 1`.
The full-prefix target still quantifies over `p=0`, where there is no admissible
`i`. The same empty index range handles `k=1`; `n=0` admits no positive-width
full-column-rank `V`. No false maximality-existence assertion is made in these
degenerate cases.

## Exact degree-two argument and every bridge

Put `a=θ_i^(k)`, `b=θ_(i+p)^(k)`, and `q(t)=(t-a)(t-b)`. The structural constants
are the monic leading coefficient `1`, degree `2`, window dimension `p+1`,
codimension `p`, and the powers through `A^k V` (full rank at `k+1`). There is no
approximate gap, tolerance, rational box, mesh, or certificate precision.

1. `quadratic_semantics` identifies this actual monic polynomial with the matrix
   evaluation `M²-(a+b)M+abI`. `spectral_gap_quadratic_psd` must derive PSD of the
   later quadratic from absence of a later eigenvalue in the open interval and
   the already derivable weak endpoint order `a ≤ b`. It includes `a=b`.
2. `spectral_window_subspace` must construct a subspace of dimension `p+1` from
   the `p+1` consecutive indexed earlier eigenvectors, including repetitions of
   their eigenvalues, and establish its nonpositive quadratic form.
3. `krylov_intersection_nonzero` must derive a nonzero vector in that subspace
   and `K_(k-1)` using the actual dimensions, nesting, and intersection formula.
   Its hypotheses do not include the conclusion or an unexplained vector.
4. `compressedQuadratic A Q a b` is exactly `Q q(Qᵀ A Q) Qᵀ`, the subspace
   quadratic extended by zero. It is not `q(Q Qᵀ A Q Qᵀ)` on the ambient space:
   the latter would add an unwanted `ab` term on the orthogonal complement.
   `compressedQuadratic_semantics` proves the quadratic-form transport and PSD
   transport needed to reason in one common ambient Euclidean space.
5. `quadratic_forms_agree` must prove equality of the earlier and later quadratic
   forms on `K_(k-1)`, using symmetry and `H_k x = H_j x = A x`. It does not
   assert `H_k²x = A²x`. `psd_zero_form_iff_kernel` must convert the zero later
   PSD quadratic form to an actual kernel equation.
6. `later_quadratic_identity` must use `k+1 ≤ j`, the true Krylov shift, and
   `A²x ∈ K_(k+1) ⊆ K_j` to identify the later quadratic action with `q(A)x`.
7. `fullRank_quadratic_nonannihilation` must prove, from full rank at `k+1`, that
   no nonzero `x ∈ K_(k-1)` is annihilated by this monic quadratic. The original
   proof uses the highest nonzero block coefficient of `x`; multiplying by
   a monic quadratic leaves that coefficient nonzero at degree two higher,
   still among the independent columns through degree `k`. The bridge is an
   exported proof obligation, never part of the input data or final hypotheses.
8. `strictIntervalOccupancy` must assemble the contradiction for every original
   matrix, dimension, iteration pair, basis pair and index; the last two exports
   then reach the canonical largest-`s` target.

Coincident proposed endpoints lead to the same contradiction with `(t-a)²`;
strict endpoint separation is an outcome in the admissible range, not a premise.
No lemma here requires a strict ordering of all Ritz values or spectral simplicity.

## Trust and remaining work

LeanCert is pinned to `621a43d7cf21f87872392a01e874f2f1dbddc926` with Lean 4.33.1.
This finite-dimensional argument needs no artificial numerical interval work.
Its current concrete role is the definition-only `#assert_trust kernel` audit,
together with actual `#print axioms` output. A future proof inspector must audit
every exported theorem, with only `propext`, `Classical.choice`, and `Quot.sound`
permitted. The placeholder-bearing Challenge is excluded from the definition
audit and must never be imported by a future Solution.

All 24 Challenge statements are unproved. Fresh source elaboration only checks
their types. Two new independent statement approvals on exact bytes and the
coordinator's acceptance are required before any proof implementation. Any
mathematical change after those reviews reopens that gate.
