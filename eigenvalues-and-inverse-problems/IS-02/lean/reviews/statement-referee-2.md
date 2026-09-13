# IS-02 independent statement review 2

Verdict: **approve** the mathematical statement boundary for proof implementation.

Reviewer: `/root/is02_statement_referee2`, an independent OpenAI Codex AI agent.
Phase: pre-proof statement fidelity and elaboration review.
Date: 13 September 2026.
I did not author or edit the candidate statements, definitions, proof, or canonical
problem pages. This is an independent AI review, not human peer review, an
official Tau Ceti review, or a Lean proof certificate.

This approval is specific to the source bytes identified below. It does not
approve nonexistent theorem implementations. The two packaging corrections
listed below do not change the mathematical contracts and do not block their
implementation.

## Sources and review order

I first read the actual canonical problem and the entire retained mathematical
proof, rather than treating an earlier PASS or the author's description as
evidence. I read the canonical Markdown and TeX problem, the complete solution
Markdown and TeX, and `docs/lean/REVIEW.md` from immutable upstream commit
`50838e37dd793830e2cecd1055cfc7e0349490f1`, through `git show` in
`/tmp/nla-lean-ke04-worktree`. I then read all definitions, all nine Challenge
signatures, the numerical targets, and the source map. Finally I checked the
package metadata, toolchain configuration and typecheck evidence. The review
applies the correctness, complete scope, definition transparency, reuse and
attribution requirements in the repository's adaptation of Tau Ceti standards.

SHA-256 digests of the original source bytes:

| Source at the pinned commit | SHA-256 |
|---|---|
| `eigenvalues-and-inverse-problems/IS-02/README.md` | `92f7c04c5ac0be67a7f6a4efd0d2439caaf000295fa27d259e01a22368f7ae24` |
| `eigenvalues-and-inverse-problems/IS-02/problem.tex` | `3298c8d66c330f792d0e34edac88631f67d9e3e3292ab2b677cdd73ad8d74537` |
| `eigenvalues-and-inverse-problems/IS-02/solution.md` | `ae29570308b2a78678875c5e56076ce09e65cea732ce6b51142399a4b234577f` |
| `eigenvalues-and-inverse-problems/IS-02/solution.tex` | `151d4cbf469629da34454d0b68e274403d292bf5566fe9a59e4c545716328f03` |
| `docs/lean/REVIEW.md` | `d967ddce620d4e754e2f9c25548f30cb537f76f4ddcf8ecf2574945bcd332553` |
| `AGENTS.md` | `d7e27520acdcb0edacebf965b56f5b1e3fb0205d83da45a7fa021e0bedb80162` |

Every source hash and Git blob in the candidate `SOURCE_MAP.md` matches the
actual Git object bytes. `EVIDENCE.json` records the corresponding blob IDs and
sizes independently.

The approved mathematical boundary is rooted at
`/tmp/nla-lean-is02-project/eigenvalues-and-inverse-problems/IS-02/lean`:

| File | SHA-256 |
|---|---|
| `NLA/IS02/Definitions.lean` | `4d2d2914838a91a30f12b1e20490c957d2b4e943eb2a51f7415cc2fedd0bf321` |
| `Challenge.lean` | `d72b58465096cb7049d453206727837eb53b87845a5d8faa97d88f5fb9244cff` |
| `NUMERICAL_TARGETS.md` | `85680cac4c689f1b0f373a60f2c4f0e3e96263fad8fb3326185afa13927e25d3` |
| `SOURCE_MAP.md` | `584f77bc097fab678a7bf969d4b060b856bb919d3bde7a843330f11d31534947` |
| `comparator.json` | `0c0af16af051b15d0b3892318738d82199f4116e5708a025653587b451bec7ed` |

All thirteen candidate files, including metadata and build configuration, have
before/after hashes in `EVIDENCE.json`. They remained unchanged during this audit.

## Complete target correspondence

1. **Ambient matrices and stochastic constraints.** `Mat n` elaborates to
   `Matrix (Fin n) (Fin n) ℝ`. Symmetry is entrywise transpose symmetry;
   nonnegativity quantifies over every entry; stochasticity requires every real
   row sum to equal one. These are exactly the canonical constraints. Symmetry
   also gives column sums one without adding an assumption. No competing matrix
   is restricted to rational entries, the displayed block structure, a finite
   list, or a special support graph. The trace is the actual sum of diagonal
   entries.

2. **Permutation similarity.** `permute σ A i j = A (σ i) (σ j)` is simultaneous
   relabeling. In ordinary matrix notation it is `Rᵀ A R` when column `j` of `R`
   is the basis vector indexed by `σ j`. Every permutation is represented by
   `Equiv.Perm (Fin n)`, so choosing the inverse convention for a permutation
   matrix makes no difference to this existential condition.

3. **Spectrum, including multiplicities.** `sameSpectrum` is equality of
   Mathlib's actual `Matrix.charpoly`, defined as `det(XI-A)`, not equality of an
   arbitrary user-defined invariant. `realEigenvalueMultiset` is the actual
   polynomial root multiset. The pinned `Polynomial.roots` definition retains
   root multiplicities, as also stated by its `count_roots` theorem. For real
   symmetric matrices the characteristic polynomial splits over the reals and
   is monic. Thus its real root multiset determines the characteristic
   polynomial and contains the entire spectrum. The separate general contract
   `sameSpectrum_iff_realEigenvalueMultiset_eq` has precisely the two symmetry
   hypotheses needed for this converse. It does not assume spectral uniqueness,
   the desired root equality, or a classification result. I checked the pinned
   Mathlib matrix spectral API: `IsHermitian.charpoly_eq`,
   `roots_charpoly_eq_eigenvalues` and `splits_charpoly` in
   `Mathlib/Analysis/Matrix/Spectrum.lean` supply the relevant established
   semantics. They are possible proof dependencies, not a proof already present
   in the candidate. The `n = 0` case of the bridge remains consistent: both
   characteristic polynomials are one and both multisets are empty.

4. **Uniqueness against arbitrary competitors.** The expanded
   `spectrallyUnique A` type is
   `∀ B ∈ symmetricStochastic n, sameSpectrum A B → permutationSimilar A B`.
   For the displayed counterexample, `n` is inferred as four. The resulting
   uniqueness theorem quantifies over all real symmetric stochastic `4 × 4`
   matrices with the same characteristic polynomial. There is no premise that
   assumes uniqueness, disconnection, bipartiteness or a block classification.

5. **The actual vertices and all locus components.** The `vertex n V` predicate
   requires membership in the same symmetric-stochastic set and rules out a
   nontrivial convex decomposition within that set. For `0 < t < 1`, its
   conclusion forces `U = W`, hence `V = U = W`; conversely an extreme point has
   this property, with the two endpoint disjuncts covering `t = 0,1`. This is
   the ordinary extreme-point definition, consistent with Mathlib's
   `Set.mem_extremePoints`. It is not a proxy for permutation matrices. The
   locus includes `[I,C_n]` and, for every such vertex, both `[I,V]` and
   `[C_n,V]`. Each segment has real `t` and both closed endpoints. `flatMatrix`
   has diagonal zero and off-diagonal `1/(n-1)`. The natural subtraction used
   in its definition agrees with the canonical real denominator at every
   relevant dimension `n ≥ 4`.

6. **Exact witness and numerical obligations.** The literal matrix is exactly
   the retained source matrix, including the four real halves. The diagonal
   comparison matrix is exactly `diag(1,1,0,-1)`, retaining both copies of one.
   The separate contracts require stochastic membership, trace exactly one,
   strictly positive trace, the characteristic polynomial, full uniqueness,
   exclusion from the entire locus, and their combined claim. Hand calculation
   of the two blocks gives characteristic polynomial
   `X (X-1)^2 (X+1)` and trace one; this is a consistency check of the statements,
   not a claim that those identities have been proved in Lean.

7. **Full negative resolution.** `targetNecessaryCondition` retains the
   universal quantifier over all natural dimensions at least four, all real
   matrices in the stipulated class, strict positive trace and spectral
   uniqueness. `not_targetNecessaryCondition` has no hypotheses. A verified
   witness at four is therefore sufficient to refute the actual universal
   necessary condition. No smaller or substituted target is being counted.

## Source proof and computation scope

The retained proof's route is consistent with the boundary: for a real
symmetric stochastic competitor the multiplicity of one equals the number of
positive-support connected components. A component carrying minus one is
bipartite with equal sign-class sizes, since symmetric crossing weights and
row sums one force those cardinalities to agree. With four vertices and two
components, this yields two blocks of size two. Their remaining eigenvalues
determine the blocks `B(0)` and `B(1/2)`. The formal uniqueness contract does not
smuggle in any part of this reasoning as an assumption.

The nonvertex witness is the genuine midpoint of `diag(S,I₂)` and
`diag(S,S)`. The zero diagonal entry excludes all identity-to-vertex segments;
the zero off-diagonal entry at indices `(0,2)` excludes all `C₄`-to-vertex
segments; that same entry excludes the direct identity-to-`C₄` segment. The
endpoint contradictions are included. Thus both sections of the retained
proof map to the stated obligations.

All displayed arithmetic data are exact rational values. No numerical interval
subdivision is needed for these finite identities. The difficult theorem is
the classification of arbitrary real competitors; a finite numerical search
could not replace it. LeanCert is pinned as a dependency, but its eventual use,
the implemented proof and the kernel audit remain later gates.

## Independently observed elaboration and trust evidence

I ran `python3 /tmp/nla-is02-statement-referee2/audit.py`, which invokes the
pinned Lean binary directly. It does not run Lake, download anything, copy a
dependency cache or build dependency objects. All new outputs are confined to
this review directory. Existing dependency objects were read from the MI-22
project's `.lake/packages` directory.

- Lean reported version `4.33.1`, compiler commit
  `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`, `arm64-apple-darwin24.6.0`.
- All ten dependency checkout HEADs match the candidate manifest exactly;
  `git status --porcelain=1 --untracked-files=no` is empty for each dependency.
- The definitions and Challenge each elaborated with exit code zero. Challenge
  produced exactly nine expected `declaration uses sorry` warnings.
- I independently printed every definition, checked all nine theorem types,
  and printed their transitive axiom lists. That inspection exited zero.
  All eighteen definitions report only `propext`, `Classical.choice` and
  `Quot.sound`; each of the nine Challenge placeholders additionally reports
  `sorryAx`. `Types.log` records the actual elaborated terms and outputs.
- The regenerated `Definitions.olean` SHA-256 is
  `e61f15f8f77eb5175775fe8743feb3f6fef5f312d89827574e95f62a9149f2ca`.
  The regenerated `Challenge.olean` SHA-256 is
  `58b2891dbbfb0be1755b920feec7a77afd52e8339faf79eadf08706dc0c52600`.
  Both are byte-for-byte identical to the supplied original typecheck prefix
  `/var/folders/pw/wkdn0vxs0b54swhpwjg6s0x00000gn/T/nla-is02-statement-typecheck.l7ar1Y/out`.

The complete command results, hashes, source provenance and dependency checks
are in `EVIDENCE.json`; `Challenge.log` and `Types.log` are direct captured
output. This local elaboration does not attest a from-source dependency rebuild,
Linux verification, a Comparator run or any completed mathematical theorem.

## Nonblocking packaging corrections and remaining gates

1. `lake-manifest.json` still has top-level `name: NLAKE04`, while the actual
   `lakefile.toml` package name is `NLAIS02`. Correct the stale root name before
   publishing or performing the final reproducible project build; the pinned
   dependency revisions themselves all match the existing checkouts.
2. `verification/statement-typecheck.md` says “all eight bodies” near its start.
   There are nine, consistently with Challenge, Comparator and the later warning
   count. Correct this wording. The introductory README also promises source
   recheck commands “in SOURCE_MAP.md” that are not actually present there;
   either add such commands or remove that sentence fragment.

The statement-stage `axioms: []` metadata is not an observed clean axiom audit:
the actual placeholder dependency is `sorryAx` as shown above. The metadata
does explicitly disclose all nine `sorry` bodies, so it does not claim a
completed proof; final proof metadata must instead agree with the final
transitive audit.

Before promotion, implement and independently review all nine contracts against
these frozen definitions; ensure Solution never imports Challenge; preserve the
original Matthew J. Colbrook attribution and George Stepaniants's stated
department and university without his email; run the required Linux/LeanCert
kernel trust checks and Comparator; and record their actual evidence. Any
mathematical changes to the approved boundary require renewed statement review.
No canonical status, proof implementation, Git state or candidate file was
changed by this reviewer.
