# SP-03: Stein normal form and certified critical points

**Status: partial; not a proof or refutation of the proposed all-rank formula.**

The target is the generic complex critical-point count for ordinary-transpose Frobenius distance on `Sp(2m,C)`:

    D_m =? 2^(m*m) + 2^(2*m - 1).

The metric and embedding are unchanged. This is not a Hermitian-distance calculation.

## Mathematical results in this continuation

The report proves an exact factorization of the previous reduction's denominator. After normalizing the upper-left data block to the identity and putting `C = 4 A - I`, the regular domain becomes

    Omega_m = { C : Delta_m(C) != 0 },
    Delta_m(C) = det(Sym^2(C) - I)
               = det(C-I) det(C+I) det(wedge^2(C)-I).

The auxiliary symmetric matrices solve two explicit Stein equations. The generic degree of the matrix map in Theorem 4.2 of `report.pdf` is exactly `D_m`. That degree has not been evaluated in all ranks.

The report also proves

    chi_c(Omega_m) = (-1)^m sum_{r=0}^m r! S(m,r),
    D_m is even for every m >= 1.

The homogenized denominator restricts at infinity to `(det C)^(m+1)`. The report proves that escaping critical families with a nonzero limiting `d` must approach singular matrix directions. No Schur-stability condition is imposed on `C`; only the stated reciprocal-eigenvalue exclusion is used.

At zero coupling (`b=c=0`) the regular fiber has exactly `2^m` simple points; the report proves that the other generic branches must approach the excluded divisor or singular directions at infinity. This specialization is not degree preserving.

The Euler characteristic is **not** asserted to equal the ED degree. The parity theorem combines with certified simple roots to round an odd lower bound up to the next even integer.

## Exact certificates and scope

| Rank | Distinct simple roots certified | Lower bound after the parity theorem |
|---:|---:|---:|
| 1 | 4 | 4 |
| 2 | 24 | 24 |
| 3 | 543 | 544 |
| 4 | 31,183 | 31,184 |

All final centers passed a fresh C++ exact-integer contraction check and a separate Python integer/fraction contraction recheck. Exact separation was checked as well. The Python reference shares the numerical inverse-proposal routine and the exact separation helper, but does not call the C++ checker. The rank-one and rank-two centers are inherited; the main certificate directory includes their fresh verification records.


The final certificate counts and their parity consequences are recorded in `claims.json` and `results/final_rank3_verification.json` / `results/final_rank4_verification.json`. These counts are existence, simplicity, and distinctness results. **No completeness certificate is supplied.**

Each binary64 real and imaginary component in a certificate file is an exact dyadic rational. The files store full ordinary-coordinate centers and the exact ordinary-coordinate data matrix. The verifier reconstructs the full polynomial system and checks contraction inequalities with arbitrary-precision integers. It separately proves disjointness of all accepted balls using exact integers and fractions.

No approximate residual, numerical monodromy stopping rule, computed Jacobian inverse, or rounded root count is trusted as proof. Jacobian inverses are untrusted proposals that are recomputed and checked, not bulky stored data. Different numerical libraries can produce different proposals; a proposal must still pass the same exact inequalities.

## Build and verify

A Linux environment with a C++17 compiler, Boost headers, and the Python dependencies in `requirements.txt` was used. Exact tested versions are recorded in `results/environment.json`. The compiler command below builds a local shared library; no prebuilt platform binary is needed.

```sh
python -m pip install -r requirements.txt
make backend
python verify/verify_roots.py certificates/rank3.npz --workers 4
python verify/verify_roots.py certificates/rank4.npz --workers 4
```

The rank-four verification took several minutes in the supplied environment. The thread count can be reduced to one without changing the mathematical test. The verifier exits with an error if any contraction or separation assertion fails.

An additional, separate implementation uses Python integers and fractions without calling the C++ checker. A sampled run is explicitly labeled as a sample:

```sh
python verify/reference_check.py certificates/rank4.npz --sample 64
```

The complete independent reference run used:

```sh
python verify/reference_check.py certificates/rank4.npz --all --workers 4
```

This is still a lower-bound verification, not a completeness test. The final run checked all 31,183 rank-four centers; a sampled rerun is explicitly labeled as a sample.

Core algebra and backend comparisons:

```sh
make tests-core
```

The full test suite additionally tests optional quad-precision *proposal* refinement. It requires GCC's `libquadmath`:

```sh
make tests
```

The quad helper is not required to verify the final stored roots. It was used only when generating some proposals. Its output is always checked by the integer backend.

To rebuild the mathematical report:

```sh
make report
```

## Continue the numerical search

All search outputs are untrusted candidates until passed through the full-coordinate certificate stage. A portable starting command is:

```sh
python experiments/monodromy_general.py --rank 4 \
  --source certificates/rank4.npz --output experiments/new_rank4.npz \
  --seconds 600 --workers 4
```

Then certify the resulting reduced-coordinate candidates against the **same exact ordinary data**:

```sh
make quad
python experiments/certify_fixed.py \
  --input experiments/new_rank4.npz \
  --ordinary-data certificates/rank4.npz \
  --output experiments/new_rank4_certified.npz --workers 4
python verify/verify_roots.py experiments/new_rank4_certified.npz --workers 4
```

Continuation can fail on ill-conditioned paths and can rediscover the same root. A numerical plateau or a large candidate count is not evidence of completeness. The rank-three diagnostic in the report specifically demonstrates this risk.

## File organization

- `report.pdf`, `report.tex`: self-contained mathematical arguments and exact scope.
- `certificates/`: final full-coordinate centers and immutable dyadic data.
- `verify/`: exact checker source, separate Python reference, exact separation, tests, and `CERTIFICATE_FORMAT.md`.
- `src/`: polynomial equations and symbolic denominator/Stein constructions.
- `results/`: successful verification summaries, implementation checks, and selected raw search logs.
- `experiments/`: exploratory continuation and proposal-generation source.
- `sources/REFERENCES.md`: precise primary sources and scope of their use.
- `prior/SP03_verified_partial.zip`: unmodified predecessor archive, including its report and rank-one through rank-three certificates.
- `SHA256SUMS`: integrity manifest. It does not certify mathematical correctness.

No repository files or status were edited. No independent external referee review or proof-assistant formal verification is claimed.
