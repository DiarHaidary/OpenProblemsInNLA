"""Exact polynomial construction used by the backward-convergence proof."""
from __future__ import annotations
from fractions import Fraction as Q


def add(a: list[Q], b: list[Q]) -> list[Q]:
    out = [Q(0)]*max(len(a), len(b))
    for i, x in enumerate(a):
        out[i] += x
    for i, x in enumerate(b):
        out[i] += x
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def scale(a: list[Q], s: Q) -> list[Q]:
    return [Q(s)*x for x in a]


def multiply(a: list[Q], b: list[Q]) -> list[Q]:
    out = [Q(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out


def evaluate(a: list[Q], x: Q) -> Q:
    value = Q(0)
    for coefficient in reversed(a):
        value = value*x + coefficient
    return value


def shifted_chebyshev(degree: int) -> list[Q]:
    """Coefficients of T_degree(2x-1), in increasing power order."""
    if degree < 0:
        raise ValueError("degree must be nonnegative")
    if degree == 0:
        return [Q(1)]
    previous, current = [Q(1)], [Q(-1), Q(2)]
    for _ in range(1, degree):
        previous, current = current, add(
            multiply([Q(-2), Q(4)], current), scale(previous, -1))
    return current


def reciprocal_polynomial(k: int) -> tuple[int, list[Q]]:
    """The cited degree < k reciprocal-approximation polynomial.

    ell is the even member of {k,k+1};
    G=(1-T_ell(2x-1))/(2*ell^2), pi=(x-G)/x^2.
    The universal bound is a cited analytic result, not established by
    this construction routine or by finite-grid tests.
    """
    if k < 2:
        raise ValueError("k must be at least two")
    ell = k if k % 2 == 0 else k+1
    T = shifted_chebyshev(ell)
    G = scale(add([Q(1)], scale(T, -1)), Q(1, 2*ell*ell))
    numerator = add([Q(0), Q(1)], scale(G, -1))
    if numerator[0] != 0 or numerator[1] != 0:
        raise ArithmeticError("double-root identity failed")
    return ell, numerator[2:]
