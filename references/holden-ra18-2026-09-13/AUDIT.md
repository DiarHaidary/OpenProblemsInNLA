# Mathematical audit

## Claim boundaries

The central claim is that there is no finite constant `alpha`, independent of **both** `r` and `n`, with `t_C(r,n) <= alpha*sqrt(n)` for all complex isometries. It is not a counterexample to the real GTZ conjecture. It is not a claim that the constructed frames attain the global maximum defining `t_C`. It is not a proof of the optimal complex exponent.

The real result is restricted to matrices having at most `r+2` distinct nonzero row directions. The unrestricted real problem remains outside the proof.

## Minimal route through the main proof

1. **Isometry.** The two local columns `a,c` have norm one and zero complex inner product. This verifies the entire column Gram matrix of the lift, including its off-diagonal blocks.

2. **All bases.** A missing row group makes a new column zero. Three rows from one group are dependent. Every nonsingular selection therefore has one or two rows in each group, exactly `r` doubled groups, and an invertible parent submatrix. The manuscript proves both directions by an explicit nullspace calculation. No unexamined row-selection patterns remain.

3. **Complex conjugation.** The actual top-right Gram block is `U* diag(s_i)`. Since every `s_i` has modulus one, the diagonal unitary on the new columns is `diag(conj(s_i))`. This produces the canonical block `U*`, not an incorrectly transposed or unconjugated block.

4. **Rayleigh test.** With `G=U_I* U_I`, `D=I+diag(1_I)`, and a unit `g`-eigenvector `x`, use `z=(x,-D^{-1}Ux)`. The numerator is `g/2`, the denominator `2-3g/4`. Both are evaluated for the full selected Gram matrix, not only a Schur complement.

5. **Direction of optimization.** The upper bound on the smallest Gram eigenvalue becomes a lower bound on the squared inverse norm. It holds for every nonsingular lifted selection, so minimizing over them gives `b(T(U)) >= 4*b(U)-3/2`.

6. **Unbounded ratio.** With `b(U_0)=2`, the recurrence gives `(3*4**k+1)/2`, while the number of rows is `2*3**k`. Dividing the **squared** inverse norm by the number of rows gives a quantity tending to infinity. This is what excludes every fixed `alpha`.

The printed and recorded lower bounds retain half-integers exactly, for example `13/2` at level one; they are not rounded down to integers.

## Exact spectral refinement

The `3 x 3` block reduction requires `n=2r`. The simpler amplification inequality does not. The manuscript makes this distinction explicitly.

The rational map is inverted only on `[0,1/3]`, where it is strictly increasing from zero to one. Selecting another root of the cubic would be incorrect. The smallest eigenvalue is identified using positivity and the unique root in this interval; endpoint cases are handled separately.

The full-spectrum induction is stronger than the common-smallest-eigenvalue statement. Its inputs are the entire parent spectrum and the exact legal-basis classification. Cauchy–Binet then checks the equal determinant against the exact number of bases.

The limiting constant belongs to the explicit family. Exact rational interval propagation, combined with `0 < L - 4**k*g_k <= (2/45)*16**(-k)`, certifies the reported enclosure. The decimal table and this rational enclosure are different computational products.

## Real-class theorem

The weighted-duality equivalence requires `eta*m_i < 1`. For the theorem, `eta=1/N` and at least two nonempty groups make this strict. The square compressed case `q=r` is handled separately.

The reduction does not assume equal lengths inside a parallel row group. It compresses the total squared norm and uses a largest-norm representative, whose rank-one contribution dominates the group average. The transformed low-column frame is an isometry. A nonsingular selection of replicated rows cannot repeat a group, which is essential to taking its complement.

The only non-elementary input to the structured real theorem is the cited real two-column result. No use of that result appears in the proof disproving the complex extension.

## Checks actually performed

All recorded checks passed. The exact script and complete output are supplied, rather than only a success claim.

| Check | Coverage | Arithmetic |
|---|---|---|
| First-level matrix | All 20 square selections | Symbolic |
| Second-level matrix | All 48,620 square selections | Floating point plus exact combinatorial classification |
| General lift identities | 500 selected bases of random frames | Floating point |
| Third-level matrix | 200 recursively sampled bases | Floating point; **not exhaustive** |
| Grouped real selector | 80 generated instances | Floating point |
| Weighted-duality equivalence | 1,212 selections away from numerical ambiguity | Floating point |
| Real sharpness fixtures | Four multiplicity patterns, all square selections | Floating point, with analytic identity in manuscript |
| Asymptotic limit | Through level 20, plus an analytic tail | Exact rational intervals |

Small numerical residuals are not a substitute for proofs. No claim of formal verification or independent peer review is made.

## A concrete barrier to transferring the counterexample to the real field

For the `6 x 3` complex example, standard realification is `12 x 6`. Its real rows numbered `{4,5,6,7,8,9}` in one-based block order form a matrix whose Gram matrix is exactly `I_6/2`. This identity is checked symbolically. Arbitrary real row selections are not restricted to real–imaginary row pairs, so the complex obstruction does not survive as a real obstruction by this operation.
