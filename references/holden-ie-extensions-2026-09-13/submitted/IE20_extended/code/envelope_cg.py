"""Exact executor for the IE-20 scalar relative-error *envelope*.

Only Python's standard library is required. Fractions are used for exact
rational arithmetic, not to approximate IEEE floating-point arithmetic.
An admissible policy chooses one rational delta per elementary operation.
Products and sums are separate; every dot product starts at zero and includes
zero terms. Copies, comparisons, and signs are exact.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction as Q
from typing import Callable, Sequence

Vector = list[Q]
Matrix = list[Vector]
Policy = Callable[[str, str, Q, Q, Q], Q]


def zero_policy(label: str, op: str, a: Q, b: Q, u: Q) -> Q:
    return Q(0)


def significant_bits(value: Q) -> int | None:
    """Bits in an exact binary significand; None means not a binary rational."""
    value = Q(value)
    denominator = value.denominator
    if denominator & (denominator - 1):
        return None
    numerator = abs(value.numerator)
    if not numerator:
        return 0
    while numerator % 2 == 0:
        numerator //= 2
    return numerator.bit_length()


@dataclass
class ErrorMachine:
    precision: int
    policy: Policy = zero_policy
    operations: int = 0
    faults: list[dict[str, str | int]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.precision < 2:
            raise ValueError("IE-20 requires precision >= 2")
        self.u = Q(1, 1 << self.precision)

    def op(self, kind: str, a: Q, b: Q, label: str) -> Q:
        a, b = Q(a), Q(b)
        if kind == "+":
            exact = a + b
        elif kind == "-":
            exact = a - b
        elif kind == "*":
            exact = a * b
        elif kind == "/":
            if not b:
                raise ZeroDivisionError(label)
            exact = a / b
        else:
            raise ValueError(f"Unknown operation: {kind}")
        delta = Q(self.policy(label, kind, a, b, self.u))
        if abs(delta) > self.u:
            raise ValueError(f"Non-admissible error at {label}: {delta}")
        self.operations += 1
        if delta:
            self.faults.append({"index": self.operations, "label": label,
                                "operation": kind, "delta": str(delta)})
        return exact * (1 + delta)

    def dot(self, a: Sequence[Q], b: Sequence[Q], label: str) -> Q:
        if len(a) != len(b):
            raise ValueError("Dot-product lengths differ")
        total = Q(0)
        for i, (ai, bi) in enumerate(zip(a, b)):
            term = self.op("*", ai, bi, f"{label}.mul[{i}]")
            total = self.op("+", total, term, f"{label}.add[{i}]")
        return total

    def matvec(self, A: Matrix, v: Vector, step: int) -> Vector:
        return [self.dot(row, v, f"q[{step},{i}]")
                for i, row in enumerate(A)]

    def axpy(self, a: Vector, alpha: Q, b: Vector,
             label: str, subtract: bool = False) -> Vector:
        out: Vector = []
        for i, (ai, bi) in enumerate(zip(a, b)):
            term = self.op("*", alpha, bi, f"{label}[{i}].mul")
            out.append(self.op("-" if subtract else "+", ai, term,
                               f"{label}[{i}].{'sub' if subtract else 'add'}"))
        return out


def exact_dot(a: Sequence[Q], b: Sequence[Q]) -> Q:
    return sum((x*y for x, y in zip(a, b)), Q(0))


def exact_matvec(A: Matrix, x: Vector) -> Vector:
    return [exact_dot(row, x) for row in A]


def validate_input(A: Matrix, b: Vector, precision: int) -> None:
    n = len(b)
    if not n or len(A) != n or any(len(row) != n for row in A):
        raise ValueError("A must be square and compatible with nonempty b")
    if not any(b):
        raise ValueError("b must be nonzero")
    for value in [v for row in A for v in row] + b:
        bits = significant_bits(value)
        if bits is None or bits > precision:
            raise ValueError(f"Input {value} is not representable at p={precision}")
    if any(A[i][j] != A[j][i] for i in range(n) for j in range(n)):
        raise ValueError("A must be symmetric")
    # Exact LDL^T positivity check, without pivoting.
    L = [[Q(int(i == j)) for j in range(n)] for i in range(n)]
    D: Vector = []
    for j in range(n):
        pivot = A[j][j] - sum((L[j][k]**2 * D[k] for k in range(j)), Q(0))
        if pivot <= 0:
            raise ValueError("A is not positive definite")
        D.append(pivot)
        for i in range(j+1, n):
            L[i][j] = (A[i][j] - sum((L[i][k]*L[j][k]*D[k]
                                       for k in range(j)), Q(0))) / pivot


@dataclass
class Iterate:
    step: int
    x: Vector
    recursive_r: Vector
    true_r: Vector

    @property
    def residual_squared(self) -> Q:
        return exact_dot(self.true_r, self.true_r)

    @property
    def solution_squared(self) -> Q:
        return exact_dot(self.x, self.x)


@dataclass
class Run:
    iterates: list[Iterate]
    status: str
    machine: ErrorMachine
    alpha: list[Q] = field(default_factory=list)
    beta: list[Q] = field(default_factory=list)


def run_cg(A: Sequence[Sequence[Q]], b: Sequence[Q], precision: int,
           policy: Policy = zero_policy) -> Run:
    A = [[Q(v) for v in row] for row in A]
    b = [Q(v) for v in b]
    validate_input(A, b, precision)
    n = len(b)
    machine = ErrorMachine(precision, policy)
    x, r, direction = [Q(0)]*n, b[:], b[:]
    run = Run([Iterate(0, x[:], r[:], b[:])], "step_limit", machine)
    rho = machine.dot(r, r, "rho[0]")
    for j in range(n):
        if not any(r):
            run.status = "zero_recursive_residual"
            break
        q = machine.matvec(A, direction, j)
        denominator = machine.dot(direction, q, f"d[{j}]")
        if not denominator:
            run.status = "zero_denominator_before_alpha"
            break
        alpha = machine.op("/", rho, denominator, f"alpha[{j}].div")
        run.alpha.append(alpha)
        x = machine.axpy(x, alpha, direction, f"x[{j+1}]")
        r = machine.axpy(r, alpha, q, f"r[{j+1}]", subtract=True)
        Ax = exact_matvec(A, x)
        true_r = [bi-ai for bi, ai in zip(b, Ax)]
        run.iterates.append(Iterate(j+1, x[:], r[:], true_r))
        if not any(r):
            run.status = "zero_recursive_residual"
            break
        if j == n-1:
            break
        next_rho = machine.dot(r, r, f"rho[{j+1}]")
        if not rho:
            run.status = "zero_denominator_before_beta"
            break
        beta = machine.op("/", next_rho, rho, f"beta[{j}].div")
        run.beta.append(beta)
        direction = machine.axpy(r, beta, direction, f"p[{j+1}]")
        rho = next_rho
    return run


def failure_margin(it: Iterate, norm_A: Q, norm_b_squared: Q,
                   epsilon: Q) -> Q:
    """Positive result is an exact, sufficient certificate that eta > epsilon.

    (norm_A*||x|| + ||b||)^2 <= 2*(norm_A^2*||x||^2 + ||b||^2).
    The caller must provide a proven upper bound on ||A||_2 (an equality is
    available in every family used by verify.py).
    """
    return (it.residual_squared - 2*epsilon**2
            * (norm_A**2*it.solution_squared + norm_b_squared))


def identity(n: int) -> Matrix:
    return [[Q(int(i == j)) for j in range(n)] for i in range(n)]


def path_outlier(n: int, exponent: int) -> tuple[Matrix, Vector, int, Q, Q]:
    if n < 2 or exponent < 2:
        raise ValueError("Require n >= 2 and exponent >= 2")
    m, T = n-1, 1 << exponent
    A = [[Q(0) for _ in range(n)] for _ in range(n)]
    for i in range(m):
        A[i][i] = Q(1 if i == 0 else 2)
        if i:
            A[i][i-1] = A[i-1][i] = Q(-1)
    A[-1][-1] = Q(T)
    b = [Q(0)]*n
    b[0] = b[-1] = Q(1)
    precision = m*exponent
    K = Q(m*m*T)
    epsilon = 1/(64*K)
    return A, b, precision, K, epsilon
