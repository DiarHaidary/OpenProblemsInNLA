# Primary sources and their roles

Checked through ordinary web access on September 13, 2026. No GitHub
plugin was used. These sources supply the problem or stated background;
they do not independently certify the manuscript's new arguments.

## 1. IE-20 specification

OpenProblemsInNLA, **IE-20: Precision required for conjugate gradients to
attain backward accuracy in n steps**.

Repository:
https://github.com/ajt60gaibb/OpenProblemsInNLA/tree/main/linear-systems-and-elimination/IE-20

Readable source:
https://raw.githubusercontent.com/ajt60gaibb/OpenProblemsInNLA/main/linear-systems-and-elimination/IE-20/README.md

Role: target, arithmetic envelope, input restrictions, operation order,
stopping convention, true-residual criterion, and all-greater-precision
quantifier. These detailed conventions are the repository's editorial
specialization. Its status label is not the reason this package is partial;
the manuscript's unmatched bounds are.

## 2. Exact reciprocal-polynomial approximation

Michał Dereziński, Yuji Nakatsukasa, and Elizaveta Rebrova,
**Towards Universal Convergence of Backward Error in Linear System Solvers**,
arXiv:2604.16075v2, May 22, 2026.

https://arxiv.org/abs/2604.16075v2
https://arxiv.org/html/2604.16075v2

Role: Lemmas 12–13 supply the positive reciprocal-polynomial inequality
used in the universal-horizon branch. The manuscript proves its own
transfer to computed CG spans. The external exact-arithmetic result is
not treated as a finite-precision CG guarantee.

## 3. Finite-precision PCG accuracy at a sufficiently late iterate

Thomas Bake, Erin Carson, and Yuxin Ma,
**Forward and backward error bounds for a mixed precision preconditioned
conjugate gradient algorithm**, arXiv:2510.11379v3, July 21, 2026.

https://arxiv.org/abs/2510.11379v3
https://arxiv.org/html/2510.11379v3

Role: scope comparison. Lemma 6 and Theorem 2 concern a sufficiently late
iteration with additional smallness conditions; they do not bound that
iteration by n. No full solution is inferred from their accuracy result.

## 4. A recent implementation-sensitive Krylov analysis

Mohit Sinha, **Finite-Precision Symmetric Krylov Methods: Exact Rounding
Examples, Block Paige Identities, and a Variable-Block Lanczos Model**,
arXiv:2609.08066v1, September 8, 2026.

https://arxiv.org/abs/2609.08066v1
https://arxiv.org/html/2609.08066v1

Role: scope comparison. Section 5 gives a sufficient precision for a
specified computation with independently recomputed residual tests, plus
a conditioning obstruction, while retaining a quantitative gap. Its
polynomial discussion is not used as an execution-level lower bound here.

## 5. Prior work supplied in the conversation

`prior/IE20_recovered.zip` preserves the earlier partial manuscript,
source notes, exact code, witness reports, and recovery provenance. The
new Section 9 refers to its Section 5 for the path/outlier asymptotic
proof. The preserved archive's earlier source list is not a replacement
for the source checks above.

This is a bounded literature check, not a claim to have exhaustively
searched all publications or established priority.
