# PR #223 optional checker repair — independent PASS

Reviewed the complete original checker, exact frozen repair patch and all 113 lines of the new regression file. The original source head remains `957c36750778d0414bdaab6ee0b92d6db7396253`; final integration reviewed at `b7495d4cf9442c2e1a12956dbd99edc0b8ad5477`.

The repair closes both reproduced false-acceptance paths. The complete homogeneous monomial basis includes a pure power of every coordinate, so its evaluation vector cannot vanish at a nonzero real parameter. Multipliers are parsed as exact homogeneous QQ polynomials with only nonzero rational-constant division; rational-function poles, floating coefficients, unknown names and evaluated function calls cannot enter the ideal-membership claim. The final polynomial identity is checked over QQ, minor metadata is compared with all recomputed minors, and exact symmetric positive-definite Gram data is required. Explicit exceptions keep every verification gate active under Python optimization. Thus an accepted Gram identity is positive at every nonzero real parameter while vanishing at any common zero of the minors, giving the intended contradiction.

The negative fixtures use an independent five-parameter pencil with an explicit nonzero rank-one member. One fixture supplies an incomplete monomial vector; the other supplies all monomials but divides its positive form by a minor. Both satisfy the old superficial identity/positivity checks, so their rejection is substantive. The positive fixture is a real quaternion pencil: its full cofactor sum divided by four equals det(A)=(sum xi²)², represented by a positive diagonal Gram matrix on all ten quadratic monomials. This proves the checker still accepts a genuine exact certificate. Other tests separately reject bad metadata, duplicate monomials, a corrupted identity, nonpositive Gram matrices and forbidden multiplier coefficients or operations.

I independently copied the exact frozen checker and regression file into `/private/tmp/nla-pr223-independent-fix/`, verified their SHA-256 hashes, and ran all ten regression methods with Python `-O -B`; all passed, including the genuine acceptance case. The log and complete file identities are `/private/tmp/nla-pr223-independent-fix/independent-optimized-tests.log` and `identities.json`. This is an independent regression run of the reviewed repair, not Lean execution or a new proof of a matrix-pencil construction. RA-17 remains Partially resolved.

| Artifact | Exact SHA-256 |
|---|---|
| Original checker | `b03f1483b0fb3eb348512a3190255586525a792c06495c554b6965eda012baa6` |
| Repaired checker | `72eda1745021758395d72ce0451cc7d0df999e0968f7d19674e4d5615fa8ae86` |
| New regression file | `438836090c48ef0f600f0b551d38503ec086d7d7a14ced03e25a06ddf7da710d` |
| Exact repair patch | `425949019459fb727af610d45498ca022924ca1290e3c2efc3cf10437fc4c8fc` |

I also read the complete new MAINTAINER_CHECKER_CORRECTION.md and the package README's four-line append. The note accurately describes the repair, unchanged mathematical scope, actual tests and original archival manifest, and its relative links resolve to the retained audit evidence. These two documentation changes are explicitly bound in the preservation gate. Original manuscripts, archives and MANIFEST.sha256 remain byte-identical; SUBMISSION.md already identifies that manifest as the original archive record. No integration/GitHub mutation was performed by this reviewer.
