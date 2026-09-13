#!/usr/bin/env python3
"""Verify finite-stage IE-27 energy certificates using integer intervals only.

No numerical eigensolver, optimizer, NumPy, SciPy, or floating-point root is
trusted by the proof checks. Acceptance establishes a statement for the supplied
stage count and EVERY positive shift. It does not establish unlisted stages.

Usage: python code/verify.py certificates/q003.json
       python code/verify.py certificates/*.json --json-output results/verified.json
"""
from __future__ import annotations
import argparse
import json
import math
import sys
import time
from pathlib import Path
from typing import Iterable

BITS = 1024
SCALE = 1 << BITS


def ceildiv(a: int, b: int) -> int:
    if b <= 0:
        raise ValueError("ceildiv requires a positive denominator")
    return -((-a) // b)


class I:
    """Closed dyadic interval [lo/2**BITS, hi/2**BITS]."""
    __slots__ = ("lo", "hi")

    def __init__(self, lo: int, hi: int | None = None):
        self.lo, self.hi = int(lo), int(lo if hi is None else hi)
        if self.lo > self.hi:
            raise ValueError("Reversed interval")

    @staticmethod
    def rational(a: int, b: int = 1) -> I:
        if b == 0:
            raise ZeroDivisionError("Zero denominator")
        if b < 0:
            a, b = -a, -b
        return I(a * SCALE // b, ceildiv(a * SCALE, b))

    def __add__(self, other: I) -> I:
        return I(self.lo + other.lo, self.hi + other.hi)

    def __neg__(self) -> I:
        return I(-self.hi, -self.lo)

    def __sub__(self, other: I) -> I:
        return self + (-other)

    def __mul__(self, other: I) -> I:
        products = (self.lo * other.lo, self.lo * other.hi,
                    self.hi * other.lo, self.hi * other.hi)
        return I(min(products) // SCALE, ceildiv(max(products), SCALE))

    def reciprocal(self) -> I:
        if self.lo <= 0 <= self.hi:
            raise ArithmeticError("Interval division through zero")
        # Reciprocal is decreasing on each of (-infinity, 0) and (0, infinity).
        # Python // rounds down, even for negative divisors.
        return I(SCALE * SCALE // self.hi,
                 -((-SCALE * SCALE) // self.lo))

    def __truediv__(self, other: I) -> I:
        return self * other.reciprocal()

    def square(self) -> I:
        high = max(self.lo * self.lo, self.hi * self.hi)
        low = 0 if self.lo <= 0 <= self.hi else min(self.lo*self.lo, self.hi*self.hi)
        return I(low // SCALE, ceildiv(high, SCALE))

    def is_zero(self) -> bool:
        return self.lo == self.hi == 0


ZERO = I(0)
ONE = I(SCALE)
Matrix = list[list[I]]


def zeros(n: int, m: int | None = None) -> Matrix:
    return [[ZERO for _ in range(n if m is None else m)] for _ in range(n)]


def identity(n: int) -> Matrix:
    out = zeros(n)
    for i in range(n):
        out[i][i] = ONE
    return out


def transpose(a: Matrix) -> Matrix:
    return [list(row) for row in zip(*a)]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    n, k, m = len(a), len(b), len(b[0])
    if any(len(row) != k for row in a) or any(len(row) != m for row in b):
        raise ValueError("Matrix dimension mismatch")
    out = zeros(n, m)
    for i in range(n):
        for j in range(k):
            aa = a[i][j]
            if aa.is_zero():
                continue
            for h in range(m):
                bb = b[j][h]
                if not bb.is_zero():
                    out[i][h] = out[i][h] + aa * bb
    return out


def add(a: Matrix, b: Matrix) -> Matrix:
    return [[x+y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def subtract(a: Matrix, b: Matrix) -> Matrix:
    return [[x-y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(t: I, a: Matrix) -> Matrix:
    return [[t*x for x in row] for row in a]


def dot(a: Iterable[I], b: Iterable[I]) -> I:
    z = ZERO
    for x, y in zip(a, b):
        z = z + x*y
    return z


def jacobi_coefficients(q: int) -> list[int]:
    """Ascending coefficients of P_(q-1)^(1,0)(2t-1)."""
    return [(-1)**(q-1-k) * math.comb(q-1, k) * math.comb(q+k, k)
            for k in range(q)]


def polynomial_numerator(coeff: list[int], m: int, bits: int) -> int:
    """Exact numerator of p(m/2**bits), denominator 2**(bits*degree)."""
    value, power = coeff[-1], 0
    for a in reversed(coeff[:-1]):
        power += bits
        value = value*m + (a << power)
    return value


def verified_nodes(data: dict) -> list[I]:
    q, bits = int(data["q"]), int(data["node_bits"])
    if not 2 <= q <= 10000 or not 1 <= bits <= BITS:
        raise ValueError("Unsupported stage count or node precision")
    brackets = data["node_brackets"]
    if len(brackets) != q-1:
        raise ValueError("Need q-1 interior root intervals")
    coeff = jacobi_coefficients(q)
    nodes, previous = [], 0
    for lo_text, hi_text in brackets:
        lo, hi = int(lo_text), int(hi_text)
        if not previous < lo <= hi < (1 << bits):
            raise ValueError("Root intervals must be disjoint and ordered in (0,1)")
        fl = polynomial_numerator(coeff, lo, bits)
        fh = polynomial_numerator(coeff, hi, bits)
        if lo == hi:
            if fl != 0:
                raise ValueError("A point interval is not an exact root")
        elif fl == 0 or fh == 0 or fl*fh >= 0:
            raise ValueError("Root endpoints lack strict opposite signs")
        shift = BITS-bits
        nodes.append(I(lo << shift, hi << shift))
        previous = hi
    # Degree is q-1; q-1 disjoint sign-changing/point intervals account for all
    # roots. Each interval therefore contains precisely one simple real root.
    nodes.append(ONE)
    return nodes


def radau_factors(nodes: list[I]) -> tuple[Matrix, Matrix, list[I]]:
    """Enclose exact B=L^-1, N=U-I, and positive L pivots.

    The report proves the differentiation-matrix formula used here. A rounded
    Butcher matrix supplied by a certificate is never taken on trust.
    """
    q = len(nodes)
    v = []
    for i, ci in enumerate(nodes):
        z = ci
        for j, cj in enumerate(nodes):
            if j != i:
                z = z*(ci-cj)
        v.append(z)
    d = zeros(q)
    for i in range(q):
        for j in range(q):
            if i != j:
                d[i][j] = v[i] / (v[j]*(nodes[i]-nodes[j]))
        d[i][i] = ONE/(I.rational(2)*nodes[i]) if i < q-1 else I.rational(q*q+1, 2)
    l, u = zeros(q), identity(q)
    pivots = []
    for j in range(q):
        for i in range(j, q):
            l[i][j] = d[i][j] - dot(l[i][:j], [u[k][j] for k in range(j)])
        if l[j][j].lo <= 0:
            raise ArithmeticError(f"Could not certify positive L pivot {j+1}")
        pivots.append(l[j][j])
        for h in range(j+1, q):
            u[j][h] = (d[j][h] - dot(l[j][:j], [u[k][h] for k in range(j)]))/l[j][j]
    b = zeros(q)
    for j in range(q):
        for i in range(j, q):
            rhs = ONE if i == j else ZERO
            b[i][j] = (rhs-dot(l[i][j:i], [b[k][j] for k in range(j, i)]))/l[i][i]
    return b, subtract(u, identity(q)), pivots


def positive_ldlt(a: Matrix, label: str) -> list[I]:
    """Certify a symmetric EXACT matrix enclosed by a is positive definite.

    The caller supplies expressions known mathematically to be symmetric.
    Interval LDL^T elimination encloses their exact pivots. A positive lower
    bound on every pivot gives positive definiteness by congruence.
    """
    n = len(a)
    l, pivots = identity(n), []
    for j in range(n):
        p = a[j][j]
        for k in range(j):
            p = p-l[j][k].square()*pivots[k]
        if p.lo <= 0:
            raise ArithmeticError(f"{label}: LDL pivot {j+1} not certified positive")
        pivots.append(p)
        for i in range(j+1, n):
            z = a[i][j]
            for k in range(j):
                z = z-l[i][k]*l[j][k]*pivots[k]
            l[i][j] = z/p
    return pivots


def decimal_lower(x: I, digits: int = 12) -> str:
    """Display only; this downward-rounded string is not a proof decision."""
    m = x.lo*10**digits // SCALE
    sign = "-" if m < 0 else ""
    whole, frac = divmod(abs(m), 10**digits)
    return f"{sign}{whole}.{frac:0{digits}d}"


def verify(path: Path) -> dict:
    start = time.monotonic()
    with path.open(encoding="utf-8") as stream:
        data = json.load(stream)
    if data.get("format") != "IE27-energy-v1":
        raise ValueError("Unknown certificate format")
    q = int(data["q"])
    nodes = verified_nodes(data)
    b, n, l_pivots = radau_factors(nodes)
    denominator = int(data["H_denominator"])
    hd = data["H_numerators"]
    if denominator <= 0 or len(hd) != q or any(len(row) != q for row in hd):
        raise ValueError("Invalid H data")
    if any(int(hd[i][j]) != int(hd[j][i]) for i in range(q) for j in range(q)):
        raise ValueError("H must be exactly symmetric")
    h = [[I.rational(int(a), denominator) for a in row] for row in hd]
    if int(data["t_denominator"]) <= 0:
        raise ValueError("t denominator must be positive")
    t = I.rational(int(data["t_numerator"]), int(data["t_denominator"]))
    if not 0 < t.lo <= t.hi < SCALE:
        raise ValueError("The squared certificate radius must be in (0,1)")
    vd, vden = data["v_numerators"], int(data["v_denominator"])
    if len(vd) != q or vden <= 0:
        raise ValueError("Invalid Rayleigh vector")
    v = [I.rational(int(a), vden) for a in vd]
    nv = [dot(row, v) for row in n]
    nvnorm, vnorm = ZERO, ZERO
    for a, aa in zip(nv, v):
        nvnorm, vnorm = nvnorm+a.square(), vnorm+aa.square()
    gap = nvnorm-t*vnorm
    if vnorm.lo <= 0 or gap.lo <= 0:
        raise ArithmeticError("Rayleigh test did not prove t < ||N||_2^2")
    hb = matmul(h, b)
    energy = add(hb, transpose(hb))
    stein = subtract(scale(t, h), matmul(transpose(n), matmul(h, n)))
    contraction = subtract(identity(q), matmul(transpose(n), n))
    matrices = [("H", h), ("HB+B^T H", energy),
                ("tH-N^T HN", stein), ("I-N^T N", contraction)]
    result = {"file": path.name, "q": q, "status": "VERIFIED",
              "arithmetic_bits": BITS, "node_bits": int(data["node_bits"]),
              "claim": "For every mu>0: rho((I+mu L^-1)^-1 N) <= sqrt(t) < ||N||_2 < 1",
              "t_numerator": str(data["t_numerator"]),
              "t_denominator": str(data["t_denominator"]),
              "L_min_pivot_lower": decimal_lower(min(l_pivots, key=lambda z:z.lo)),
              "Rayleigh_gap_lower": decimal_lower(gap)}
    for label, mat in matrices:
        pp = positive_ldlt(mat, label)
        result[label+"_min_LDL_pivot_lower"] = decimal_lower(min(pp, key=lambda z:z.lo))
    result["seconds"] = round(time.monotonic()-start, 3)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificates", nargs="+", type=Path)
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()
    results, failed = [], False
    for path in args.certificates:
        try:
            result = verify(path)
        except (ValueError, ArithmeticError, KeyError, OSError, TypeError) as exc:
            result = {"file": str(path), "status": "FAILED", "error": str(exc)}
            failed = True
        results.append(result)
        print(json.dumps(result, sort_keys=True), flush=True)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(results, indent=2)+"\n", encoding="utf-8")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
