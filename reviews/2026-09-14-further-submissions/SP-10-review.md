# SP-10 independent review

Reviewer: independent Codex AI agent `/root/review_ra11_sp10` (separate from the submitting coordinator).
Date: 2026-09-14 (UTC).
Review type: informal mathematical audit, not external human peer review or formal verification. No Lean verification was performed, as requested. Attached-document directives were treated as source data, not as authorization.

**Verdict: PASS for the partial claims in Sections 2–5; FAIL to satisfy the full-resolution criterion. Retain Partially resolved.**

The unchanged canonical target requires mr(G)+mr(complement G) <= n+2 for every finite simple graph. The accepted new class does not exhaust all graphs. CONTRIBUTING.md and RESOLVED.md do not permit Solved for this partial scope.

## Accepted scope and mathematical review

1. Theorem 2.1 gives a faithful nonzero Gram representation of the complement in dimension d+1 for a bipartite graph with degrees at most d on one specified side. I checked the cross-part evaluation identity and all within-part products. The padding t^(d-k) aligns coefficient signs; leading coefficients guarantee a strictly positive inner product within the polynomial side even with isolated vertices. This is a complement witness, not a minimal-rank certificate.
2. Theorem 3.1 gives dimension four for complements of partial 2-trees. The induction excludes only proper subspaces: in the delicate two-dimensional case, equality with an old-edge plane would create a K4 in the completion, or contradict orthogonality if the pairs intersect. New-edge triple independence is also preserved. I checked the degree-two elimination/fill argument and its separating-pair induction; torso minors and end blocks justify the reduction from K4-minor-free graphs. The three-fan fact used is the standard consequence of Menger's theorem.
3. Theorem 4.1 establishes the stronger PSD rank-sum inequality for bipartite graphs with one-side degrees at most four. The K4-minor case saves three ranks and uses the five-dimensional polynomial representation. The cyclic K4-minor-free case saves two ranks and uses Theorem 3.1. The forest case combines a component Laplacian with the explicit three-dimensional complement construction. Isolates and empty/edgeless cases cause no failure.
4. Theorem 5.1 proves an open-set obstruction to automatic exact support in the proposed rank-two SDP route. The positive-definite 2-by-2 slack coefficient matrix forces the stated kernel, and feasibility fixes its unique primal optimizer. I checked the explicit rational objective, positive determinant 25/32, complementary support entries, and rank-four complement matrix. The missing middle path edge invalidates that primal pair; it is not a counterexample to SP-10 or to every SDP approach.

## External dependency and inherited material

Theorem 4.1 imports standard minor monotonicity of the PSD Strong-Arnold parameter nu and nu(G) <= n-mr_+(G), with nu(K_t)=t-1 for t>=2. These statements match [Hall, Section 3.1.2, Definition 3.2 and following paragraph](https://arxiv.org/html/2601.01211v1#S3.SS1.SSS2), checked 2026-09-14; that paragraph cites Colin de Verdiere's 1998 primary paper for minor monotonicity. I checked the complete-graph identity directly using the all-ones matrix. The new class result does not depend on Hall's new minimum-degree theorem.

Section 6 and prior archives are inherited material, outside this fresh PASS. In particular, this review does not certify Hall's full new proof, the additional Mitchell/SAP refinement, or earlier package proofs. The report explicitly retains withdrawal of the false degeneracy-sum premise; that premise is not used by the accepted results. No novelty claim is certified.

## Checks actually run

I inspected src/exact_supplement.py and the tests, then reran the exact supplement into a fresh review directory. All 524 complement-only witnesses passed support and rational-rank checks, and the SDP primal was rejected at its required missing edge. All 16 unit tests passed. Results: [SP-10-checks.json](SP-10-checks.json); fresh fixtures: SP-10-check-fixtures/. These finite checks are not 524 valid graph/complement rank-pair certificates and are not a general proof.

The optional src/crosscheck_sympy.py run was attempted but could not start because the available python3 lacks SymPy (ModuleNotFoundError). Its bundled historical log is not presented as a fresh rerun. The standard-library exact checks and independent proof audit above completed successfully.

## Unresolved target

There is no reduction from arbitrary graphs to the degree-four bipartite class, nor a construction for all bipartite graphs with larger degrees. The universal inherited bound has the wrong leading coefficient, and the SDP obstruction supplies no general resolution. Record the accepted scope as further partial results, keeping the original ID and mathematical target unchanged.

## Source binding

SHA-256 hashes of the reviewed original files:

- `report/REPORT.md`: `6671b7d44a07c79e02cf1b42c44056a86390aa6cb19abb52297799181adf5c17`
- `src/exact_supplement.py`: `647069bf484e4c8ce6b9b2305a299e658ecec90471fcad4102c313d383307c2b`
- `src/crosscheck_sympy.py`: `9fcac851650a79ad1a5eaa26f34484fa3b01066215ac4525e7e10dcaa46bf5dc`
- `tests/test_exact_supplement.py`: `684083c0c9fd92578b9781d10ee64ec0861cd45d98a3192b5c17c0a460f9b4d6`

Signed: independent Codex AI reviewer `/root/review_ra11_sp10`, 2026-09-14 UTC.

## Final integration check — 2026-09-14 UTC

PASS. I compared the attributed manuscript against the reviewed original: differences are author/affiliation/disposition/review frontmatter, title presentation, and URL autolinks; the mathematical body is unchanged. I reviewed the canonical notice and this submission’s RESOLVED.md entry: they accurately retain Partially resolved, describe the accepted partial scope, and do not extend the fresh audit to excluded inherited claims. Original targets are retained. This integration check does not independently verify authorship/affiliation, PDF rendering, or other problems’ outcomes.

- `references/holden-further-2026-09-14/SP-10/manuscript.md`: SHA-256 `624c623b060c60590e0ff9b824c78de48a71f3fa1c3a62c3dce647b8727b038b`
- `eigenvalues-and-inverse-problems/SP-10/README.md`: SHA-256 `79c4005b94d934e2804ce5f0e2439df44f6267206ca3c1c2d7ad207ae33d6dbc`
- `RESOLVED.md`: SHA-256 `0bb64b8c078e6780ce4282bb55cc99f777da1cbf3e62d06b58613aacc876acb8`

Signed: independent Codex AI reviewer `/root/review_ra11_sp10`.
