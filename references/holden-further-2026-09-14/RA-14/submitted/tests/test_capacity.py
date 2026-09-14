import math
import sys
import unittest
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from capacity import (orth, null, minimum_energy_certificate, chebyshev_data,
    allocate, nodal_capacity, first_moment_bound, pure_top_dimension,
    graph_basis, residual, householder_map, simulate_coordinate_policy)

class CapacityTests(unittest.TestCase):
    def setUp(self):
        self.rng = np.random.default_rng(71423)

    def test_full_rank_optimal_coefficients(self):
        t = self.rng.normal(size=(2, 5)); w = self.rng.normal(size=(9, 5))
        result = minimum_energy_certificate(t, w, np.eye(2))
        np.testing.assert_allclose(t @ result.coefficients, np.eye(2), atol=1e-11)
        np.testing.assert_allclose((w @ result.coefficients).T @ (w @ result.coefficients), result.minimum_energy, atol=1e-10)

    def test_energy_minimum_is_loewner(self):
        t = self.rng.normal(size=(2, 5)); w = self.rng.normal(size=(9, 5))
        r = minimum_energy_certificate(t, w, np.eye(2))
        change = null(t) @ self.rng.normal(size=(3, 2))
        trial = r.coefficients + change
        difference = (w @ trial).T @ (w @ trial) - r.minimum_energy
        self.assertGreaterEqual(np.linalg.eigvalsh(difference).min(), -1e-10)

    def test_successful_graph_has_target_residual(self):
        a, tau, k = 2.0, 1.2, 2
        tail_values = np.linspace(-0.9, 0.9, 9)
        e = tau*tau - tail_values**2; delta = a*a-tau*tau
        t = self.rng.normal(size=(k, 5)); w = self.rng.normal(size=(9, 5))
        r = minimum_energy_certificate(t, w, delta*np.eye(k))
        t *= math.sqrt(2*delta/np.linalg.eigvalsh(r.capacity).min())
        r = minimum_energy_certificate(t, w, delta*np.eye(k))
        z = graph_basis(t, np.sqrt(e)[:, None]*w, r.coefficients)
        self.assertGreater(r.criterion_margin, 0)
        self.assertLessEqual(residual(np.r_[np.full(k,a), tail_values], z), tau+1e-10)

    def test_unsuccessful_graph_violates_target(self):
        a, tau, k = 2.0, 1.2, 2
        tail_values = np.linspace(-0.9, 0.9, 9)
        e = tau*tau-tail_values**2; delta=a*a-tau*tau
        t = self.rng.normal(size=(k,5)); w=self.rng.normal(size=(9,5))
        r=minimum_energy_certificate(t,w,delta*np.eye(k))
        t *= math.sqrt(0.5*delta/np.linalg.eigvalsh(r.capacity).min())
        r=minimum_energy_certificate(t,w,delta*np.eye(k))
        z=graph_basis(t,np.sqrt(e)[:,None]*w,r.coefficients)
        self.assertLess(r.criterion_margin,0)
        self.assertGreater(residual(np.r_[np.full(k,a),tail_values],z),tau+1e-7)

    def test_singular_tail_free_direction(self):
        t=np.array([[1.,0.,1.],[0.,1.,0.]])
        w=np.array([[0.,1.,0.],[0.,0.,1.]])
        r=minimum_energy_certificate(t,w,np.eye(2))
        self.assertEqual(r.free_rank,1)
        np.testing.assert_allclose(t@r.coefficients,np.eye(2),atol=1e-12)
        np.testing.assert_allclose((w@r.coefficients).T@(w@r.coefficients),r.minimum_energy,atol=1e-12)

    def test_every_top_direction_can_be_free(self):
        t=np.eye(2);w=np.zeros((3,2))
        r=minimum_energy_certificate(t,w,4*np.eye(2))
        self.assertEqual(r.free_rank,2)
        np.testing.assert_allclose(r.minimum_energy,0,atol=1e-12)
        np.testing.assert_allclose(t@r.coefficients,np.eye(2),atol=1e-12)

    def test_rank_deficient_top_is_rejected(self):
        r=minimum_energy_certificate(np.ones((2,3)),np.eye(3),np.eye(2))
        self.assertFalse(r.feasible_top)

    def test_anisotropic_leading_excess(self):
        t=np.diag([2.,3.]);w=np.eye(2);d1=np.diag([3.,8.])
        r=minimum_energy_certificate(t,w,d1)
        self.assertAlmostEqual(r.criterion_margin,1)

    def test_nodal_formula_matches_feature_matrix(self):
        degree,width,k=3,2,2
        _,e,ell,_=chebyshev_data(degree,.07)
        blocks=[self.rng.normal(size=(7,width)) for _ in range(degree+1)]
        g0=self.rng.normal(size=(k,width))
        top=np.hstack([lj*g0 for lj in ell])
        w=np.zeros((28,8))
        for j,gj in enumerate(blocks): w[7*j:7*j+7,2*j:2*j+2]=gj/np.sqrt(e[j])
        result=minimum_energy_certificate(top,w,np.eye(k))
        np.testing.assert_allclose(result.capacity,nodal_capacity(g0,blocks,e,ell),rtol=1e-10,atol=1e-10)

    def test_cardinal_weights_interpolate_monomials(self):
        for d in [1,2,5,9]:
            nodes,_,ell,_=chebyshev_data(d,.03)
            a=1.06
            for j in range(d+1):
                self.assertAlmostEqual(float(ell@nodes**j),a**j,places=9)

    def test_weighted_mass_bound(self):
        for d in [1,2,5,10,20]:
            for epsilon in [.00001,.01,.1,.49]:
                _,_,_,mass=chebyshev_data(d,epsilon)
                bound=10*math.sqrt(epsilon)*math.log(math.e*d)*math.exp(2*d*math.sqrt(epsilon))
                self.assertLessEqual(mass,bound*(1+1e-10))

    def test_integer_allocation_spends_exact_dimension(self):
        nodes,e,ell,m=allocate(600,3,5,12,.02)
        self.assertEqual(int(m.sum()),597)
        self.assertTrue(np.all(m>=7))
        self.assertEqual(len(nodes),13)

    def test_allocation_rejects_insufficient_dimension(self):
        with self.assertRaises(ValueError): allocate(30,3,5,12,.02)

    def test_first_moment_bound_is_exact_expression(self):
        m=np.array([8,9]);e=np.array([.2,.3]);ell=np.array([2.,-1.])
        got=first_moment_bound(2,m,e,ell,.4)
        expected=2/.4*(4*.2/5+.3/6)
        self.assertAlmostEqual(got,expected)

    def test_infinite_inverse_moment_is_rejected(self):
        with self.assertRaises(ValueError): first_moment_bound(2,np.array([3]),np.ones(1),np.ones(1),1)

    def test_reciprocal_chi_square_gamma_identity(self):
        for degrees in range(3,30):
            val=math.gamma(degrees/2-1)/(2*math.gamma(degrees/2))
            self.assertAlmostEqual(val,1/(degrees-2),places=12)

    def test_pure_top_dimension_deficits(self):
        self.assertEqual(pure_top_dimension(2,3,np.array([3,3,3])),0)
        self.assertEqual(pure_top_dimension(2,3,np.array([2,3,3])),1)
        self.assertEqual(pure_top_dimension(2,3,np.array([2,2,3])),2)

    def test_actual_free_dimension_matches_deficits(self):
        width,k=4,3
        for m in ([5,5,5],[3,5,5],[2,3,5],[1,1,5]):
            blocks=[self.rng.normal(size=(mi,width)) for mi in m]
            kernels=np.hstack([null(g) for g in blocks])
            g0=self.rng.normal(size=(k,width))
            self.assertEqual(orth(g0@kernels).shape[1],pure_top_dimension(k,width,np.array(m)))

    def test_dimension_saturation_implies_pure_top(self):
        for width,k,m in [(4,2,[3,3,3]),(5,3,[4,4,4,4]),(3,1,[2,2])]:
            self.assertGreaterEqual(len(m)*width,k+sum(m))
            self.assertEqual(pure_top_dimension(k,width,np.array(m)),k)

    def test_continuous_threshold_at_sixteen(self):
        z=16.
        log_value=math.log(400)+2*math.log(1+z)-.75*z
        self.assertLess(log_value,0)
        self.assertLess(2/(1+z)-.75,0)

    def test_householder_maps_and_preserves_orthogonality(self):
        u=self.rng.normal(size=12);u/=np.linalg.norm(u)
        v=self.rng.normal(size=12);v/=np.linalg.norm(v)
        h=householder_map(u,v)
        np.testing.assert_allclose(h@u,v,atol=1e-12)
        np.testing.assert_allclose(h.T@h,np.eye(12),atol=1e-12)

    def test_householder_fixes_preexisting_span(self):
        known=np.eye(12)[:,:4]
        u=np.r_[np.zeros(4),self.rng.normal(size=8)];u/=np.linalg.norm(u)
        v=np.r_[np.zeros(4),self.rng.normal(size=8)];v/=np.linalg.norm(v)
        h=householder_map(u,v)
        np.testing.assert_allclose(h@known,known,atol=1e-12)

    def test_rotating_simulator_preserves_complete_transcript(self):
        q,_=np.linalg.qr(self.rng.normal(size=(24,24)))
        a=q@np.diag(np.linspace(-1,1.1,24))@q.T
        out=simulate_coordinate_policy(a,6,123)
        self.assertEqual(out['query_count'],6)
        self.assertLessEqual(out['innovation_count'],6)
        self.assertLess(out['transcript_error'],1e-9)
        self.assertLess(out['span_error'],1e-9)
        self.assertLess(out['orthogonality_error'],1e-9)

    def test_known_span_queries_do_not_require_new_start(self):
        q,_=np.linalg.qr(self.rng.normal(size=(24,24)))
        a=q@np.diag(np.linspace(-1,1.1,24))@q.T
        out=simulate_coordinate_policy(a,6,321)
        self.assertEqual(out['innovation_count'],3)

if __name__=='__main__': unittest.main(verbosity=2)
