# IE-20: exact scalar threshold and extended precision bounds

**Status: extended partial resolution, not a full solution to IE-20.**

Start with `IE20_extended_results.pdf` (18 pages). This is a new manuscript,
not a relabeling of the recovered work. The previous archive is preserved
unchanged as `prior/IE20_recovered.zip`.

## The remaining gap

The requested target is a characterization with universal multiplicative
constants for every `(n, K, epsilon)`. That target is not met here. For example,
at `K = n^2` and `epsilon = n^(-2)`, the proved generally applicable lower and
upper bounds are still `Omega(log n)` and `O(n log n)`. Section 9 states this
limitation. Passing the accompanying finite checks does not close it.

## Main additions

Theorem 2.1 determines the scalar threshold exactly. With `u = 2^(-p)`, set

```text
E1(u) = ((1+u)^4 - (1-u)^5) / ((1+u)^4 + (1-u)^5).
P_CG(1,K,epsilon) = min {p >= 2 : E1(2^(-p)) <= epsilon}.
```

Theorem 3.2 gives a jointly dimension- and conditioning-dependent breakdown
construction. In particular, for `n >= 2`, the lower bound is at least
`log2(n*K) - 5`, uniformly over admissible tolerances.

Theorem 4.2 gives a first-step precision guarantee above the exact first-step
maximum `M(K) = (K-1)/sqrt(8*K*(K+1))`. For `n >= 2` and
`3/8 <= epsilon < 1/2`, the resulting explicit two-sided estimate is

```text
log2(n*K) - 5 <= P_CG(n,K,epsilon) <= log2(n*K) + 17.
```

Lemma 5.1 bounds the prescribed left-to-right matvec error by
`4*n*u*||A||_2*||v||_2` when `n*u <= 1/2`. This uses the actual row-prefix
structure rather than an entrywise absolute-value matrix bound.

Theorem 7.1 proves a stronger general sufficient precision. Define

```text
Kbar = max(2,K)
kC   = ceil(sqrt(Kbar)) * ceil(log2(16*Kbar/epsilon))
kU   = ceil((64/epsilon)^(2/3))
m    = min(n,kC,kU)
H    = min(K,64/epsilon^2)
D    = 1024*H^2.
```

Then a sufficient precision is

```text
max(2, ceil(log2(1024*(n+1)*K*D^(12*m+20)/epsilon^2))).
```

The proof controls the actual rounded recurrence, excludes premature
breakdown, and transfers polynomial approximation to computed iterates.
It does not assume exact Krylov identities for rounded vectors.

For each fixed tolerance, Corollary 8.2 yields the additive characterization

```text
P_CG(n,K,epsilon) = log2(n*K) + O_epsilon(1),
```

uniformly in `n >= 2` and `K >= 1`. **The additive constant depends on the
fixed tolerance.** This is not a universal all-parameter formula. Other
sharp regions include `1 <= K <= 2`, dimension two, and sufficiently fine
tolerances as specified in Section 8.

## Reproduce the checks

Use Python 3.10 or later from this directory. No third-party Python package
is required. Run without `-O`; assertion-based witness verifiers reject
optimized mode.

```sh
python -m unittest discover -s code -v
python code/verify_extended.py
python code/verify_legacy.py --output results/legacy_checks.json
python code/bounds.py --n 16 --K 256 --epsilon 1/256
```

The recorded validation passed all 26 unit tests, all 15 retained witnesses,
1,536 scalar sign-corner executions, 256 first-step executions, 31 exact
polynomial constructions, 3,999 rational-grid polynomial checks, 90
parameter-bound consistency checks, 14 joint breakdown witnesses, and 24
dense matvec prefix-bound executions.

These categories overlap in purpose; they are not independent theorem
verifications. Polynomial grid checks do not establish an inequality
between grid points. The finite checks do not establish the general
bootstrap, the asymptotic hard family, or the missing matching theorem.

## Bound evaluator

`code/bounds.py` distinguishes the exact scalar threshold from general
lower and upper bounds. General upper bounds need not be sharp. The code
uses integer/rational comparisons rather than floating-point logarithms.
To avoid huge rational powers, its reported general upper uses

```text
ceil(log2(1024*(n+1)*K/epsilon^2)) + (12*m+20)*ceil(log2(D)).
```

This conservative integer can exceed the single ceiling in the theorem by
at most `12*m+20` bits. The report says so explicitly.

## Arithmetic model and scope

This is the adversarial scalar relative-error envelope in the IE-20
specification, not a simulation of IEEE round-to-nearest. Input
significands are checked exactly, but intermediate results are exact
rationals satisfying the selected error equations. Every required zero
term and addition is retained. All lower-bound schedules are admissible
in this envelope; no claim transfers them to a stricter rounding map.

The proofs have not been independently refereed or proof-assistant
verified. `PROOF_SCOPE.md` separates analytic arguments, imported facts,
finite certificates, and remaining gaps. `SOURCES.md` records the primary
sources and their roles. No priority claim is made.

## File map

| Path | Purpose |
| --- | --- |
| `IE20_extended_results.pdf` | New 18-page manuscript |
| `IE20_extended_results.tex` | Editable LaTeX source |
| `code/envelope_cg.py` | Exact scalar-error-envelope executor |
| `code/bounds.py` | Exact scalar threshold and conservative general bounds |
| `code/joint_breakdown.py` | Rational joint dimension/conditioning witness |
| `code/polynomials.py` | Exact shifted-Chebyshev polynomial construction |
| `code/verify_extended.py` | New reproducible checks and JSON report |
| `code/test_extended.py` | New unit tests and shared exact first-step helper |
| `code/verify_legacy.py`, `code/test_legacy.py` | Retained witnesses/regressions |
| `code/build_pdf.py` | Optional three-pass PDF rebuild |
| `results/` | Regenerated reports and logs |
| `PROOF_SCOPE.md` | Claims, dependencies, quantifiers, and limits |
| `SOURCES.md` | Primary references and source roles |
| `DIFFERENCES_FROM_RECOVERY.md` | Changes from the prior package |
| `prior/IE20_recovered.zip` | Original partial archive, unchanged |
| `MANIFEST.sha256` | Checksums for all other package files |

## PDF rebuilding and integrity

The PDF is ready to read. To rebuild it, install `pdflatex` and the packages
listed in the source preamble, then run:

```sh
python code/build_pdf.py
```

The helper compiles in a temporary directory and keeps only the final PDF.
Rebuilding may change PDF metadata and checksums. Before regenerating any
files, systems with `sha256sum` can verify the delivery using:

```sh
sha256sum -c MANIFEST.sha256
```
