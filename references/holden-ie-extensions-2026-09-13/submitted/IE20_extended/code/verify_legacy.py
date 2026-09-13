"""Reproduce exact IE-20 counterexamples; no third-party dependencies.

Usage: python code/verify.py [--output results/exact_checks.json]
This is exact rational verification of particular witnesses, not formal
verification of an asymptotic theorem or of the upper-bound proof.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

from envelope_cg import (failure_margin, identity, path_outlier, run_cg,
                         significant_bits)


def rational_summary(value: Q) -> dict:
    encoded = f"{value.numerator:x}/{value.denominator:x}".encode("ascii")
    return {"sign": (value > 0) - (value < 0),
            "numerator_bits": abs(value.numerator).bit_length(),
            "denominator_bits": value.denominator.bit_length(),
            "sha256": hashlib.sha256(encoded).hexdigest()}


def verify_identity(n: int = 32, precision: int = 6) -> dict:
    A, b = identity(n), [Q(1)] + [Q(0)]*(n-1)
    epsilon = Q(1, 10)
    def policy(label, op, a, b, u):
        return u if label.startswith("q[0,0].add[") else Q(0)
    run = run_cg(A, b, precision, policy)
    t = (1 + Q(1, 1 << precision))**n
    eta = (t-1)/(t+1)
    assert len(run.iterates) == 2
    assert run.status == "zero_recursive_residual"
    assert run.iterates[-1].x[0] == 1/t
    assert run.iterates[-1].true_r[0] == 1-1/t
    assert eta > epsilon
    return {"family": "identity", "n": n, "precision": precision,
            "epsilon": str(epsilon), "eta_exact": str(eta),
            "status": run.status, "operation_count": run.machine.operations,
            "nonzero_error_count": len(run.machine.faults), "all_assertions_passed": True}


def verify_breakdown(n: int = 4, precision: int = 8) -> dict:
    A, b = identity(n), [Q(1), Q(-1)] + [Q(0)]*(n-2)
    u = Q(1, 1 << precision)
    A[0][1] = A[1][0] = 1-u
    bad_labels = {"q[0,0].mul[0]", "q[0,1].mul[1]"}
    def policy(label, op, a, b, u):
        return -u if label in bad_labels else Q(0)
    run = run_cg(A, b, precision, policy)
    assert len(run.iterates) == 1
    assert run.status == "zero_denominator_before_alpha"
    return {"family": "breakdown", "n": n, "precision": precision,
            "condition_number_exact": str((2-u)/u), "eta_at_only_iterate": "1",
            "status": run.status, "operation_count": run.machine.operations,
            "faults": run.machine.faults, "all_assertions_passed": True}


def verify_outlier(n: int, exponent: int) -> dict:
    A, b, precision, K, epsilon = path_outlier(n, exponent)
    label_to_fault = f"rho[0].add[{n-1}]"
    def policy(label, op, a, b, u):
        return u if label == label_to_fault else Q(0)
    run = run_cg(A, b, precision, policy)
    assert len(run.iterates) == n+1, (n, exponent, run.status)
    assert run.status == "step_limit"
    assert len(run.machine.faults) == 1
    T = Q(1 << exponent)
    certificates = []
    for it in run.iterates:
        assert it.true_r == it.recursive_r
        margin = failure_margin(it, T, Q(2), epsilon)
        assert margin > 0, (n, exponent, it.step)
        certificates.append({"step": it.step, "failure_margin": rational_summary(margin),
                             "residual_squared": rational_summary(it.residual_squared)})
    high = run.iterates[-1].true_r[-1]
    # Optional numerical display only; certificate signs above use exact rationals.
    displayed_high = float(high)
    max_bits = max(significant_bits(a) or 0 for row in A for a in row)
    return {"family": "path_outlier", "n": n, "exponent": exponent,
            "T": str(T), "precision": precision, "K_upper_bound": str(K),
            "epsilon": str(epsilon), "stored_matrix_max_significand_bits": max_bits,
            "condition_bound_proof": "kappa(A) <= (n-1)^2*T via inverse bidiagonal factor",
            "status": run.status, "operation_count": run.machine.operations,
            "faults": run.machine.faults,
            "last_high_residual_display_only": displayed_high,
            "twice_signed_last_high_display_only": 2*((-1)**n)*displayed_high,
            "certificates": certificates, "all_assertions_passed": True}


def main() -> None:
    if not __debug__:
        raise RuntimeError("Run without -O: exact certificate checks use assertions")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("results/exact_checks.json"))
    args = parser.parse_args()
    checks = [verify_identity(), verify_breakdown()]
    for n in range(2, 11):
        print(f"Exact path/outlier check: n={n}, exponent=12", flush=True)
        checks.append(verify_outlier(n, 12))
    for exponent in (4, 8, 16, 24):
        print(f"Exact asymptotic sample: n=6, exponent={exponent}", flush=True)
        checks.append(verify_outlier(6, exponent))
    report = {
        "arithmetic": "Python Fraction, exact rational operations",
        "model": "IE-20 adversarial relative-error envelope, not IEEE round-to-nearest",
        "scope": "Finite exact certificates only; analytic arguments are in the recovered manuscript",
        "hash_encoding": "ASCII signed hexadecimal numerator / positive hexadecimal denominator",
        "all_checks_passed": True, "number_of_witnesses": len(checks), "checks": checks}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(f"PASS: {len(checks)} witnesses; report written to {args.output}")


if __name__ == "__main__":
    main()
