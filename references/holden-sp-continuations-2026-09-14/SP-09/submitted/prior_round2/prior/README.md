# SP-09: exact certificates and partial results

**Status: PARTIAL. This package does not prove or disprove SP-09 for arbitrary normal matrices.**

The main result is an exact, all-amplifications theorem for the three-point Krause example. Both spectra have three distinct eigenvalues, and their optimal unitary-orbit distance is strictly smaller than their bottleneck eigenvalue-matching distance. The result therefore goes beyond the supplied two-eigenvalue special case without assuming the false general identity between these two distances.

For

\[
A=\operatorname{diag}\left(1,\frac{4+5i\sqrt3}{13},\frac{-1+2i\sqrt3}{13}\right),\qquad B=-A,
\]

the exact conclusion is

\[
\delta_{3k}(A\otimes I_k,-A\otimes I_k)=\sqrt{27/13}
<\sqrt{28/13}=d_\infty(A\otimes I_k,-A\otimes I_k)
\quad(k\ge1).
\]

The proof also characterizes every equality-attaining unitary: up to unitaries commuting with the spectral projections of A, it is the explicit three-dimensional Householder reflection tensored with I_k. The manuscript gives the proof, additional geometric cases, amplification-independent lower bounds, and the exact remaining gap.

## Read and verify

Start with `SP09_writeup.pdf`. Its editable source is `manuscript/SP09_writeup.tex`.

From the package root:

```bash
python -m pip install -r requirements.txt
python -O certificate/verify_certificate.py --json-report verification/local_certificate_check.json
python -O certificate/verify_witness_and_rigidity.py --json-report verification/local_witness_check.json
```

Python 3.10 or newer is recommended. The acceptance checks remain active under `python -O`. The first program verifies a universal cyclic trace identity and positive-definiteness certificates using arbitrary-precision integers. The second checks the exact upper-bound witness, all six spectral matchings, and the algebraic relation kernel needed for equality rigidity. No numerical eigensolver or optimization tolerance is used to accept the main certificate.

`certificate/krause_certificate.json` is part of the proof, not optional experimental data. It encodes matrices over Q(s), where s = i sqrt(3). The manuscript and `certificate/FORMAT.md` specify their meaning.

## Optional reconstruction

The certificate was discovered numerically and then reconstructed and checked exactly. Discovery is not used as a substitute for verification. To repeat the complete construction:

```bash
python -m pip install -r reconstruction/requirements.txt
python reconstruction/rebuild.py --work-dir reconstruction_work
```

This runs the numerical semidefinite feasibility search, constructs exact sparse kernel bases, corrects rationalized matrices to satisfy all linear identities, and finally invokes both exact verifiers. Different numerical stacks may produce a different valid certificate. An unsuccessful reconstruction would not invalidate the supplied certificate; its exact verifier is the acceptance criterion.

## Other contents

`verification/` contains the recorded exact checks, a successful reconstruction log, and a summary of the saved exploratory search. `experiments/` contains the code and data for 60 joint spectrum/unitary searches with base size 4 and amplification 2. No candidate improvement larger than 1e-6 was found; this is not a universal proof or a certified comparison of global minima.

`STATUS.md` separates established conclusions from unresolved claims. `SOURCES.md` records the public sources consulted. `SHA256SUMS.txt` records hashes for integrity checking with `sha256sum -c SHA256SUMS.txt`.

No repository files were changed. No claim of independent peer review, formal proof-assistant verification, or priority over the literature is made.
