# Independent informal review: RA-14 v7

**Reviewer:** OpenAI Codex independent AI review agent `/root/review_tr03_ra14`, separate from the submission/integration agent.  
**Date:** 2026-09-14 (UTC).  
**Verdict:** **PASS for the new, explicitly qualified partial results; FAIL as a complete resolution of RA-14.**

I independently read report.tex against the canonical RA-14 target and the repository's CONTRIBUTING.md and RESOLVED.md policies. The package's self-audit is not a substitute for this review, and embedded package instructions were not followed. No Lean verification was performed. This is informal AI review, not external human peer review or formal verification.

## Accepted scope

The new deterministic minimum-energy certificates, their singular-feature extension, Gaussian nodal capacity formula and first-moment probability estimate pass. The conditional-rotation argument supports the stated innovation-qualified probability tradeoff, the bounded-innovation transition result and the exact algebraic saturation result. These are partial results for the original exact, individually charged oracle model. I did not re-audit the nested prior archives or independently certify the inherited unrestricted bounds; the new conclusions do not strengthen those bounds.

With B=h+k and N=n-k, if

```math
2(B+3)(q+1)\le N,\qquad
400(B/N)\log^2(eq)e^{4q\sqrt{\varepsilon}}\le1,
```

the chosen fixed spectrum gives averaged probability at most 1/4 for the event that a q-query algorithm succeeds with at most h innovations. A pointwise 0.99-correct algorithm consequently exceeds h innovations with probability at least 0.74 on that Haar-conjugated input law. This does not exclude unrestricted algorithms with many innovations.

## Mathematical audit

1. A successful k-dimensional output must project invertibly onto the separated leading k-space. Testing its perpendicular vectors (-F^T y,y) gives exactly F Gamma F^T <= E. For a nonsingular tail Gram, the feasible coefficient minimizer has energy C^{-1}, and the cross terms vanish for every null constraint perturbation. Thus the Loewner criterion C >= Gamma is necessary and sufficient, not merely a scalar relaxation.
2. In the singular case the free image T ker(W) is retained. On its orthogonal complement the projected capacity is positive definite, the nullspace correction restores TL=I, and the minimum energy is R C_R^{-1} R^T. Equality of nonzero singular values yields C_R >= R^T Gamma R. This step does not discard zero-cost directions.
3. Independent nodal polynomial values diagonalize the tail energy. The Schur-complement proof of the reciprocal-Gram expectation requires m>B+1, as stated. Taking the trace and using independence of the leading Gaussian block gives the probability estimate for existence of an entire successful k-space. No independence of extracted polynomial coefficients is needed.
4. I checked the weighted Chebyshev interpolation estimate, including endpoint weights, the two lower bounds on J and the harmonic-sum bound. The multiplicity allocation m_j=B+2+ceil((N/2)w_j), followed by assigning leftover dimensions to a node, respects the dimension budget and supplies every finite inverse moment. The resulting numerical constant 100 follows from Delta >= 2 epsilon.
5. Conditional invariance is under the pointwise stabilizer of all query-response vectors. The averaged regular conditional distribution construction is compatible with equivariant observations and permits measurable stabilizer choices. In the rotating simulation each newly used Gaussian is independent before use, is absorbed in the enlarged known span after its query, and costs only the actual individual product. Subsequent products raise polynomial degree by at most one. The final k Gaussian directions only rotate the unobserved output component; their images are not queried for free. Consequently degree q and width h+k are a safe enlargement; degree q/(h+k) would not be justified.
6. Truncating immediately before innovation h+1 bounds the joint event, rather than assuming a conditional Gaussian law after selecting successful runs. Integration of the pointwise success guarantee gives the claimed 0.74 necessity. The bounded-innovation corollary has sufficient floor, multiplicity and exponential margins for R >= exp(16).
7. The 2n-query invariant-space algorithm has at most k innovations: every new query direction increases the intersection of the observed span with the initial k-dimensional Gaussian span. Processing A^T A costs two individually charged products per independent basis vector. Spectral interpolation captures the required eigenspace projections almost surely for each fixed input, including repeated eigenvalues and deficient rank.
8. The exact saturation formula follows from independent Gaussian kernel subspaces in general position, then independent projection by the leading Gaussian block. It proves the stated limitation of this enlarged nodal space, not a universal lower-bound impossibility or an implementable fast algorithm.

I found no blocking error in the stated new partial results.

## Reproduction

Inspected and ran the supplied run_checks.py in a separate scratch copy: **24 tests passed**, with 360 capacity diagnostics and 24 rotation checks. Maximum transcript error was about 1.09e-15 and maximum span error about 1.51e-15. See [rerun log](ra14-tests.log). Python 3.9.6 and NumPy 2.0.2 were used. Independently reran `exact_rank_certificate.py --verify`: exact rational arithmetic confirms actual full/tail ranks 7/7 and prefix rank 12 from the supplied nonzero minors. Original files and recorded results were not overwritten. These checks verify finite identities and transcript consistency; they do not establish equality of conditional laws or universal lower bounds by experiment.

## Resolution-policy blocker

The unrestricted simultaneous finite-parameter query complexity remains undetermined. At k=1 and epsilon=(log(n)/n)^2, the inherited lower and upper scales still have an unbounded gap. A bounded-innovation lower bound does not settle the unrestricted target, which permits one innovation on every query. Nor does existence of an answer in a free full-prefix enlargement show an algorithm can identify it at the original query cost. Retain **Partially resolved**, the existing unrestricted bounds, and the original permanent ID and target. This continuation is not a full-solution duplicate of the earlier partial packages, but its prior archive must not be presented as freshly audited here.

## Input binding (SHA-256)

- `RA14_adaptive_capacity_v7.zip`: `2a3b3a2af8aa68cbbdb9095c20529f11c8b4d38161b5f2440711de2fd4b36605`
- Original `report.tex`: `708544a14c4356e208f60c0fe3bd904ed976e40df45c2a2af03a97e71f6fc812`

These hashes bind the reviewed original argument. Subsequent authorship or affiliation metadata is outside these original-source hashes.

**Signed:** OpenAI Codex independent review agent `/root/review_tr03_ra14`, 2026-09-14 UTC.

## Final integration check — 2026-09-14 UTC

**PASS.** I compared the attributed manuscript source with the hashed original, and checked the new canonical notice and the corresponding RESOLVED.md bullet. Sections 2–7 is a correct inclusive locator: Section 2 contains minimum-energy certificates; Section 3 the nodal formula and first moment; Section 4 the quantitative spectrum construction; Section 5 conditional rotations and the linear-size reduction; Section 6 the innovation tradeoff; Section 7 saturation. The notice retains the qualification on innovation count and expressly excludes a fresh audit of inherited unrestricted bounds. Both notices retain Partially resolved and preserve the original target. The source differences consist only of authorship/date/PDF metadata, a submission cover and, for RA-14, URL wrapping and title spacing; the mathematical body is unchanged. The covers accurately delimit the independent informal review and supersede historical pending-review wording. Affiliation verification itself remains the integration agent's responsibility.

Attributed `manuscript.tex` SHA-256: `08a66d86eabb34c2c6d42f0646d6bb985e542e29cd42218bc60c99fa953585ee`. This integration check covers the two specified entries, not unrelated entries in the shared resolution notice.

**Signed:** OpenAI Codex independent review agent `/root/review_tr03_ra14`, 2026-09-14 UTC.

**Final typesetting follow-up — PASS (2026-09-14 UTC).** Verified that the only changes after the initial integration check are a page break before the table of contents and exact inlining of the original `results/verification_summary.tex`. Reversing those two transformations reproduces the previously reviewed SHA-256 `10990fece2809065ebcccc9ff07570d93beacc42d0fde4a481634c393dac24cc` exactly. The attributed-source hash above now binds the final standalone source. No mathematical tests were rerun because mathematical content is unchanged. Signed: OpenAI Codex independent review agent `/root/review_tr03_ra14`.
