# Independent corroborating review: PR #244 / TR-29

**Mathematical verdict: PASS for the stated two-factor result and general binary-form extension. No overlooked hypothesis or substantive gap found.** Reviewed head `65356703cfa1c750c1c881e7d3fbc8ed586028a0`, full `references/behr-tr29-2026-09-13/manuscript/TR29_two_factor_rank.tex`, and `tensor-computations/TR-29/README.md`. This is an informal AI-agent cross-review independent of the submission reviews and root's initial proof reading. No code was run, source edited, or PDF rebuilt; root handles reproducibility and integration.

## Core proof and rank fidelity

The original fixed-block complex partially symmetric rank is exactly the Segre–Veronese rank used in the proof. Each point represents one pure symmetric tensor in each original block. No regrouping, ordinary tensor-rank substitution, or border-rank substitution occurs. Over C, nonzero scalar weights can be absorbed into a block vector by taking a degree-th root. A minimal decomposition may be taken with distinct projective points and nonzero weights: proportional repeated terms combine, and cancellations/zero terms can be deleted.

For `T=x^p y u^q v`, `p,q>=1`, the low-degree annihilator calculation is correct, including p=1 or q=1. On a reduced point set, if `lambda^2 g` vanishes, then `lambda g` vanishes. Minimality in the second degree therefore contradicts the required square factor in every low-degree annihilator. This establishes maximal Hilbert functions at `(1,q)` and `(p,1)`. The apolar bilinear form has Gram matrix `A! B! V1^T W V2`; its rank equals the catalecticant rank by the perfect complementary apolar pairing. Sylvester's inequality, with W invertible, yields the claimed lower bound `2(p+q)`. Positivity of weights or a Hermitian Gram interpretation is not needed.

The explicit root-of-unity upper sum has exactly the surviving `(i,k)=(p,q)` coefficient. At the exceptional N=p+q=2 endpoint, p=q=1 and the t=4 contribution cancels between epsilon=+1 and -1. The 2N points remain distinct. Thus both the original d_i>=3 range and the stated extension to d_i=2 are covered.

## General binary theorem: critical edge checks

- For a degree-A nonzero binary form, the apolar complete intersection has degrees r<=s, r+s=A+2, and border rank r. If r<s, the minimal generator is unique up to scale; its repeated-root property is therefore well-defined. Its squarefreeness determines whether rank is r or s. When r=s, rank and border rank are both r=s, independent of which generator is named phi. This agrees with [Comas–Seiguer's original binary-rank paper](https://arxiv.org/pdf/math/0112311).
- If `r'=s'`, all degrees k<=s'-1 are below either generator, so `Ann(G)_k=0`. Lemma 5.1 immediately excludes a nonzero vanishing form in that range. The proof's deduction `k>=r'` contradicts `k<=s'-1`; the subsequent repeated-factor step is only reached when r'<s'. It does not accidentally assume a repeated generator in the balanced case.
- Under H_G, r'>=2: degree B>=1 excludes the balanced r'=s'=1 case, and a degree-one generator cannot have a repeated factor. Consequently s'-1=B+1-r'<=B-1, so the apolar differentiation range in Lemma 5.1 is valid. Likewise r-1<=A. There is no derivative-degree overrun hidden in “note `(r-1,k)<=(A,B)`.”
- In the general peeling argument, below s' the annihilator is generated only by phi'. If a vanishing form is divisible by phi'=lambda^2 mu, deleting one lambda preserves vanishing on the reduced set and decreases k. Other factors of phi' and their roots do not affect this implication.
- At the complementary pair `(r-1,s'-1)` and `(s-1,r'-1)`, the Hilbert dimensions are rs' and sr'. The binary apolar Hilbert function at s'-1 equals r', both when r'<s' and when r'=s'. Thus the catalecticant rank rr' and the bound `rs'+sr'-rr'` are correct.
- Pure powers have r=1, s=A+1 and a squarefree linear minimal generator; they do **not** satisfy H_F. Theorem 5.2 therefore does not wrongly assign them high rank. They are valid arbitrary factors in the one-sided Proposition 5.3, whose complementary first degree is zero when appropriate. Its multiplicativity consequence handles pure powers, degree-one forms, and all rank-equals-border-rank factors through either the one-sided estimate or the ordinary catalecticant lower bound. Zero forms and degree-zero constants are explicitly excluded.
- Positive-exponent monomials have r=b+1, s=a+1. Balanced exponents invoke r=s; unbalanced exponents have the repeated factor required by H. Substitution into the lower bound gives exactly the formula in Corollary 5.4. [Gałązka v3, Theorem 1.5(i)](https://arxiv.org/html/1601.06211v3) supplies its matching upper bound for precisely `a>=b>=1,c>=d>=1`, including balanced cases.

The no-H counterexample in Remark 5.5 is consistent: the cubic's degree-two apolar generator is squarefree, both factor ranks are two, and a rank-four product is obtained and certified by flattening.

## PDF and publication observations

All five manuscript PDF pages were visually inspected after read-only Poppler rendering at 1250 pixels. Equations, theorem/corollary labels, proof continuations, bibliography, attribution, and disclosure are legible; no clipping, overlap, or missing mathematical glyphs found. The PDF's Theorem 5.2 and Corollary 5.4 match the TeX and canonical notice.

The one-page canonical PDF was also inspected. It is the stale 10 September version and lacks the new two-factor notice, as root already identified. **It must be regenerated during integration**; this is a publication synchronization issue, not a mathematical defect. The canonical README retains the original statement and accurately keeps k>=3 unresolved.

This cross-review does not certify historical novelty, universal three-factor results, finite-field-to-complex inference, or formal verification. The accepted complex proofs do not depend on finite-field searches. No further mathematical correction is required based on this review.
