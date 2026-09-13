# RA-11: partial mathematical results and reproducible checks

**This package is not a complete solution of RA-11.** The requested general
minimax characterization has not been established here. The manuscript gives
proofs of a matched tensor-product subclass result, an explicit counterexample
to a conjecture in a cited paper, and general upper and lower bounds that do not
match throughout the parameter range.

Prepared on 13 September 2026. These are internally checked research arguments,
not independently refereed results. No claim of formal theorem-prover
verification or of an exhaustive novelty/priority search is made.

## Start here

Read `manuscript/ra11_partial_results.pdf` (18 pages). The complete editable
LaTeX source is alongside it. `STATUS.md` separates the established arguments
from the unresolved target and identifies the delicate proof obligations.

The exact problem is trace estimation of **arbitrary** real PSD matrices of
order `N = n**q`, with adaptive, exact, real product-vector queries returning the
**entire vector** `M(v1 ⊗ ... ⊗ vq)`. A tensor structure on the allowed queries
is not a tensor-product promise on the unknown matrix. Success is relative
error epsilon with probability at least 2/3 on every fixed input.

## Results in the manuscript

1. **Complex-to-real simulation.** A complex product query is simulated with
   `q+1` real product queries by polynomial interpolation. This uses exact
   arithmetic and may be ill-conditioned.

2. **Counterexample to Conjecture 23 of arXiv:2502.08029v2.** For `n=2`, the
   span of `(e1+t_j e2)^{⊗q}` at `q+1` distinct real nodes has squared projection
   at least `2^{1-q}` on every real unit product vector. This contradicts the
   conjectured universal exponentially smaller projection scale, not the
   conditioned theorems in that paper and not RA-11 itself. An explicitly
   normalized spanning family has squared condition number
   `binomial(q, floor(q/2))`.

3. **Matched tensor-product subclass.** Under the additional promise
   `M = A1 ⊗ ... ⊗ Aq` with PSD `n × n` factors,

   `Q_product(n,q,epsilon) = Theta(min(n, sqrt(q)/epsilon))`.

   A reference normalization and a shift of each local target vector provide
   one parallel round of all local matrix-vector products per original call.
   Exact factor recovery takes `n` calls total, and `n` is optimal when exact
   trace recovery is required. Independent unbiased local
   Hutch++ estimators give the approximate upper bound. An adaptive Wishart
   posterior plus log-concave anti-concentration gives the lower bound under
   the required bounded-probability criterion, not just an RMSE criterion.

4. **General RA-11 bounds.** Define

   `L = max_{1<=b<=q} min(n**b, sqrt(floor(q/b))/epsilon)`.

   Then `Q >= L/80000`. A proved upper bound is the minimum of

   - `n**q`;
   - `ceil(3*((3*n/(n+2))**q - 1)/epsilon**2)`;
   - `(q+1)*ceil(3*((2*n/(n+1))**q - 1)/epsilon**2)`;
   - `n**(q-1)*(5*ceil(4/epsilon)+4)`.

   These establish `Q = Theta(n**q)` when `epsilon <= n**(-q)`, but leave a
   substantial gap in general.

5. **Low-rank PSD recovery.** A known rank bound `r` allows exact Nyström
   reconstruction from `r` independent generic real product queries almost
   surely. In particular, rank-one PSD trace is obtained from one full-vector
   response. The one-query rank-one observation is also in Meyer–Avron.

## Reproduce the checks

Python 3.10 or newer is recommended. Install NumPy and SymPy, then run from
this directory:

```bash
python -m pip install -r requirements.txt
python tests/exact_checks.py
OPENBLAS_NUM_THREADS=1 python tests/numerical_checks.py
```

The scripts write JSON records to `results/`. The reference run used Python
3.13.5, NumPy 2.3.5, and SymPy 1.14.0. The numerical seed is 20260913.

The exact tests use rational or Gaussian-rational arithmetic. The numerical
checks include interpolation, query counts, product recovery, complex partial-
trace second moments, and moments of an adaptively exposed Wishart residual.
They are finite checks, not proofs of the general theorems. In particular,
matching residual moments and low empirical correlation do not establish
conditional independence.

Rebuild the PDF with a TeX distribution containing `pdflatex` and the standard
packages listed in the source:

```bash
./build.sh
```

No network access is needed to run the tests or rebuild the PDF once the
software dependencies are installed.

## Code map

`src/ra11.py` provides a real-only product-oracle wrapper, complex-query
interpolation, complex-sphere trace estimation, normalized parallel factor
access, exact product recovery, parallel local Hutch++ estimation, partial
traces, and the displayed bound functions. The tensor-product access class
**does not verify the product promise**; using it on a general PSD matrix is
not justified. `DenseProductOracle` likewise does not certify that its input
matrix is PSD; that is an input promise.

These routines are small-instance floating-point reference implementations.
They do not implement a stable large-q algorithm, do not prevent tensor-size
explosion, and do not remove conditioning, overflow, or underflow issues.
The paper's query bounds are statements in exact arithmetic only. The bound
utility uses ordinary floating-point exponentiation and is intended for modest
parameters; the symbolic definitions in the manuscript cover all parameters.

## Files

- `manuscript/`: the PDF and full LaTeX source.
- `src/`: reference implementations.
- `tests/`: exact and numerical checks.
- `results/`: recorded outputs, environment information, and PDF validation.
- `SOURCE_NOTES.md`: primary sources and the precise limitations of the source results.
- `STATUS.md`: scope, proof audit, and remaining gap.
- `MANIFEST.sha256`: hashes of all other package files.

No repository files have been changed and no claim of a completed solution has
been submitted anywhere. See `SOURCE_NOTES.md` for the public source URLs.
