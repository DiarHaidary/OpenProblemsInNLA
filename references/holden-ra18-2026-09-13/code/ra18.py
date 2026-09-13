"""Explicit frames and verification helpers for the RA-18 manuscript.

b(U) denotes the SQUARED best inverse norm, not the inverse norm itself.
All array computations are numerical checks; the manuscript supplies the proof.
"""
from __future__ import annotations

from itertools import combinations, islice
from math import comb
from fractions import Fraction
from typing import Iterator, Sequence

import mpmath as mp
import numpy as np
from numpy.typing import NDArray
from scipy.linalg import null_space

Array = NDArray[np.complex128] | NDArray[np.float64]


def validate_isometry(U: Array, tolerance: float = 1e-9) -> None:
    """Raise ValueError unless U is a finite tall numerical isometry."""
    if U.ndim != 2 or U.shape[0] < U.shape[1] or U.shape[1] < 1:
        raise ValueError("U must have shape (n, r) with n >= r >= 1")
    if not np.isfinite(U).all():
        raise ValueError("U has nonfinite entries")
    error = np.linalg.norm(U.conj().T @ U - np.eye(U.shape[1]), ord=2)
    if error > tolerance:
        raise ValueError(f"U is not an isometry within tolerance: error={error}")


def trine_lift(U: Array) -> NDArray[np.complex128]:
    """Return [U tensor a, I_n tensor c], with a=(1,1,1)/sqrt(3)."""
    U = np.asarray(U, dtype=np.complex128)
    validate_isometry(U)
    n, _ = U.shape
    omega = complex(-0.5, np.sqrt(3.0) / 2.0)
    a = np.ones((3, 1), dtype=np.complex128) / np.sqrt(3.0)
    c = np.array([1, omega, omega**2], dtype=np.complex128)[:, None] / np.sqrt(3.0)
    return np.concatenate((np.kron(U, a), np.kron(np.eye(n), c)), axis=1)


def family(level: int, max_bytes: int = 128 * 1024**2) -> NDArray[np.complex128]:
    """Build U_level densely. Use the scalar recurrence for very large levels."""
    if not isinstance(level, int) or level < 0:
        raise ValueError("level must be a nonnegative integer")
    r = 3**level
    if 2 * r * r * np.dtype(np.complex128).itemsize > max_bytes:
        raise ValueError("Dense matrix exceeds max_bytes; use scalar_recurrence instead")
    U = np.ones((2, 1), dtype=np.complex128) / np.sqrt(2.0)
    for _ in range(level):
        U = trine_lift(U)
    return U


def structural_basis(level: int, indices: Sequence[int]) -> bool:
    """Exact combinatorial classification of a row set of U_level.

    This uses integers only, not numerical determinant thresholds.
    """
    if not isinstance(level, int) or level < 0:
        raise ValueError("level must be a nonnegative integer")
    idx = np.asarray(indices, dtype=int)
    n, r = 2 * 3**level, 3**level
    if idx.ndim != 1 or len(idx) != r or len(set(idx.tolist())) != r:
        return False
    if np.any(idx < 0) or np.any(idx >= n):
        return False
    if level == 0:
        return True
    counts = np.bincount(idx // 3, minlength=n // 3)
    if np.any((counts != 1) & (counts != 2)):
        return False
    return structural_basis(level - 1, np.flatnonzero(counts == 2))


def sample_basis(level: int, rng: np.random.Generator) -> NDArray[np.int64]:
    """Sample a legal basis recursively, uniformly among all legal bases."""
    if level < 0:
        raise ValueError("level must be nonnegative")
    if level == 0:
        return np.array([rng.integers(2)], dtype=np.int64)
    parent = set(sample_basis(level - 1, rng).tolist())
    chosen = []
    for i in range(2 * 3**(level - 1)):
        j = int(rng.integers(3))
        phases = [p for p in range(3) if p != j] if i in parent else [j]
        chosen.extend(3 * i + p for p in phases)
    return np.array(chosen, dtype=np.int64)


def subset_batches(n: int, r: int, batch_size: int = 512) -> Iterator[NDArray[np.int64]]:
    if batch_size < 1:
        raise ValueError("batch_size must be positive")
    iterator = combinations(range(n), r)
    while batch := list(islice(iterator, batch_size)):
        yield np.asarray(batch, dtype=np.int64)


def exhaustive_spectra(U: Array, max_subsets: int = 100_000):
    """Yield (indices, sorted squared singular values) for EVERY square row set."""
    validate_isometry(U)
    n, r = U.shape
    count = comb(n, r)
    if count > max_subsets:
        raise ValueError(f"{count} subsets exceed the safety limit {max_subsets}")
    for idx in subset_batches(n, r):
        A = U[idx]
        grams = np.swapaxes(A.conj(), -1, -2) @ A
        yield idx, np.linalg.eigvalsh(grams)


def H(g: float) -> NDArray[np.float64]:
    """The exact spectral lift block, evaluated in floating point."""
    if not -1e-12 <= g <= 1.0 + 1e-12:
        raise ValueError("g must lie in [0, 1]")
    g = float(np.clip(g, 0, 1))
    return np.array([[1 + g, np.sqrt(g), np.sqrt(1-g)],
                     [np.sqrt(g), 2, 0],
                     [np.sqrt(1-g), 0, 1]], dtype=float) / 3.0


def predicted_spectrum(level: int) -> NDArray[np.float64]:
    if level < 0:
        raise ValueError("level must be nonnegative")
    spectrum = np.array([0.5])
    for _ in range(level):
        spectrum = np.sort(np.concatenate([np.linalg.eigvalsh(H(g)) for g in spectrum]))
    return spectrum


def R_scalar(x):
    return x * (2 - 3*x)**2 / (1 - 3*x + 3*x*x)


def inverse_R(g, digits: int = 80):
    """Monotone bisection on [0, 1/3]; no root-selection ambiguity."""
    with mp.workdps(digits + 15):
        g = mp.mpf(g)
        if not 0 <= g <= 1:
            raise ValueError("g must lie in [0, 1]")
        if g == 0:
            return mp.mpf(0)
        if g == 1:
            return mp.mpf(1) / 3
        lo, hi = mp.mpf(0), mp.mpf(1) / 3
        for _ in range(int(3.5 * (digits + 15)) + 20):
            mid = (lo + hi) / 2
            if R_scalar(mid) < g:
                lo = mid
            else:
                hi = mid
        return +(lo + hi) / 2


def scalar_recurrence(max_level: int = 12, digits: int = 80) -> list[dict]:
    """Return high-precision scalar data without constructing the matrices."""
    if max_level < 0 or digits < 20:
        raise ValueError("max_level must be nonnegative and digits at least 20")
    rows = []
    with mp.workdps(digits):
        g = mp.mpf(1) / 2
        for k in range(max_level + 1):
            n, r = 2 * 3**k, 3**k
            inv = 1 / mp.sqrt(g)
            rows.append({
                "level": k, "n": n, "r": r,
                "beta": mp.nstr(g, digits),
                "n_times_beta": mp.nstr(n*g, digits),
                "best_inverse_norm": mp.nstr(inv, digits),
                "ratio_to_sqrt_n": mp.nstr(inv/mp.sqrt(n), digits),
                "four_power_k_times_beta": mp.nstr(4**k*g, digits),
                "proved_lower_bound_on_squared_inverse": str(Fraction(3 * 4**k + 1, 2)),
                "nonsingular_basis_count_formula": f"2 * 3**({3**k - 1})",
            })
            g = inverse_R(g, digits)
    return rows


def invsqrt(A: Array) -> Array:
    eigs, Q = np.linalg.eigh(A)
    if eigs[0] <= 0:
        raise ValueError("A must be positive definite")
    return (Q * (1 / np.sqrt(eigs))) @ Q.conj().T


def weighted_dual(V: Array, multiplicities: Sequence[int], eta: float):
    """Return the isometry Z and complement W from the weighted-duality lemma."""
    validate_isometry(V)
    q, r = V.shape
    m = np.asarray(multiplicities, dtype=float)
    if m.shape != (q,) or np.any(m <= 0):
        raise ValueError("multiplicities must have q positive entries")
    if not 0 < eta or np.any(eta*m >= 1) or q == r:
        raise ValueError("Require q > r and 0 < eta*m_i < 1")
    W = null_space(V.conj().T)
    weights = eta * m / (1 - eta*m)
    R = W.conj().T @ (weights[:, None] * W)
    Z = (np.sqrt(weights)[:, None] * W) @ invsqrt(R)
    validate_isometry(Z)
    return Z, W


def select_grouped_real(U: Array, labels: Sequence[int], tolerance: float = 1e-8):
    """Select a certified-class basis, numerically.

    labels specify exact parallel row groups; -1 is reserved for zero rows.
    At most r+2 nonzero groups are allowed. The function checks these premises
    numerically, but a tolerance check is not an exact proof of membership.
    """
    if np.iscomplexobj(U) and np.max(np.abs(np.imag(U))) > tolerance:
        raise ValueError("This selector is for real matrices")
    U = np.asarray(np.real(U), dtype=float)
    validate_isometry(U)
    n, r = U.shape
    labels = np.asarray(labels, dtype=int)
    if labels.shape != (n,):
        raise ValueError("labels must have one entry per row")
    if np.any(np.linalg.norm(U[labels == -1], axis=1) > tolerance):
        raise ValueError("Rows with label -1 must be zero")
    keys = sorted(set(labels.tolist()) - {-1})
    if not r <= len(keys) <= r + 2:
        raise ValueError("Require between r and r+2 nonzero row groups")
    V, m, representatives = [], [], []
    for key in keys:
        indices = np.flatnonzero(labels == key)
        rows = U[indices]
        norms = np.linalg.norm(rows, axis=1)
        j = int(np.argmax(norms))
        if norms[j] <= tolerance:
            raise ValueError("Each group must contain a nonzero row")
        direction = rows[j] / norms[j]
        if np.linalg.norm(rows - (rows @ direction)[:, None]*direction) > tolerance:
            raise ValueError("A supplied group is not parallel within tolerance")
        V.append(np.linalg.norm(norms) * direction)
        m.append(len(indices))
        representatives.append(int(indices[j]))
    V = np.asarray(V)
    validate_isometry(V, tolerance)
    s, N = len(keys) - r, sum(m)
    if s == 0:
        return np.asarray(representatives, dtype=int)
    Z, _ = weighted_dual(V, m, 1.0/N)
    B = Z / np.sqrt(np.asarray(m))[:, None]
    best_J, best_value = None, -np.inf
    for J in combinations(range(len(keys)), s):
        sub = B[list(J)]
        value = np.linalg.eigvalsh(sub.T @ sub)[0]
        if value > best_value:
            best_J, best_value = J, value
    if best_value < 1.0/N - tolerance:
        raise ArithmeticError("Rank-one/two selection bound not met numerically")
    return np.array([representatives[i] for i in range(len(keys)) if i not in best_J])


def sharp_real_example(multiplicities: Sequence[int]) -> NDArray[np.float64]:
    """Unequally duplicated simplex frame with beta exactly 1/N."""
    m = np.asarray(multiplicities, dtype=float)
    r = len(m) - 1
    if r < 1 or np.any(m < 1) or np.any(m != np.floor(m)):
        raise ValueError("At least two positive integer multiplicities are required")
    z = np.sqrt((1 - m / m.sum()) / r)
    V = null_space(z[None, :])
    return np.vstack([np.tile(V[i]/np.sqrt(mi), (int(mi), 1)) for i, mi in enumerate(m)])
