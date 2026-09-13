# KE-04 contract 21: complete nonannihilation helper

The exact frozen theorem `NLA.KE04._proved.fullRank_quadratic_nonannihilation`
is proved in `NLA/KE04/Nonannihilation.lean`. It retains arbitrary natural
dimensions, real `A`, real starting block `V`, `k ≥ 2`, full block dimension at
`k+1`, every nonzero `x ∈ K_(k−1)`, and arbitrary real endpoints `a,b`. There is
no symmetry, nonzero-root, distinct-endpoint, additional rank, polynomial-kernel
or trajectory assumption.

The proof first establishes a reusable stronger affine fact. If `K_(ell+1)` has
full rank and `x ∈ K_ell` satisfies `A x = a x`, represent `x` by its actual
finite block coefficient map. Appending a zero block represents the same vector;
shifting the blocks represents its actual image under `A`. Full rank gives
injectivity, hence equality of these coefficient arrays. Backward induction from
the appended zero proves that every coefficient is zero. This works also when
`a=0`, without any scalar division.

For the quadratic, put `y=(A−bI)x`. The true Krylov shift and nesting put `y` in
`K_k`. If `(A−aI)y=0`, the affine lemma at `k` gives `y=0`; the same lemma at
`k−1`, using proved prefix full rank, gives `x=0`, contradicting the original
nonzero hypothesis. The matrix factors act through the genuine Euclidean matrix
action. This is equivalent to the source's highest-block-coefficient argument
and avoids all numerical computation, even for `a=b`.

Imports are the stable `Krylov` and `Frames` helpers plus finite-sum APIs. The
public helper names under `NLA.KE04._proved` are `blockExtend`, `blockShift`,
`krylovCombination_extend`, `krylovCombination_shift`,
`blockShift_eq_smul_extend`, `fullRank_krylov_eigenvector_zero`,
`act_sub_smul_one`, and the exact target. There is no Spectral import or cycle.

The final fresh source attempt `attempt-96bth7us` compiled Definitions, Krylov,
Frames, Nonannihilation and its exact-type inspector: five successful source
commands. The inspector imports no Challenge, uses a proof-free expected type,
matches contract 21 exactly, traverses 32 actual safe/nonpartial project
declarations by their types and bodies, and retains all 17 required material
dependencies. Its actual axiom traversal permits only `propext`,
`Classical.choice` and `Quot.sound`. Across that run, 31 actual axiom reports and
31 explicit LeanCert kernel assertions pass; eight pairs are in the new module
itself. The new module emits no warnings. The unchanged imported Krylov file has
its already documented unused-simp-argument warning, and the inspector has four
unused names for hypothesis binders in its proof-free expected proposition.

Two failed attempts remain intact. The first exposed an overly broad simp
normalization of `Fin.castSucc`/`Fin.succ` during backward induction; the second
needed explicit simplification of the zero function after using the induction
hypothesis. Their elaboration failures caused the dependent kernel assertions
to reject Lean's error-recovery `sorryAx`; neither failed attempt is counted as a
proof. The final correction uses a documented explicit `simp only`, with no
statement alteration or trusted shortcut. Every attempt retains source copies,
commands, complete output, pin checks and hashed object records. Only each
completed attempt's private disposable objects were removed.

The 1598 statement-freeze inputs and all explicitly recorded imported boundaries
are unchanged. Both imported helper manifests were independently checked at their
exact historical scopes, 85 and 75 files. The full proof gate preceded all work.
The ten pinned dependency sources and nine compiled directories remained shared
read-only, with no downloads, copies or dependency rebuilds.

This is a scoped author validation by `/root/mf16_final_referee`, already a KE-04
proof contributor, not an independent mathematical approval. It was performed
on the pinned local macOS Lean 4.33.1 installation. It does not claim a complete
KE-04 proof, Linux Comparator/default-kernel replay, publication readiness, or a
status change. Original mathematical credit remains Matthew J. Colbrook;
formalization credit remains George Stepaniants, Department of Computing and
Mathematical Sciences, California Institute of Technology, Pasadena, California,
USA, without an email address. Every IE-05 byte remains untouched.
