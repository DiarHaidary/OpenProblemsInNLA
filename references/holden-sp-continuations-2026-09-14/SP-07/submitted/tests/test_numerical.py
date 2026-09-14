import sys,unittest
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from completion import formula,canonical,optimal_angles,compressed_optimal,twirl_overlap,fourier,norm

class NumericalTests(unittest.TestCase):
    def test_canonical_attainment(self):
        rng=np.random.default_rng(931511)
        for p in [3,5,7,9,17,33]:
            for j in range(20):
                lam=np.r_[1,rng.uniform(-1,1,p-1)]
                if j==0:lam[1::2]=-1
                if j==1:lam[1::2]=1
                D,U=canonical(lam)
                self.assertLess(norm(U@U-np.eye(2*p-1)),1e-12)
                self.assertAlmostEqual(norm(D@U+U@D),formula(lam),places=11)
    def test_random_complement_lower_bound(self):
        rng=np.random.default_rng(931512)
        for p in [3,5,7,9,11]:
            for _ in range(30):
                lam=np.r_[1,rng.uniform(-1,1,p-1)]
                C=rng.normal(size=(p-1,p-1))+1j*rng.normal(size=(p-1,p-1))
                D,U=canonical(lam,C)
                self.assertGreaterEqual(norm(D@U+U@D)+1e-10,formula(lam))
    def test_all_angle_minimum(self):
        rng=np.random.default_rng(931513)
        for p in range(3,52,2):
            lam=np.cos(2*optimal_angles(p));D,U=canonical(lam)
            target=2*np.sin(np.pi/(2*p))
            self.assertAlmostEqual(formula(lam),target,places=12)
            self.assertAlmostEqual(norm(D@U+U@D),target,places=11)
            for _ in range(10):
                x=np.r_[1,rng.uniform(-1,1,p-1)]
                self.assertGreaterEqual(formula(x)+1e-12,target)
    def test_compressed_optimizer(self):
        for p in range(3,52,2):
            lam=compressed_optimal(p);D,U=canonical(lam)
            H=D@U+U@D
            self.assertAlmostEqual(norm(H[:p,:p]),2/p,places=12)
            self.assertAlmostEqual(norm(H),2/np.sqrt(p),places=11)
    def test_noncirculant_twirl(self):
        rng=np.random.default_rng(931514)
        for p in [3,5,7,9]:
            F=fourier(p);ds=np.diag(np.exp(2j*np.pi*np.arange(p)/p))
            for _ in range(30):
                W=np.linalg.qr(rng.normal(size=(p,p))+1j*rng.normal(size=(p,p)))[0]
                lam=np.r_[1,rng.uniform(-1,1,p-1)];v=W[:,0]
                X=(W*lam)@W.conj().T;Y=W[:,1:]*np.sqrt(1-lam[1:]**2)
                U=np.block([[X,Y],[Y.conj().T,-np.diag(lam[1:])]])
                C=rng.normal(size=(p-1,p-1))+1j*rng.normal(size=(p-1,p-1))
                D=np.block([[ds,np.zeros((p,p-1))],[np.zeros((p-1,p)),C]])
                Z=twirl_overlap(X,v)
                self.assertLess(norm(Z-Z.conj().T),1e-12)
                self.assertLess(norm(Z-np.roll(np.roll(Z,1,0),1,1)),1e-12)
                self.assertLess(np.linalg.norm(Z@np.ones(p)-np.ones(p)),1e-12)
                zz=F.conj().T@Z@F
                self.assertLess(norm(zz-np.diag(np.diag(zz))),1e-12)
                self.assertLessEqual(formula(np.diag(zz).real),norm(D@U+U@D)+1e-10)
    def test_explicit_twirl_dilation(self):
        rng=np.random.default_rng(931515)
        for p in [3,5,7]:
            for _ in range(5):
                W=np.linalg.qr(rng.normal(size=(p,p))+1j*rng.normal(size=(p,p)))[0]
                lam=np.r_[1,rng.uniform(-1,1,p-1)];v=W[:,0]
                X=(W*lam)@W.conj().T;Y=W[:,1:]*np.sqrt(1-lam[1:]**2)
                U=np.block([[X,Y],[Y.conj().T,-np.diag(lam[1:])]])
                C=rng.normal(size=(p-1,p-1))+1j*rng.normal(size=(p-1,p-1))
                n=2*p-1;omega=np.exp(2j*np.pi/p)
                ds=np.diag(omega**np.arange(p));D=np.zeros((n,n),complex);D[:p,:p]=ds;D[p:,p:]=C
                DD=np.zeros((p*n,p*n),complex);UU=np.zeros_like(DD);J=np.zeros((p*n,p),complex)
                for g in range(p):
                    perm=np.r_[np.roll(np.arange(p),g),np.arange(p,n)]
                    # P^g acts by cyclically shifting selected rows and columns.
                    Ug=U[np.ix_(perm,perm)];Dg=omega**g*D[np.ix_(perm,perm)]
                    UU[g*n:(g+1)*n,g*n:(g+1)*n]=Ug
                    DD[g*n:(g+1)*n,g*n:(g+1)*n]=Dg
                    for i in range(p):J[g*n+i,i]=np.roll(v,g)[i]
                self.assertLess(norm(J.conj().T@J-np.eye(p)),1e-12)
                self.assertLess(norm(DD@J-J@ds),1e-11)
                self.assertLess(norm(DD.conj().T@J-J@ds.conj().T),1e-11)
                self.assertLess(norm(J.conj().T@UU@J-twirl_overlap(X,v)),1e-12)
                self.assertAlmostEqual(norm(DD@UU+UU@DD),norm(D@U+U@D),places=10)
    def test_phase_multiplier_identity(self):
        rng=np.random.default_rng(931516)
        sx=np.array([[0,1],[1,0]],complex);sz=np.diag([1.,-1.]);I=np.eye(2)
        for _ in range(600):
            B,C=rng.uniform(0,2,2);ph,th=rng.uniform(-8,8,2);speed=rng.normal()
            Y=B/2*I+C/2*sz
            W=1j*np.sin(ph)*I+np.cos(ph)*sx
            V=np.exp(-.5j*th)*W
            Vp=np.exp(-.5j*th)*(-.5j*W+speed*(1j*np.cos(ph)*I-np.sin(ph)*sx))
            H=-1j*Vp+.5*V+1j*(Y@V+V@Y)
            expected=np.sqrt(speed*speed+B*B)+C*abs(np.sin(ph))
            self.assertAlmostEqual(norm(H),expected,places=11)
    def test_invalid_inputs(self):
        for lam in [[1,0],[0,0,0],[1,2,0],[1,float('nan'),0]]:
            with self.assertRaises(ValueError):formula(lam)
        with self.assertRaises(ValueError):canonical([1,0,0],np.zeros((3,3)))

if __name__=='__main__':unittest.main()
