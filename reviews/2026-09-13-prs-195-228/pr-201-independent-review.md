# PR 201 — independent mathematical review

**Head:** `f1e8b7d324823ccca225cbd261330b727b423cab`  
**Published base:** `5830ed4fb06da0659414a3deb2a40ad327aca052`  
**Disposition:** PASS for the stated partial results. No mathematical blocker found. This submission alone does not resolve unrestricted RA-04.

I read the complete 304-line Markdown report and complete 388-line LaTeX manuscript, the original canonical target and its diff, and both executable checkers. I did not use the submitted audit verdict as evidence. The prior PR 191 theorem and its primary convergence dependency were independently audited earlier in this review session; that review is `/private/tmp/nla-pr-191-independent-review.md`.

The Gaussian rectangular-block estimate correctly uses the independently signed least left singular vector, its independence from singular values, the inverse-Gram row-distance identity, and a chi lower tail. It applies to every block with at most b rows. The barycentric row error and tail ratio are valid without a leading condition-number factor, including signed normalization constants. The rectangular right inverse is in the correct order: R0(I+ER0)^(-1), followed by D^(-1). The width assumption bounds ||ER0|| by 1/2 on the common event, so no independence between the Gaussian block and its perturbation is assumed. Three failure events cost exactly delta; an empty tail is harmless.

The t-band corollary requires the displayed width restriction. The relative-gap comparison follows from the ratios of band endpoints; the stronger intermediate beta±2w bounds in LaTeX also hold under this restriction. The fixed-spectrum corollary splits delta at m^(-t) correctly and explicitly relies on the earlier extra-t-log-m all-input theorem. It does not silently exchange a spectrum dependent on delta for one fixed spectrum.

The balanced-coloring construction proves the full rectangular Vandermonde rank statement, including repeated nodes with multiplicity at most b. In exact tail deflation, the full cutoff multiplicity matters: rho=a+min(d_theta,b), not merely k. Chosen cutoff rows span the accessible cutoff directions when d_theta>b, while all strictly higher directions remain independently accessible. Counting zero once in the distinct lower tail gives the correct polynomial degree. The example (5,4,3,2,2,2), b=2,k=4 correctly needs a third block for exact Frobenius recovery; it is not presented as an RA-04 counterexample.

The convergence import matches the original prescribed projection/SVD algorithm and ordered **right** singular-vector energy convention: Chen et al., [arXiv:2508.06486v2](https://arxiv.org/html/2508.06486v2), Definition 3.1, Imported Theorem 3.2, Observation 3.3. The earlier PR 191 result is credited with an immutable revision link. The RA-04 ID, path, and original mathematical target are preserved; the canonical status is Partially resolved.

After inspecting the scripts, I ran their scratch copies using Python 3.12.14, NumPy 2.3.5 and SymPy 1.14.0. All 459 rational coloring cases, three rational graph fixtures and the exact cutoff-boundary check passed. The optional numerical script produced all 27 diagnostics, including cases explicitly outside the proved width; these are not probability or theorem certificates. Outputs are under `/private/tmp/nla-pr-201-independent-run`.

I also wrote `/private/tmp/nla-ra04-new-independent.py` without importing submitted code. It exactly checks a new unequal-band rectangular graph with sizes (1,2,1), Krylov membership, and a separate deflation fixture with a cutoff multiplicity exceeding b and a zero tail. All passed; output `/private/tmp/nla-ra04-new-independent.json`.

I visually inspected every page of the canonical PDF (2 pages) and manuscript PDF (7 pages), rendered with Poppler. No clipped equations, missing glyphs, overlapping text, or status discrepancy was observed. Images and page inventory are under `/private/tmp/nla-ra04-new-pdf-review`.

This is an independent informal mathematical/code audit, not external peer review or a proof-assistant certificate. Reviewed worktree remained unchanged and clean. When integrating this continuation with PR 191 and any later full proof, retain both earlier partial-result records rather than overwriting their history.
