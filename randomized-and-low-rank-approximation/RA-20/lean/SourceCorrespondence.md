# RA-20 source and semantic correspondence

The immutable source baseline is `5830ed4fb06da0659414a3deb2a40ad327aca052` in
`ajt60gaibb/OpenProblemsInNLA`. This package was drafted outside a Git worktree;
it changes no canonical page or published status. The source inventory records
both SHA-256 and exact Git blob identities, with original text retained under
`verification/original-sources/`.

The complete canonical RA-20 page, complete published Markdown and TeX
resolution, and the complete independent reconstruction in
`references/research-expansion-2026-09-11/ra20-resolution/` were read. The source
ascribes the negative-resolution mathematics to the Codex automated maintainer
audit. Formalization authorship is George Stepaniants; it does not replace that
mathematical provenance. The conjecture belongs to Kubjas, Sodomaco and Tsigaridas.

The primary [author paper](https://arxiv.org/pdf/2010.15636v2), Section 2.2 and
Conjecture 5.6/Table 7 (printed p.21), was opened directly. Its geometric
conventions and displayed formulas agree with the retained canonical target.
The formalization does not reinterpret singular rank-two points as smooth.

| Canonical/source concept | Draft implementation |
| --- | --- |
| All complex symmetric rank-at-most-two matrices with `s` prescribed diagonal zeros | `variety n s`, using actual `Matrix.IsSymm`, `Matrix.rank`, and all prescribed entries |
| Reduced affine variety | `definingIdeal` is `MvPolynomial.vanishingIdeal` of that actual point set; `CoordinateRing` is its quotient |
| Algebraic smooth locus over the complex field | `SmoothPoint` pulls back the actual point prime and requires membership in `Algebra.smoothLocus C CoordinateRing` |
| Tangent vectors | `TangentVector` annihilates derivatives of **every** polynomial in the reduced vanishing ideal |
| Complex bilinear full-Frobenius distance | `fullFrobeniusDistance`, the sum over all entries without conjugation |
| Differential vanishes along the tangent space | `SmoothCriticalPoint`, using actual complex `fderiv` |
| Finite number of critical points | `HasCriticalCount`, a `Cardinal.mk` equality rather than `Nat.card` without a finiteness guard |
| Generic symmetric complex data | `HasGenericCriticalCount`, an arbitrary polynomial with a nonvanishing symmetric point, and all symmetric data where it is nonzero |
| One joint four-formula conjecture, all allowed dimensions | `criticalCountConjecture`, with no changed endpoint or separate fixed-case replacement |
| Source `det X=2abc` and reduced union of planes | Contracts 1–2 |
| Source true smooth locus and tangent planes | Contracts 3–4; the equivalences remain to prove |
| Metric coefficient two / derivative coefficient four | Contracts 5–6 and 8 |
| Exhaustion, distinctness, and generic count three | Contracts 7 and 9–11 |
| Counterexample refutes the complete original conjecture | Contract 12 |

The use of one nonempty principal open set is the usual equivalent formulation
of a generic assertion: if an assertion holds off a proper algebraic exceptional
set, choose one defining polynomial nonzero at a point outside that set; its
principal open set is nonempty and lies in the complement. Conversely, the
zero locus of a polynomial not identically zero on symmetric data is a proper
algebraic exceptional set. The generic-intersection contract explicitly closes
the possible gap between two different exceptional sets. No `e(n,s)` is
defined through a default-valued choice of a count.

The imported `fderiv` uses the standard finite-dimensional product topology on
matrices; the metric being differentiated is separately and explicitly fixed
by the bilinear distance polynomial. No matrix operator norm or Hermitian
inner product is substituted for it. The Hessian obligation states actual
second derivatives and their zero-kernel property, rather than presupposing
algebraic multiplicity one. The canonical target itself counts distinct smooth
critical points for generic data, and that is the cardinality used here.

Pinned library APIs inspected directly include `Mathlib/RingTheory/Nullstellensatz.lean`
(`vanishingIdeal`, `pointToPoint`), `Mathlib/RingTheory/Smooth/Locus.lean`
(`Algebra.IsSmoothAt` means formal smoothness of the localized coordinate ring),
`Mathlib/LinearAlgebra/Matrix/Rank.lean`, `Mathlib/Algebra/MvPolynomial/PDeriv.lean`,
and `Mathlib/Analysis/Calculus/FDeriv/Basic.lean`. Their source identities are in
the dependency inventory. Mathlib's standard-smooth/localization APIs are
available, but their application to this quotient has not been proved here.

Relevant Tau Ceti review scope: exact target/quantifier/field/metric fidelity,
correctness and nonvacuity of all definitions, complete smooth-locus bridges,
generic-open intersection, exact type matching, pure kernel trust, reusable
general algebra/calculus lemmas, clear API/documentation, and original attribution.
This package makes no automated or human referee-approval claim. All future proof
authors must be excluded from the two independent final mathematical reviews.
