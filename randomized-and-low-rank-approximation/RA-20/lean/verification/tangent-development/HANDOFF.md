# RA-20 entire-ideal tangent helper completion

Exact frozen contract **4** is complete in `NLA/RA20/Tangent.lean`, SHA-256
`b03b6a1112737372072832d89b17ff0e19e00f631a925252269b75af3c44e178`.
Its export is `NLA.RA20.algebraic_tangent_space_proved`. The actual elaborated
type agrees with the frozen Challenge, including the point condition `abc=0`,
all matrix directions, and all singular points.

The helper introduces the same finite sum of evaluated formal partial
derivatives used by frozen `TangentVector`. It proves its constant, variable,
sum, difference and product rules directly from Mathlib partial derivatives.
Polynomial induction proves the substitution rule through `hollowPullback`.
This is a theorem about every polynomial, not a premise about a determinant
gradient or a redefinition of the tangent space.

For necessity, the diagonal coordinates, symmetry differences and the product
of the three independent off-diagonal coordinates are proved to belong to the
actual reduced vanishing ideal. Testing the frozen universal condition on them
gives zero diagonal, symmetry and the displayed gradient equation. For
sufficiency, these linear conditions first identify the direction with its
hollow coordinates, without any rank condition on that direction. The sealed
Algebra ideal-pullback theorem makes the substitution of every vanishing
polynomial an actual multiple of `abc`. The proved substitution and product
rules show its differential vanishes from `abc=0` and the gradient equation.
At component intersections the equation degenerates naturally; no nonzero
coordinate or smoothness hypothesis is added.

The final helper compiled in about 6.6 seconds with no warnings. Three successful
direct-source commands checked the final helper, a namespace-only diagnostic
reference, and the actual type/body dependency inspector. The inspector checked
44 safe project declarations and 21 required mathematical dependencies,
including the entire-ideal definition, polynomial substitution, partial
derivatives, principal-ideal divisibility and the genuine Nullstellensatz
step inherited from Algebra. Two source and four diagnostic LeanCert kernel
assertions and all six printed standard-three axiom lists passed. The admitted
reference is not a dependency of the actual proof. No native compiler axiom,
additional axiom or numerical interval certificate occurs.

Both failed initial elaborations are retained with exact source snapshots and
raw diagnostics. Corrections supplied the formal differential of zero, finite
coordinate reductions, and explicit ideal/coercion simplification. The
mathematical statement and all prior sealed files stayed unchanged.

The additional ownership record was read before the first Tangent edit. The
same author's active private prefix retained the already source-checked,
immutable Definitions and Algebra objects. All ten exact MI-22 dependencies
were read-only and were rechecked clean at their pinned revisions. No Lake,
dependency downloads, cache copies or shared writes occurred. All 68 frozen
project inputs, 16 original source snapshots/Git identities and every byte of
the complete 148-file Algebra seal remain exact. `validation.json` records
these checks. The new outer seal includes the previous manifest and its entire
closure; only this outer manifest's exact path is excluded from its inventory.

Author diagnostics and implementation: `/root/formal_review_standards`; this
is not an independent final mathematical review. Formalization author: George
Stepaniants, Department of Computing and Mathematical Sciences, California
Institute of Technology, Pasadena, California, USA. The original mathematics
is the repository's Codex automated maintainer audit, addressing the conjecture
of Kubjas, Sodomaco and Tsigaridas.

Full integration, two independent final reviews, actual Linux replay,
Comparator verification and publication remain pending. This helper evidence
records local macOS work only.
