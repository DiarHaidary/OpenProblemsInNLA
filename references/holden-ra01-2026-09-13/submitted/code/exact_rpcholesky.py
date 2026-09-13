"""Exact finite-state RPCholesky checks using only the Python standard library.

All arithmetic is fractions.Fraction. Inputs must be rational real PSD matrices.
This is a finite-example verifier, not a formal proof of the general theorems.
"""
from __future__ import annotations
from fractions import Fraction as F
from typing import Iterable

Matrix = tuple[tuple[F, ...], ...]


def matrix(rows: Iterable[Iterable[int | F]]) -> Matrix:
    a = tuple(tuple(F(x) for x in row) for row in rows)
    if not a or any(len(row) != len(a) for row in a):
        raise ValueError("Expected a nonempty square matrix.")
    if any(a[i][j] != a[j][i] for i in range(len(a)) for j in range(len(a))):
        raise ValueError("Expected a real symmetric matrix.")
    return a


def trace(a: Matrix) -> F:
    return sum((a[i][i] for i in range(len(a))), F(0))


def diagonal(values: Iterable[int | F]) -> Matrix:
    d = tuple(map(F, values))
    return matrix([[d[i] if i == j else 0 for j in range(len(d))]
                   for i in range(len(d))])


def direct_sum(*blocks: Matrix) -> Matrix:
    n = sum(map(len, blocks))
    a = [[F(0) for _ in range(n)] for _ in range(n)]
    offset = 0
    for block in blocks:
        for i, row in enumerate(block):
            for j, x in enumerate(row):
                a[offset + i][offset + j] = x
        offset += len(block)
    return matrix(a)


def householder_conjugate(values: Iterable[int | F],
                          vector: Iterable[int | F]) -> Matrix:
    """A rational orthogonal conjugate with exactly the supplied eigenvalues."""
    d, v = tuple(map(F, values)), tuple(map(F, vector))
    if len(d) != len(v) or not d or any(x < 0 for x in d):
        raise ValueError("Dimensions must agree and eigenvalues must be nonnegative.")
    vv = sum((x*x for x in v), F(0))
    if vv == 0:
        raise ValueError("Householder vector must be nonzero.")
    n = len(d)
    q = [[F(i == j) - 2*v[i]*v[j]/vv for j in range(n)] for i in range(n)]
    return matrix([[sum((q[i][h]*d[h]*q[j][h] for h in range(n)), F(0))
                    for j in range(n)] for i in range(n)])


def spike(n: int, amplitude: int | F, noise: int | F) -> Matrix:
    if n < 1 or amplitude < 0 or noise < 0:
        raise ValueError("Invalid spike parameters.")
    return matrix([[F(amplitude) + (F(noise) if i == j else F(0))
                    for j in range(n)] for i in range(n)])


def update(a: Matrix, j: int) -> Matrix:
    d = a[j][j]
    if d <= 0:
        raise ValueError("Only strictly positive pivots can be selected.")
    b = matrix([[a[i][h] - a[i][j]*a[j][h]/d for h in range(len(a))]
                for i in range(len(a))])
    assert all(b[i][i] >= 0 for i in range(len(a)))
    assert all(b[i][j] == 0 for i in range(len(a)))
    assert 0 <= trace(b) <= trace(a)
    return b


def exact_expectations(a: Matrix, max_steps: int | None = None) -> list[F]:
    """Enumerate the distribution on selected index sets, with exact probabilities.

    Every transition is an actual rank-one residual update. When two histories
    reach the same index set, their residuals are checked for exact equality.
    Exponential cost: intended for matrices of order roughly eight or less.
    """
    n = len(a)
    steps = n if max_steps is None else max_steps
    if not isinstance(steps, int) or steps < 0:
        raise ValueError("max_steps must be a nonnegative integer.")
    if any(a[i][i] < 0 for i in range(n)):
        raise ValueError("A PSD input cannot have a negative diagonal entry.")
    residuals: dict[int, Matrix] = {0: a}
    probabilities: dict[int, F] = {0: F(1)}
    out = [trace(a)]
    for _ in range(steps):
        nxt: dict[int, F] = {}
        for mask, prob in probabilities.items():
            r = residuals[mask]
            t = trace(r)
            if t == 0:
                assert all(x == 0 for row in r for x in row)
                nxt[mask] = nxt.get(mask, F(0)) + prob
                continue
            assert t > 0
            for j in range(n):
                if r[j][j] == 0:
                    continue
                assert not mask & (1 << j)
                new_mask = mask | (1 << j)
                b = update(r, j)
                if new_mask in residuals:
                    assert residuals[new_mask] == b, "Order independence failed."
                else:
                    residuals[new_mask] = b
                nxt[new_mask] = nxt.get(new_mask, F(0)) + prob*r[j][j]/t
        assert sum(nxt.values(), F(0)) == 1
        probabilities = nxt
        value = sum((p*trace(residuals[m]) for m, p in probabilities.items()), F(0))
        assert F(0) <= value <= out[-1]
        out.append(value)
    return out


def contraction(value: F, tail: F, rank: int) -> F:
    if rank < 1 or value < 0 or tail < 0:
        raise ValueError("Invalid contraction arguments.")
    if value == 0 or value <= tail:
        return value
    return value - (value-tail)**2/(rank*value)


def fraction_record(x: F) -> dict[str, str | float]:
    return {"exact": str(x), "decimal": float(x)}
