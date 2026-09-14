# Provenance

## Public sources checked

**Open Problems in Numerical Linear Algebra — SP-07.** The canonical public
statement was read directly from the website. It requires a single sharp
all-dimension normal-matrix matching constant and matching sharpness evidence.
The page currently describes the target as open and distinguishes supporting
subclass results from a full solution.

https://raw.githubusercontent.com/ajt60gaibb/OpenProblemsInNLA/main/eigenvalues-and-inverse-problems/SP-07/README.md

**Qiyue Tang — A Truncated Singular-Value Bound for Spectral Variation of Normal
Matrices, arXiv:2609.09177v1.** The HTML was read, and the PDF introduction was
visually checked. Its reported bound C_normal < 2.9038872828 is used as a literature
baseline. The paper's lower baseline is not substituted for the stronger inherited
finite certificate. The auxiliary Fourier extremal problem is not identified with
the matrix constant.

https://arxiv.org/html/2609.09177v1
https://arxiv.org/pdf/2609.09177v1

**Repository contribution/status guidance.** The public guidance was read to
maintain the distinction between partial results and independently audited full
solutions. Nothing was written to the repository.

https://raw.githubusercontent.com/ajt60gaibb/OpenProblemsInNLA/main/CONTRIBUTING.md

## Conversation-provided work

`prior/SP-07_round4_sharp_subclass.zip` is a byte-for-byte copy of the round-4 ZIP
supplied in this conversation. Its report contains the sharp rank-one-reflection
proof and the fixed-reflection-rank finite-order reduction. Earlier continuations,
including the rational n=193 certificate, remain nested in this unchanged archive.
Their general proofs are attributed to those reports; no external review is
inferred from successful arithmetic rechecks.

The file `research/inputs/n193_prior_search_candidate.npz` is copied unchanged
from the nested round-3 archive at
`SP-07_round3_bundle/results/chart_reset/chain193_best.npz`. It is a floating-point
search candidate used only for the numerical bulk fit. It is not the rational
certificate. Its hash is recorded both in the fit output and the provenance hash
file.

## New work and limitations

The polygon completion, orbit-dilation, and stationary-model arguments are proved
in the new report. Exact programs supplement the proofs. Numerical regressions,
ODE integration, coefficient comparisons, and local optimizers are diagnostics
only. The rational model integral is certified at the chosen parameter pair; no
parameter-global maximum, finite normal-matrix transfer, or unrestricted sharp
upper bound is certified.

The literature check is bounded and does not establish historical priority. No
external human referee report or proof-assistant verification is claimed. Logs
record actual local executions; source versions and file hashes accompany them.
