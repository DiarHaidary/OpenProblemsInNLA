# IS-02 numerical and logical targets

Source base: `50838e37dd793830e2cecd1055cfc7e0349490f1`.

The canonical target asks whether every spectrally unique real symmetric,
entrywise nonnegative, row-stochastic matrix with positive trace in every
dimension `n ≥ 4` lies in the union of the segment `[I,C_n]` and the two
families of segments from `I` or `C_n` to a vertex of the symmetric
stochastic polytope.

This formalization preserves that universal implication as
`targetNecessaryCondition`. Its negative resolution is witnessed at `n = 4`
by the exact rational matrix

```text
0 1 0 0
1 0 0 0
0 0 1/2 1/2
0 0 1/2 1/2
```

The exported proof must establish all of the following exact obligations:

1. `counterexample` is symmetric, entrywise nonnegative, and every row sums
   to `1`.
2. Its trace is exactly `1` (hence strictly positive).
3. Its characteristic polynomial agrees with the diagonal spectrum
   `{1, 1, 0, -1}`, including multiplicity.
4. Every real symmetric, entrywise nonnegative, row-stochastic `4 × 4`
   matrix with that characteristic polynomial is permutation-similar to the
   displayed matrix. This is the formal spectral-uniqueness statement.
5. The displayed matrix is outside the complete locus, including the direct
   segment `[I,C_4]` and both vertex-indexed segment families. The vertex
   predicate is defined from the original symmetric-stochastic convex set;
   it is not replaced by “permutation matrix”.
6. From (1)--(5), construct `¬ targetNecessaryCondition` by instantiating the
   universal implication at `n = 4` and `counterexample`.

The statement boundary records the exact trace computation separately as
`counterexample_trace`; the positive-trace theorem remains an explicit bridge
to the canonical hypothesis.

The bridge theorem `sameSpectrum_iff_realEigenvalueMultiset_eq` is an explicit
proof obligation. Under the two symmetry hypotheses it must prove that the
characteristic-polynomial encoding is exactly equality of the real eigenvalue
root multisets, with algebraic multiplicity retained. No informal appeal to
“same spectrum” is allowed to replace this bridge.

The characteristic-polynomial definition is equivalent to equality of real
symmetric spectra with multiplicities, while avoiding an arbitrary ordering
of eigenvalue lists. The proof must not assume a classification theorem as an
axiom; the component/bipartite argument from the submitted manuscript must be
formalized or imported only from a separately verified dependency.
