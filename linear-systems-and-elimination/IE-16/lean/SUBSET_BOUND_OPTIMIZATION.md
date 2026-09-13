# IE-16 subset-bound implementation statements

These are helper statements for the already independently approved full
IE-16 boundary. They do not change its 15 contracts or constants. Written
and checked mathematically before their proof implementation on 13 September
2026; source-only drafts are not Lean verification evidence.

Put `l = 999/1000`, `q = 13/7500`, and `r = 2603/1500`.
Since `sqrt(3) < 26/15`, the explicit nine points satisfy:

- every point has modulus at least `l`;
- any two points in one cluster have distance at most `q`;
- any two points have distance at most `r`.

For a five-point set `S` excluding zero and `z in S`, its Lagrange
coefficient at zero has absolute value

```
prod (w in S.erase z) |w| / prod (w in S.erase z) |z-w|.
```

All four denominator factors are strictly positive. If `H` is a subset of
`S.erase z`, has cardinality `h`, and all its distances to `z` are at most
`q`, while all distances are at most `r`, the numerator is at least `l^4`
and the denominator is at most `q^h * r^(4-h)`. The cases we use are:

```
109 * q * r^3 < l^4
146 * q^2 * r^2 < l^4.
```

Both inequalities were checked by exact rational arithmetic. Thus a point
with one close companion contributes more than 109, and a point with two
close companions contributes more than 146, to the Lagrange sum.

For any five-element subset of `Fin 3 x Fin 3`, either at least four chosen
points have a companion with the same first coordinate, or at least three
chosen points have two such companions. Indeed, a cluster containing three
points gives the second case; otherwise the occupancies must be 2, 2, 1
in some order and give the first. All subsets are included.

Consequently the Lagrange sum is greater than 436 or greater than 438.
Both exceed `10000/23`, and its positive reciprocal is strictly less than
the approved `23/10000` target. This avoids separate irrational arithmetic
for all 126 five-point subsets; any finite kernel computation is confined
to the nine-label occupancy statement. No floating-point checker is used
as a trusted proof premise.
