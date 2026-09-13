# PR #239 independent mathematical audit

**Verdict: PASS for the stated partial result. No actionable blocker found.**

Audited head: `37bd70b93d56a0e722d3f463b3f2158015e2bf04` against base `b73cd1804e40e0d101294eedb156984f0d62b4a6`. Source: `/private/tmp/nla-audit-239`. Review date: 13 September 2026. This is an independent informal AI audit, not human peer review, a novelty certificate, or formal proof verification.

## Exact scope

The submitted theorem refutes the separately stated complex dimension-independent constant. It does **not** refute or prove the unrestricted original real square-root conjecture. The real theorem covers frames with at most `r+2` nonzero row directions. The canonical README retains the original real mathematical target, retained complex conjecture text, permanent RA-18 path/ID, prior references and Partially resolved status. The added RESOLVED record repeats those qualifications. No previous contribution was removed or replaced.

## Full argument review

Read the complete 680-line manuscript, all actual Python implementation/verification code, and canonical text changes. Submitted checklists and previous PASS reports were not taken as evidence of correctness.

- **Isometry and all-bases classification:** the new columns are orthogonal because the three roots sum to zero. Missing groups create zero columns and tripled groups create row dependencies. With `n+r` selected rows, every legal selection therefore has exactly `r` doubled groups; nullspace elimination proves equivalence with an invertible parent basis. This genuinely covers every square row subset.
- **Phase removal and amplification:** singleton and doubleton phase sums have modulus one. Conjugation gives the displayed canonical Gram matrix. For a parent least-eigenvector with eigenvalue `g`, the test vector `(x,-D^{-1}Ux)` has energy `g/2` and squared norm `2-3g/4`. The resulting reciprocal inequality is `4/g-3/2`, and minimization over all parent bases is in the correct direction. Iteration from `b(U0)=2` proves the divergent square-root ratio without numerical assumptions.
- **Exact spectrum:** the half-rank decomposition uses complementary parent Gram matrices `G` and `I-G`; zero complement columns can be completed to orthonormal bases. The 3-by-3 blocks, characteristic polynomial, derivative of the rational map, inverse branch on `[0,1/3]`, and monotonicity all check. The common-spectrum induction, basis count `2*3^(3^k-1)`, Cauchy–Binet determinants and monic polynomial recurrence agree.
- **Asymptotic enclosure:** `4^k g_k` increases, the earlier lower bound bounds it above, and the cubic remainder gives the geometric tail `(2/45)16^-k`. Exact rational endpoint propagation is outward and legitimate.
- **Other dimensions:** complement duality, block direct sums, row replication and zero padding preserve the claimed inverse-norm relations. The constants `sqrt(3/8)` and `sqrt(3/32)` follow with the stated floors and cover every `1<=r<n`.
- **Weighted real theorem:** the two square Gram comparisons and Schur complement give the stated weighted equivalence. Compression by row directions and choice of maximum-norm representatives is valid for arbitrary lengths/signs and multiplicities. The strict condition `m_i<N` holds in the excess-rank cases. Replication reduces the result to real one/two-column selection without allowing duplicated parallel rows in a nonsingular basis.
- **Sharp real fixtures and field distinction:** the unequal-simplex identity is PSD with rank `r-1`, giving equality `1/N` in every distinct-group selection. The realification example has the claimed orthogonal basis; arbitrary real row selections cannot be identified with paired complex selections.

## Primary-source verification

Opened and read [Sengupta–Pautov v5](https://arxiv.org/html/2604.05944v5), including its complete two-column argument. Its hypotheses and conclusion match the real theorem’s only non-elementary imported selection result: arbitrary real `N x 2` isometry and smallest selected singular value at least `1/sqrt(N)`. Its small-row induction and positive-matrix/Perron argument are consistent.

Opened [Nesterenko v1](https://arxiv.org/html/2604.24087v1), Proposition 1, to verify the complex two-column comparison constant. The recursive complex obstruction does not depend on either paper. The maximal-volume upper bound is proved directly in the submitted manuscript; no unseen publisher proof is imported.

The [official Simons Foundation profile](https://www.simonsfoundation.org/people/sidney-holden/) identifies Sidney Holden as Flatiron Research Fellow in CCB, consistent with the credited affiliation. This checks affiliation, not independent authorship/priority provenance.

## Fresh computations

Runtime: Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0, mpmath 1.3.0. `PYTHONDONTWRITEBYTECODE=1`; output directed to scratch; no source mutation.

The complete supplied verifier was actually rerun, with fresh output `/private/tmp/nla-239-new-results/verification.json` and log `/private/tmp/nla-239-check.log`:

- Symbolic first-lift orthogonality, all 20 minors, 18 nonsingular spectra, rational map identities, realification and degree-9 recurrence passed.
- Every one of the 48,620 level-2 square subsets was enumerated. Exactly 13,122 were nonsingular and 35,498 singular, with zero structural/numerical mismatches. Maximum full-spectrum error was `1.23e-15`.
- 500 random lifted bases, 200 level-3 samples, 80 grouped real cases, 1,212 weighted-duality comparisons, and four unequal-multiplicity equality fixtures passed.
- Exact rational bisection reproduced `0.50974201649977507082328463645059... < L < 0.50974201649977507082328467321417...`.

An independent scratch implementation `/private/tmp/nla-independent-239-243.py` rebuilt the lift directly from rows, without calling submission helpers. It enumerated 3,036 subsets of eight additional parents including `n=r`, zero rows, unit Gram eigenvalues, real and complex unbalanced frames. All 1,092 nonsingular cases satisfied the amplification inequality; minimum slack was approximately 0.5 and maximum half-rank spectrum error `8.89e-16`. A further 176 weighted-duality comparisons included thresholds approaching `eta*max(m)=1`; no robust-sign disagreement occurred (seven cases were within `1e-8` of a boundary and were not assigned a sign test). Output: `/private/tmp/nla-independent-239-243-results.json`.

The repository-edition manifest’s 20 listed hashes matched. This establishes byte consistency only; original upload authenticity is outside this audit.

## PDF inspection

Applied the PDF skill read-only. Rendered and visually inspected all 14 manuscript pages and all three canonical problem pages with Poppler. Mathematical symbols, equations, table values, footnotes, page transitions, references and scope text were legible; no clipping, overlap or broken symbols found. The canonical PDF accurately preserves the original real target and distinguishes the negative complex result. No PDF was reauthored.

## Limits and disposition

No Lean formalization is present or claimed. Finite enumerations support algebra but are not the proof of the infinite-family theorem; acceptance rests on the argument above. No optimal complex exponent or full real resolution follows. Root review owns shared catalog/ID/CI integration checks. Both source worktrees remained clean.
