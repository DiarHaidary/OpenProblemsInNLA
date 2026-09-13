# IS-02 source correspondence

All source bytes below are pinned to commit
`50838e37dd793830e2cecd1055cfc7e0349490f1` of
`ajt60gaibb/OpenProblemsInNLA`.

| role | repository path | git blob | SHA-256 of `git show` bytes |
|---|---|---|---|
| canonical problem | `eigenvalues-and-inverse-problems/IS-02/README.md` | `6af05f8ffac99a75c248a3f098d90105378cc37e` | `92f7c04c5ac0be67a7f6a4efd0d2439caaf000295fa27d259e01a22368f7ae24` |
| complete mathematical solution | `eigenvalues-and-inverse-problems/IS-02/solution.md` | `508d844c6ff1466777d4666b0ff6e8152cf994df` | `ae29570308b2a78678875c5e56076ce09e65cea732ce6b51142399a4b234577f` |
| canonical TeX | `eigenvalues-and-inverse-problems/IS-02/problem.tex` | `66aefc851e82b70f0d8cc705cb9c9f4ae3769444` | `3298c8d66c330f792d0e34edac88631f67d9e3e3292ab2b677cdd73ad8d74537` |
| solution TeX | `eigenvalues-and-inverse-problems/IS-02/solution.tex` | `9ffc49701f64b0f03da57eff6a4e0577fb6a371e` | `151d4cbf469629da34454d0b68e274403d292bf5566fe9a59e4c545716328f03` |

Original mathematical author: Matthew J. Colbrook, Department of Applied
Mathematics and Theoretical Physics, University of Cambridge. Formalization
author: George Stepaniants, Department of Computing and Mathematical Sciences,
California Institute of Technology, Pasadena, California, USA. No email is
included for George.

## Reproducible source check

From a checkout containing the pinned commit, recheck the source bytes and Git
blob IDs directly:

```sh
base=50838e37dd793830e2cecd1055cfc7e0349490f1
git show "${base}:eigenvalues-and-inverse-problems/IS-02/README.md" | shasum -a 256
git show "${base}:eigenvalues-and-inverse-problems/IS-02/solution.md" | shasum -a 256
git rev-parse "${base}:eigenvalues-and-inverse-problems/IS-02/README.md"
git rev-parse "${base}:eigenvalues-and-inverse-problems/IS-02/solution.md"
```

The first two outputs must equal the SHA-256 values in the table, and the last
two must equal its Git blob IDs. The TeX rows can be checked with the same
commands and their paths from the table.
