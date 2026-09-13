# PR 197 independent review

Exact source head: `31756a4a1cc997e48af77637ee90f44e3b8fb7fb`.
Published comparison base: `5830ed4fb06da0659414a3deb2a40ad327aca052`.
Read-only checkout: `/private/tmp/nla-audit-197`.

**Disposition: PASS for the stated partial results. No mathematical or publication blocker found. RA-17 remains partially resolved and open.** This is an independent informal mathematical/code audit, not formal verification or external human peer review.

## Material reviewed and mathematical scope

I read the entire 715-line actual manuscript `references/holden-ra17-2026-09-12/writeup/RA17_exact_cases_and_bounds.tex`, all five supplied code files (580 lines), the original target, canonical README/LaTeX presentation, package README, source notes, certificate inputs, PR body and exact head. I did not treat the submitted review or saved PASS output as evidence of correctness.

The original target remains the exact minimum number of unrestricted real linear measurements uniformly injective on every real square rank-at-most-r matrix. The proof uses the rank-at-most-2r difference set correctly; no PSD, generic-signal, decoder, or probabilistic assumption is substituted.

The following arguments check out:

- The kernel/difference equivalence, rank-nullity conversion to independent measurements, full-difference boundary d=2r, and odd-determinant boundary d=2r+1 are valid. The antidiagonal construction has exactly (d-2r)^2 free parameters. Its first nonzero antidiagonal produces a triangular (2r+1)-minor with nonzero diagonal; the integer finite-difference measurement rows have the claimed independence and annihilator.
- Restriction to complementary planes gives a fiberwise injection of the trivial kernel bundle into dQ. The rank, Pontryagin and Stiefel-Whitney formulas follow from this actual injection. The rational ring used is the **unoriented** Grassmannian ring, in both ambient parities. The rectangular Schur coefficient is nonzero. The Euler-square refinement treats the odd-dimensional orientation local system correctly: the Poincare-dual degree is 2r(s+1), and the mod-four vanishing condition has the stated parity. The rank-one refinement on the oriented two-plane cover and the four-by-four H²=0, p1≠0 obstruction are valid.
- Both Xu measurement variants retain source attribution and explicitly identify the two different entries. Simultaneous transpose is harmless because it preserves the rank cone. The exact construction proves a necessary real-eigenvalue condition using evaluated row relations and the constant monomial 1; it does **not** assume a truncated Macaulay reduction is a full Groebner basis. The separate degree-five full-rank homogeneous calculation rules out the entire chart at infinity over C. Thus the upper bound eleven and the independent lower bound eleven prove μ_R(4,1)=11.
- The odd-degree argument uses an open real-avoidance neighborhood, a sufficiently small generic real perturbation, and conjugate pairing of transverse complex intersection points. It only infers exactness for odd degree, never existence from even degree or vanishing characteristic classes.
- The quaternion/octonion and 16-fold Clifford constructions satisfy the full norm coefficient identity, establishing independence and nonsingularity for every nonzero parameter. The cofactor map A+i adj(A)^T is invertible on real rank-at-least-(d−1) matrices and odd for even d. Complex K-theory then gives κ≤2ν₂(d)+2. The manuscript only claims the corank-one exact families where its explicit construction matches that bound; it correctly avoids relying on the broader wording of Causin Proposition 3.6. The Xu–octonion block lift has minimum rank d−1 and parameter dimension five.
- The numerical table is expressly a table of the manuscript's bounds, not a literature-wide optimality claim. The gaps (12,5) and (16,7) remain explicit. Schur enumeration skipped for size limits is not labeled an exact classification.

## Primary imports checked

I read the relevant statements and surrounding definitions directly in:

- [Xu, arXiv:1505.07204v1](https://arxiv.org/pdf/1505.07204v1), equation (3.5) and Theorem 3.2; and the [author's Maple data](https://lsec.cc.ac.cn/~xuzq/rank1.htm). The two input discrepancies and vectorization convention agree with the manuscript.
- [Xu's 2026 survey, Theorem 5.5](https://arxiv.org/html/2506.17572v2), including the rank-range restriction on d=2^a+r and the real-versus-complex distinction.
- [Carlson, Corollary 2.3, printed pp.10–11](https://arxiv.org/pdf/1611.01175v2) and [He, Corollary 5.26, printed p.19](https://arxiv.org/pdf/1609.06243): the two unoriented even-plane rational presentations used here are exactly the stated ones. Carlson's oriented-cover presentation also corroborates the rank-one Euler-root argument.
- [Matszangosz–Wendt, Section 3.1](https://arxiv.org/pdf/2310.11129), for the recalled **unoriented** mod-two ring.
- [Causin, Propositions 2.1–2.4 and Theorem 3.5](https://arxiv.org/pdf/0911.1810v1): the complexified tautological class has order 2^floor((κ−1)/2), and the real even-size minimum-rank-(d−1) bound applies as used.

Rees is historical context only: the construction needed for the proof is supplied and checked directly.

## Reproduced and independent computations

All runs used scratch copies; the audited checkout stayed unchanged. Runtime was `/private/tmp/nla-batch-python/bin/python` (Python 3.12, SymPy 1.14). Scratch evidence is `/private/tmp/nla-pr-197-independent-run`.

1. Ran the inspected `verify_xu.py --variant both --backend sympy`, independently of the submitted GMP execution. Both variants regenerated rank(W)=11, all sixteen cubic minors, affine rank 106/126, the twenty-dimensional multiplication matrix and exact degree-20 characteristic polynomial, Sturm variations 10→10, and homogeneous infinity rank 56/56. Both regenerated saved certificates agree. Logs: `xu.log`; newly generated certificates: `results/verified_{paper,website}.json`.
2. Ran the inspected construction suite. All 25 antidiagonal systems through d=10 passed exact dimensions/ranks/annihilation; every Hurwitz norm coefficient passed at sizes 1,2,4,8,16,24,32; all three Xu block lifts passed; all 256 degree/parity/bound checks through d=32 passed, including the asserted exact cases and unresolved intervals. Log: `constructions.log`.
3. Regenerated the full bounds table through d=16 with Schur enumeration enabled. Log: `bounds.log`; output `results/bounds_table.json`.
4. Wrote `/private/tmp/nla-ra17-independent-checks.py`, with results `/private/tmp/nla-ra17-independent-checks.json`. It independently computes all rank-one SW classes by polynomial multiplication and Groebner reduction in the Grassmannian quotient for d=3,…,14, compares their actual last nonzero degree with the submitted hook/Schur implementation, computes determinantal degrees by a separate Jacobi–Trudi determinant, and verifies fresh nonsymmetric rank-(d−1) cofactor examples at d=4,6,8. These checks pass. The same file also contains separate index checks relevant to PR223.

These exact computations verify algebra and finite instances. The all-parameter topological implications were assessed from the written proofs and primary hypotheses, not inferred from finite tests.

## Publication and PDF disposition

The ID RA-17, canonical path and full original target are preserved. The canonical page and package consistently claim partial resolution, explicitly retain open gaps, and do not claim Lean verification, external peer review or priority.

Using the PDF skill, I rendered and visually inspected all **2 canonical pages and 17 manuscript pages**. Equations, tables, references and page boundaries are readable; no clipping, missing symbols or misleading solved status was found. Render evidence: `/private/tmp/nla-ra17-pdf-review/197-canonical` and `197-manuscript`.

Integration must preserve the stronger later partial results separately; this PR by itself establishes exactly the scope above, not an all-dimension solution.
