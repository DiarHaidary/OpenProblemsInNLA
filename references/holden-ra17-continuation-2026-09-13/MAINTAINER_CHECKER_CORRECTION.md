# Maintainer correction to the optional certificate checker

The integration audit found two false-acceptance paths in the optional saved-certificate checker: an incomplete monomial vector can vanish on a nonzero parameter, and rational-function multipliers can cancel a denominator only away from the bad locus. Both violate the stated certificate lemma. The mathematical continuation is unaffected, and no pencil construction is promoted: RA-17 remains partially resolved.

The corrected checker enforces the complete homogeneous monomial basis, exact rational positive-definite Gram data, polynomial multipliers in QQ[x], compatible metadata and the full polynomial identity. Explicit exceptions retain these gates under Python optimization. Ten regression tests include both rejected false certificates and an accepted exact quaternion certificate; all pass normally and with `-O`. The original 137 arithmetic checks also pass.

Only `code/sos_pencil_certificate.py` was replaced; `code/test_sos_pencil_certificate.py` and this note are new, and the package README gains a link here. The manuscript, original archives and original `MANIFEST.sha256` remain unchanged. That manifest records the original submission, as explained in `SUBMISSION.md`.

| File | SHA-256 before | SHA-256 after |
| --- | --- | --- |
| `code/sos_pencil_certificate.py` | `b03f1483b0fb3eb348512a3190255586525a792c06495c554b6965eda012baa6` | `72eda1745021758395d72ce0451cc7d0df999e0968f7d19674e4d5615fa8ae86` |
| `code/test_sos_pencil_certificate.py` | new | `438836090c48ef0f600f0b551d38503ec086d7d7a14ced03e25a06ddf7da710d` |

[Independent review](../../reviews/2026-09-13-prs-195-228/pr-223-independent-review.md) · [Repair patch](../../reviews/2026-09-13-prs-195-228/pr-223-checker-fix.patch) · [Normal tests](../../reviews/2026-09-13-prs-195-228/pr-223-checker-tests.log) · [Optimized tests](../../reviews/2026-09-13-prs-195-228/pr-223-checker-tests-optimized.log).

Patch SHA-256: `425949019459fb727af610d45498ca022924ca1290e3c2efc3cf10437fc4c8fc`.

Reproduce from this contribution directory with SymPy installed:

```sh
python -m unittest discover -s code -p 'test_sos_pencil_certificate.py' -v
python -O -m unittest discover -s code -p 'test_sos_pencil_certificate.py' -v
```
