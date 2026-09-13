# PR 223 independent review

Exact source head: `957c36750778d0414bdaab6ee0b92d6db7396253`.
Published comparison base: `5830ed4fb06da0659414a3deb2a40ad327aca052`.
Read-only checkout: `/private/tmp/nla-audit-223`.

**Disposition: mathematical PASS for the stated partial continuation; acceptance is conditional on the supplied narrow correction to the optional saved-certificate checker.** The original checker has two independently reproduced false-acceptance paths. Neither is used by the proved topological results or an accepted pencil construction. The corrected checker and regression tests pass. RA-17 remains partially resolved and open.

## Concrete source-head blocker and tested repair

File `references/holden-ra17-continuation-2026-09-13/code/sos_pencil_certificate.py`, original lines **41–46**: `verify()` accepts an arbitrary list of monomials and parses purported polynomial multipliers with unrestricted `sympify`. It checks an expression identity and a positive Gram matrix, but never establishes that the monomial vector is nonzero at every nonzero parameter or that the multipliers are polynomials. These are essential hypotheses of the manuscript's acceptance proof.

Reproducer: `/private/tmp/nla-pr-223-independent-run/check_false_certificate.py`. It supplies the independent five-parameter real pencil

`A(x)=diag(x0,x1,x2,x3)+x4 E01`,

which contains the rank-one matrix E00 at `(1,0,0,0,0)`. Its first listed cubic minor is `f0=x0*x1*x2`. The original checker returns `EXACTLY_VERIFIED` for both:

1. Degree six, `z=[x0*x1*x2]`, `H=[1]`, `h0=f0`, all other multipliers zero. The polynomial identity is true but z vanishes on the bad locus.
2. Degree four, the complete degree-two monomial vector z and H=I, `h0=(sum z_i^2)/f0`, all other multipliers zero. SymPy cancels the denominator in the expression identity, although h0 is not a polynomial and is undefined on the bad locus.

Outputs are in `false_certificate_results.json` in that scratch directory. The missing `data/interrupted_pencil.json` in the actual archive is transparently explained by `pencil_audit_status.json` (`NOT_PROMOTED`, no successfully extracted pencil). I supplied the above synthetic pencil only in scratch to test the advertised checker; I did not manufacture an accepted archived construction or change the source checkout.

Root authorized a narrow integration repair. Final files:

- `/private/tmp/nla-pr223-checker-fix/code/sos_pencil_certificate.py`
- `/private/tmp/nla-pr223-checker-fix/code/test_sos_pencil_certificate.py`
- Integration patch: `/private/tmp/nla-pr223-checker-fix.patch`
- Exact old/new SHA-256 records: `/private/tmp/nla-pr223-checker-fix/hashes.json`

The repair requires a complete, duplicate-free monomial basis of a common positive degree, strict integer degree/exponent metadata, compatible matrix/minor dimensions, exact finite rational Gram entries, symmetry and positive definiteness, and homogeneous multipliers in QQ[x] of the required degree. A bounded arithmetic AST parser permits only polynomial operations and division by nonzero rational constants, with no expression evaluation or nonpolynomial functions. Acceptance uses explicit exceptions rather than assertions, so Python `-O` does not remove verification gates. The whole polynomial identity is recomputed from the pencil's actual minors.

Ten regression tests, including both false certificates, pass in normal and optimized Python. The positive fixture is the genuine four-variable real quaternion pencil, with `A^T A=(sum x_i^2)I` and determinant `(sum x_i^2)^2`. The complete quadratic monomial Gram matrix has diagonal one on pure powers and two on mixed monomials; Euler's determinant identity supplies exact linear minor multipliers. Additional controls reject nonpositive Gram forms even when the polynomial identity holds, identity corruption, invalid domains, incomplete/duplicate monomials, and malformed metadata. The original 137 arithmetic checks also pass after the repair. Logs: `checker-tests.log`, `checker-tests-optimized.log`, `relaxation-tests.log` in the repair directory.

SHA-256 identities:

| File | Original | Corrected/new |
|---|---|---|
| sos_pencil_certificate.py | b03f1483b0fb3eb348512a3190255586525a792c06495c554b6965eda012baa6 | 72eda1745021758395d72ce0451cc7d0df999e0968f7d19674e4d5615fa8ae86 |
| test_sos_pencil_certificate.py | new file | 438836090c48ef0f600f0b551d38503ec086d7d7a14ced03e25a06ddf7da710d |

The source-head manuscript and original-archive manifest should remain preserved; a separate integration repair note can identify the explicit checker exception and new hashes.

## Full mathematical audit

I read all 622 lines of the actual `writeup/main.tex`, its three-line `pencil_audit.tex` input, the canonical original target/status, package README and provenance/scope notes, all of the primary arithmetic script, and both optional certificate-checker implementations. Preserved exploratory archives are clearly not promoted to additional theorems. This review does not infer correctness from the submitted independent review or recorded PASS logs.

The original unrestricted, uniform, real linear measurement problem is unchanged. The continuation consistently separates linear measurement systems, continuous odd maps on the low-rank link, and arbitrary evaluation-bundle frames. It does not infer a constant-matrix linear space from either relaxation.

**Continuous critical relaxation.** With k=2r<d, c=d−k, n=d²−c²−1, the projectivized rank-at-most-k locus X has dimension n, and its singular locus has codimension 2c+1≥3. The projective resolution P(dS) has first tangent Stiefel-Whitney class `dk h + du + du = 0`, so its smooth rank-k stratum U is orientable. Full-row-rank k×d matrices are connected for k<d, establishing connectedness. Since k is even, an SO(k) path from I to −I gives the nontrivial tautological sign monodromy on U.

The finite-triangulation/relative-cohomology argument legitimately identifies top cohomology of X with compactly supported top cohomology of U; the singular codimension removes both adjacent terms. Twisted Poincare duality gives H^n(X;Z_lambda)=Z/2, and the coefficient sequence gives an isomorphism to H^n(X;F2). The rank-n sphere bundle has only its degree-n Euler obstruction on the n-dimensional base, including the orientation local system. Its mod-two reduction is a^n, whose evaluation equals determinantal degree modulo two by a transverse generic real hyperplane intersection avoiding the lower strata. Thus even degree is necessary and sufficient for the stated odd continuous map at this critical dimension. No higher obstruction is being omitted. Polynomial approximation, odd symmetrization, rational approximation and odd homogenization preserve the compact nonvanishing margin, but do not yield a linear measurement system.

**Critical evaluation frame.** Here E=dQ has rank N=dc, the Grassmannian has even dimension b=kc, and q=c²+1=N−b+1≥2. The Stiefel fiber is (b−2)-connected with first homotopy group pi_(b−1)=Z/2: the reduction to V_(b+1,2) and its sphere tangent-bundle Euler boundary, multiplication by two, are correct, including b=2/q=2. Therefore w_b(E) is the entire obstruction on the b-dimensional base. Generic constant-matrix sections compute its parity through the finite projective determinantal intersection, each generic rank-k pencil element having a unique c-dimensional kernel. The resulting equivalence to even degree is correct. The ensuing limitation is explicitly limited to the abstract bundle decomposition; it does not claim all possible topological obstructions to linearity are exhausted.

**Rank-one index lower bound.** For d=2l, the unoriented Grassmannian ring is Q[p]/(p^l). The normalization integral p^(l−1)=1 follows from the degree-two oriented-plane cover and the quadric hyperplane number two: the map [v+iw] identifies oriented planes with isotropic lines and the Euler root is the hyperplane root up to sign. Both TG and eta are oriented. The formulas w2(TG)=(l−1)u² and w2(eta)=l u² are correct; the integral Bockstein of u is a torsion lift, so Spin^c structures with torsion determinants suffice. The proof never assumes these bundles are spin.

The stable tangent identity and normalized spinor character multiply to `(z/sinh z)^(d−1)`. Residue substitution v=sinh z gives the signed central-binomial coefficient and the stated power of two. The half-spin refinement applies exactly when the complementary rank is 2 mod 4, when its rational Euler class vanishes. It correctly converts the central-binomial valuation h=popcount(l−1) to the forbidden kernel dimensions and hence to `mu_R(d,1) >= 4d−4−2h+(h mod 2)`. Larger kernels contain the forbidden smaller kernel. In dimension six, the impossible half-index is 3/2 at an eighteen-dimensional kernel, while the seventeen-dimensional kernel's total index is 3. The even degree 1764 genuinely permits the latter abstract complement, which is why the original linear gap remains. The d=10 lower endpoint 35 also follows directly from this theorem; the generic integer construction supplies 36.

**Algebraic constructions and scope.** The antidiagonal Vandermonde moment rows have the correct rank and minimum-support property and yield a triangular nonzero (k+1)-minor on the first nonzero antidiagonal. The odd-degree exactness argument is sound. The mathematical positive-Gram certificate lemma is sound with its full stated hypotheses; the original implementation failed to enforce them as described above. The projective-chart coverage and Hermite trace-signature argument correctly account for all real points, including nilpotent local factors and conjugate complex pairs. A positive-dimensional chart or absent candidate remains inconclusive. No optional small-pencil construction is accepted in this continuation.

## Primary imports checked

- [Xu's original paper](https://arxiv.org/pdf/1505.07204v1) and [survey Theorem 5.5](https://arxiv.org/html/2506.17572v2), for determinantal degree and the real/complex target distinction.
- [Carlson, Corollary 2.3](https://arxiv.org/pdf/1611.01175v2), including oriented versus unoriented presentations and the Euler/Pontryagin relation. I also checked [He, Corollary 5.26](https://arxiv.org/pdf/1609.06243) in the related PR197 audit.
- [Hatcher, Vector Bundles and K-Theory, Section 3.3](https://pi.math.cornell.edu/~hatcher/VBKT/VB.pdf), particularly Lemma 3.20 (the exact first Stiefel homotopy group), the primary-obstruction construction, Stiefel-Whitney obstruction identification, and Euler-class obstruction. The local-coefficient extension is explicitly discussed there; in the manuscript its top-degree coefficient group is computed rather than assumed untwisted.
- For the Spin^c import, the integral-lift criterion is stated in [Ginzburg–Guillemin–Karshon, Appendix D, Proposition D.31 and D.43](https://ncatlab.org/nlab/files/StableComplexSpinC.pdf). The required **twisted** index formula is also explicitly stated in [Dessai, Section 3, printed p.5](https://homeweb.unifr.ch/dessaia/pub/papers/0102061.pdf): the determinant factor is e^(c/2), and arbitrary complex twisting bundles contribute ch(V). Its reduction to the manuscript's formula when c is torsion is valid. The spinor product was independently checked from the formal weights. I did not claim to have obtained the entire cited Lawson–Michelsohn book.

## Independent computation and PDF evidence

The inspected primary script was rerun in `/private/tmp/nla-pr-223-independent-run`, producing 137 passing exact checks, including regenerated integer measurement systems, degree identities/parities and index coefficients. No source files changed.

`/private/tmp/nla-ra17-independent-checks.py` independently recomputes SW classes through quotient-ring multiplication/Groebner reduction and degrees through Jacobi–Trudi, independently of the submitted hook/parity implementation, and recomputes the dimension-six half/total spinor indices through Newton sums in Pontryagin roots. All 17 combined RA-17 checks pass; output `/private/tmp/nla-ra17-independent-checks.json`. Fresh exact Hermite controls for Q[x]/(x²+1), Q[x]/x² and Q[x]/((x−1)²(x²+1)) have signatures 0,1,1, respectively, including both complex and nonreduced factors; output `hermite-controls.json` in the independent-run directory.

Using the PDF skill, I rendered and visually inspected **all 2 canonical pages and 11 manuscript pages**. No clipping, missing formulas, broken tables or incorrect solved status was found. The table of contents continues onto page two but is legible. Evidence: `/private/tmp/nla-ra17-pdf-review/223-canonical` and `223-manuscript`.

The canonical ID/path and original all-parameter target are retained. The manuscript and page explicitly leave 19≤mu_R(6,1)≤20 and 35≤mu_R(10,1)≤36 undecided, distinguish the continuous result from linear recovery, and claim neither Lean verification nor external human peer review. Acceptance with the narrowly documented checker repair is warranted for that scope only.
