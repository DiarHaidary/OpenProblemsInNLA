# The exact remaining mathematical gap

## Unrestricted target

For every `n>=2`, `1<=k<n`, and `0<epsilon<1/2`, RA-14 asks for universal-factor matching bounds for arbitrary adaptive queries to `A` and `A^T`, each individual product charged, with success probability at least 0.99 for every fixed matrix.

Let `s=sqrt(epsilon)`, `x=n/k`, `y=x*s`, and `ell=log(e*x)`. The scales currently supported by this series are

```
F = (k/s) log(1+y),
U = min(n,(k/s) ell).
```

They satisfy

```
U/F = min(y,ell)/log(1+y).
```

The function `y/log(1+y)` increases for positive `y`, while `ell/log(1+y)` decreases. Thus the largest ratio occurs at `y=ell` and equals `ell/log(1+ell)`. This is unbounded as `n/k` grows.

The concrete sequence `k=1`, `epsilon=(log n/n)^2` still has only the interval

```
Omega(n log log n / log n) <= q_sp <= n.
```

Neither endpoint is established as the exact unrestricted scale here.

## What the new restricted theorem does establish

It proves `q_fb=Theta(U)` for the exact class in Definition 2.1. This covers all finite dimensions, ranks, and accuracies, and its output may lie outside the original observed span. Its width is deterministic, every round is fully charged, and no fresh direction or selectively charged update is allowed.

A global `O(F)` method could not remain in this class. That statement is useful, but it does not prove that such a method is impossible outside the class.

## Why the existing lifting does not complete the proof

The primitive lower bound uses a Gaussian block of width `B` and polynomials of degree `d`. Its dimension condition includes

```
2 (8B+1) (d+1) <= n-k.
```

The full-block application takes `B=b+k` and charges `b` products per round, so `B*d` is on the order of the original query budget. A general adaptive-to-Krylov enlargement instead grants many Gaussian starts and many powers. A substitution of sizes `B` around `q+k` and `d` around `q` requires dimension on the order of `q^2`, not `q`. This fails precisely in the near-linear transition.

No same-cost elimination of arbitrary fresh directions is proved. Knowing that an output belongs to a large space is not enough: an independent initial space equal to all of R^n would already contain every possible output before any query, while still not identify the correct one.

## Why the shifted-posterior route does not complete the proof

The posterior and first-exit formulas are exact on their stated domain. They do not give a suitable lower bound for all stopping times. More decisively, Theorem 11.2 supplies an averaged rank-one algorithm on that very shifted law at the smaller rate `F`. At the critical sequence its cost is `o(n)`.

Thus this particular averaged input law cannot witness a linear critical-transition lower bound. Conditioning on a rare hard event would define another law, change the posterior and probabilities, and require new arguments. No such conditioning is silently applied.

## What a completion would need

A completion could establish a stronger all-adaptive lower bound matching `U`, an unrestricted all-input algorithm matching `F`, or another pair of matching bounds between them. The current work supplies none of these alternatives for the remaining transition.

Any proposed bridge must retain all of the following: arbitrary real measurable adaptive queries; both oracle directions; pointwise rather than merely ensemble-average success; the cost of every vector product, including output extraction and postprocessing; simultaneous finite parameters; and universal constants independent of the rank, dimension, and accuracy.

A direct sum of visible hard blocks can be queried in parallel. A block-iteration lower bound cannot simply be multiplied by a chosen width for every algorithm. An exact `n`-column upper cap cannot extend a lower bound outside its proved domain. These are not valid substitutes for the missing theorem.
