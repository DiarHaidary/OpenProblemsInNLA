"""IE-28: constructive two/three-stage results and numerical diagnostics.

The three-stage existence proof is in writeup.pdf.  Returned decimals are
approximations, not interval certificates.  No all-stage solver is claimed.
Inputs should be strings, integers, Fractions, or mp.mpf for full precision.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import comb, factorial
from typing import Any, Iterable, Sequence
import mpmath as mp


def as_mpf(x: Any) -> mp.mpf:
    """Convert without silently replacing decimal strings by binary floats."""
    if hasattr(x, "numerator") and hasattr(x, "denominator") and not isinstance(x, (str, float)):
        return mp.mpf(int(x.numerator)) / int(x.denominator)
    return mp.mpf(x)


def nodes(values: Iterable[Any]) -> list[mp.mpf]:
    c = [as_mpf(v) for v in values]
    if len(c) < 2:
        raise ValueError("At least two nodes are required.")
    if any(not mp.isfinite(v) or v <= 0 for v in c):
        raise ValueError("All nodes must be finite and strictly positive.")
    if any(a >= b for a, b in zip(c, c[1:])):
        raise ValueError("Nodes must be strictly increasing and distinct.")
    return c


def inverse_similar(values: Iterable[Any]) -> mp.matrix:
    """M = S^{-1} A^{-1} S; S_ii = c_i / barycentric_weight_i."""
    c = nodes(values)
    n = len(c)
    M = mp.matrix(n)
    for i in range(n):
        for j in range(n):
            M[i, j] = (1 / (c[i] - c[j]) if i != j else
                       1 / c[i] + mp.fsum(1 / (c[i] - c[k]) for k in range(n) if k != i))
    return M


def collocation_matrix(values: Iterable[Any]) -> mp.matrix:
    """A = C V diag(1, 1/2, ..., 1/n) V^{-1}."""
    c = nodes(values)
    n = len(c)
    V = mp.matrix([[t ** k for k in range(n)] for t in c])
    return mp.diag(c) * V * mp.diag([mp.mpf(1) / k for k in range(1, n + 1)]) * V ** -1


def determinant_coefficients(B: mp.matrix) -> list[mp.mpf]:
    """[e_0,...,e_n], in ASCENDING order: det(I+t B)=sum e_k t^k.

    Faddeev--LeVerrier; cancellation can be severe. Increase working precision
    for clustered nodes or large n. This is not a validated-arithmetic routine.
    """
    if B.rows != B.cols:
        raise ValueError("A square matrix is required.")
    n = B.rows
    P = mp.eye(n)
    es = [mp.mpf(1)]
    for k in range(1, n + 1):
        LP = B * P
        e = mp.fsum(LP[i, i] for i in range(n)) / k
        es.append(e)
        P = e * mp.eye(n) - LP
    return es


def matrix_inf_norm(B: mp.matrix) -> mp.mpf:
    return max(mp.fsum(abs(B[i, j]) for j in range(B.cols)) for i in range(B.rows))


def diagnostics(values: Iterable[Any], diagonal: Sequence[Any]) -> dict[str, Any]:
    c = nodes(values)
    d = [as_mpf(v) for v in diagonal]
    n = len(c)
    if len(d) != n or any(not mp.isfinite(v) or v <= 0 for v in d):
        raise ValueError("The diagonal must contain one positive finite entry per node.")
    A = collocation_matrix(c)
    D = mp.diag(d)
    M = inverse_similar(c)
    L = M * D
    es = determinant_coefficients(L)
    N = mp.eye(n) - D ** -1 * A
    Nn = N ** n
    return {
        "coefficient_error": max(abs(es[k] / comb(n, k) - 1) for k in range(1, n + 1)),
        "determinant_error": abs(factorial(n) * mp.fprod(d[i] / c[i] for i in range(n)) - 1),
        "nilpotency_power_norm": matrix_inf_norm(Nn),
        "nilpotency_power_relative": matrix_inf_norm(Nn) / max(mp.mpf(1), matrix_inf_norm(N) ** n),
        "characteristic_coefficients": es,
        "positive": all(v > 0 for v in d),
        "ordered": all(a < b for a, b in zip(d, d[1:])),
        "inside_ansatz_box": all(c[i] / n < d[i] < c[i] for i in range(n)),
    }


def solve_two(values: Iterable[Any], dps: int = 80) -> list[mp.mpf]:
    if dps < 30:
        raise ValueError("Use at least 30 decimal digits.")
    with mp.workdps(dps + 25):
        c = nodes(values)
        if len(c) != 2:
            raise ValueError("solve_two requires exactly two nodes.")
        r = mp.sqrt(2 * c[0] * c[1])
        return [t * (t + r) / (2 * t + r) for t in c]


def three_diagonal(c: Sequence[mp.mpf], r: mp.mpf, theta: mp.mpf) -> list[mp.mpf]:
    """p(t)=t(t+r)(theta*t+r), d_i=p(c_i)/p'(c_i)."""
    return [1 / (1 / t + 1 / (t + r) + theta / (theta * t + r)) for t in c]


def three_trace(c: Sequence[mp.mpf], r: mp.mpf, theta: mp.mpf) -> mp.mpf:
    """Stable pairwise trace formula, with no division by node differences.

    For f(t)=t(a*t^2+b*t+g)/(3*a*t^2+2*b*t+g), the positive
    polynomial H(x,y) below is its exact divided-difference numerator.
    """
    a, b, g = theta, (1 + theta) * r, r * r
    den = [3 * a * t * t + 2 * b * t + g for t in c]
    d = three_diagonal(c, r, theta)
    T = mp.fsum(d[i] / c[i] for i in range(3))
    for i in range(3):
        x = c[i]
        for j in range(i + 1, 3):
            y = c[j]
            H = (3 * a * a * x * x * y * y + 2 * a * b * x * y * (x + y)
                 + a * g * (x * x + y * y) + 2 * (b * b - a * g) * x * y
                 + b * g * (x + y) + g * g)
            T += H / (den[i] * den[j])
    return T


def _three_radius(c: Sequence[mp.mpf], theta: mp.mpf, tol: mp.mpf,
                  maxiter: int = 2500) -> mp.mpf:
    """Unique positive r with det(MD)=1, using safeguarded Newton."""
    lo, hi = mp.mpf(0), 4 * c[-1]
    x = c[1]
    for _ in range(maxiter):
        us = [1 + t / (t + x) + theta * t / (theta * t + x) for t in c]
        f = mp.log(6) - mp.fsum(mp.log(u) for u in us)
        if abs(f) < tol:
            return x
        if f < 0:
            lo = x
        else:
            hi = x
        deriv = mp.fsum((t / (t + x) ** 2 + theta * t / (theta * t + x) ** 2) / u
                        for t, u in zip(c, us))
        proposal = x - f / deriv
        if not lo < proposal < hi or not mp.isfinite(proposal):
            proposal = (lo + hi) / 2
        if proposal == x:
            raise ArithmeticError("Working precision exhausted while normalizing determinant.")
        x = proposal
    raise ArithmeticError("Determinant normalization did not converge; raise maxiter or precision.")


@dataclass
class ThreeSolution:
    diagonal: list[mp.mpf]
    theta: mp.mpf
    radius: mp.mpf
    endpoint_traces_minus_three: tuple[mp.mpf, mp.mpf]
    trace_residual: mp.mpf
    iterations: int


def solve_three(values: Iterable[Any], dps: int = 80) -> ThreeSolution:
    """Provably bracketed scalar construction for every positive node triple.

    The proof guarantees a zero; this finite-precision implementation returns
    an approximation after checking determinant and trace residuals.
    """
    if dps < 30:
        raise ValueError("Use at least 30 decimal digits.")
    with mp.workdps(dps + 30):
        c = nodes(values)
        if len(c) != 3:
            raise ValueError("solve_three requires exactly three nodes.")
        scale = c[-1]
        z = [v / scale for v in c]
        tol = mp.power(10, -dps)
        inner_tol = tol * mp.mpf("1e-12")
        r0 = _three_radius(z, mp.mpf(0), inner_tol)
        r1 = _three_radius(z, mp.mpf(1), inner_tol)
        f0 = three_trace(z, r0, mp.mpf(0)) - 3
        f1 = three_trace(z, r1, mp.mpf(1)) - 3
        if not f0 > 0 > f1:
            raise ArithmeticError("Endpoint signs lost; increase precision for these nodes.")
        lo, hi = mp.mpf(0), mp.mpf(1)
        for it in range(1, 5 * dps + 200):
            theta = (lo + hi) / 2
            r = _three_radius(z, theta, inner_tol)
            f = three_trace(z, r, theta) - 3
            if abs(f) < tol:
                d = [scale * v for v in three_diagonal(z, r, theta)]
                return ThreeSolution(d, theta, scale * r, (f0, f1), f, it)
            if f > 0:
                lo = theta
            else:
                hi = theta
        raise ArithmeticError("Trace bisection did not meet tolerance; increase precision.")


def ansatz_diagonal(values: Iterable[Any], alphas: Sequence[Any]) -> list[mp.mpf]:
    c = nodes(values)
    a = [as_mpf(v) for v in alphas]
    if len(a) != len(c) - 1 or any(not mp.isfinite(v) or v <= 0 for v in a):
        raise ValueError("Supply exactly n-1 positive finite negative-root magnitudes.")
    return [1 / (1 / t + mp.fsum(1 / (t + v) for v in a)) for t in c]


def _ansatz_system(x: mp.matrix, c: Sequence[mp.mpf], M: mp.matrix):
    """Residual and Jacobian for exploratory all-stage Newton iteration."""
    n = len(c)
    a = [mp.exp(v) for v in x]
    d = ansatz_diagonal(c, a)
    dd = mp.matrix([[v * d[i] ** 2 / (c[i] + v) ** 2 for v in a] for i in range(n)])
    L, P = M * mp.diag(d), mp.eye(n)
    f, J = mp.matrix(n - 1, 1), mp.matrix(n - 1, n - 1)
    for k in range(1, n - 1):
        LP = L * P
        e = mp.fsum(LP[i, i] for i in range(n)) / k
        PM = P * M
        f[k - 1] = e / comb(n, k) - 1
        for j in range(n - 1):
            J[k - 1, j] = mp.fsum(PM[i, i] * dd[i, j] for i in range(n)) / comb(n, k)
        P = e * mp.eye(n) - LP
    f[n - 2] = mp.log(factorial(n)) + mp.fsum(mp.log(d[i] / c[i]) for i in range(n))
    for j in range(n - 1):
        J[n - 2, j] = mp.fsum(dd[i, j] / d[i] for i in range(n))
    return f, J, d


def refine_ansatz(values: Iterable[Any], initial_alphas: Sequence[Any],
                  dps: int = 80, maxiter: int = 80) -> dict[str, Any]:
    """Numerical refinement only; failure is not a counterexample.

    Success means a small computed residual, NOT an existence certificate or
    proof of uniqueness. This does not replace solve_three's existence proof.
    """
    if dps < 30 or maxiter < 1:
        raise ValueError("Use at least 30 decimal digits and a positive iteration limit.")
    with mp.workdps(dps + 35):
        c = nodes(values)
        initial = [as_mpf(v) for v in initial_alphas]
        if len(initial) != len(c) - 1 or any(not mp.isfinite(v) or v <= 0 for v in initial):
            raise ValueError("Provide n-1 strictly positive initial alphas.")
        x = mp.matrix([mp.log(v) for v in initial])
        M = inverse_similar(c)
        tol = mp.power(10, -dps)
        for it in range(maxiter + 1):
            f, J, d = _ansatz_system(x, c, M)
            err = max(abs(v) for v in f)
            if err < tol:
                return {"diagonal": d, "alphas": [mp.exp(v) for v in x],
                        "residual": err, "iterations": it}
            if it == maxiter:
                break
            try:
                step = mp.lu_solve(J, -f)
            except (ZeroDivisionError, ValueError) as exc:
                raise ArithmeticError("Singular Newton Jacobian; not evidence of nonexistence.") from exc
            stepnorm = max(abs(v) for v in step)
            length = min(mp.mpf(1), 2 / max(mp.mpf(2), stepnorm))
            accepted = False
            for _ in range(50):
                proposal = x + length * step
                ff, _, _ = _ansatz_system(proposal, c, M)
                if max(abs(v) for v in ff) < err:
                    x, accepted = proposal, True
                    break
                length /= 2
            if not accepted:
                raise ArithmeticError("Newton line search failed; not evidence of nonexistence.")
        raise ArithmeticError(f"Newton iteration limit reached; residual {mp.nstr(err, 8)}.")
