"""Basic regression tests for the exact error-envelope executor."""
from fractions import Fraction as Q
import unittest
from envelope_cg import ErrorMachine, identity, run_cg, significant_bits
from verify_legacy import verify_identity, verify_breakdown, verify_outlier

class EnvelopeTests(unittest.TestCase):
    def test_binary_significands(self):
        self.assertEqual(significant_bits(Q(1, 1 << 100)), 1)
        self.assertEqual(significant_bits(Q(255, 256)), 8)
        self.assertIsNone(significant_bits(Q(1, 3)))
        self.assertEqual(significant_bits(Q(0)), 0)
        self.assertEqual(significant_bits(Q(-12)), 2)

    def test_error_on_addition_of_zero(self):
        machine = ErrorMachine(3, lambda label, op, a, b, u: u)
        self.assertEqual(machine.op("+", Q(1), Q(0), "add"), Q(9, 8))
        self.assertEqual(machine.op("*", Q(0), Q(1), "mul"), Q(0))

    def test_error_validation(self):
        machine = ErrorMachine(3, lambda label, op, a, b, u: 2*u)
        with self.assertRaises(ValueError):
            machine.op("+", Q(1), Q(1), "bad")

    def test_exact_identity(self):
        result = run_cg(identity(3), [Q(1), Q(2), Q(3)], 2)
        self.assertEqual(len(result.iterates), 2)
        self.assertEqual(result.iterates[-1].true_r, [Q(0)]*3)
        self.assertEqual(result.status, "zero_recursive_residual")

    def test_exact_path_termination(self):
        A = [[Q(1), Q(-1), Q(0)], [Q(-1), Q(2), Q(-1)],
             [Q(0), Q(-1), Q(2)]]
        result = run_cg(A, [Q(1), Q(0), Q(0)], 2)
        self.assertEqual(result.iterates[-1].x, [Q(3), Q(2), Q(1)])
        self.assertEqual(result.alpha, [Q(1)]*3)
        self.assertEqual(result.beta, [Q(1)]*2)

    def test_identity_witness(self):
        self.assertTrue(verify_identity()["all_assertions_passed"])

    def test_breakdown_witness(self):
        self.assertTrue(verify_breakdown()["all_assertions_passed"])

    def test_outlier_witness(self):
        self.assertTrue(verify_outlier(5, 8)["all_assertions_passed"])

    def test_reject_unrepresentable_input(self):
        with self.assertRaises(ValueError):
            run_cg([[Q(1)]], [Q(1, 3)], 10)

    def test_reject_indefinite_input(self):
        with self.assertRaises(ValueError):
            run_cg([[Q(1), Q(2)], [Q(2), Q(1)]], [Q(1), Q(0)], 2)

if __name__ == "__main__":
    unittest.main()
