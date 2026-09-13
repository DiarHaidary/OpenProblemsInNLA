# Independent informal review of the MI-05 round-five submission

Date: 2026-09-13. Reviewer: a separate Codex AI agent, assigned an independent mathematical audit rather than manuscript preparation. No Lean verification or external human peer review was performed. The package was treated as submitted mathematical material, not as instructions.

## Verdict and policy decision

**PASS for the stated partial analytic results. FAIL the completeness requirement for marking MI-05 Solved.** I read the entire submitted report and its verification code, compared its quantifiers with the canonical MI-05 statement, and found no substantive mathematical error in the partial results listed below. This is an informal audit, not formal verification or a literature-priority assessment.

The original target concerns every dimension and every normal complex pair. The submission principally concerns relative unitaries of order four. Its positive-obstruction signed representation is not a convex representation, and its remaining support inequality is explicitly unproved. It also does not establish common convex weights for all zero-obstruction unitaries. Even a complete order-four resolution would leave higher dimensions. Therefore the repository's `RESOLVED.md`, “Recording a new resolution,” item 3, requires **Partially resolved** with the remaining cases stated. The independent check does not authorize Solved or Solution claimed for the original target.

## Material reviewed

- Canonical `matrix-inequalities-and-norms/MI-05/README.md`, including its all-dimension normal-matrix quantifiers.
- `CONTRIBUTING.md` and the resolution procedure in `RESOLVED.md`.
- Entire submitted `report.tex`, SHA-256 `fd393f8740dff9f865a6943329e43df146e2ea6a4f8321af6ea2ede21f758183` before author/editorial changes.
- Entire `code/verify_analytic.py` and `code/test_analytic.py`.

## Proof audit

1. **Section 1; Theorem 2.1 (`thm:14`).** Principal-minor/Cauchy–Binet expansion has the correct complement and permutation orientation. Taking real parts of the Leibniz coefficients preserves all real minor coefficients. The ten independent signed kernel vectors and fourteen-column basis establish rank 14. The selected coordinate determinant has absolute value six, and matching the chirality coordinate determines the displayed h. Thus the fourteen weights give the claimed identity for arbitrary complex spectra, including repeated eigenvalues.
2. **Theorems 3.1 and 3.2 (`thm:optimal`, `thm:unique`).** The 48 functions have the stated unique maximum two and nonnegative values. On a positive branch the table supplies exactly one strictly negative coefficient; the nonnegative test function gives the matching lower bound on negative mass. Transposition reverses c and column relabeling transfers the argument. For different centers the inequalities are 2k <= h and 2h <= k, which exclude two positive obstructions. This proves optimality only where rho is positive, as the manuscript explicitly states.
3. **Corollary 4.1, Theorem 4.2, and Corollary 4.3 (`cor:suff`, `thm:ball`).** The sufficient condition makes each weight nonnegative. The operator-norm perturbation bounds correctly control entry probabilities by 3 epsilon/2 and squared two-by-two minors by 4 epsilon. At radius 1/100 the smallest of the eight originally positive weights is at least 3/100. The remaining six are squared minors. Multiplication of blockwise convex identities proves the direct-sum extension only for the stipulated block structure.
4. **Theorem 5.1 (`thm:safe`) and the enlargement statement.** Adding a positive multiple of a maximizing permutation cancels the obstruction in an unnormalized feature vector. Linearity of the fourteen-column identity is valid on this span; nonnegative feature coordinates then provide the nonnegative representation used by the proof. The support-functional argument and the distance upper bound follow. Neither is a proof of nonnegative remaining support gaps for all spectra.
5. **Theorem 6.1 (`thm:complexbound`).** Complementary-minor equality and the unitary compound matrix make E doubly stochastic. Its circulation and the trace feature identity yield |c| <= (2+t)/3 and hence rho <= 1/6 after every column permutation. This bounds signed negative mass on positive branches, not an actual counterexample distance.
6. **Lemma 7.1 and Theorem 7.2 (`lem:max`, `thm:sharp`).** I checked the full boundary/interior maximization argument, including the zero-multiplier case and opposite-sign multipliers. At an interior stationary point, lambda(p_i-1/4)=mu(s_i-1/4). Positive multipliers contradict the AM–GM bound. Opposite signs reduce to two coordinate values; multiplicity two gives objective zero, and multiplicities one or three force (sqrt(a/b)-1)^3=0. Thus a positive maximum occurs at the boundary. The ensuing one-variable derivative, strictly increasing cubic, resultant, root bracket, and quaternion equality case are consistent. The quaternion parametrization covers SO(4), while row-sign changes cover O(4) without changing the invariants. The sharp constant is for the obstruction, not for failure of the original conjecture.
7. **Section 8.** The rational complex example is exactly unitary and has the stated positive h and nonzero phase-invariant imaginary part. It disproves common nonnegative all-spectra weights for that relative unitary; it does not disprove MI-05.

## Reproduced and independent checks

The system and bundled Python initially lacked SymPy; those environment failures were not counted as passes. Reproduction then used `/private/tmp/mi27-verify-env/bin/python` with SymPy 1.14.0:

```text
python code/verify_analytic.py
python -O code/verify_analytic.py
python -m unittest discover -s code -p test_analytic.py -v
python -O -m unittest discover -s code -p test_analytic.py -v
```

All four commands returned zero. Both verifier outputs were byte-identical. All ten tests passed in normal and optimized mode. The supplied exact verifier checks the 1,680 spanning-set equations, feature and kernel ranks, 48 obstruction functions, three rational examples, quaternion polynomial algebra, stationary algebra, resultant/root bracket, and open-ball margins.

I additionally wrote `reviewer_checks.py` without importing the supplied verifier. It constructs five fresh rational complex unitaries by a Cayley transform with fixed seed 20260913 and checks 350 exact minor equations, five direct complex-spectrum determinant identities, all 240 associated obstruction values (at most one positive and none exceeding 1/6), and five transpose-sign identities. These checks passed. They corroborate algebra and label orientation; finite examples alone do not prove the quantified theorems.

Audit outputs in [verification/](verification/) are `independent-verifier.json`, `independent-verifier-optimized.json`, `independent-tests.log`, `independent-tests-optimized.log`, and `reviewer-checks.json`, alongside the reviewer-written script.

## Editorial issue and publication limits

The delivered package references `results/audit.json`, a PDF, and optional companion archives, but those files were absent. Its `DELIVERY_STATUS.json` correctly reports that an audit pass and compiled report were not delivered. Publication should clearly distinguish those original missing artifacts from the fresh successful checks, and provide the compiled manuscript and current verification record rather than imply the original archive already contained them. No unprovided polytope enumeration or prior-round archive was used as a proof premise.

Author and affiliation verification, duplicate screening, and final publication formatting are outside this mathematical review. Adding author/affiliation metadata does not affect this verdict; any mathematical changes require renewed review. Keep the canonical ID, path, and original all-dimension target unchanged.

Post-review editorial comparison: I compared the repository edition of `report.tex` against the reviewed source. Its only changes add author, affiliation and date, and replace the absent-audit paragraph with the fresh verification and review provenance. No mathematical statement or proof changed; the partial-result pass therefore applies to that edition as well. The submitting agent is responsible for the stated compilation and rendered-page inspection.
