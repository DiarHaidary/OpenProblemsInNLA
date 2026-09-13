# TR-29: the two-factor case — Maximilian Behr

**Author:** Maximilian Behr. **Contact:** maximilian.behr@gmx.de.

**Submission date:** 2026-09-13. **Whole-entry status: Partially resolved.**

[Manuscript PDF](manuscript/TR29_two_factor_rank.pdf) · [LaTeX source](manuscript/TR29_two_factor_rank.tex) · [Canonical target](../../tensor-computations/TR-29/README.md) · [Independent review](verification/independent-review.md).

## Exact scope

Theorem 1.1 proves, over the complex numbers, that the partially symmetric rank of $`W_{d_1}\otimes W_{d_2}`$ equals $`2(d_1+d_2-2)`$ for all $`d_1,d_2\ge2`$; this is the case $`k=2`$ of the catalog target and of Oneto–Ventura, Question 12. Corollary 5.4 determines $`R(x^ay^b\otimes u^cv^d)=(a+1)(c+1)-(a-b)(c-d)`$ for all $`a\ge b\ge1`$, $`c\ge d\ge1`$.

**Still open:** every tuple with $`k\ge3`$ factors, for example $`W_3\otimes W_3\otimes W_3`$ (known here only $`17\le R\le20`$; that lower bound is not part of this submission).

## Credit and prior work

- Upper bound: Gałązka, *Multigraded apolarity*, Thm 1.5(i) (Math. Nachr. Thm 1.8(i)); Canino–Casarotti–Santarsiero, Thm 1.1.
- Known equality cases: $`d_1=2`$ or $`d_2=2`$ (Ballico–Bernardi–Christandl–Gesmundo Prop 4.4; Gałązka Thm 1.5(ii)), $`(3,3)`$ (BBCG Prop 4.2), $`(4,4)`$ (Gałązka, unpublished note, 2021).
- The catalecticant–Sylvester inequality (Lemma 3.4) is, up to notation, the key step of Wang–Seigal, arXiv:2202.11740. The peeling idea of Lemma 3.3 appears in BBCG Prop 4.4 and in Gałązka's proofs of Thm 1.5(ii),(iii). New here is their combination at the unbalanced pair of bidegrees $`(1,q)/(p,1)`$.
- The rank theorem for binary forms used in Section 5 is Comas–Seiguer (2011).
- Gałązka's thesis (2023), Remark 1.10, anticipates the value $`2(k+m)`$ for $`x^kyz^mw`$ over the reals without proof.

## Review and reproducibility

- [Independent review](verification/independent-review.md): a separate AI agent refereed both the two-factor theorem and the monomial formula (verdict: correct; issues were attribution and exposition, addressed in the manuscript) and searched the literature for prior proofs (none found; bounded search).
- [Internal referee passes](verification/internal-referee/): a second AI agent's two referee passes and its independent checks.
- [Checks](code/): `code/run_all.sh` reruns every check (Python 3 with sympy and numpy, see `code/requirements.txt`; the exhaustive finite-field search K6 takes about 30 minutes on one core). [Rerun logs](verification/rerun-logs/) from 2026-09-13: K1 and K4 ALL OK; K2 Lemma 3.3 confirmed in all 13 runs; K3 no spanning subset of size $`2(p+q)-1`$; K6 no 8 of 30,260,340 point subsets of $`\mathbb P^1\times\mathbb P^1(\mathbb F_5)`$ span $`x^2y^2\otimes u^2v`$.
- The finite checks are black-box sanity tests; the proofs do not depend on them.

## Provenance and AI disclosure

The work was carried out in the context of the [OpenTorus project](https://github.com/maximilianbehr/OpenTorus), an open-source AI agent for open mathematical problems. An OpenTorus campaign on TR-29 produced the first apolarity-based sketch for the tuple (3,4); the proof in the manuscript was developed from that starting point.


The results, proofs, checks and this record were produced with extensive assistance from AI agents (Anthropic Claude) during a session on 2026-09-13, and were reviewed only by AI agents and by re-deriving the arguments. No external human peer review, formal verification or priority claim is asserted. The literature search for prior results was bounded.
