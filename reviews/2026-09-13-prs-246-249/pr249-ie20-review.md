# Independent IE-20 audit for PR #249

Reviewed head: `9e11821e2e999afb1699272005a167da7ee42861`.
Base: `752218e5417998b7f4d2aee9c447ca5d256fe530`.
Reviewer: independent AI subagent `/root/review_246_ie16`, 13 September 2026.
Read-only source checkout: `/private/tmp/nla-audit-249`.

**Verdict: accept the documented partial scope. No blocking mathematical, code, source-fidelity, or PDF finding identified.** This is an informal mathematical and executable-evidence review, not proof-assistant verification or external human peer review. The global matching-bound problem remains open as explicitly disclosed.

## Scope and exact target preservation

I read all 1,268 lines of `references/holden-ie-extensions-2026-09-13/manuscripts/IE-20/report.tex`, the canonical IE-20 README, all substantive exact-execution, bound, polynomial, witness and test modules, and Section 5 of the recovered manuscript inside `prior/IE20_recovered.zip`. I also read the primary reciprocal-polynomial dependency directly. Submitted acceptance statements were not mathematical premises.

A direct Git comparison with the PR base confirms that the canonical mathematical specification, from “This fixes an implementation and arithmetic model” through the References heading, is byte-identical. `problem_ids.json` is also byte-identical and retains all 217 entries. The model still requires p-bit exactly stored SPD inputs, unbounded exponents, every permitted scalar relative-error schedule, separately rounded products and additions, left-to-right full-index accumulations from zero, the specified short recurrence, the n-step cap, true backward error, and success at every precision at or above the threshold. The manuscript explicitly treats intermediate error equations as an envelope rather than a correctly rounded binary map. No rounding of the input or distributional error assumption is introduced.

## Mathematical findings

The scalar threshold is correct: the first iterate contains five multiplicative factors in the numerator and four in the denominator; the lower multiplicative endpoint has the larger logarithmic deviation. Its exact degree-five rational error expression, equality cases and monotonicity give the full all-greater-precisions threshold.

The identity and conditioning lower bounds use representable inputs and actual admissible failed executions. The joint dimension/conditioning construction uses a representable 2-by-2 active block on the first and last coordinates. Its n selectable prefix factors can reach the stated cancellation targets, with all selected errors within the envelope. The condition bound and integer precision calculation are valid also for odd dimensions and noninteger K. The first-step exact maximum follows from the displayed moment/square identity; it is properly distinguished from a representable finite-p extremizer. The finite-precision perturbation constants are conservative enough.

The long upper argument is sound within the stated model:

1. **Normalization and local envelopes.** Scaling an execution preserves every relative-error equation and the true backward error; normalized representability is not presumed. The prefix matvec argument groups an already completed execution and does not reorder its arithmetic. Its operator-norm estimate avoids an unjustified replacement by entrywise absolute values. Actual K controls denominator perturbations and ensures positive scalar divisors once a nonzero direction is available.
2. **Failure-conditioned bootstrap.** At index j, residual-gap and already established defect bounds prove `r_j^T v_j > 0`, hence the direction is nonzero and the next step is legal. Only after producing `x_{j+1}` does failure of that iterate exclude an excessively long step. This makes the cap `H=min(K,64/epsilon^2)` legitimate without presuming existence of later coefficients. The lower alpha bound, beta bound, iterate/residual growth, residual gap, residual orthogonality and direction conjugacy follow in a consistent induction order. The adjacent cancellation uses the actual rounded scalar relations. Powers of `D=1024H^2` provide ample slack for the displayed local-error and defect estimates.
3. **Stopping.** The residual-gap estimate ensures that a zero recursive residual under the failure assumption is impossible; it is not automatically treated as a certificate of success. Positive rho and d exclude both zero-divisor mechanisms. At the endpoint, only residuals through `r_m` and directions through `v_{m-1}` are needed; no unwanted `v_m` or post-horizon step is assumed.
4. **Polynomial transfer.** The three-term relation for `Av_i` has the correct signs, including the local errors. Monomial induction controls coefficients and representation error, then conversion through the rounded x-updates gives a vector in the actual computed-iterate span. This does not assert exact Krylov membership or exact Galerkin optimality of computed iterates.
5. **Dimension horizon.** Under failure, the n+1 normalized residuals have a positive definite Gram matrix by the established tiny off-diagonal row sums. This contradicts their ambient dimension and proves success by n, with no extra direction required.
6. **Chebyshev horizon.** The approximation polynomial has the stated degree and coefficient bound. The proof controls the cross term against the actual rounded iterate using the approximate span representation and the true-residual gap. The exact energy identity, followed by `A^2 <= A`, yields the stated residual bound at the selected integer horizon.
7. **Universal backward horizon.** The cited reciprocal polynomial has degree below k, is positive, and satisfies the exact uniform reciprocal approximation. Under failure, the nearly orthogonal residuals and residual-gap bound impose a lower backward-error bound on every nonzero vector in the computed-iterate span. The approximate polynomial vector in that same span has a contradictory upper bound. The k-dependent square-root factors and perturbation constants fit the selected `ceil((64/epsilon)^(2/3))` horizon.
8. **Quantifiers.** Taking the minimum of the three horizons covers ties and always stays at most n. The precision inequality is sufficient at every larger p; the upper proof applies to all real normalized inputs and therefore to all admissible stored inputs at each precision. It does not rely on monotonicity of a fixed representable input set.

The bounded-conditioning, coarse-tolerance, fixed-tolerance additive, fixed-n leading-conditioning, and two-dimensional/fine-tolerance corollaries follow with the stated domains. The retained path/outlier proof establishes its fixed-n, sufficiently-large-outlier quantifier: its positive limiting divisors and high-component power-counting induction are consistent; all produced iterates, rather than just the last, are checked. No dimension-uniform onset is asserted. The gap at `K=n^2`, `epsilon=n^-2` remains `Omega(log n)` versus `O(n log n)` in this package, so **Partially resolved** is the appropriate classification.

## Primary theorem dependency

I directly checked [Dereziński, Nakatsukasa and Rebrova, arXiv:2604.16075v2](https://arxiv.org/html/2604.16075v2), Lemmas 12–13 and equations (8)–(10). Their even-degree shifted Chebyshev construction is exactly the report's `G(t)` and `(t-G(t))/t^2`; the degree and `3/(k^2-1)` bound match. The report imports only this exact polynomial approximation, not MINBERR's algorithm or an external finite-precision CG guarantee. Its transfer to rounded CG is proved separately. Other cited contemporary work is contextual and not a premise for these new upper/lower arguments; this was not an exhaustive literature or priority audit.

## Code and executable verification

The executor checks binary significands, exact symmetry and LDL positivity. It retains zero products/additions, separates products from additions, records admissible operation errors, stops on a zero recursive residual or before a zero divisor, produces at most n updates, and separately evaluates the true residual against the stored A and b. The bound evaluator returns the exact scalar threshold only in the scalar case; its general bound is explicitly conservative. Its rational comparison of backward errors correctly keeps signs before squaring, including equality and zero-cross-term cases. Finite polynomial grids and recorded witnesses are accurately disclosed as finite evidence.

Replayed entirely in `/private/tmp/nla-ie20-replay-249` with `/private/tmp/nla-batch-python/bin/python`:

- `python -m unittest discover -s code -v`: **26 tests passed**.
- `python code/verify_extended.py`: **1,536 scalar corners; 256 first-step executions; 31 polynomial constructions; 3,999 rational grid checks; 90 bound-consistency triples; 14 joint-breakdown witnesses; 24 dense matvec checks passed**.
- `python code/verify_legacy.py --output results/legacy_checks.json`: **15 retained witnesses passed**, with positive exact failure certificates for every produced iterate.

Both regenerated JSON reports equal their supplied structured records exactly. Logs are `/private/tmp/nla-ie20-extended-replay.log` and `/private/tmp/nla-ie20-legacy-replay.log`.

I additionally wrote `/private/tmp/nla-ie20-extra-checks-249.py`: 96 joint witnesses across dimensions 2–17, including odd dimensions and noninteger condition bounds, passed independent active-block eigenvalue, representability, admissible-fault and zero-matvec checks. Another 216 backward-error comparisons matched directly computed rational-norm cases. Results: `/private/tmp/nla-ie20-extra-checks-249.json`. These additional cases improve execution coverage; the universal claims rest on the written proof and cited analytic theorem.

## PDF inspection and provenance

Using the PDF skill read-only, I rasterized and visually inspected all 18 pages of the public report and both pages of the canonical problem PDF. All equations, references, page numbers, proof sections and status/scope notices are readable, with no clipping, overlap or broken mathematical glyphs observed.

I also rasterized the 18-page submitted original. Pages 2–18 are pixel-identical to the public report at the review resolution. The differing submitted title page was inspected directly and is clean: it retains “Prepared by ChatGPT,” while the public title credits Sidney Holden and expressly discloses substantial AI assistance. Text comparison shows only this attribution/associated title-page spacing difference. This is consistent with preserving the original submission while producing an attributed public manuscript.

PDFs reviewed: `references/holden-ie-extensions-2026-09-13/manuscripts/IE-20/report.pdf`, `references/holden-ie-extensions-2026-09-13/submitted/IE20_extended/IE20_extended_results.pdf`, and `linear-systems-and-elimination/IE-20/problem.pdf`. The archived earlier hard-family manuscript's relevant TeX proof was read; its historical PDF was not separately re-rendered in this pass.

No source, proof, result artifact in the PR checkout, shared checkout, or GitHub state was modified. No PDF was rebuilt. Integration/publication and repository-wide checks remain the coordinator's responsibility.
