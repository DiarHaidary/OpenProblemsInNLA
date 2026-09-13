"""Exact, conservative evaluations of the IE-20 bounds in the manuscript.

Only the scalar function returns the *exact* threshold. General upper and
lower bounds need not match. No floating-point logarithms are used.

Example:
    python code/bounds.py --n 16 --K 256 --epsilon 1/256
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from fractions import Fraction as Q
from math import isqrt


def ceil_log2(q: Q) -> int:
    """Smallest integer k with 2**k >= q, for positive rational q."""
    q = Q(q)
    if q <= 0:
        raise ValueError("logarithm argument must be positive")
    n, d = q.numerator, q.denominator
    k = n.bit_length() - d.bit_length()
    below = n <= (d << k) if k >= 0 else (n << (-k)) <= d
    return k if below else k + 1


def floor_log2(q: Q) -> int:
    return -ceil_log2(1 / Q(q))


def ceil_sqrt(q: Q) -> int:
    q = Q(q)
    if q < 0:
        raise ValueError("square-root argument must be nonnegative")
    a = isqrt(q.numerator // q.denominator)
    return a if a*a*q.denominator == q.numerator else a+1


def check_parameters(n: int, K: Q, epsilon: Q) -> tuple[Q, Q]:
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("n must be a positive integer")
    K, epsilon = Q(K), Q(epsilon)
    if K < 1:
        raise ValueError("K must be at least one")
    if not 0 < epsilon < Q(1, 2):
        raise ValueError("epsilon must be strictly between zero and one half")
    return K, epsilon


def scalar_worst_error(precision: int) -> Q:
    """Exact worst backward error of the scalar first iterate."""
    if precision < 2:
        raise ValueError("IE-20 requires precision >= 2")
    u = Q(1, 1 << precision)
    a, b = (1 + u)**4, (1 - u)**5
    return (a - b) / (a + b)


def scalar_threshold(epsilon: Q) -> int:
    """Exact P_CG(1,K,epsilon), independent of the parameter K."""
    _, epsilon = check_parameters(1, Q(1), epsilon)
    hi = max(2, ceil_log2(16 / epsilon))
    # The following guard keeps this routine valid independently of any
    # particular analytic constant used to initialize the search.
    while scalar_worst_error(hi) > epsilon:
        hi *= 2
    lo = 2
    while lo < hi:
        mid = (lo + hi) // 2
        if scalar_worst_error(mid) <= epsilon:
            hi = mid
        else:
            lo = mid + 1
    return lo


def first_step_max_squared(K: Q) -> Q:
    K = Q(K)
    if K < 1:
        raise ValueError("K must be at least one")
    return (K-1)**2 / (8*K*(K+1))


def first_step_upper(n: int, K: Q, epsilon: Q) -> int | None:
    """The one-step sufficient precision, or None if epsilon <= M(K).

    Compares epsilon - 512(n+1) K 2^-p with M(K) by exact squaring.
    This is not claimed to be the exact threshold for n > 1.
    """
    K, epsilon = check_parameters(n, K, epsilon)
    M2 = first_step_max_squared(K)
    if epsilon**2 <= M2:
        return None
    C = 512*(n+1)*K
    def enough(p: int) -> bool:
        t = epsilon - C / (1 << p)
        return t >= 0 and t*t >= M2
    hi = max(2, ceil_log2(2*C/epsilon))
    while not enough(hi):
        hi *= 2
    lo = 2
    while lo < hi:
        mid = (lo + hi)//2
        if enough(mid):
            hi = mid
        else:
            lo = mid+1
    return lo


def capped_backward_horizon(n: int, epsilon: Q) -> int:
    """min(n, ceil((64/epsilon)**(2/3))) by integer comparisons."""
    epsilon = Q(epsilon)
    if n <= 2 or n**3 * epsilon**2 < 4096:
        return n
    lo, hi = 2, n
    while lo < hi:
        mid = (lo+hi)//2
        if mid**3 * epsilon**2 >= 4096:
            hi = mid
        else:
            lo = mid+1
    return lo


@dataclass(frozen=True)
class BoundReport:
    n: int
    K: str
    epsilon: str
    lower_bits: int
    general_upper_bits: int
    first_step_upper_bits: int | None
    best_upper_bits: int
    scalar_exact_bits: int | None
    H: str
    D: str
    chebyshev_horizon_capped_at_n: int
    backward_horizon_capped_at_n: int
    proof_horizon: int
    general_upper_rounding: str = (
        "ceil(log2(prefactor)) + exponent*ceil(log2(D)); "
        "a conservative integer upper, not the exact ceiling of their sum"
    )
    completion_status: str = "general bounds may not match; not a full solution"


def bounds(n: int, K: Q, epsilon: Q) -> BoundReport:
    K, epsilon = check_parameters(n, K, epsilon)
    H = min(K, 64/epsilon**2)
    D = 1024*H**2
    Kbar = max(Q(2), K)
    kC = min(n, ceil_sqrt(Kbar)*ceil_log2(16*Kbar/epsilon))
    kU = capped_backward_horizon(n, epsilon)
    m = min(n, kC, kU)
    exponent = 12*m+20
    prefactor = 1024*(n+1)*K/epsilon**2
    general = max(2, ceil_log2(prefactor)+exponent*ceil_log2(D))
    lower = max(2, 1+floor_log2(Q(n, 1)/(4*epsilon)))
    if n >= 2:
        lower = max(lower, floor_log2(K+1))
        if K >= 15:
            lower = max(lower, 1+floor_log2(Q(n//2)*(K+1)/2))
    first = first_step_upper(n, K, epsilon)
    candidates = [general]
    if first is not None:
        candidates.append(first)
    if K == 1:
        # This explicit tighter constant is from the recovered aI proof.
        candidates.append(max(2, ceil_log2(128*(n+1)/epsilon)))
    scalar = scalar_threshold(epsilon) if n == 1 else None
    if scalar is not None:
        lower = scalar
        candidates.append(scalar)
    return BoundReport(n, str(K), str(epsilon), lower, general, first,
                       min(candidates), scalar, str(H), str(D), kC, kU, m)


def backward_error_compare(residual_squared: Q, x_squared: Q,
                           norm_A: Q, b_squared: Q, epsilon: Q) -> int:
    """Return sign(eta-epsilon), with no square roots or approximations.

    norm_A must be the exact spectral norm, not merely an upper bound.
    Squared norms must be nonnegative and b_squared positive.
    """
    R2, X2, a, B2, eps = map(Q, (residual_squared, x_squared,
                                  norm_A, b_squared, epsilon))
    if R2 < 0 or X2 < 0 or a <= 0 or B2 <= 0 or eps <= 0:
        raise ValueError("invalid norm or tolerance")
    C = R2/eps**2 - a*a*X2 - B2
    cross2 = 4*a*a*X2*B2
    if C < 0:
        return -1
    if C == 0:
        return 0 if cross2 == 0 else -1
    return (C*C > cross2) - (C*C < cross2)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--K", type=Q, required=True)
    parser.add_argument("--epsilon", type=Q, required=True)
    args = parser.parse_args()
    try:
        report = bounds(args.n, args.K, args.epsilon)
    except (ValueError, ZeroDivisionError) as exc:
        parser.error(str(exc))
    print(json.dumps(asdict(report), indent=2))


if __name__ == "__main__":
    main()
