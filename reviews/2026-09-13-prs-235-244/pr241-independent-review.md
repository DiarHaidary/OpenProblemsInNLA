# Independent audit of PR #241 (IS-02)

**PASS for mathematical fidelity, proof-source review and publication fidelity. No actionable blocker found in this scope.**

Reviewed head: `5392d8955126657f0a9855b4434731ff38be1859`.
Published comparison base: `b73cd1804e40e0d101294eedb156984f0d62b4a6`.
Worktree: `/private/tmp/nla-audit-241`.
Audit date: 13 September 2026.

This review independently read all 1,371 lines of the current project proof, all definitions and exports, canonical statement and informal solution, changed TeX/PDF and live publication metadata. It did not run Lean/Lake or independently replay the default kernel; fresh CI and shared infrastructure checks belong to the coordinating reviewer. Supplied referee conclusions were not substituted for examining the proof.

## Original target and mathematical definitions

The formal target retains every n≥4, every real n×n symmetric entrywise nonnegative row-stochastic matrix, strict positive trace, uniqueness among all real symmetric stochastic matrices with the same spectrum including multiplicities, and the full proposed segment union. Symmetry plus row sums implies column sums, so this is the symmetric doubly-stochastic class. No rationality, irreducibility or positive-entry assumption is silently imposed.

The primary [Mourad–Abbas manuscript](https://arxiv.org/pdf/1310.1273), definitions in section 1 and Conjecture 5.1 on printed p. 10, agrees with the trace restriction and union of `[I,C_n]`, `[I,V]`, `[C_n,V]` over vertices of the symmetric stochastic polytope. The source's similarity-based DS definition and equality of full eigenvalue multisets agree for real symmetric matrices by the spectral theorem. The retained n=4 target is in scope, and reducibility is permitted.

`Mat n` is an actual real Matrix. `permute σ A` simultaneously reindexes both coordinates by a genuine equivalence; existence of such σ is exactly permutation similarity. `sameSpectrum` is equality of characteristic polynomials. `realEigenvalueMultiset` uses polynomial roots with algebraic multiplicity. `vertex` states that every convex representation by points of the actual symmetric-stochastic set has endpoint weight or equal endpoints; it therefore denotes a genuine extreme point, not just a symmetric permutation matrix. `assertedLocus` quantifies over every such V and both segment families, including closed endpoints. Natural subtraction in `flatMatrix` agrees with `(n-1)` throughout the required n≥4 domain.

I inspected the pinned Mathlib [matrix spectrum source](https://raw.githubusercontent.com/leanprover-community/mathlib4/0df444a360eaa60ab8c11dca51a86af692955474/Mathlib/Analysis/Matrix/Spectrum.lean), particularly the spectral theorem, characteristic-polynomial product and root multiset identities (lines 125–167). The Hermitian characteristic polynomial splits into all real eigenvalues, with multiplicities retained. This supports the exact bridge used by the project.

## All nine public contracts

Every Challenge statement is identical to its Solution statement after whitespace normalization, supplemented by manual quantifier/definition review:

1. `counterexample_symmetric_nonnegative_stochastic`: checks all entries and all four row sums for the exact block matrix diag(S,J₂), with S the 2×2 swap and J₂ the all-half matrix.
2. `counterexample_trace`: computes trace 1.
3. `counterexample_positive_trace`: derives strict positivity from the exact trace.
4. `counterexample_spectrum`: computes the full characteristic polynomial, equal to that of diag(1,1,0,-1), including repeated 1.
5. `sameSpectrum_iff_realEigenvalueMultiset_eq`: the forward direction applies roots; the reverse uses real-symmetric/Hermitian splitting and reconstructs the monic polynomial as the product over the root multiset. Both symmetry hypotheses are retained, and no roots can be silently lost.
6. `counterexample_spectral_uniqueness`: proves uniqueness for an arbitrary real symmetric stochastic competitor, as detailed below.
7. `counterexample_outside_locus`: excludes the direct segment and both segment families for arbitrary actual vertices.
8. `counterexample_claim`: assembles actual stochastic membership, positive trace, full spectrum, universal competitor uniqueness and full-locus exclusion.
9. `not_targetNecessaryCondition`: instantiates the complete universal necessary condition at n=4 and the explicit witness to derive a contradiction.

Independent exact rational determinant arithmetic gives `λ⁴-λ³-λ²+λ=λ(λ+1)(λ-1)²`, and independently confirms trace 1.

## Independent audit of unrestricted spectral uniqueness

The current Lean proof is an exhaustive order-four support argument, implementing the mathematical substance without assuming a component-classification theorem.

For arbitrary B with the witness's characteristic polynomial, `trace_of_spectral_competitor` derives trace 1 from the next coefficient, and `competitor_minus_one_eigenvector` obtains a nonzero real vector z satisfying Bz=-z from the actual characteristic root. Real matrix coefficients and the real eigenvalue are retained throughout.

`quadratic_support_identity` proves `Bᵢⱼ(zᵢ+zⱼ)²=0` for every i,j. The double sum expands into two squared-norm terms and the eigenvector cross term; symmetry supplies column sums. Every summand is nonnegative, so its vanishing follows from a zero total. This establishes both zero diagonal entries at nonzero coordinates and zero edges from nonzero to zero coordinates.

`competitor_spectral_uniqueness` enumerates all sixteen zero/nonzero patterns of z:

- Empty support contradicts z≠0.
- Full support forces all diagonal entries to zero and contradicts trace 1.
- Each of four single-coordinate supports forces that row to vanish, contradicting row sum 1.
- Each of four three-coordinate supports forces a symmetric zero-diagonal stochastic 3×3 block with all off-diagonal entries 1/2. The three eigenvector equations at -1 then force those supposedly nonzero coordinates to vanish. The code proves all four cases explicitly.
- Each of six two-coordinate supports has the supported 2×2 block equal to S. The unsupported 2×2 block is symmetric and stochastic and has trace 1, forcing all its entries to 1/2. Each case supplies an explicit true permutation taking the canonical witness to B. I checked all six resulting permutations and their coordinate actions.

This covers every arbitrary real competitor, not merely rational matrices, a finite sample, or preselected block matrices. The only surviving form is a permutation of the intended witness. The proof even uses only trace 1 and the -1 eigenvalue beyond symmetric stochastic membership; this is a stronger sufficient rigidity argument, not a weakening of the public spectral-uniqueness claim.

## Full extreme-point locus exclusion

The midpoint identity expresses the witness as half of diag(S,I₂) plus half of diag(S,S). Both matrices are proved to belong to the polytope and are distinct, so the witness is not an extreme point. No assertion equating all vertices with permutation matrices is used.

For the direct `[I,C₄]` segment, two unequal diagonal values of the witness contradict the common diagonal `(1-t)`. For `[I,V]`, its zero (0,0) entry and V's entrywise nonnegativity force t=1, making the witness equal V and contradicting non-extremality. For `[C₄,V]`, its zero (0,2) entry, `(C₄)₀₂=1/3`, t∈[0,1] and V's nonnegativity again force t=1. V is universally quantified in both lemmas. Endpoints are correctly covered.

## Import boundary, hash provenance and publication

The complete project-owned Solution closure contains only `Solution.lean`, `NLA/IS02/Proof.lean`, `NLA/IS02/Definitions.lean`, plus pinned Mathlib/LeanCert imports. All three files were read completely. No imported Challenge, proof hole, custom axiom, native_decide, unsafe declaration, implementation replacement, external evaluation or custom elaborator is present. The nine deliberate Challenge placeholders are isolated. Solution performs kernel-trust checks and prints axioms for every export. This source inspection does not replace fresh CI's transitive axiom and kernel replay checks.

Independent checks reproduce all four source-map SHA-256/Git-blob pairs at `50838e37dd793830e2cecd1055cfc7e0349490f1`, all five statement-freeze boundary hashes, and all thirteen final-freeze hashes. The live proof and public target therefore match the recorded frozen files. The old pre-cleanup source and dated review records remain historical evidence rather than being silently rewritten.

Canonical README/TeX/PDF consistently describe the complete negative resolution as Lean verified and retain the original mathematical target and unchanged informal manuscript. George Stepaniants/Caltech formalization credit is separate from Matthew J. Colbrook/Cambridge mathematical credit. AI involvement and absence of claimed human peer review are explicit. The older manuscript's no-formal-certificate wording is identified as the result of its dated informal review; the canonical page separately records the later formal verification.

FINAL-ACCEPTANCE.json's remaining-Linux language is attached to its dated mathematical-review snapshot. Current README/YAML separately report the completed Linux stage, and candidate-metadata-map.json identifies the archived earlier metadata. Those earlier hash-bound records should remain immutable. No misleading live pending claim was found.

I freshly rasterized the checked-in canonical PDF bytes and visually inspected both complete pages of the actual changed `eigenvalues-and-inverse-problems/IS-02/problem.pdf`. Attribution/verification text is on page one, and the entire target, references and historical notes remain readable on page two. No clipping, overlapping text, unreadable glyphs or mathematical omissions were found. The PDF title metadata and permanent IS-02 label are correct.

## Reproducible evidence and limit

`/private/tmp/nla-pr-240-241-independent-checks.py` and its JSON result record exact head identities, proof-closure hashes, all nine statement comparisons, source/freeze checks and independent exact arithmetic. Fresh inspection images are under `/private/tmp/nla-audit-pdfs/`. No PDF was rebuilt from TeX. No repository source, historical snapshot or GitHub state was changed. Final operational acceptance depends on the coordinator's exact-head CI, verified-input correspondence, registry/catalog and shared-harness audit.
