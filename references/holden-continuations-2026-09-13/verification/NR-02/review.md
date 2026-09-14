# Independent informal audit: NR-02 round four

Reviewer: independent Codex AI agent `/root/review_nr_mi`, separate from the submission integrator. Date: 2026-09-13 (America/New_York).

Verdict: PASS for the standalone theorem that any two convex polygons of extension complexity six have product extension complexity twelve, the explicit octagon and square, and the stated obstruction to the particular higher-complexity support assignment. Retain NR-02 **Partially resolved**. This is an informal AI-agent audit, not formal verification or external human peer review. No Lean was run. No historical novelty claim was checked.

The canonical target asks for additivity for all complete polytope slack matrices. The reviewed theorem covers a proper subclass and neither proves the general equality nor supplies a counterexample.

## Mathematical audit

I independently checked the written reduction, rather than accepting a successful SAT run as evidence for the geometry. The positive facet-normal dependence bounds the standard nonnegative-factorization extension. The six-facet extension has dimension 2–5; the Euler and simplex counts, and the one-dimensional affine-dependence/Gale count pq+t<=9 in dimension four, correctly restrict polygon sizes to 6–9. Projection cannot increase the vertex count.

For an eleven-term saving factorization, padding by splitting nonzero terms preserves all constraints. Edge slices are complete prism slacks after positive row scaling, so the prism lower bound eight yields the row and strengthened omission caps. Pure columns and incident-row unions omit genuinely distinct terms on vertex slices. The strengthened edge condition correctly counts the union of the three omission mechanisms, not their sum. Positive-entry witnesses and cross-facet exclusions are necessary conditions; they are not asserted sufficient for realizable weights. Sorting full support columns does not discard a factorization. I read the gate, cardinality, witness, and prefix-comparator implementation in support_cnf.py and found it consistent with these conditions.

I checked the stated RUP soundness argument and the Python positive-hint checker: each step derives a contradiction from a negated proposed clause using previously available unit or empty clauses, and acceptance requires an empty clause. The C++ checkers are additional implementations, not a substitute for this argument.

The octagon's six-facet extension is bounded, its factors are nonnegative, and the vertex-count obstruction excludes a five-facet extension. The barrier argument correctly forces two nonalternating antipodal normal pairs, impossible in strict cyclic facet order. This excludes only the displayed support assignment.

Primary-source check: Grande–Padrol–Sanyal, Lemma 2.3 and Corollary 2.4, directly support the disjoint-facet and prism inequalities used here: https://arxiv.org/html/1601.02416v2 . The pyramid result is https://arxiv.org/abs/1702.01959 .

## Reproduction

Ran the unmodified supplied verifier with `/tmp/nr01-verify-env/bin/python -B code/verify_all.py --require-cpp`, from its supplied extracted location, writing output outside that location. The verifier makes temporary directories for compiled checkers and archived predecessor extraction. No original files were changed. Python 3.12.14, SymPy 1.14.0, NumPy 2.3.5. See verify_all.json.

All 17 top-level checks passed: manifest integrity; checker controls; all ten regenerated CNFs and Python LRAT, C++ LRAT, and hint-free RUP checks; exact octagon/square; encoding semantics; barrier checks; and predecessor computational regressions. The ten refutations cover 831,540 original clauses and 96,286 added clauses. The optional occurrence-list deep-RUP run was not requested.

The earlier packs' code was rerun through the aggregate verifier, but this audit did not reread every earlier mathematical proof. Accordingly it does not independently certify the broader inherited claim about all polytopes with both complexities at most six. Recommended canonical summary: “An independent informal AI-agent audit passed the computer-assisted result xc(P×Q)=12 whenever P and Q are polygons with xc(P)=xc(Q)=6, together with an exact octagon example. The unrestricted additivity question remains partially resolved.”
