# Independent informal mathematical review: IE-28

Reviewed 13 September 2026 by a separate Codex AI agent, independently of the submitting/coordinating agent. No Lean or other formal verification was performed. This is an informal automated mathematical audit, not external human peer review or a novelty assessment.

## Verdict

PASS for the partial results listed below. FAIL as a full resolution: neither bundle proves nor disproves the original universal positive-diagonal existence assertion. Keep IE-28 **Partially resolved**, as required by RESOLVED.md, “Recording a new resolution,” item 3. The remaining target is arbitrary prescribed positive distinct nodes in every stage count n >= 4. No result justifies marking IE-28 Solved.

## Material examined

The canonical IE-28 README and repository resolution policy; the complete editable `IE28_extended_results/writeup.tex`; its scope audit; the exact certificate verifier, supplied certificates and symbolic regression tests; and `IE-28_verified_extensions/STRUCTURAL_REDUCTION.md` with its verification script. The recovered PDF in the second bundle is historical supporting material, not an independently re-audited additional theorem source in this review.

## Accepted scope and mathematical checks

1. **Every two- and three-node set** (extended writeup, Section 2). The eigenpolynomial construction gives one eigenvalue equal to one. For two stages the determinant fixes the remaining eigenvalue. For three stages the determinant-normalized root has uniform positive lower/upper brackets, making it continuous even at theta = 0. The exact endpoint trace identities have opposite signs, so the intermediate value theorem gives trace three. The remaining two eigenvalues consequently have sum two and product one. This reasoning does not extend to general stage count.
2. **Scaled Laguerre nodes, all stage counts** (Theorem 3.2). Integration modulo the node polynomial in the factorial-scaled monomial basis gives the claimed companion characteristic polynomial. Matching coefficients gives exactly the scaled ordinary Laguerre node polynomial for a scalar positive diagonal. Rodrigues orthogonality proves positivity and simplicity of its n zeros. This is a special family, not all node sets.
3. **All-stage local clustered-node existence** (Theorem 5.3). Alternant divisibility genuinely regularizes the determinant as a polynomial. The augmented Taylor recursion proves the confluent determinant identity with the correct normalization. Reversing coefficient equations yields a triangular Jacobian with nonzero diagonal. The implicit function theorem applies to the regularized coefficient system, and positivity follows by continuity from g(1) = (n!)^(1/n). The neighborhood depends on n; no global continuation argument is supplied.
4. **Eleven-stage nonnegative-coefficient eigenpolynomial obstruction** (Proposition 6.1 and Theorem 6.2). The exact root bracket and outward integer interval recurrence establish the strict negative leading coefficient. The normalized nonnegative polynomials lie in a compact simplex; their logarithmic derivatives converge uniformly with the required derivatives near 1. Interpolation tends to the Taylor jet, and the unique negative-a1 seed forces the limiting polynomial to have the certified negative coefficient. This excludes only the stronger eigenpolynomial ansatz. It is compatible with positive diagonals guaranteed locally by item 3.
5. **Six points and six specified node boxes, dimensions 4–7** (Section 7). The verifier recomputes the characteristic coefficients and Jacobian through interval principal minors and verifies strict contraction/self-mapping. The theorem correctly establishes invertibility of the preconditioner from the derivative bound, so fixed points are actual zeros. Positivity and separated admissible nodes are checked. Uniqueness is only within the specified diagonal box.
6. **Structural supplement** (STRUCTURAL_REDUCTION.md, Sections 2–4). Differentiating the cardinal polynomials on the degree-n zero-at-origin space gives the claimed diagonal similarity to a diagonal-plus-skew reciprocal-difference matrix. Row differentiation of the Vandermonde determinant proves the all-subset principal-minor identity. The auxiliary 3x3 matrix has principal minors 1, 17, 49; AM–GM contradicts the necessary characteristic equations because 17^3 > 49^2. It does not have the required collocation reciprocal-difference structure and is not a counterexample to IE-28.

No mathematical correction was necessary for these restricted claims.

## Replayed checks

- All twelve exact point/neighborhood certificates: PASS (`ie28-certificates-review.log`).
- Eleven-stage strict sign certificate: PASS (`ie28-seed-review.log`).
- Complete exact regression suite: PASS (`ie28-exact-review.log`): 1,500 rational interval trials; 50 exact determinant comparisons; formal seed Jacobians n=2..6; confluent identities n=2..5; collocation identities n=2..7; Laguerre identities n=1..15; all twelve certificates and three corrupt-input rejection tests.
- Prior symbolic endpoint checks: PASS (`ie28-symbolic-review.log`).
- Structural reduction script: PASS (`ie28-structural-review.log`), including all principal subsets at its four prescribed node sets and the auxiliary counterexample.

Python 3.9 initially failed because int.bit_count requires newer Python; that was an environment mismatch, not a failed mathematical certificate. Successful exact regression used bundled Python with SymPy 1.14.0 and mpmath made available from an existing environment. Numerical continuation results for n=8,11,15 were not promoted to exact certificates or used to establish any accepted theorem. Finite regression checks supplement the analytical audit; they do not prove universal statements by sampling.

## Overlap and packaging

Both bundles describe the same two-/three-stage and clustered-node results and eleven-stage auxiliary obstruction. Record a single IE-28 submission/update, with the main extended writeup as the proof source and the structural note as a supplement. Do not count these as separate problem resolutions.

The structural bundle README describes additional recovered source, continued_work and additional_checks files that are absent from the supplied extraction; only recovered_work/report.pdf is present there. A submission wrapper should accurately list delivered files and avoid repeating those availability claims. The extended-results bundle contains the editable main proof and verification dependencies used above. Original AI attribution in supplied files should be preserved as provenance while the requested submission authorship is added transparently.
