"""Regression tests of exact algebra and bound-evaluation utilities.

These tests do not certify the universal analytic proofs.
"""
from __future__ import annotations
from fractions import Fraction as Q
from itertools import product
import unittest

from bounds import (backward_error_compare, bounds, ceil_log2, ceil_sqrt,
                    first_step_max_squared, first_step_upper, floor_log2,
                    scalar_threshold, scalar_worst_error)
from envelope_cg import (ErrorMachine, exact_dot, exact_matvec, run_cg,
                         significant_bits, validate_input)
from joint_breakdown import joint_breakdown
from polynomials import evaluate, reciprocal_polynomial


def first_step(A, b, precision, policy):
    """Evaluate the specified operations only as far as the produced x1."""
    machine = ErrorMachine(precision, policy)
    rho = machine.dot(b, b, "rho[0]")
    q = machine.matvec(A, b, 0)
    d = machine.dot(b, q, "d[0]")
    if d == 0:
        raise ZeroDivisionError("first denominator")
    alpha = machine.op("/", rho, d, "alpha[0].div")
    x = machine.axpy([Q(0)]*len(b), alpha, b, "x[1]")
    return x, machine


SCALAR_NUMERATOR_LABELS = {
    "rho[0].mul[0]", "rho[0].add[0]", "alpha[0].div",
    "x[1][0].mul", "x[1][0].add"
}
SCALAR_DENOMINATOR_LABELS = {
    "q[0,0].mul[0]", "q[0,0].add[0]", "d[0].mul[0]", "d[0].add[0]"
}
SCALAR_LABELS = sorted(SCALAR_NUMERATOR_LABELS | SCALAR_DENOMINATOR_LABELS)


class ExtendedTests(unittest.TestCase):
    def test_exact_logarithms(self):
        for numerator in range(1, 81):
            for denominator in range(1, 41):
                q = Q(numerator, denominator)
                c, f = ceil_log2(q), floor_log2(q)
                pow2 = lambda k: Q(1 << k) if k >= 0 else Q(1, 1 << (-k))
                self.assertGreaterEqual(pow2(c), q)
                self.assertLess(pow2(c-1), q)
                self.assertLessEqual(pow2(f), q)
                self.assertGreater(pow2(f+1), q)

    def test_exact_square_root_ceiling(self):
        for numerator in range(0, 100):
            for denominator in range(1, 12):
                q = Q(numerator, denominator)
                a = ceil_sqrt(q)
                self.assertGreaterEqual(a*a, q)
                if a:
                    self.assertLess((a-1)**2, q)

    def test_scalar_operation_labels(self):
        x, machine = first_step([[Q(1)]], [Q(1)], 4,
                               lambda label, op, a, b, u: u)
        self.assertEqual(machine.operations, 9)
        self.assertEqual({f["label"] for f in machine.faults}, set(SCALAR_LABELS))
        self.assertEqual(x, [Q(17, 16)])  # five factors divided by four

    def test_scalar_extremizer(self):
        def policy(label, op, a, b, u):
            return -u if label in SCALAR_NUMERATOR_LABELS else u
        for p in (2, 3, 6, 12, 40):
            x, machine = first_step([[Q(1)]], [Q(1)], p, policy)
            eta = abs(1-x[0])/(1+abs(x[0]))
            self.assertEqual(eta, scalar_worst_error(p))
            self.assertEqual(len(machine.faults), 9)

    def test_scalar_all_corners(self):
        for p in (2, 6, 12):
            maximum = Q(0)
            for signs in product((-1, 1), repeat=9):
                mapping = dict(zip(SCALAR_LABELS, signs))
                def policy(label, op, a, b, u):
                    return mapping[label]*u
                x, _ = first_step([[Q(1)]], [Q(1)], p, policy)
                maximum = max(maximum, abs(1-x[0])/(1+abs(x[0])))
            self.assertEqual(maximum, scalar_worst_error(p))

    def test_scalar_threshold_and_equality(self):
        for p in range(4, 28):
            epsilon = scalar_worst_error(p)
            self.assertLess(epsilon, Q(1, 2))
            self.assertEqual(scalar_threshold(epsilon), p)
            self.assertEqual(scalar_threshold(epsilon-Q(1, 1 << (10*p))), p+1)
        for exponent in range(2, 80):
            epsilon = Q(1, 1 << exponent)
            p = scalar_threshold(epsilon)
            self.assertLessEqual(scalar_worst_error(p), epsilon)
            if p > 2:
                self.assertGreater(scalar_worst_error(p-1), epsilon)

    def test_scalar_input_scaling(self):
        def policy(label, op, a, b, u):
            return -u if label in SCALAR_NUMERATOR_LABELS else u
        for a in (Q(1, 8), Q(3, 2), Q(1 << 20)):
            for b in (Q(-3, 8), Q(1), Q(1 << 25)):
                x, _ = first_step([[a]], [b], 8, policy)
                eta = abs(b-a*x[0])/(a*abs(x[0])+abs(b))
                self.assertEqual(eta, scalar_worst_error(8))

    def test_backward_comparator(self):
        # All quantities have rational square roots here, for independent checks.
        for r, x, a, b, eps in product(
                (Q(0), Q(1, 3), Q(2)), (Q(0), Q(1, 2), Q(3)),
                (Q(1, 4), Q(2)), (Q(1), Q(3, 2)), (Q(1, 8), Q(3, 8))):
            eta = r/(a*x+b)
            expected = (eta > eps)-(eta < eps)
            self.assertEqual(backward_error_compare(r*r, x*x, a, b*b, eps), expected)
        self.assertEqual(backward_error_compare(Q(1, 4), Q(0), Q(1), Q(1), Q(1, 2)), 0)

    def test_first_step_maximum_identity(self):
        # Exact algebraic square identity underlying the endpoint maximum.
        for a, t in product((Q(1), Q(1, 2), Q(1, 8), Q(1, 100)),
                            (Q(0), Q(1, 4), Q(1, 2), Q(1))):
            M2 = (1-a)**2/(8*(1+a))
            gap = M2-(1-t)*(t-a)/(1+t)**2
            square = (a*t-3*a+3*t-1)**2/(8*(1+a)*(1+t)**2)
            self.assertEqual(gap, square)
            self.assertEqual(M2, first_step_max_squared(1/a))

    def test_first_step_bound_domain(self):
        self.assertIsNotNone(first_step_upper(3, Q(1), Q(1, 100)))
        self.assertIsNone(first_step_upper(3, Q(100), Q(1, 8)))
        for K in (Q(1), Q(2), Q(100), Q(1 << 100)):
            p = first_step_upper(4, K, Q(3, 8))
            self.assertIsNotNone(p)
            self.assertLessEqual(p, ceil_log2(32768*5*K))

    def test_bound_order_and_capping(self):
        for n, K, eps in product((1, 2, 4, 16, 64, 256),
                                 (Q(1), Q(3, 2), Q(2), Q(16), Q(1 << 30)),
                                 (Q(3, 8), Q(1, 16), Q(1, 1024))):
            report = bounds(n, K, eps)
            self.assertLessEqual(report.lower_bits, report.best_upper_bits)
            self.assertLessEqual(report.best_upper_bits, report.general_upper_bits)
            self.assertLessEqual(report.proof_horizon, n)
        eps, n = Q(1, 16), 16
        a = bounds(n, Q(1 << 30), eps)
        b = bounds(n, Q(1 << 60), eps)
        self.assertEqual(a.H, b.H)
        self.assertEqual(a.proof_horizon, b.proof_horizon)
        self.assertEqual(b.general_upper_bits-a.general_upper_bits, 30)

    def test_reciprocal_polynomial_algebra(self):
        for k in range(2, 33):
            ell, coefficients = reciprocal_polynomial(k)
            self.assertLess(len(coefficients)-1, k)
            self.assertEqual(coefficients[0], Q(ell*ell-1, 3))
            self.assertLessEqual(sum(map(abs, coefficients)), 16**(k+1))
            # Finite checks only; the uniform reciprocal bound is cited and proved analytically.
            for j in range(65):
                t = Q(j, 64)
                value = evaluate(coefficients, t)
                self.assertGreaterEqual(value, Q(1, 2))
                self.assertGreaterEqual(1/value-t, 0)
                self.assertLessEqual(1/value-t, Q(3, k*k-1))

    def test_joint_breakdown_witnesses(self):
        for n, K in product((2, 3, 4, 8, 16, 32, 64), (Q(15), Q(255))):
            A, b, p, actual_K, policy = joint_breakdown(n, K)
            self.assertGreaterEqual(p, 2)
            self.assertLessEqual(actual_K, K)
            self.assertLessEqual(significant_bits(A[0][-1]), p)
            out = run_cg(A, b, p, policy)
            self.assertEqual(out.status, "zero_denominator_before_alpha")
            self.assertEqual(len(out.iterates), 1)
            self.assertGreater(p+1, floor_log2(Q(n)*K/8))

    def test_joint_breakdown_invalid(self):
        for n, K in ((1, 15), (2, 14), (True, 15)):
            with self.assertRaises(ValueError):
                joint_breakdown(n, K)

    def test_dense_matvec_prefix_bound(self):
        for n in (4, 16):
            h = [[1]]
            while len(h) < n:
                h = [row+row for row in h] + [row+[-v for v in row] for row in h]
            root_n = ceil_sqrt(Q(n))
            A = [[Q(int(i == j))+Q(h[i][j], 2*root_n) for j in range(n)]
                 for i in range(n)]
            b = [Q((-1)**i*(i+1), 1 << (i % 4)) for i in range(n)]
            for p in (8, 12):
                validate_input(A, b, p)
                for sign in (-1, 0, 1):
                    machine = ErrorMachine(p, lambda label, op, a, b, u: sign*u)
                    q = machine.matvec(A, b, 0)
                    exact = exact_matvec(A, b)
                    err = [x-y for x, y in zip(q, exact)]
                    # A=I+H/(2sqrt(n)) has norm exactly 3/2.
                    bound_squared = (4*n*machine.u*Q(3, 2))**2 * exact_dot(b, b)
                    self.assertLessEqual(exact_dot(err, err), bound_squared)

    def test_invalid_parameters(self):
        for args in ((0, 1, Q(1, 8)), (True, 1, Q(1, 8)),
                     (2, Q(1, 2), Q(1, 8)), (2, 1, Q(1, 2)), (2, 1, 0)):
            with self.assertRaises(ValueError):
                bounds(*args)
        with self.assertRaises(ValueError):
            ceil_log2(0)
        with self.assertRaises(ValueError):
            ceil_sqrt(-1)


if __name__ == "__main__":
    unittest.main()
