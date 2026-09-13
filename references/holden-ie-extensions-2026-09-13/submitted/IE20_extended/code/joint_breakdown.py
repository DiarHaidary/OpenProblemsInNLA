"""Joint dimension/conditioning zero-divisor witness, in exact rationals."""
from __future__ import annotations
from fractions import Fraction as Q
from bounds import floor_log2
from envelope_cg import identity


def joint_breakdown(n: int, K: Q):
    """Return A,b,p,actual_K and a rational admissible error policy.

    The active 2-by-2 block uses the first and last indices, so its initial
    nonzero term undergoes n factors (one product and n-1 additions) before
    cancellation with the final column. The remaining block is identity.
    """
    K = Q(K)
    if not isinstance(n, int) or isinstance(n, bool) or n < 2 or K < 15:
        raise ValueError("require integer n >= 2 and K >= 15")
    a = n//2
    p = floor_log2(Q(a)*(K+1)/2)
    u = Q(1, 1 << p)
    t, c = a*u, 1-a*u
    A = identity(n)
    A[0][-1] = A[-1][0] = c
    b = [Q(0)]*n
    b[0], b[-1] = Q(1), Q(-1)
    actual_K = (2-t)/t

    def policy(label, op, x, y, error_bound):
        if label.startswith("q[0,0]."):
            target, increasing = c, False
        elif label.startswith(f"q[0,{n-1}]."):
            target, increasing = Q(1), True
        else:
            return Q(0)
        active = (label.endswith(".mul[0]") or
                  (".add[" in label and not label.endswith(f".add[{n-1}]")))
        if not active:
            return Q(0)
        value = x*y if op == "*" else x+y
        if value <= 0:
            raise ArithmeticError("unexpected nonpositive prefix")
        if increasing:
            factor = min(1+error_bound, target/value)
            if factor < 1:
                raise ArithmeticError("prefix exceeded increasing target")
        else:
            factor = max(1-error_bound, target/value)
            if factor > 1:
                raise ArithmeticError("prefix fell below decreasing target")
        return factor-1

    return A, b, p, actual_K, policy
