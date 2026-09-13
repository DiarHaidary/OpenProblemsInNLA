"""Regenerate finite, exact checks for the extended IE-20 manuscript.

No finite report establishes the parameter-uniform analytic upper bound.
Run without -O; checks use assertions. Standard library only.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
from fractions import Fraction as Q
import hashlib
from itertools import product
import json
from pathlib import Path

from bounds import (backward_error_compare, bounds, first_step_upper,
                    scalar_threshold, scalar_worst_error)
from envelope_cg import ErrorMachine, exact_dot, exact_matvec, run_cg, validate_input
from joint_breakdown import joint_breakdown
from polynomials import evaluate, reciprocal_polynomial
from test_extended import first_step, SCALAR_LABELS, SCALAR_NUMERATOR_LABELS


def scalar_checks() -> dict:
    records = []
    for p in (2, 6, 12):
        maximum = Q(0)
        for signs in product((-1, 1), repeat=9):
            mapping = dict(zip(SCALAR_LABELS, signs))
            def policy(label, op, a, b, u):
                return mapping[label]*u
            x, machine = first_step([[Q(1)]], [Q(1)], p, policy)
            assert machine.operations == 9
            maximum = max(maximum, abs(1-x[0])/(1+abs(x[0])))
        assert maximum == scalar_worst_error(p)
        records.append({"precision": p, "corner_schedules": 512,
                        "maximum_eta_exact": str(maximum)})
    thresholds = []
    for eps in (Q(3, 8), Q(1, 10), Q(1, 1000), Q(1, 1 << 40)):
        p = scalar_threshold(eps)
        assert scalar_worst_error(p) <= eps
        assert p == 2 or scalar_worst_error(p-1) > eps
        thresholds.append({"epsilon": str(eps), "exact_threshold": p})
    return {"corner_schedules_checked": 1536, "records": records,
            "threshold_examples": thresholds}


def schedule(kind: str, salt: int = 0):
    def policy(label, op, a, b, u):
        if kind == "zero":
            return Q(0)
        if kind == "plus":
            return u
        if kind == "minus":
            return -u
        digest = hashlib.sha256(f"{salt}:{label}".encode()).digest()
        return (Q(-1), Q(-1, 2), Q(0), Q(1, 2), Q(1))[digest[0] % 5]*u
    return policy


def first_step_checks() -> dict:
    records = []
    policies = [("zero", 0), ("plus", 0), ("minus", 0)] + [("hash", i) for i in range(5)]
    for n, exponent, eps in product((2, 3, 5, 8), (0, 1, 6, 20), (Q(3, 8), Q(7, 16))):
        K = Q(1 << exponent)
        diagonal = [Q(1)] + [1/K]*(n-1)
        A = [[diagonal[i] if i == j else Q(0) for j in range(n)] for i in range(n)]
        b = [Q((-1)**i * (i+1), 1 << (i % 3)) for i in range(n)]
        p = first_step_upper(n, K, eps)
        assert p is not None
        validate_input(A, b, p)
        for kind, salt in policies:
            x, machine = first_step(A, b, p, schedule(kind, salt))
            r = [bi-ai for bi, ai in zip(b, exact_matvec(A, x))]
            comparison = backward_error_compare(exact_dot(r, r), exact_dot(x, x),
                                                Q(1), exact_dot(b, b), eps)
            assert comparison <= 0
            records.append({"n": n, "K": str(K), "epsilon": str(eps),
                            "precision": p, "policy": kind, "salt": salt,
                            "operations": machine.operations,
                            "nonzero_errors": len(machine.faults),
                            "exact_eta_comparison": comparison})
    return {"executions_checked": len(records), "records": records,
            "scope": "finite diagonal inputs and specified schedules, not all errors"}


def polynomial_checks() -> dict:
    grid_checks = 0
    algebra_checks = 0
    records = []
    for k in range(2, 33):
        ell, pi = reciprocal_polynomial(k)
        assert len(pi)-1 < k
        assert pi[0] == Q(ell*ell-1, 3)
        l1 = sum(map(abs, pi), Q(0))
        assert l1 <= 16**(k+1)
        algebra_checks += 1
        maximum = Q(0)
        for j in range(129):
            t = Q(j, 128)
            value = evaluate(pi, t)
            assert value >= Q(1, 2)
            error = 1/value-t
            assert 0 <= error <= Q(3, k*k-1)
            maximum = max(maximum, error)
            grid_checks += 1
        records.append({"k": k, "ell": ell, "degree": len(pi)-1,
                        "coefficient_l1": str(l1), "grid_maximum": str(maximum),
                        "analytic_bound": str(Q(3, k*k-1))})
    return {"polynomials_checked": algebra_checks, "rational_grid_checks": grid_checks,
            "records": records,
            "scope": "coefficient identities and finite grid only; uniform result is a cited lemma"}


def joint_breakdown_checks() -> dict:
    records = []
    for n, K in product((2, 3, 4, 8, 16, 32, 64), (Q(15), Q(255))):
        A, b, p, actual_K, policy = joint_breakdown(n, K)
        assert actual_K <= K
        out = run_cg(A, b, p, policy)
        assert out.status == "zero_denominator_before_alpha"
        assert len(out.iterates) == 1
        assert all(x == 0 for x in out.iterates[0].x)
        records.append({"n": n, "K": str(K), "actual_K": str(actual_K),
                        "precision": p, "status": out.status,
                        "nonzero_errors": len(out.machine.faults),
                        "operations": out.machine.operations})
    return {"witnesses_checked": len(records), "records": records,
            "scope": "finite rational executions of the joint dimension/conditioning witness"}


def dense_matvec_checks() -> dict:
    records = []
    for n in (4, 16, 64):
        h = [[1]]
        while len(h) < n:
            h = [row+row for row in h] + [row+[-v for v in row] for row in h]
        root_n = {4: 2, 16: 4, 64: 8}[n]
        A = [[Q(int(i == j))+Q(h[i][j], 2*root_n) for j in range(n)] for i in range(n)]
        b = [Q((-1)**i*(i+1), 1 << (i % 4)) for i in range(n)]
        for p, kind in product((8, 12), ("zero", "plus", "minus", "hash")):
            validate_input(A, b, p)
            machine = ErrorMachine(p, schedule(kind, 123))
            q = machine.matvec(A, b, 0)
            error = [x-y for x, y in zip(q, exact_matvec(A, b))]
            bound2 = (4*n*machine.u*Q(3, 2))**2 * exact_dot(b, b)
            error2 = exact_dot(error, error)
            assert error2 <= bound2
            records.append({"n": n, "precision": p, "policy": kind,
                            "error_to_bound_squared": str(error2/bound2),
                            "operations": machine.operations})
    return {"executions_checked": len(records), "records": records,
            "scope": "finite dense SPD matvec examples; the general prefix bound is analytic"}


def bound_checks() -> dict:
    parameters = [(1, Q(1 << 40), Q(1, 1000)),
                  (2, Q(1 << 40), Q(1, 1000)),
                  (64, Q(2), Q(1, 1024)),
                  (1000, Q(1 << 60), Q(3, 8)),
                  (256, Q(256**2), Q(1, 256**2)),
                  (10000, Q(1 << 100), Q(1, 100))]
    records = [asdict(bounds(*p)) for p in parameters]
    count = 0
    for n, K, eps in product((1, 2, 4, 16, 64, 256),
                             (Q(1), Q(3, 2), Q(2), Q(16), Q(1 << 30)),
                             (Q(3, 8), Q(1, 16), Q(1, 1024))):
        b = bounds(n, K, eps)
        assert b.lower_bits <= b.best_upper_bits <= b.general_upper_bits
        count += 1
    return {"parameter_triples_checked": count, "illustrative_records": records,
            "scope": "consistency of formula evaluations, not empirical precision thresholds"}


def main() -> None:
    if not __debug__:
        raise RuntimeError("Run without -O: checks use assertions")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("results/extended_checks.json"))
    args = parser.parse_args()
    report = {"arithmetic": "exact Python fractions.Fraction",
              "completion_status": "extended partial mathematical results; not a full solution",
              "scalar": scalar_checks(),
              "first_step": first_step_checks(),
              "polynomial": polynomial_checks(),
              "joint_breakdown": joint_breakdown_checks(),
              "dense_matvec": dense_matvec_checks(),
              "bounds": bound_checks(),
              "all_checks_passed": True}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print("PASS: 1536 scalar sign-corner executions")
    print(f"PASS: {report['first_step']['executions_checked']} first-step executions")
    print(f"PASS: {report['polynomial']['polynomials_checked']} polynomial constructions; "
          f"{report['polynomial']['rational_grid_checks']} rational grid checks")
    print(f"PASS: {report['bounds']['parameter_triples_checked']} parameter-bound consistency checks")
    print(f"PASS: {report['joint_breakdown']['witnesses_checked']} joint breakdown witnesses")
    print(f"PASS: {report['dense_matvec']['executions_checked']} dense matvec prefix-bound checks")
    print(f"Report written to {args.output}")


if __name__ == "__main__":
    main()
