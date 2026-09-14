import copy,json,random,sys,unittest
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT))
from rational_quadrature import sqrt_bounds,pi_bounds,integral_bounds,atan_bounds,require
from model_certificate import verify_spec
from verify_polygon import audit_order

class ExactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec=json.loads((ROOT/'certificates/model_parameters.json').read_text())
    def test_square_root_enclosures(self):
        rng=random.Random(931501)
        for _ in range(1200):
            q=F(rng.randrange(10**9),rng.randrange(1,10**9))
            a,b=sqrt_bounds(q,48)
            self.assertLessEqual(a*a,q);self.assertGreaterEqual(b*b,q)
            self.assertLessEqual(b-a,F(1,2**48))
        self.assertEqual(sqrt_bounds(F(9,4),64),(F(3,2),F(3,2)))
    def test_pi_and_arctangent(self):
        lo,hi=pi_bounds()
        self.assertGreater(lo,F(314159265358979323846,10**20))
        self.assertLess(hi,F(314159265358979323847,10**20))
        a,b=atan_bounds(F(1,5),4)
        c,d=atan_bounds(F(1,5),5)
        self.assertLessEqual(a,c);self.assertGreaterEqual(b,d)
    def test_model_certificate(self):
        out=verify_spec(self.spec)
        self.assertEqual(out['status'],'PASS')
        self.assertLess(F(out['actual_infinite_ratio_upper']),1)
    def test_refinement_compatible(self):
        b=F(self.spec['b']);c=F(self.spec['c'])
        a0,a1,_=integral_bounds(b,c,16,12)
        b0,b1,_=integral_bounds(b,c,32,12)
        self.assertLessEqual(a0,b0);self.assertGreaterEqual(a1,b1)
    def test_false_lower_rejected(self):
        s=copy.deepcopy(self.spec);s['formal_lower']='1038/1000';s['formal_upper']='104/100'
        with self.assertRaises(ValueError):verify_spec(s)
    def test_false_upper_rejected(self):
        s=copy.deepcopy(self.spec);s['formal_lower']='1';s['formal_upper']='1037/1000'
        with self.assertRaises(ValueError):verify_spec(s)
    def test_invalid_domains_rejected(self):
        for changes in [{'b':'4/5','c':'1/2'},{'b':'-1/5'}, {'cells':0},
                        {'degree':0},{'bits':3},{'schema':'incorrect'},
                        {'formal_lower':'2','formal_upper':'1'}]:
            s=copy.deepcopy(self.spec);s.update(changes)
            with self.assertRaises((ValueError,KeyError,TypeError)):verify_spec(s)
    def test_polygon_orders(self):
        for p in range(3,204,2):
            out=audit_order(p)
            self.assertEqual(F(out['completed_norm_squared_over_R_squared']),F(4,p))
    def test_bad_polygon_orders(self):
        for p in [0,1,2,4,6,2.5]:
            with self.assertRaises(ValueError):audit_order(p)
    def test_explicit_checks_not_assert_statements(self):
        with self.assertRaises(ValueError):require(False,'intentional rejection')
        with self.assertRaises(ValueError):sqrt_bounds(F(-1),32)

if __name__=='__main__':unittest.main()
