# IE-11 — recovered write-up and exact verification package

**This package is not a full solution of IE-11.** It does not establish
`g_5 = alpha` and does not supply a counterexample. The matching global upper
bound has not been proved by this work.

Read **[the mathematical report](report/IE11_report.pdf)** first. Its LaTeX
source and two generated tables are included in the same directory.

## What is established

The algebraic candidate has fifth pivot

`alpha = 4.132517078632472854223346853277371269952791537799...`

Exact symbolic checks reconstruct the degree-61 polynomial, match all 62
coefficients against the cited paper, and prove its root in `(4,5)` is unique.
Integer-based outward interval arithmetic proves feasibility and strict local
maximality in all 24 free matrix entries, **with A_11 = 1 and the diagonal CP
path fixed**. This does not exclude other pivot configurations or remote matrices.

A separate rational matrix is checked with `fractions.Fraction`: all 100
nontrivial pivot comparisons are strict, the matrix is nonsingular, and its
fifth pivot exceeds

`4.13251707863247285422334685327737126995279153779`.

The candidate and its lower-bound interpretation are attributed to Chen,
Edelman, and Urschel; they are not claimed as new discoveries.

The global LU model includes every normalized diagonal pivot pattern, not just
the candidate family. The supplied counterexample query is **not solved**.
One recovered convex-hull relaxation is proved to have optimum `81/16 = 5.0625`;
its maximizing mixture fails a rank-one condition and is **not a CP matrix**.
This explains why that relaxation does not settle the problem.

## Reproduce all exact checks

Use Python 3.10 or later. From this directory:

```sh
python -m pip install -r requirements.txt
python src/check_manifest.py
python src/run_all.py
```

Do not use Python's `-O` option: the scripts intentionally use assertions as
exact verification checks. The aggregate command stops on a failure.

The symbolic reconstruction requires SymPy. All other verification scripts
use only the Python standard library and supplied data. A minimal independent
check of the rational matrix is:

```sh
python src/rational_witness.py
```

The exact rational witness is already included; generation is not needed for
verification. `python src/rational_witness.py --generate` rebuilds it from the
finite rational centers and then checks it.

## Package map

| Location | Contents |
|---|---|
| `report/IE11_report.pdf` | Definitions, exact derivations, local-maximality proof, global formulation, and explicit gap |
| `src/run_all.py` | Aggregate check runner |
| `src/derive_algebra.py` | Polynomial reconstruction, identities, reference comparison, discriminant and root count |
| `src/intervals.py` | Small integer-based outward interval kernel |
| `src/verify_local.py` | Root, feasibility, Jacobian-rank and multiplier certificates |
| `src/rational_witness.py` | Independent exact strict-CP witness verification |
| `src/global_model.py` | All-path LU formulation, SMT-LIB generation and exact identity tests |
| `src/verify_layer_hull.py` | Exact optimum certificate for the **relaxation**, not for `g_5` |
| `data/` | Exact integer/rational inputs and the unsolved global query |
| `results/` | Machine-readable reports from successful checks |
| `exploratory/layer_hull.py` | Optional numerical-support discovery followed by exact reconstruction; not required by the verifiers |
| `SOURCES.md`, `PROVENANCE.md`, `VERIFICATION.md` | Attribution, recovery history, and trust boundary |

The optional exploratory generator additionally requires NumPy and SciPy. It is
not needed to reproduce the exact relaxation certificate already supplied.

`MANIFEST.sha256` records the distributed files. Running the checks rewrites
some generated result files and timing fields, so check the manifest **before**
rerunning them.

## The unproved statement

For **every** unit lower-triangular `L` and upper-triangular `U` satisfying the
complete-pivoting inequalities in Section 7 of the report, with positive pivots
and `u_11 = 1`, prove `u_55 <= alpha`, or produce a valid matrix violating it.
A strict local maximum, a polynomial root, numerical searches, and an unsolved
SMT file do not establish this universal assertion.
