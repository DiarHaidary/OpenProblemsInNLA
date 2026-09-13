"""Reference implementations for the RA-11 research note.

The proofs use exact real arithmetic. These routines use floating point and are
small-instance demonstrations, not numerically stable large-q implementations.
All calls to DenseProductOracle must use real rank-one tensor inputs.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Sequence
import math
import numpy as np

Array = np.ndarray


def kron_vectors(vectors: Sequence[Array]) -> Array:
    out = np.array([1.0])
    for vector in vectors:
        v = np.asarray(vector)
        if v.ndim != 1:
            raise ValueError("Each factor must be a vector.")
        out = np.kron(out, v)
    return out


def contract_except(tensor: Array, vectors: Sequence[Array], keep: int) -> Array:
    """Contract every mode except `keep`, without complex conjugation."""
    if not 0 <= keep < len(vectors):
        raise ValueError("Invalid retained mode.")
    out = np.asarray(tensor).reshape(tuple(len(v) for v in vectors))
    for j in reversed(range(len(vectors))):
        if j != keep:
            out = np.tensordot(out, vectors[j], axes=([j], [0]))
    return np.asarray(out)


@dataclass
class DenseProductOracle:
    matrix: Array
    n: int
    q: int
    calls: int = 0

    def __post_init__(self) -> None:
        if self.n < 2 or self.q < 1:
            raise ValueError("Require n >= 2 and q >= 1.")
        a = np.asarray(self.matrix)
        size = self.n ** self.q
        if a.shape != (size, size) or np.iscomplexobj(a):
            raise ValueError("Expected a real n**q by n**q matrix.")
        self.matrix = a.astype(float)

    def __call__(self, factors: Sequence[Array]) -> Array:
        if len(factors) != self.q:
            raise ValueError("Wrong number of product factors.")
        vv = []
        for factor in factors:
            v = np.asarray(factor)
            if v.shape != (self.n,) or np.iscomplexobj(v):
                raise ValueError("The actual oracle accepts only real factors.")
            if not np.all(np.isfinite(v)):
                raise ValueError("Non-finite query.")
            vv.append(v)
        self.calls += 1
        return self.matrix @ kron_vectors(vv)


def complex_product_via_real(
    oracle: Callable[[Sequence[Array]], Array], factors: Sequence[Array]
) -> Array:
    """Compute M(kron(factors)) with exactly q+1 real product queries.

    Interpolation can be badly conditioned. The exact-arithmetic identity is
    tested separately with SymPy in tests/exact_checks.py.
    """
    q = len(factors)
    if not q:
        raise ValueError("At least one factor is required.")
    # Real Chebyshev nodes reduce, but do not eliminate, interpolation growth.
    nodes = np.cos(np.pi * (np.arange(q + 1) + 0.5) / (q + 1))
    answer = None
    for j, t in enumerate(nodes):
        weight = 1.0 + 0.0j
        for k, s in enumerate(nodes):
            if k != j:
                weight *= (1j - s) / (t - s)
        response = oracle([np.real(v) + t * np.imag(v) for v in factors])
        term = weight * response
        answer = term if answer is None else answer + term
    return np.asarray(answer)


def interpolated_trace(
    oracle: Callable[[Sequence[Array]], Array], n: int, q: int,
    samples: int, rng: np.random.Generator,
) -> float:
    """Unbiased complex-sphere estimator, implemented using real queries.

    Normalization is in the scalar weight, so no square root is required by the
    corresponding exact-arithmetic algorithm.
    """
    if samples < 1:
        raise ValueError("samples must be positive.")
    total = 0.0
    for _ in range(samples):
        factors = [rng.normal(size=n) + 1j*rng.normal(size=n) for _ in range(q)]
        z = kron_vectors(factors)
        mz = complex_product_via_real(oracle, factors)
        weight = math.prod(n / float(np.vdot(v, v).real) for v in factors)
        total += weight * float(np.vdot(z, mz).real)
    return total / samples


class ParallelProductAccess:
    """Simultaneous ordinary matvec access when M is promised to be a PSD product.

    If M = kron(A_i), initialization obtains gamma and b_i = B_i g_i, where
    B_i = A_i/(g_i.T A_i g_i) and M = gamma*kron(B_i).
    The promise is NOT verified by this class and cannot be dropped.
    """
    def __init__(self, oracle: Callable[[Sequence[Array]], Array], n: int, q: int,
                 rng: np.random.Generator):
        self.oracle, self.n, self.q = oracle, n, q
        self.g = [rng.normal(size=n) for _ in range(q)]
        y = oracle(self.g)
        self.gamma = float(np.dot(kron_vectors(self.g), y))
        self.zero = self.gamma == 0.0
        if self.zero:
            self.b = [np.zeros(n) for _ in range(q)]
        elif self.gamma < 0.0:
            raise ArithmeticError("Negative reference quadratic form: PSD promise/numerics failed.")
        else:
            self.b = [contract_except(y, self.g, i)/self.gamma for i in range(q)]

    def round(self, targets: Sequence[Array]) -> list[Array]:
        if len(targets) != self.q:
            raise ValueError("Need one local vector per factor.")
        if self.zero:
            return [np.zeros(self.n) for _ in range(self.q)]
        vv = [np.asarray(v, dtype=float) for v in targets]
        if any(v.shape != (self.n,) for v in vv):
            raise ValueError("Incorrect local vector dimension.")
        alpha = [1.0 - float(np.dot(b, v)) for b, v in zip(self.b, vv)]
        w = [v + a*g for v, a, g in zip(vv, alpha, self.g)]
        y = self.oracle(w)
        # In exact arithmetic, b_i.T w_i = 1 for every i.
        return [contract_except(y, self.g, i)/self.gamma - alpha[i]*self.b[i]
                for i in range(self.q)]

    def recover_factors(self) -> list[Array]:
        """Use n-1 additional calls; total including initialization is n."""
        if self.zero:
            return [np.zeros((self.n, self.n)) for _ in range(self.q)]
        indices = [[j for j in range(self.n) if j != int(np.argmax(np.abs(g)))]
                   for g in self.g]
        inputs = [[g.copy()] for g in self.g]
        outputs = [[b.copy()] for b in self.b]
        eye = np.eye(self.n)
        for s in range(self.n - 1):
            targets = [eye[:, indices[i][s]] for i in range(self.q)]
            values = self.round(targets)
            for i in range(self.q):
                inputs[i].append(targets[i]); outputs[i].append(values[i])
        return [np.linalg.solve(np.column_stack(inputs[i]).T,
                                np.column_stack(outputs[i]).T).T
                for i in range(self.q)]


def product_trace_exact(access: ParallelProductAccess) -> float:
    if access.zero:
        return 0.0
    factors = access.recover_factors()
    return access.gamma * math.prod(float(np.trace(a)) for a in factors)


def product_trace_hutchpp(access: ParallelProductAccess, r: int,
                         rngs: Sequence[np.random.Generator]) -> float:
    """Parallel, unbiased local Hutch++ estimators; at most 5r+4 extra calls.

    r >= ceil(8*sqrt(q)/epsilon) is the conservative proved choice. For small n,
    exact recovery is preferable. This function is a numerical demonstration.
    """
    if r < 1 or len(rngs) != access.q:
        raise ValueError("Require r >= 1 and q independent random generators.")
    if access.zero:
        return 0.0
    n, q, m = access.n, access.q, 2*r + 2
    if n <= 5*r + 5:
        return product_trace_exact(access)
    g = [rng.normal(size=(n, m)) for rng in rngs]
    y = [np.empty((n, m)) for _ in range(q)]
    for j in range(m):
        values = access.round([a[:, j] for a in g])
        for i in range(q):
            y[i][:, j] = values[i]
    bases = []
    for a in y:
        u, singular, _ = np.linalg.svd(a, full_matrices=False)
        tol = np.finfo(float).eps * max(a.shape) * singular[0] if singular.size else 0.0
        bases.append(u[:, singular > tol])
    exact = np.zeros(q)
    for j in range(max(b.shape[1] for b in bases)):
        targets = [b[:, j] if j < b.shape[1] else np.zeros(n) for b in bases]
        values = access.round(targets)
        for i in range(q):
            exact[i] += np.dot(targets[i], values[i])
    rest = np.zeros(q)
    for _ in range(r):
        h = [rng.normal(size=n) for rng in rngs]
        targets = [v - b@(b.T@v) for v, b in zip(h, bases)]
        values = access.round(targets)
        for i in range(q):
            rest[i] += np.dot(targets[i], values[i])/r
    return access.gamma * math.prod(float(x) for x in exact + rest)


def partial_trace(matrix: Array, n: int, q: int, traced: Sequence[int]) -> Array:
    if len(set(traced)) != len(traced) or any(i < 0 or i >= q for i in traced):
        raise ValueError("Invalid subsystem set.")
    a = np.asarray(matrix).reshape((n,)*(2*q))
    remaining = q
    for i in sorted(traced, reverse=True):
        a = np.trace(a, axis1=i, axis2=i+remaining)
        remaining -= 1
    return a.reshape((n**remaining, n**remaining))


def complex_second_moment(matrix: Array, n: int, q: int) -> float:
    total = 0.0
    for mask in range(1 << q):
        a = partial_trace(matrix, n, q, [i for i in range(q) if mask & (1 << i)])
        total += float(np.vdot(a, a).real)
    return (n/(n+1))**q * total


def proved_bound_functions(n: int, q: int, epsilon: float) -> dict[str, float | int]:
    if n < 2 or q < 2 or not 0 < epsilon < 0.5:
        raise ValueError("Require n,q >= 2 and 0 < epsilon < 1/2.")
    size = n**q
    alpha, beta = 3*n/(n+2), 2*n/(n+1)
    real_upper = math.ceil(3*(alpha**q - 1)/epsilon**2)
    complex_upper = (q+1)*math.ceil(3*(beta**q - 1)/epsilon**2)
    simulated_hutchpp = n**(q-1)*(5*math.ceil(4/epsilon)+4)
    lower_scale = max(min(n**b, math.sqrt(q//b)/epsilon) for b in range(1, q+1))
    return {"N": size, "lower_scale_L": lower_scale,
            "proved_lower_constant": 1/80000,
            "explicit_upper": min(size, real_upper, complex_upper, simulated_hutchpp),
            "real_sphere_upper": real_upper, "interpolated_complex_upper": complex_upper,
            "simulated_hutchpp_upper": simulated_hutchpp}
