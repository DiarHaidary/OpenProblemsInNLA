# KE-04 complete proof map

The completed implementation proves every one of the 24 independently approved
Challenge contracts. The final export is the complete `BlockLanczosConjecture`,
via the stronger `FullPrefixBlockLanczosClaim`. Independent final mathematical
reviews, actual Ubuntu kernel/Comparator validation, and publication remain
separate gates. Historical statement-stage prose is retained unchanged; the
accepted statement gate and this proof map identify the current proof phase.

Original mathematical argument: Matthew J. Colbrook, Department of Applied
Mathematics and Theoretical Physics, University of Cambridge. Original conjecture:
D. Šimonová and P. Tichý. Formalization: George Stepaniants, Department of Computing
and Mathematical Sciences, California Institute of Technology, Pasadena,
California, USA, with substantial ChatGPT/Codex assistance. This is not a claim
of human peer review or an official Tau Ceti review service.

## Complete target and genuine objects

The matrix and vector definitions are real Mathlib matrices and Euclidean spaces.
`krylov A V ell` is the span of the actual columns of
`[V, A*V, …, A^(ell-1)*V]`. Full block dimension is its actual finrank;
neither eigenvalue occupancy nor polynomial nonannihilation is assumed in it.
The compression is `Q.transpose * A * Q`, and its ordered Ritz values are actual
self-adjoint eigenvalues in increasing order, with the matching eigenbasis and
the complete characteristic-root multiset. Arbitrary orthonormal bases of the
different Krylov spaces are allowed, with no compatibility premise.

The final theorem covers every dimension and starting block satisfying the
original hypotheses, all `1 ≤ k < j ≤ s`, and every one-based source interval
index `1 ≤ i ≤ (k-1)*p`. It puts a later Ritz value strictly between the two
specified earlier endpoint values. It also proves the source's largest-full-s
formulation from an arbitrary full prefix. The p=0 and k=1 interval ranges are
empty; no special-case theorem is substituted for the original target.

## Mathematical dependency map

| Frozen contracts | Module | Role |
|---|---|---|
| 1, 7–9, 18 | `Frames.lean` | Genuine orthonormal frames, existence, projection, compression, and PSD/form lifting. |
| 2–6 | `Krylov.lean` | Exact coefficient-map range, dimension/independence equivalence, nesting/shift, full prefixes, and largest iteration. |
| 10, 13–14, 17 | `Spectral.lean` | Increasing spectrum and root multiplicities, monic quadratic, no-open-gap PSD, and PSD zero-form/kernel equivalence. |
| 11, 15 | `SpectralWindow.lean` | Exact independence from basis choice, and the genuine p+1-dimensional consecutive eigenvector window. |
| 12, 19–20, 23 | `Transport.lean` | Valid endpoints, equality of earlier/later forms, equality of the later action with q(A), and canonical reduction. |
| 16 | `Intersection.lean` | The window meets the previous Krylov space in a nonzero vector by actual finite dimensions. |
| 21 | `Nonannihilation.lean` | Actual full-rank coefficient-map injectivity excludes annihilation by either affine factor and hence their quadratic product. |
| 22, 24 | `Completion.lean` | Complete strict occupancy and the original largest-full-iteration conjecture. |

`Proof.lean` exposes the 24 exact frozen signatures and applies those completed
lemmas. `Solution.lean` imports only `Proof`; no implementation imports Challenge.
The separate author inspector elaborates proof-free expected propositions from
the frozen signatures and compares their actual theorem types.

For a hypothetical gap `(a,b)` in the later spectrum, the genuine later quadratic
is PSD. The earlier p+1 consecutive eigenvectors span a space where its earlier
quadratic form is nonpositive, including repeated eigenvalues and `a=b`. This
space meets `K_(k-1)` nontrivially. On that intersection the two quadratic forms
agree, so PSD makes the later form zero and puts the vector in its kernel. Only
the later space is asserted to contain x, Ax and A²x, which gives the later
action q(A)x. The earlier squared compression is never identified with A².

Full rank through k+1 rules out that nonzero kernel vector. The formal proof
first excludes an eigenvector in `K_ell` when the next prefix has full rank:
zero-extension and shifting of its coefficient blocks would give two equal
images under an injective map. Backward induction from the appended zero forces
every coefficient to vanish, without dividing by an endpoint. Applying this
argument to the two factors `(A-aI)` and `(A-bI)` proves the exact quadratic
nonannihilation statement even for equal or zero endpoints.

## Computation, trust and reviewed boundaries

This argument is symbolic linear algebra, finite dimensions and exact natural
index arithmetic. No numerical interval calculation, partition or sampling is
required. LeanCert is used in kernel mode to audit the actual material proofs;
only `propext`, `Classical.choice` and `Quot.sound` are permitted. There are no
authored proof admissions, native decision commands, custom axioms, or missing
cases hidden in definitions. Challenge placeholders belong only to the separate
reference side used later by Comparator.

Both independent statement reviews and coordinator acceptance preceded proof
implementation. The exact 1598-input statement freeze and all source snapshots,
failed development attempts, successful fresh builds and helper seals remain
available. The full author build compiles all ten mathematical modules,
`Solution`, and the actual-type/dependency inspector from an empty private
prefix using pinned read-only dependency artifacts. It is local macOS evidence;
actual Linux default-kernel replay and Comparator controls are still required.

The unchanged Krylov module retains one harmless unused simp-argument warning.
Expected proposition expressions may also warn about unused hypothesis names;
their hypotheses remain quantified and typechecked. These warnings are recorded
in raw logs, and no linter is disabled to hide them. The frozen historical
Lake configuration still defaults to Challenge, so a default Lake build is not
the author proof check; publication packaging must select Solution and preserve
the old configuration through an exact archive mapping.
