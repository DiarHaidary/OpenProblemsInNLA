# RA-18: complex counterexample and structured real results

**Author:** Sidney Holden, Center for Computational Biology, Flatiron Institute, Simons Foundation. [Affiliation and submission provenance](SUBMISSION.md).

**This is not a full solution of the unrestricted real GTZ conjecture.** The package contains a complete explicit proof refuting the *separate proposed complex extension*, together with a real theorem for a restricted class of frames. The main manuscript is `manuscript/ra18.pdf` (attributed repository edition), with editable LaTeX source alongside it.

## Main result

There is an explicit sequence of complex isometries

\[
U_k\in\mathbb C^{(2\cdot3^k)\times3^k},\qquad U_k^*U_k=I,
\]

such that **every** nonsingular square row submatrix satisfies

\[
\|U_{k,I}^{-1}\|_2^2\ge\frac{3\cdot4^k+1}{2}.
\]

Every row has squared norm 1/2. Consequently,

\[
\frac{t_{\mathbb C}(3^k,2\cdot3^k)}{\sqrt{2\cdot3^k}}
\ge\sqrt{\frac{3\cdot4^k+1}{4\cdot3^k}}\longrightarrow\infty.
\]

**No constant independent of both dimensions can satisfy the proposed complex bound.** This is stronger than finding a counterexample to the constant one or to the known two-column constant.

The construction starts with `U_0 = (1,1)^T/sqrt(2)` and iterates

\[
\mathcal T(U)=[U\otimes a\quad I_n\otimes c],\qquad
 a=(1,1,1)^T/\sqrt3,\quad c=(1,\omega,\omega^2)^T/\sqrt3,
\quad \omega=e^{2\pi i/3}.
\]

The proof classifies **all** nonsingular row selections and establishes the squared-norm inequality

\[
b(\mathcal T(U))\ge4b(U)-3/2,\qquad
b(U)=\min_{\det U_I\ne0}\|U_I^{-1}\|_2^2.
\]

No numerical optimization is needed for this proof.

## Additional conclusions

The manuscript gives the exact common singular spectrum of all bases of a fixed `U_k`, not just an inequality. The exact minimum squared singular value obeys `g_0=1/2` and

\[
R(g_{k+1})=g_k,\qquad
R(x)=\frac{x(2-3x)^2}{1-3x+3x^2},\quad 0\le x\le1/3.
\]

The function `R` is strictly increasing on this interval. The number of nonsingular bases is exactly `2*3**(3**k-1)`. For every `r,n`, the construction and elementary operations also give

\[
t_{\mathbb C}(r,n)\ge\sqrt{3/32}\,\sqrt n\,
\min(r,n-r)^{\log_3 2-1/2}.
\]

This is a lower bound, **not** a claimed optimal complex growth rate.

For the real field, a weighted-complement equivalence transfers the established real two-column theorem to any Parseval frame with at most `r+2` distinct nonzero row directions. The sharp bound `sqrt(n)` is proved for that class. The manuscript also provides an unequal-multiplicity simplex equality example for every `1 <= r < n`.

## Contents

| File | Purpose |
|---|---|
| `manuscript/ra18.pdf` | Full theorem statements, proofs, scope, and references |
| `manuscript/ra18.tex` | Editable LaTeX source |
| `code/ra18.py` | Construction, exact combinatorial basis classification, scalar recurrence, real-class selector |
| `code/verify.py` | Reproducible symbolic, exhaustive numerical, sampled, and rational-interval checks |
| `results/verification.json` | Recorded detailed test results and exact rational limit enclosure |
| `results/recurrence.csv` and `.json` | 80-digit scalar values through level 12 |
| `results/run.log` | Full output from the recorded verification run |
| `AUDIT.md` | Proof obligations, potential confusions, and verification limits |
| `REPOSITORY_NOTE.md` | Proposed scope-aware repository update; no update was applied |
| `SOURCES.md` | Public source inventory, versions, and access notes |
| `requirements.txt` | Exact package versions used |
| `build_pdf.sh` | Rebuild the PDF with a local LaTeX installation |
| `MANIFEST.sha256` | Integrity hashes of package files, excluding the manifest itself |

## Reproduce the checks

The recorded run used Python 3.13.5. A virtual environment is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python code/verify.py
```

On Windows, activate the virtual environment using `.venv\Scripts\activate` instead. The verification script writes into `results/` by default. To keep the recorded results untouched, use:

```bash
python code/verify.py --out-dir fresh_results
```

The default run includes every square selection of the `18 x 9` matrix: 48,620 subsets, of which 13,122 are nonsingular and 35,498 singular. The exact structural classification and numerical classification agree on all of them. All 20 square selections of the `6 x 3` matrix are checked symbolically. Additional checks include 500 random lifted bases, 200 sampled level-three bases, 80 grouped real instances, and 1,212 weighted-duality equivalences. **The level-three check is not exhaustive.**

The asymptotic limit `L = lim 4**k * g_k` is enclosed using exact rational bisection and a proved tail bound, not decimal extrapolation:

```
0.5097420164997750708232846364 < L
L < 0.5097420164997750708232846733
```

For direct use:

```python
import sys
sys.path.insert(0, "code")
from ra18 import family, scalar_recurrence

U2 = family(2)              # The explicit 18-by-9 counterexample
rows = scalar_recurrence(12, digits=80)  # No large matrices needed
print(U2.shape)
print(rows[2]["best_inverse_norm"])
```

The dense constructor and exhaustive enumerator have safety limits to avoid accidental large allocations. Use the scalar recurrence for large levels.

## Scope and review status

The counterexample proof is self-contained. The structured real theorem invokes the stated real rank-two preprint; the general real conjecture is not proved or refuted. The manuscript also explains why realification of the complex construction is not a real counterexample.

The package is a proof submission with reproducible checks. See the separate [independent informal AI-agent review](independent-review.md) for the repository audit. This is not external human peer review or a proof-assistant formalization. No exhaustive novelty claim is made for every auxiliary lemma or special-case construction. The original package was supplied without repository changes; this repository edition adds authorship, verified affiliation, and review evidence. Only original write-up, code, and output files are included; third-party papers are referenced rather than redistributed.
