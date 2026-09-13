# IE-05 mathematical and numerical statements — draft for review

This is the proposed boundary **before proof implementation**. Every assertion
below is an obligation, not an established Lean result. The 17 declarations in
`Challenge.lean` intentionally have reference placeholders. Definitions and
statements may still change in response to coordinator and independent reviews.

## Complete original target

For every natural dimension `n ≥ 2`, let `L_n` be the real unit lower triangular
matrix with all strict-lower entries `−1`. Let `Q_n` be the unique orthogonal
factor of `L_n = Q_n R_n` with upper triangular `R_n` and positive diagonal.
The original assertion is

\[
 \sup\{\rho(A,p):A\in O(n),\ p\text{ an admissible partial-pivoting path}\}
   =\rho(Q_n,\operatorname{firstPath}(Q_n)).
\]

The exported negative result is `¬ OrthogonalExtremizerConjecture`. Its positive
definition retains **all** `n ≥ 2`, all real orthogonal inputs, and all allowable
tie choices on the supremum side. The right side uses increasing current row
positions, retaining the first row when magnitudes tie. An order-eight strict
counterexample negates this full assertion.

`Orthogonal` means the actual matrix identity `A.transpose * A = 1` over `ℝ`.
`candidateQ` is Mathlib's normalized Gram–Schmidt applied to the actual **L2
Euclidean** columns of `L_n`. A separate universal contract must prove that this
definition has the specified positive-diagonal QR property and its uniqueness;
the property is not an argument, field, or assumed fact in the definition.

## Actual elimination and maximum semantics

Indices are zero based. At stage `k`, the active rows and columns are those
`i,j ≥ k`. Choosing current row `p ≥ k` first swaps rows `k,p`, producing `B`;
the next active entries are exactly

\[
 S_{k+1}(i,j)=B(i,j)-\frac{B(i,k)}{B(k,k)}B(k,j),\qquad i,j>k.
\]

The representation pads inactive positions by zero. It does not store the
elimination multipliers there, or count them in growth. Stage zero is the full
input; the maximum uses the `n` stages `0,…,n−1`, including the final pivot.
The post-elimination zero matrix at stage `n` is excluded. An admissible pivot
must be nonzero and of maximal absolute value in its active first column.

`firstPivotIndex` is an actual fold over the increasing list `List.finRange n`,
initialized at `k`, replacing its current index only for a **strictly** larger
active magnitude. It assumes neither successful elimination nor candidate
behavior. `firstPath_semantics` must prove that nonsingularity makes every pivot
valid, that both recursive trajectory definitions agree, and that this is the
unique first-available path. The nonsingularity premise is appropriate to the
general semantics lemma; it is absent from the full conjecture because real
square orthogonality implies nonsingularity.

Entry maxima are `Finset.sup` of actual real nonnegative norms, in `ℝ≥0`, then
coerced to `ℝ`. These are absolute **entries**, not matrix operator, row-sum or
Frobenius norms. Growth is the finite active-stage maximum divided by the input
maximum. Empty dimension has total definitions with zero maxima, but the
original assertion only uses `n ≥ 2`.

The supremum is real `sSup`, with no default-value assumption in a predicate.
The proposed generic bound is

\[
 1\le\rho(A,p)\le 2^{n-1}\quad(n\ge1)
\]

for each actual admissible path. Its first conclusion also proves the input
maximum is positive. The proof obligation starts with the actual one-step
bound `activeMax(next,k+1) ≤ 2*activeMax(current,k)`. The orthogonal growth set
must then be proved nonempty (the identity gives a path) and bounded above.
`le_csSup` may only be applied after that genuine boundedness proof.

## Exact order-eight data

`integerH`, `integerD`, `integerT`, `integerLower` are literal integer data.
Boolean `false` denotes the candidate and `true` the witness. The witness changes
one-based entry **(8,2)** of `L_8` from `−1` to `0`. The later recovered (7,2)
variant is distinct and is not transcribed into these definitions.

For each case, the following finite facts must be proved:

\[
 H^T H=\operatorname{diag}(D),\qquad H=L T,\qquad D_j>0,
\]

with `L` unit lower triangular, `|L_ij| ≤ 1` below its diagonal, and `T` upper
triangular with positive diagonal. Define `Q_ij=H_ij/√D_j`. The genuine diagonal
Gram lemma must establish `Q^T Q=I`.

The scaling vectors are exactly

```
candidate: 8,248,3286,36146,349184,2796544,2,5462
witness:   8,16,240,47640,472430,3644970,16148136,5272
```

The full printed `H,T` arrays remain in `Definitions.lean`. The candidate's `T`
is explicitly supplied, while the manuscript defines it as `L_8⁻¹ H_0`.
Independent integer forward substitution checks that the supplied array has
exactly that value; this arithmetic diagnostic is not an imported theorem.

The universal `scaledLU_trajectory` obligation derives, rather than assumes,

\[
 S_k(i,j)=\frac{\sum_{r=k}^{n-1}L_{ir}T_{rj}}{\sqrt{D_j}}
 \quad(i,j\ge k),
\]

and the no-exchange first-available path. Its hypotheses are only the displayed
factor structure, lower multiplier bound, and positive scalings/diagonals.
It must hold up to `k=n`, where the tail is the empty sum. Positive QR uniqueness
then identifies `normalizedInteger false` with the actual `candidateQ 8`.

## Minimized sufficient certificate

The formalization does not need the manuscript's two exact growth tables.
The following **one-sided** claims suffice and are the reviewed-to-be contract:

1. For all 64 witness entries, prove the integer inequality
   `5272 * H_ij^2 ≤ 3969 * D_j`. Consequently its actual input maximum is
   at most `63/√5272`. Its actual final-pivot numerator is `5272` and its
   last scaling is `5272`, so its final pivot is `√5272`. These give
   `firstGrowth(witnessQ) ≥ 5272/63` without any witness intermediate bound.
2. The single candidate input entry with zero-based index `(2,2)` is
   `51/√3286`, hence its actual input maximum is at least that number.
   No upper bound for the candidate's input maximum is requested.
3. For every candidate active triple `0≤k≤i,j<8`, prove
   `(Σ_{r≥k} L_ir T_rj)^2 ≤ 5462*D_j`. There are 204 such triples; the
   off-active padded zeros do not create extra numerical obligations.
   Thus every actual candidate active entry is at most `√5462`, giving
   `firstGrowth(candidateQ 8)^2 ≤ 17948132/2601`.
4. Prove the exact rational identity and its positive right side:
   `((5272:ℝ)/63)^2 - 17948132/2601 = 117335164/1147041 > 0`.
   Combine these bounds to obtain the strict comparison and then the strict
   real-supremum gap. This uses actual membership of the witness/path in the
   genuinely bounded growth set.

Integer and rational algebra comes before square-root manipulation. The only
potential LeanCert numerical invocation is the **material** final rational
positivity check, explicitly using kernel trust and retaining its consumption
in the full negation. A singleton point check has no subdivision or uncertain
interval width. If ordinary exact arithmetic is simpler, LeanCert's explicit
kernel dependency auditor is sufficient; no artificial interval computation is
required or claimed. This choice remains to be finalized before implementation.

## Scope and outstanding work

The 17 contracts include all universal semantic bridges, not just the finite
order-eight arithmetic. The difficult implementation work is expected in
nonsingular recursive Schur complements, positive-diagonal QR identification
and finite maximum coercions; a numerical pass alone cannot discharge them.
No library theorem asserting the conjecture or the candidate growth is used.

The full original equality will be negated if these contracts are proved. The
formal scope intentionally does not claim the witness's exact growth equality,
the true orthogonal supremum, all active-stage maxima, the recovered variant's
equivalence, the witness's own QR identification, or any asymptotic constant.
