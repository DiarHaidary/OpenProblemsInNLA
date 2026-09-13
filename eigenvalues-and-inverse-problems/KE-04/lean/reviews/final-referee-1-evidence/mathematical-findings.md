# KE-04 source-first independent mathematical findings

Reviewer: AI agent `/root/ra09_final_referee1`, independent final referee 1.
This is preparation before the final proof freeze and fresh source checks, not
a final approval. I did not author, design, steer or fix any KE-04 mathematics.

The full Colbrook argument is represented by real Euclidean vectors, actual
matrix powers and actual finite-dimensional spans. Full block dimension is
only a rank equality. The target has no hidden spectral, nonannihilation,
compatible-basis, simplicity, rationality, positivity or invertibility premise.
Its arbitrary-full-prefix form is stronger than the original largest-full-index
form, and the implication to the latter has the correct direction.

The spectrum is genuinely ordered with multiplicity. The code reverses the
indices of Mathlib's decreasing self-adjoint eigenvalues and reverses the
matching orthonormal eigenbasis. The eigenvector equation and full multiset of
characteristic roots are proved, and equal-span frames have orthogonally similar
compressions and equal ordered spectra. I checked the actual library definitions,
not just the theorem names. `Fin.revPerm` is an involution, so the inverse in
orthonormal-basis reindexing reverses the same indices. Natural-index fallback
zero is harmless only after both valid-index inequalities have been derived;
that derivation is present for every source-admissible interval.

The critical chain is complete. For an absent later interval `(a,b)`, every
later eigenvalue lies outside it; the true compressed quadratic `(H-aI)(H-bI)`
is PSD by diagonalizing it in its actual eigenbasis. The earlier window uses
`Fin (p+1)` distinct basis indices, so repeated eigenvalues do not reduce its
dimension. It gives a genuine subspace of dimension `p+1` with nonpositive
earlier quadratic form. Dimension addition for its sum/intersection with
`K_(k-1)` produces a nonzero vector because the latter has codimension `p`
inside `K_k`.

Only quadratic forms are transported through the earlier compression. For
`x` in `K_(k-1)`, both spaces contain `x` and `Ax`; symmetry then gives the
common expression `||Ax||²-(a+b)<x,Ax>+ab||x||²`. The code never substitutes
`A²x` for the squared earlier compressed action. The later space also contains
`A²x`, since `k+1 <= j`, and only there is the full quadratic action transported.
The ambient quadratic lift is `Q q(QᵀAQ) Qᵀ`, not `q(QQᵀAQQᵀ)`; it therefore
has no spurious `ab(I-P)` term. Positivity and the zero form imply an actual
zero vector action using the genuine PSD-kernel theorem, including singular PSD.

Nonannihilation is proved from actual coefficient-map injectivity. Extending
the coefficient array by a zero last block and shifting it by one block express
the same vector and its actual image under `A`. An eigenvector equation equates
two images under the full next-prefix coefficient map. Reverse induction from
the appended zero then kills all coefficients, without dividing by the
eigenvalue. For `q(A)x=0`, apply this first to `y=(A-bI)x` in `K_k`, obtaining
`y=0` from full rank at `k+1`, and then to `x` in `K_(k-1)` from full rank at
`k`. This is an exact implementation of the source's monic leading-coefficient
argument. Equal endpoints and zero endpoints are included.

The final contradiction derives a later eigenvalue strictly between the
specified earlier values. It includes all `1 <= k < j <= s` and all
`1 <= i <= (k-1)p`, with bases independently chosen at `k` and `j`. At the
last admissible pair, only full rank through `s` is needed. At `k=2`, the
intersection lies in the starting block and the quadratic uses powers through
two. No dimension or index is bounded for computational convenience.

For positive `p`, the first block is full and every full index has `ell*p <= n`;
the genuine largest index therefore exists. At `p=0` it does not exist, and
the existence theorem correctly requires positive width. The stronger target
still permits zero width but has no admissible interval index. The same range
is empty at `k=1`. A positive-width full-rank starting block is impossible at
`n=0`. These are proper boundary extensions, not the source of the nontrivial
theorem. For example, the three-vertex symmetric path matrix with starting
vector `e1` has three independent Krylov columns `e1,e2,e1+e3`; the pair
`k=2,j=3` has earlier spectrum `-1,1` and a later eigenvalue zero. This is a
manual nonvacuity check, not a Lean certificate.

Exact symbolic linear algebra eliminates all interval arithmetic and sampling
here. LeanCert's justified role is explicit kernel trust auditing of actual
proof terms, not an artificial numerical certificate. Its pinned implementation
collects transitive axioms and rejects admissions, custom axioms and native
compiler trust in kernel mode. Actual external default-kernel replay and Linux
Comparator remain separate gates.

The code preserves Colbrook's original mathematical authorship and the
Šimonová–Tichý conjecture attribution. George Stepaniants is credited for the
formalization with his Department of Computing and Mathematical Sciences,
California Institute of Technology affiliation and AI assistance. No George
email was added. Schiffer and Forsythe are cited as structural examples;
their mathematical arguments are not imported as KE-04 proofs. The supplied
Mathlib APIs carry the spectral, dimension, orthonormal-basis and PSD work.

Within the NLA adaptation of all ten Tau Ceti rubric angles, the fixed public
contract wrappers form the independently approved comparison boundary; they
are not a compatibility layer or a proposal to replace Mathlib APIs. The
problem-specific helper modules make the material chain readable. The frozen
historical statement-stage prose and default Challenge Lake target require
honest later packaging; they do not establish current proof verification.
