"""Diagnostic linear algebra for the RA-14 capacity and innovation note.

These routines use hidden spectral coordinates for validation. They are NOT
an oracle algorithm for arbitrary RA-14 inputs and do not prove probability
statements. The manuscript gives the mathematical proofs.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
import numpy as np
from numpy.typing import NDArray

Array = NDArray[np.float64]


def orth(a: Array, tol: float = 1e-10) -> Array:
    a = np.asarray(a, dtype=float)
    if a.ndim != 2:
        raise ValueError("Expected a two-dimensional matrix")
    if a.shape[1] == 0:
        return np.empty((a.shape[0], 0))
    u, s, _ = np.linalg.svd(a, full_matrices=False)
    cut = tol * max(1.0, float(s[0]) if s.size else 1.0)
    return u[:, s > cut]


def null(a: Array, tol: float = 1e-10) -> Array:
    a = np.asarray(a, dtype=float)
    if a.ndim != 2:
        raise ValueError("Expected a two-dimensional matrix")
    if a.shape[1] == 0:
        return np.empty((0, 0))
    _, s, vh = np.linalg.svd(a, full_matrices=True)
    cut = tol * max(1.0, float(s[0]) if s.size else 1.0)
    rank = int(np.sum(s > cut))
    return vh[rank:].T.copy()


@dataclass
class CapacityResult:
    feasible_top: bool
    free_rank: int
    free_complement: Array
    capacity: Array
    minimum_energy: Array
    coefficients: Array | None
    criterion_margin: float


def minimum_energy_certificate(top: Array, weighted_tail: Array,
                               d1: Array, tol: float = 1e-10) -> CapacityResult:
    """Exact-formula diagnostic, including singular weighted-tail features.

    `d1` is the positive definite leading squared-singular-value excess above
    the residual threshold. A nonnegative criterion margin means that the
    feature space contains a valid graph, up to numerical rounding.
    """
    t = np.asarray(top, dtype=float)
    w = np.asarray(weighted_tail, dtype=float)
    d1 = np.asarray(d1, dtype=float)
    if t.ndim != 2 or w.ndim != 2 or t.shape[1] != w.shape[1]:
        raise ValueError("Top and tail must share their coefficient dimension")
    k, p = t.shape
    if d1.shape != (k, k) or not np.allclose(d1, d1.T):
        raise ValueError("d1 must be a symmetric k-by-k matrix")
    if np.linalg.eigvalsh(d1).min() <= 0:
        raise ValueError("d1 must be positive definite")
    if orth(t, tol).shape[1] < k:
        return CapacityResult(False, 0, np.eye(k), np.empty((0, 0)),
                              np.full((k, k), np.nan), None, -math.inf)
    n0 = null(w, tol)
    free = orth(t @ n0, tol)
    r = null(free.T, tol)
    _, s, vh = np.linalg.svd(w, full_matrices=False)
    cut = tol * max(1.0, float(s[0]) if s.size else 1.0)
    active = s > cut
    va = vh[active].T
    gplus = (va / (s[active] ** 2)) @ va.T if np.any(active) else np.zeros((p, p))
    if r.shape[1] == 0:
        cap = np.empty((0, 0))
        energy = np.zeros((k, k))
        l0 = np.zeros((p, k))
        margin = math.inf
    else:
        cap = r.T @ t @ gplus @ t.T @ r
        cap = (cap + cap.T) / 2
        if np.linalg.eigvalsh(cap).min() <= tol:
            raise ArithmeticError("Numerically singular projected capacity")
        inverse = np.linalg.inv(cap)
        energy = r @ inverse @ r.T
        l0 = gplus @ t.T @ energy
        margin = float(np.linalg.eigvalsh(cap - r.T @ d1 @ r).min())
    correction = n0 @ np.linalg.pinv(t @ n0, rcond=tol) @ (np.eye(k) - t @ l0)
    coeff = l0 + correction
    return CapacityResult(True, free.shape[1], r, cap, energy, coeff, margin)


def chebyshev_data(degree: int, epsilon: float) -> tuple[Array, Array, Array, float]:
    if degree < 1 or not 0 < epsilon < 0.5:
        raise ValueError("Require degree >= 1 and 0 < epsilon < 1/2")
    a, tau = 1 + 2 * epsilon, 1 + epsilon
    if not (a > tau > 1):
        raise ValueError("Accuracy cannot be represented in this float dtype")
    nodes = np.cos(np.arange(degree + 1) * np.pi / degree)
    endpoint = np.ones(degree + 1)
    endpoint[[0, -1]] = 0.5
    raw = endpoint / (a - nodes)
    tval = math.cosh(degree * math.acosh(a))
    ell = ((-1.0) ** np.arange(degree + 1)) * raw / raw.sum() * tval
    e = (tau - nodes) * (tau + nodes)
    mass = float(np.sum(np.abs(ell) * np.sqrt(e)))
    return nodes, e, ell, mass


def allocate(n: int, k: int, width: int, degree: int,
             epsilon: float) -> tuple[Array, Array, Array, Array]:
    if min(n, k, width, degree) < 1 or k >= n:
        raise ValueError("Invalid dimensions")
    remaining = n - k
    if 2 * (width + 3) * (degree + 1) > remaining:
        raise ValueError("The stated integer multiplicity condition fails")
    nodes, e, ell, mass = chebyshev_data(degree, epsilon)
    weights = np.abs(ell) * np.sqrt(e) / mass
    multiplicities = width + 2 + np.ceil(remaining / 2 * weights).astype(int)
    if multiplicities.sum() > remaining:
        raise ArithmeticError("Rounding exceeded the dimension budget")
    multiplicities[0] += remaining - int(multiplicities.sum())
    return nodes, e, ell, multiplicities


def nodal_capacity(g0: Array, blocks: list[Array], e: Array, ell: Array) -> Array:
    if len(blocks) != len(e) or len(e) != len(ell):
        raise ValueError("Node data lengths must match")
    width = g0.shape[1]
    s = np.zeros((width, width))
    for gj, ej, lj in zip(blocks, e, ell):
        gram = gj.T @ gj
        if np.linalg.matrix_rank(gram) != width:
            raise ValueError("This formula requires full-column-rank node blocks")
        s += float(lj * lj * ej) * np.linalg.inv(gram)
    h = g0 @ s @ g0.T
    return (h + h.T) / 2


def first_moment_bound(width: int, multiplicities: Array, e: Array,
                       ell: Array, delta: float) -> float:
    denominators = np.asarray(multiplicities) - width - 1
    if delta <= 0 or np.any(denominators <= 0):
        raise ValueError("The reciprocal-Gram moment is not finite here")
    return float(width * np.sum(ell**2 * e / denominators) / delta)


def pure_top_dimension(k: int, width: int, multiplicities: Array) -> int:
    """Almost-sure dimension, not a numerical rank estimate."""
    deficits = int(np.maximum(width - np.asarray(multiplicities), 0).sum())
    return min(k, width, deficits)


def graph_basis(top: Array, tail: Array, coefficients: Array) -> Array:
    return orth(np.vstack((top, tail)) @ coefficients)


def residual(spectrum: Array, basis: Array) -> float:
    n = len(spectrum)
    return float(np.linalg.norm(np.diag(spectrum) @ (np.eye(n) - basis @ basis.T), 2))


def householder_map(source: Array, target: Array, tol: float = 1e-12) -> Array:
    """Orthogonal reflection taking one unit vector to another."""
    source, target = np.asarray(source), np.asarray(target)
    if not np.isclose(np.linalg.norm(source), 1) or not np.isclose(np.linalg.norm(target), 1):
        raise ValueError("Both inputs must be unit vectors")
    difference = source - target
    squared = float(difference @ difference)
    if squared <= tol**2:
        return np.eye(source.size)
    return np.eye(source.size) - 2 * np.outer(difference, difference) / squared


def simulate_coordinate_policy(matrix: Array, queries: int, seed: int = 0) -> dict:
    """Algebraic check of rotating fresh innovations into independent starts.

    The virtual policy uses alternating coordinate-dependent and known-span
    queries. This tests transcript consistency, NOT equality of probability
    laws. All calls to the physical matrix are counted explicitly.
    """
    a = np.asarray(matrix, dtype=float)
    n = a.shape[0]
    if a.shape != (n, n) or not np.allclose(a, a.T):
        raise ValueError("A symmetric matrix is required")
    rng = np.random.default_rng(seed)
    transform = np.eye(n)
    known = np.empty((n, 0))
    vhist, whist, physical_q, physical_a, starts = [], [], [], [], []
    max_span_error = 0.0
    for i in range(queries):
        if i % 2 and whist:
            v = whist[-1] + 0.3 * vhist[-1]
        else:
            v = np.eye(n)[:, i % n].copy()
            if whist:
                v += 0.2 * np.roll(whist[-1], 1)
        mapped = transform @ v
        outside = mapped - known @ (known.T @ mapped)
        radius = float(np.linalg.norm(outside))
        if radius > 1e-9 * max(1.0, np.linalg.norm(mapped)):
            g = rng.standard_normal(n)
            fresh = g - known @ (known.T @ g)
            if np.linalg.norm(fresh) < 1e-12:
                raise ArithmeticError("Unexpected vanishing projected Gaussian")
            fresh /= np.linalg.norm(fresh)
            rotation = householder_map(outside / radius, fresh)
            transform = rotation @ transform
            starts.append(g)
            mapped = transform @ v
        available = np.column_stack(starts + physical_a) if starts or physical_a else np.empty((n, 0))
        available = orth(available)
        max_span_error = max(max_span_error, float(np.linalg.norm(mapped - available @ (available.T @ mapped))))
        answer = a @ mapped  # exactly one physical matrix-vector query
        virtual_answer = transform.T @ answer
        physical_q.append(mapped.copy())
        physical_a.append(answer.copy())
        vhist.append(v.copy())
        whist.append(virtual_answer.copy())
        known = orth(np.column_stack(physical_q + physical_a))
    final_virtual = transform.T @ a @ transform
    consistency = max((np.linalg.norm(final_virtual @ v - w) for v, w in zip(vhist, whist)), default=0.0)
    return {"query_count": queries, "innovation_count": len(starts),
            "transcript_error": float(consistency), "span_error": max_span_error,
            "orthogonality_error": float(np.linalg.norm(transform.T @ transform - np.eye(n)))}
