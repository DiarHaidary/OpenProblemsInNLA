# Independent audit: PR #244 / TR-29

**PASS for the stated complex two-factor theorem and binary-form extension, with canonical PDF synchronization required before publication.** This is an informal AI-agent mathematical audit, not human peer review, historical-priority certification or Lean verification.

Reviewed exact head `65356703cfa1c750c1c881e7d3fbc8ed586028a0` against published base `b73cd1804e40e0d101294eedb156984f0d62b4a6`. Read the complete manuscript, canonical target/notice, exact differentiation helpers and K1/K4/K5 verification source. An additional independent agent read the complete proof and its boundary cases; see `pr244-cross-review.md`.

## Claim and proof

The rank is the original complex partially symmetric rank with two fixed blocks. It does not regroup factors or replace rank by border rank. For T=x^p y u^q v, p,q>=1, the low-degree apolar annihilator consists of multiples of the appropriate square. On reduced decomposition points, removing one copy of a repeated linear factor preserves vanishing, contradicting minimal degree. Hence the two complementary Hilbert functions are 2(q+1) and 2(p+1). The actual bilinear apolar Gram form is A!B! V1^T W V2 with W invertible after deleting zero/repeated terms. Its rank is the catalecticant rank 4. Sylvester's rank inequality gives 2(p+q).

The matching root-of-unity decomposition has 2(p+q) distinct points and only one nonzero coefficient. The exceptional p=q=1 top-degree term cancels between the two signs. The argument is over characteristic zero, and finite-field examples are not used to infer it.

For general binary factors, the apolar complete-intersection degrees r<=s sum to A+2. The hypothesis is exactly the balanced case or a repeated minimal generator. In the balanced case, the relevant lower degrees have zero annihilator, so the peeling proof does not require a repeated generator there. In the unbalanced case it does. The complementary Hilbert dimensions rs' and sr' and catalecticant rank rr' give rs'+sr'-rr'. The one-sided bound also handles pure powers, which fail the repeated-generator hypothesis and are not incorrectly assigned the high rank. Degree-one forms, endpoints and strictly positive exponents were checked. The positive-exponent monomial corollary matches the cited upper bound exactly.

The explanation for three or more factors merely identifies why this peeling argument fails: squarefree low-degree annihilators can appear. It does not infer an impossibility theorem for other approaches. The retained k>=3 target, including the previous W3 cubed discussion and upper bound, stays open.

## Primary sources

- [Galazka, Multigraded apolarity, v3](https://arxiv.org/html/1601.06211v3), Theorem 1.5(i), supplies the matching upper bound for precisely a>=b>=1 and c>=d>=1. Its divided-power convention does not change the monomial rank assertion after scalar rescaling.
- [Comas–Seiguer's original binary-rank paper](https://arxiv.org/pdf/math/0112311) supports the rank/border-rank dichotomy used with apolar generator degrees; the independent cross-review checked this correspondence.
- [Wang–Seigal v2](https://arxiv.org/html/2202.11740v2) confirms the acknowledged Sylvester-rank-inequality antecedent. The manuscript gives the needed apolar Gram calculation directly.
- [Canino et al. v1](https://arxiv.org/html/2512.05828v1) was opened for the W-state source context. The new two-factor proof does not depend on treating an upper bound as an exact rank.

No claim of an exhaustive priority search is made.

## Fresh reproducibility

Scratch copy `/private/tmp/nla-root-replay-244`, Python 3.12.14, exact rational/integer arithmetic and SymPy 1.14. No source files were edited.

- K1 passed for all 49 p,q pairs from 1 through 7, with the exact low-degree annihilator and rank statements, and 504 random exact Gram/Sylvester comparisons.
- K5 passed for all 225 allowed monomial exponent quadruples through 5, including both annihilator strips and complementary catalecticants.
- K4 reproduced ten finite-field root-of-unity decompositions, distinct support, exact target coefficients and equality in the lower-bound ingredients. These are examples only.
- The supplied corrected E3/E5 script reproduced the necessity of nonzero weights using zero-weight control points and five non-monomial/balanced examples. Its diagnostic bound/products are not by themselves certificates of rank; its comparisons were inspected.
- Newly authored `tr29-independent.py` imports no submitted code. Exact coefficient filtering checked the root-of-unity identity in 275,625 coefficients over 900 parameter pairs p,q=1,...,30, including p=q=1. Three independently GL2-transformed repeated-factor, balanced and pure-power cases passed exact complementary derivative-rank tests.

The expensive exhaustive finite-field decomposition searches were not rerun, and no claim that their 30-million-subset records were freshly reproduced is made. Neither those searches nor the finite checks are premises of the accepted characteristic-zero proof.

The second reviewer rasterized and inspected all five manuscript PDF pages: no clipping, overlap, broken symbols or incomplete theorem text. The canonical PDF is stale and was not changed in the source PR despite updated README/TeX. Integration must regenerate it and visually inspect every page; this is the only required publication fix. Permanent ID, canonical path, original mathematical target, attribution and old references remain intact. Status must remain **Partially resolved**.
