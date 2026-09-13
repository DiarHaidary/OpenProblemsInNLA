# Independent review of PR #249: IE-27 and IE-28

Reviewed head `9e11821e2e999afb1699272005a167da7ee42861` against base `752218e5417998b7f4d2aee9c447ca5d256fe530` in `/private/tmp/nla-audit-249`. This is an independent informal mathematical/code audit, with fresh execution of the actual supplied verification code. It is not external human peer review or proof-assistant formalization.

**Verdict: no actionable correctness findings in the IE-27/IE-28 changes.** The two entries appropriately remain **Partially resolved**. Neither original universal target has been replaced or declared solved. No source, archive, attribution, registry, or GitHub state was modified by this review.

## Scope and mathematical audit

I read the full IE-27 continuation and retained nine-page proof, the IE-28 extended report and retained prior writeup, and the structural supplement. I also read the ten-page historical recovered IE-28 PDF. The actual trusted interval/exact-field implementations and relevant tests were read before execution; submitted PASS logs were not used as evidence of acceptance.

### IE-27

- The canonical statement retains the Radau IIA nodes, no-pivot Crout normalization with unit upper diagonal, stipulated Euclidean radius `||U-I||_2<1`, SPD spatial pencil, and **real positive** shifts. Its mathematical target is unchanged from the base.
- The differentiation formula follows from interpolation on degree-at-most-q polynomials vanishing at zero. The Jacobi coefficient formula, Legendre relation and differential equation correctly give the special diagonal entries. Diagonal similarity produces a skew off-diagonal part with strictly positive diagonal; every leading principal submatrix has eigenvalues in the open right half-plane, so the leading determinants and Crout pivots are positive.
- The spatial congruence/simultaneous permutation correctly reduces the generalized spectrum to `(I+mu L^-1)^-1 N` with `mu>0`. The common-energy criterion correctly bounds the product in an H norm for the entire half-line; it does not rely on a sampled grid.
- The interval checker isolates all q-1 interior nodes by exact polynomial signs, reconstructs the exact Radau factors from enclosing intervals, checks rational metric symmetry/dimensions, uses outward-rounded integer interval arithmetic and LDL congruence to prove all required positive matrices, and verifies a nonzero Rayleigh vector with a strictly positive gap. The supplied data certify **exactly q=2,...,64,80,96,128 (66 stages)**, not all stages up to 128.
- The all-stage small-shift proof uses the finite nilpotent resolvent expansion and excludes an eigenvalue beyond the radius when `mu<=1/(q||L^-1||_2)`. Strictness survives at the endpoint because `N` is nonzero and q>=2. The large-shift Neumann bound works for `mu>=2||L||_2`, including that endpoint. Both results leave a nonempty unproved intermediate regime for uncertified stages.
- The square-root sufficient norm criterion uses the correct `PP^T`/`NN^T` orientation and the identity `K+mu(L+L^T)+mu^2 I=(mu I-K^(1/2))^2+mu(L+L^T+2K^(1/2))`. It is not asserted to hold for every stage.
- The exact generic-matrix obstruction, Euclidean resolvent obstruction and complex-shift Schur test are valid and are explicitly kept outside the original target where applicable.

### IE-28

- The canonical target remains one positive diagonal for every prescribed ordered positive distinct node set, with nilpotence of `I-D^-1 A`; no increasing-diagonal requirement, special family, nonstiff matrix, triangular matrix or variable-sweep sequence replaces this target.
- The inverse diagonal similarity and determinant/characteristic identities are correct. The two-stage eigenpolynomial and determinant finish that case. The three-stage determinant-normalized parameter has uniform positive finite brackets; its continuity and the exact opposite endpoint trace signs give the required root by the intermediate value theorem. One known eigenvalue, trace and determinant finish the spectrum only in dimension three.
- Integration modulo the node polynomial in the factorial monomial basis gives the stated companion characteristic polynomial. Rodrigues orthogonality proves simple positive Laguerre roots. Matching coefficients proves the scalar-diagonal characterization; it remains a special all-stage node family.
- The alternant numerator is divisible by the Vandermonde product in the polynomial ring, so the regularization genuinely extends across node collisions. The augmented Taylor recursion gives the confluent determinant with correct constant normalization. The reversed coefficient system has the stated nonsingular triangular Jacobian at the algebraic seed. The implicit function theorem and positivity by continuity therefore prove a neighborhood for each fixed stage, with no global continuation inference.
- The n=11 obstruction combines an exact negative leading-coefficient certificate with compactness of the normalized nonnegative-coefficient simplex, convergence of logarithmic derivatives and divided differences, uniqueness of the negative-a1 seed, and the Taylor recursion. It excludes the stated stronger eigenpolynomial ansatz; it is compatible with the locally existing positive diagonals.
- The twelve certificates use all characteristic coefficients of the original inverse collocation matrix, exact node/diagonal boxes, outward interval principal determinants and the full Jacobian. Strict contraction and self-mapping give a zero for each node vector in the box. The proof correctly deduces invertibility of the square preconditioner from `||I-RJ||<1`; uniqueness is confined to the diagonal box.
- The supplement's Vandermonde row-differentiation argument proves all principal-minor identities. Its auxiliary matrix has principal minors 1,17,49, and AM-GM gives the stated contradiction. It lacks the collocation reciprocal-difference structure and does not disprove IE-28.

## Fresh verification

Runtime: `/private/tmp/nla-batch-python/bin/python`. Outputs were directed to `/private/tmp`, preserving supplied results. All commands completed with exit code 0.

| Fresh run | Outcome | Evidence |
| --- | --- | --- |
| IE-27 `code/run_all.py --output /private/tmp/nla-pr-249-ie27-fresh` | All 66 certificates, 20 tests, exact q=3 proof and exact obstructions passed | `/private/tmp/nla-pr-249-ie27-fresh/summary.json`, `tests.txt`, `verified.json`, `exact_q3.json`, `exact_obstructions.json`; console `/private/tmp/nla-pr-249-ie27-console.jsonl` |
| IE-28 `certification/verify.py` on both delivered certificate files | Six point and six neighborhood certificates passed | `/private/tmp/nla-pr-249-ie28-certs.json`, `.log` |
| IE-28 `cluster/certify_seed.py` | Checked n=11 root bracket and strict negative coefficient, approximately -1.664574554026851e-10 | `/private/tmp/nla-pr-249-ie28-seed.json`, `.log` |
| IE-28 `tests/test_exact.py` | 1,500 rational interval trials; 50 determinants; seed Jacobians n=2..6; confluent identities n=2..5; collocation identities n=2..7; Laguerre identities n=1..15; 12 certificates and 3 corrupted-input rejection checks passed | `/private/tmp/nla-pr-249-ie28-exact.log` |
| IE-28 prior `scripts/check_symbolic.py` | Formal low-stage endpoint identities and all other supplied symbolic checks passed | `/private/tmp/nla-pr-249-ie28-symbolic.log` |
| Supplement `verify_structural_reduction.py` | Similarity, all-subset principal-minor tests and auxiliary obstruction passed | `/private/tmp/nla-pr-249-ie28-structural.log` |

Additional reviewer-written tests in `/private/tmp/nla-pr-249-independent-exact-check.py` passed. For every one of the six point centers, these build A by **direct exact Lagrange integration**, invert it, compare every principal minor with the verifier's enclosures, and independently match the coefficient system and Jacobian, including dimensions six and seven. They also check the IE-27 Legendre/Jacobi/ODE identities through q=24 and match its inverse formula against exact direct integration for q=2,3. Evidence: `/private/tmp/nla-pr-249-independent-exact-check.log`.

## PDF inspection and provenance

All nine relevant PDFs were rasterized with Poppler at 100 dpi without rebuilding or editing any PDF: IE-27 manuscript/submitted continuation (8 pages each), prior report (9); IE-28 manuscript/submitted extension (13 each), prior writeup (9), historical recovered report (10); and the two canonical PDFs (2 each). Total **74 pages**. I visually inspected all **55 distinct page images** using 14 contact sheets and a full-page follow-up. The remaining 19 pages were matched byte-for-byte at the rendered pixel level: IE-27 continuation pages 2-8 and IE-28 extended pages 2-13 match their attributed manuscripts. All mathematical content, author/status lines, tables, equations and references are legible, with no material clipping or overlaps observed. Files and pixel mapping: `/private/tmp/nla-pr-249-pdf-ie27-ie28/`.

The historical structural-bundle README advertises source/certificate directories missing from that delivered bundle. This is already explicitly disclosed in the submission wrapper and existing review. Its historical four-stage algebraic certificate cannot be replayed from the supplied files and was not used as additional proof evidence here; the accepted present four-stage existence result has separate replayed exact certificates in the main extended bundle. Preserve the historical payload unchanged.

## Primary-source and review limits

I checked the original van der Houwen-de Swart conjecture and positive-distinct-node setting at pp.46-47 of https://ir.cwi.nl/pub/2191/2191D.pdf, and the fixed MIN-SR-S/no general existence guarantee at p.A439 of https://d-nb.info/1363153935/34. Outrata's https://arxiv.org/html/2510.21241v1 confirms the Radau spectral-disk context and real-positive SPD reduction; the repository correctly calls out its radius/diameter wording discrepancy. The original IE-27 institutional PDF endpoint returned a browser internal error in this review. This does not affect the unchanged base statement or the self-contained proof/certificate implication checked above; it is not a fresh exhaustive literature search.

The n=8,11,15 continuation logs and optional numerical generator/optimizer outputs were not promoted to proof evidence or rerun as exact certificates. This audit supports the specific restricted claims and preservation of both unresolved universal targets, not novelty, optimality, or all-stage/all-node completion.
