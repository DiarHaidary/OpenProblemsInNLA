"""Checks for the supplementary exact-posterior identity, not a query bound."""
import unittest
import numpy as np
from scipy.linalg import null_space
from src.weighted_krylov import shifted_kernel_posterior_geometry

class ShiftedPosteriorTests(unittest.TestCase):
    def setUp(self):self.rng=np.random.default_rng(910)

    def test_empty_transcript_posterior(self):
        d,k,h=8,2,.3
        q=np.linalg.qr(self.rng.normal(size=(d,k)),mode='reduced')[0]
        ans=shifted_kernel_posterior_geometry(np.zeros((0,0)),np.zeros((d,0)),q,h)
        np.testing.assert_allclose(ans['K'],np.zeros((d,d)),atol=1e-14)
        np.testing.assert_allclose(ans['R'],np.eye(d),atol=1e-14)
        np.testing.assert_allclose(ans['shorted_R'],np.eye(d-k),atol=1e-13)
        self.assertAlmostEqual(ans['log_density_up_to_constant'],h*k/2,places=12)

    def test_trace_shorting_identity(self):
        for d,k,t in ((8,1,2),(11,3,4)):
            h=.2; j=np.eye(t)+self.rng.normal(size=(t,t)); j=j.T@j+np.eye(t)
            b=self.rng.normal(size=(d,t)); q=np.linalg.qr(self.rng.normal(size=(d,k)),mode='reduced')[0]
            ans=shifted_kernel_posterior_geometry(j,b,q,h)
            lhs=np.trace(ans['shorted_R'])
            rhs=np.trace(ans['R'])-np.trace(np.linalg.solve(q.T@ans['R']@q,q.T@ans['R']@ans['R']@q))
            self.assertAlmostEqual(lhs,rhs,places=11)
            self.assertAlmostEqual(ans['log_density_up_to_constant']-ans['log_density_with_trace_constant'],h/2*np.trace(ans['R']),places=11)

    def test_inertia_equivalence_above_and_below_wall(self):
        d,k,t=9,2,3; h=.3
        j=np.eye(t)*2+self.rng.normal(size=(t,t)); j=j.T@j+np.eye(t)
        b=self.rng.normal(size=(d,t)); q=np.linalg.qr(self.rng.normal(size=(d,k)),mode='reduced')[0]
        ans=shifted_kernel_posterior_geometry(j,b,q,h); v=ans['complement']; wall=h*ans['shorted_R']
        for sign in (1,-1):
            sp=wall+sign*.03*np.eye(d-k)
            self.assertGreater(np.linalg.eigvalsh(sp)[0],0)
            ss=v@sp@v.T
            matrix=np.block([[j,b.T],[b,b@np.linalg.solve(j,b.T)+ss]])
            eig=np.linalg.eigvalsh(matrix)
            self.assertLess(max(abs(eig[:k])),1e-12)
            self.assertEqual(eig[k]>=h,sign>0)

    def test_zero_shift_matches_negative_tilt(self):
        d,k,t=10,3,2
        j=np.eye(t)*3; b=self.rng.normal(size=(d,t)); q=np.linalg.qr(self.rng.normal(size=(d,k)),mode='reduced')[0]
        ans=shifted_kernel_posterior_geometry(j,b,q,0.)
        expected=(1-k)/2*np.linalg.slogdet(np.eye(k)+q.T@ans['K']@q)[1]
        self.assertAlmostEqual(ans['log_density_up_to_constant'],expected,places=13)
        np.testing.assert_allclose(ans['R'],np.eye(d)+ans['K'],atol=1e-13)

    def test_kernel_coordinate_invariance(self):
        d,k,t=9,3,2; h=.1; j=np.eye(t)*2
        b=self.rng.normal(size=(d,t)); q=np.linalg.qr(self.rng.normal(size=(d,k)),mode='reduced')[0]
        o=np.linalg.qr(self.rng.normal(size=(k,k)))[0]
        a=shifted_kernel_posterior_geometry(j,b,q,h)
        c=shifted_kernel_posterior_geometry(j,b,q@o,h)
        self.assertAlmostEqual(a['log_density_up_to_constant'],c['log_density_up_to_constant'],places=12)

    def test_first_exit_pivot_identity(self):
        d,k,t=10,2,3; h=.4
        j=np.eye(t)*3+self.rng.normal(size=(t,t)); j=j.T@j+np.eye(t)
        b=self.rng.normal(size=(d,t)); q=np.linalg.qr(self.rng.normal(size=(d,k)),mode='reduced')[0]
        ans=shifted_kernel_posterior_geometry(j,b,q,h); vv=ans['complement']; r=ans['R']
        gaussian=self.rng.normal(size=(d-k,d-k+1)); w=gaussian@gaussian.T
        ss=vv@(h*ans['shorted_R']+w)@vv.T
        v=self.rng.normal(size=d); v/=np.linalg.norm(v)
        direct=v@(ss-h*r)@v
        rhs=np.linalg.norm(gaussian.T@vv.T@v)**2-h*(q.T@r@v)@np.linalg.solve(q.T@r@q,q.T@r@v)
        self.assertAlmostEqual(direct,rhs,places=11)
        # The full newly queried compression has the same scalar Schur pivot.
        bj=b.T@v; hjj=v@(b@np.linalg.solve(j,b.T)+ss)@v
        pivot=hjj-h-bj@np.linalg.solve(j-h*np.eye(t),bj)
        self.assertAlmostEqual(pivot,direct,places=11)

    def test_compression_domain_is_checked(self):
        with self.assertRaises(ValueError):shifted_kernel_posterior_geometry(np.eye(2),np.zeros((3,2)),np.eye(3)[:,:1],1.)

if __name__=='__main__':unittest.main()
