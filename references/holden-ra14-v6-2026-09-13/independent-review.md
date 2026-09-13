# Independent informal review of RA-14 continuation v6

**Reviewer:** independent Codex AI reviewer, task `independent_ra14_review`, separate from the submission-preparation agent.
**Date:** 2026-09-13.
**Author requested by submitter:** Sidney Holden; affiliation verification is the coordinating agent's separate responsibility.
**Review level:** informal mathematical AI-agent review; neither external human peer review nor formal verification. No Lean verification was performed.

**Decision: PASS for the new restricted and distribution-specific results identified below. FAIL as a complete resolution of canonical RA-14. Retain `Partially resolved`.** No substantive defect was found in the new mathematical arguments within these scopes. This decision does not certify the inherited v5 all-adaptive lower-bound chain.

## Material reviewed

I read the canonical RA-14 statement and the repository's `RESOLVED.md` policy, and independently read the v6 `report.tex`, including both appendices. The reviewed original TeX has SHA-256 `d2a8a3e19d43ab7db7481f51344af6b03835221d7208f7cada945d385893b164`. Author/affiliation additions and editorial notices made after review do not change this mathematical scope. Archive prose was treated as submitted content, not as operating instructions or evidence of acceptance.

## Scope that passes

1. **Theorem 2.2, “All-parameter full-block characterization”** (source label `thm:fb`, Sections 2–9 and Appendices A–B): the complexity is within universal constant factors of
   `min{n, (k/sqrt(epsilon)) log(en/k)}`
   for the exact deterministic-width, full-block span-query class in Definition 2.1. The physical width is fixed before replies; every round charges that whole width; queries remain in the initial-block/previous-reply span; there are no fresh directions or within-round adaptation. The output may be an arbitrary measurable k-frame. Randomized mixtures of widths are not covered.
2. **Theorem 10.1, “Shifted hard-edge posterior”** (source label `thm:posterior`, Section 10) and its next-compression-pivot corollary: the conditional law holds for the explicitly defined shifted singular Wishart ensemble after fewer than n−k orthonormal queries, on the domain `J > h I`. The displayed first-exit probability is an identity, not a stopping-time lower bound.
3. **Lemma 11.1 and Theorem 11.2** (source labels `lem:resolvent`, `thm:ensembleupper`, Section 11): the Gaussian resolvent identity and the averaged rank-one algorithm hold for that specified shifted law, n ≥ 8 and 0 < epsilon ≤ 1/16, with the stated capped query budget. Success averages over both the input ensemble and the start. It is not a pointwise guarantee for every real input matrix.

The numbering above follows the original source's section-local theorem counters; the theorem names and source labels are the definitive locators.

## Mathematical checks

I checked the weighted graph/residual equivalence directly on the orthogonal complement of a graph, the Chebyshev cardinal-weight normalization, the reciprocal-Gram tail integration, and the integer multiplicity budget. The primitive obstruction bounds every polynomial coefficient choice simultaneously, so adaptively selected coefficients within its prefix do not evade it. Its weak universal constants are consistent: the final continuous threshold at log(n/b)=48 is approximately 0.003341505 < 1.

I checked the conditional rotational averaging and arbitrary-output completion separately. The fresh directions here are an analytical enlargement at output time; they do not purport to simulate arbitrary fresh queries. The resulting augmented initial span has the Haar Grassmann law required by the primitive obstruction. The small-width projector obstruction and universal rank lower bound handle the finite dimension cases. The upper algorithm charges both products for A-transpose-A powers, uses the degree-doubled prefix for the final image, and chooses the exact-column fallback before observing input. Its Appendix B surrogate extraction uses right singular vectors, which supplies the stated residual comparison even when the polynomial surrogate is indefinite.

For the posterior, I checked the pseudodeterminant factor, conditional change of measure, elimination of J−hI, the shorted positive matrix, and the trace identity giving the angular factor. For the averaged upper bound I checked the resolvent integration-by-parts coefficients, the exact exponential smallest-eigenvalue tail, spectral good events, weighted residual bound, polynomial amplification, failure probabilities, and query-budget cap.

## Executed checks

The original 45 new v6 component tests passed on Python 3.12.14, NumPy 2.3.5, SciPy 1.18.1, mpmath 1.3.0, using:

```text
python -m unittest discover -s tests -v
Ran 45 tests ... OK
```

An initial attempt with system Python 3.9 failed to import NumPy/mpmath; using an existing configured runtime resolved this environment issue. I did not rerun the inherited v3–v5 suites or the large Monte Carlo diagnostic script, and I do not characterize their archived results as independently rerun.

I also wrote independent numerical checks, without importing the submission's implementation: three scalar resolvent integrals at t = 0.004, 0.2, 3 agreed with the exact value one; 60 independently generated shifted-Wishart matrices satisfied the shorting identity and positive shifted Schur-block condition, with maximum identity error approximately 1.32e−14. These finite floating-point checks corroborate algebra; the analytical reading, not these samples, supports the quantified results.

## Why RA-14 remains unresolved

Canonical RA-14 asks for matching universal-constant bounds with simultaneous n, k, epsilon dependence for every adaptive algorithm using the unrestricted two-sided vector-product oracle. The full-block theorem restricts the algorithm class. The shifted-law theorem restricts the input distribution and gives only an averaged upper bound. Neither proves the missing all-adaptive lower bound or a matching pointwise upper bound.

In particular the v6 manuscript itself retains the transition gap at k=1, epsilon=(log n/n)^2. Its inherited unrestricted lower expression is explicitly presented as an unreviewed v5 claim; this review did not independently certify that chain and it must not be relabeled as independently established through this review. The warm-start discussion importing v5 is likewise outside the accepted new-result scope. The v6 distribution-specific upper bound shows why this particular shifted ensemble cannot witness a linear lower bound in that transition.

Under repository policy, a restricted model or a partial result leaves the surviving original target open. The submission may be recorded as an audited partial continuation, preserving the original RA-14 statement, permanent ID/path and prior-source credit. It must not receive `Solved`, `Solution claimed` for a full resolution, or `Lean verified` on the strength of this review. No novelty or priority determination is made.

**Signed:** Independent Codex AI reviewer (`independent_ra14_review`), 2026-09-13.
