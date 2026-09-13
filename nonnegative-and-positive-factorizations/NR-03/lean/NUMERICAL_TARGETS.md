# NR-03: full target and exact finite certificate

Statement preparation, 13 September 2026. No Lean proof implementation
before the completed definitions and contracts receive two independent
statement approvals. Canonical source base:
`50838e37dd793830e2cecd1055cfc7e0349490f1`.

For each `n >= 3`, the original matrix is indexed by all Boolean vectors
of length `n` and has every real entry fixed by

```
C_n(a,b) = (1 - sum_i (a_i as Real) * (b_i as Real))^2.
```

Equivalently use all subsets of `Fin n` and intersection cardinality,
with an explicit correspondence to Boolean vectors. The subtraction
inside the square must be over the integers or reals, never truncated
natural subtraction: entries with intersection cardinality greater than
one are essential parts of the prescribed matrix.

Nonnegative rank is the actual minimum width of a factorization `X = W H`
over real entrywise nonnegative matrices. A formal encoding by a natural
infimum/minimum must include its attained-minimum and minimality semantics
for nonnegative input matrices. No restricted support, rational-only
minimum or rank proxy may replace this definition. Rational witness
factors are nevertheless admissible real factors.

The complete negative resolution needs the following obligations:

1. Retain the original universal target `forall n >= 3, rank_+(C_n) = 2^n`.
2. Define every entry of `C_7` on all 128 Boolean/subset indices.
3. Give nonnegative integer matrices `W : 128 by 127` and
   `V : 127 by 128`, and 128 strictly positive integer denominators `d_b`.
4. Prove, for every pair of indices, the exact identity
   `sum_k W[a,k] V[k,b] = d_b (1 - |a intersect b|)^2`.
5. Define the genuine real right factor by `H[k,b] = V[k,b] / d_b`.
   Prove every entry is nonnegative and `W H = C_7` over the reals.
6. Deduce `rank_+(C_7) <= 127 < 128` from the actual minimum definition.
7. Instantiate the original universal assertion at `n = 7` to prove its
   negation. No hypothesis that assumes the factorization, rank bound,
   certificate correctness or negated conclusion is permitted.

All data are available in the exact retained certificate
`references/holden-nr03-2026-09-13/data/factors_n7.json`, SHA-256
`fa515775f9c77e5dfe85109125d3f730c4b36684894730096247cd67fcc60bb9`.
Rows and columns use masks `0,...,127`; bit `i` denotes coordinate `i`.
The 127 atom indices are 64 complementary pairs, seven singletons,
21 pairs and 35 four-element sets. Denominators are in
`{1,4,9,16,25,36}`; `W` entries are at most two, and `V` entries at most 36.
The full TeX proof is
`references/holden-nr03-2026-09-13/NR03_counterexample.tex`, SHA-256
`26cac3ed5aa30226530bbf8562a626b6582444abcc8ef8e8e69ebde6160565a3`.

Optimize computation without discarding any matrix entries. Sparse `W`
has 2,648 nonzero entries, reducing a complete integer check to 338,944
multiply-adds. Alternatively, the four explicitly defined atom families
reduce the identity to intersection-cardinality counting and one exact
polynomial identity. Choose the method with the smallest transparent
kernel proof after checking the pinned Mathlib APIs. No numerical interval
subdivision or floating-point arithmetic is needed. A Python checker or
generated data file is a source of a proposed certificate, not a trusted
proof oracle; Lean must establish the full identities and semantics.

The source additionally proves a general-n upper bound and strictness for
every n >= 7. A single allowed-dimension counterexample already refutes
the complete original universal target, so those stronger statements,
the exact value of rank_+(C_7), and the smallest counterexample dimension
are not extra claimed formalizations.

Original mathematical proof: Sidney Holden, Center for Computational
Biology, Flatiron Institute, Simons Foundation. Preserve the historical
partial-result credit to Matthew J. Colbrook in the canonical page.
Formalization author: George Stepaniants, Department of Computing and
Mathematical Sciences, California Institute of Technology, Pasadena,
California, USA; no George email. Substantial AI assistance is disclosed.

Use the pinned LeanCert kernel workflow, the Schiffer/Forsythe structural
examples, two independent statement reviews, two independent final reviews
under the repository's Tau Ceti adaptation, actual Linux Comparator and
default-kernel/standard-axiom checks, and truthful formalization.yaml.
One complete canonical counterexample counts as one verified problem;
certificate helper exports do not increase the campaign count.
