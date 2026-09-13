# Independent review: IE-27 research update

Reviewer: separate Codex AI agent (`review_ie27`), 2026-09-13. This is an informal independent mathematical and executable-certificate audit, not external human peer review or formal verification. No Lean was used. The reviewer did not write the submitted proofs and made no repository edits.

**Decision: PASS for the precise partial scope below; NOT a complete solution. Keep IE-27 Partially resolved.**

## Target and policy

I compared both submitted manuscript sources with the canonical IE-27 README. The original target concerns every admissible Radau stage q, every real positive shift, and radius ||U-I||_2 under the stated norm assumption. Section “Recording a new resolution,” item 3 of RESOLVED.md requires Partially resolved for restricted results and explicit remaining cases. Neither the finite stage set nor the new endpoint shift regimes covers that full target. The broader counterexamples do not refute the canonical conjecture.

## Analytic audit

The differentiation formula is derived from the cardinal basis t ell_j(t)/c_j on polynomials vanishing at zero. Its diagonal simplification follows from the displayed Jacobi equation. Diagonal similarity transforms the inverse into a matrix with skew off-diagonal entries and strictly positive diagonal symmetric part. Every leading principal determinant is positive, giving positive Crout pivots and real-positive-shift invertibility.

The spatial SPD congruence and permutation correctly reduce the original pencil to I+(I+mu L^-1)^-1 N. Thus all-positive-shift stage results transfer to every admissible spatial discretization.

The new rank-two identity is entrywise correct: off-diagonal entries of XC+C^T X equal one, with the claimed diagonal correction. The small-shift proof correctly uses N^q=0 and a strict geometric-sum bound for any eigenvalue outside radius ||N||. It includes the endpoint mu=1/(q||B||). The large-shift Neumann bound holds at and above 2||L||. The square-root condition is correctly sufficient, with the essential PP^T/NN^T orientation and congruence by L; it is not shown to hold for all stages.

The common-energy criterion correctly bounds the inverse factor in the H norm and N by sqrt(t), yielding a spectral-radius bound for every positive shift. The rational Rayleigh gap proves sqrt(t)<||N||, while positive definiteness of I-N^T N proves ||N||<1.

The exact two-stage formula and its maximum at sqrt(6) are consistent. The explicit three-stage metric and signs are also checked by the executable exact calculation. The generic 2x2 obstruction is not Radau. The genuine q=3 complex-shift obstruction violates the real-shift hypothesis; the quadratic Schur necessary condition used to establish its spectral violation is valid. Neither obstruction changes the original status to solved.

## Verification implementation audit

I read the interval verifier, including rational conversion, signed division, polynomial sign isolation, factor reconstruction, LDL pivots, and Rayleigh bounds. All proof decisions use integer interval endpoints. Ordered disjoint q-1 root intervals account for all roots of the degree q-1 polynomial. The exact matrices passed to LDL are symmetric by construction, despite potentially differing interval enclosures in transposed locations. Optimizer output and numerical spectra are not trusted as proof.

I independently wrote `ie27-reviewer-check.py`: 6,773 enclosure checks against Fraction endpoint arithmetic passed, covering positive and negative values and divisors. Separately generated Legendre polynomials using their recurrence agree with the Jacobi coefficient formula for q=2,...,128, and their coefficients satisfy the stated Jacobi ODE. These finite implementation checks support, but do not replace, the analytic derivation.

The submitted `code/run_all.py` was rerun from a fresh output directory. Execution results are recorded in `ie27-independent-recheck/`, with console output in `ie27-independent-console.jsonl`.

## Accepted scope and remaining gap

The accepted finite set is q=2,...,64,80,96,128: 66 specified stages, each covering every real mu>0. It is not all stages through 128. For every stage, the analytic proof covers 0<mu<=1/(q||B_q||_2) and mu>=2||L_q||_2. For q outside that finite set, the intermediate regime remains unproved. There is no all-stage existence or success theorem for the common-energy certificates or square-root condition.

No mathematical correction was needed in the reviewed partial claims. Authorship/affiliation and submission provenance are the coordinating contributor's responsibility; source drafts identify OpenAI ChatGPT and that assistance should remain disclosed when adding Sidney Holden as requested.

## Completed execution outcome

**PASS:** the fresh complete run exited 0. All 66 selected certificates passed, including q=96 and q=128, and all 20 regression tests passed. The exact three-stage and both obstruction calculations also passed. `ie27-independent-recheck/summary.json` explicitly records `complete_solution_of_IE27: false`. Reviewed source hashes are retained in `ie27-reviewed-source-sha256.json`. No extrapolation from these finite tests is part of this acceptance.
