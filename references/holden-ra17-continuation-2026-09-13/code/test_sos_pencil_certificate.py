"""Exact positive and negative controls for the optional saved-certificate checker.

The accepted fixture is a real quaternion pencil with determinant ||x||^4.
The two rejected attack fixtures use an independent five-parameter real pencil
that contains a nonzero rank-one matrix. No numerical proposal or SDP is used.
"""
from copy import deepcopy
from itertools import combinations
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import json
import unittest
import sympy as s
import sos_pencil_certificate as checker

def pencil_input(xs,A):
    ijs=list((I,J) for I in combinations(range(4),3) for J in combinations(range(4),3))
    fs=[s.expand(A.extract(I,J).det()) for I,J in ijs]
    return {},xs,A,ijs,fs

def quaternion_fixture():
    xs=s.symbols('x0:4');a,b,c,d=xs
    A=s.Matrix([[a,-b,-c,-d],[b,a,-d,c],[c,d,a,-b],[d,-c,b,a]])
    inp=pencil_input(xs,A);ijs=inp[3]
    es=checker.exponents(4,2)
    G=s.diag(*[1 if 2 in e else 2 for e in es])
    hs=[]
    for I,J in ijs:
        i=next(v for v in range(4) if v not in I)
        j=next(v for v in range(4) if v not in J)
        hs.append(str((-1)**(i+j)*A[i,j]/4))
    norm=sum(x*x for x in xs)
    if A.T*A!=norm*s.eye(4):raise AssertionError('Invalid quaternion fixture')
    obj={'degree':4,'monomials':es,'gram':[[str(v) for v in G.row(i)] for i in range(G.rows)],
         'minor_indices':ijs,'multipliers':hs}
    return inp,obj

def bad_fixture():
    xs=s.symbols('x0:5');A=s.diag(*xs[:4]);A[0,1]=xs[4]
    inp=pencil_input(xs,A)
    if A.subs(dict(zip(xs,[1,0,0,0,0]))).rank()!=1:raise AssertionError('Missing rank-one witness')
    return inp

class CertificateTests(unittest.TestCase):
    def verify(self,inp,obj):
        with TemporaryDirectory() as folder:
            path=Path(folder)/'certificate.json';path.write_text(json.dumps(obj))
            with patch.object(checker,'input_pencil',return_value=inp):return checker.verify(path)

    def test_accept_exact_quaternion_certificate(self):
        inp,obj=quaternion_fixture();result=self.verify(inp,obj)
        self.assertEqual(result['status'],'EXACTLY_VERIFIED')
        self.assertEqual(result['gram_dimension'],10)
        self.assertTrue(all(s.Rational(v)>0 for v in result['positive_pivots']))

    def test_reject_missing_monomial_coverage(self):
        inp=bad_fixture();obj={'degree':6,'monomials':[[1,1,1,0,0]],'gram':[['1']],
              'minor_indices':inp[3],'multipliers':[str(inp[4][0])]+['0']*15}
        with self.assertRaisesRegex(ValueError,'complete monomial'):self.verify(inp,obj)

    def test_reject_rational_function_with_full_coverage(self):
        inp=bad_fixture();xs=inp[1];es=checker.exponents(5,2)
        poly=sum(checker.monomial(xs,e)**2 for e in es)
        obj={'degree':4,'monomials':es,'gram':[[str(v) for v in s.eye(15).row(i)] for i in range(15)],
             'minor_indices':inp[3],'multipliers':[str(poly/inp[4][0])]+['0']*15}
        with self.assertRaises(ValueError):self.verify(inp,obj)

    def test_reject_degree_and_exponent_metadata(self):
        inp,obj=quaternion_fixture()
        for degree in (0,2,5,10,4.0,True,'4'):
            bad=deepcopy(obj);bad['degree']=degree
            with self.subTest(degree=degree),self.assertRaises(ValueError):self.verify(inp,bad)
        for exponent in (-1,0.5,True,'1',100):
            bad=deepcopy(obj);bad['monomials']=[list(e) for e in bad['monomials']];bad['monomials'][0][0]=exponent
            with self.subTest(exponent=exponent),self.assertRaises(ValueError):self.verify(inp,bad)

    def test_reject_duplicate_basis_monomial(self):
        inp,obj=quaternion_fixture();obj['monomials'][0]=obj['monomials'][1]
        with self.assertRaisesRegex(ValueError,'exactly once'):self.verify(inp,obj)

    def test_reject_invalid_gram(self):
        inp,obj=quaternion_fixture()
        for value in (0.5,True,'1/0','sqrt(2)','1.0'):
            bad=deepcopy(obj);bad['gram'][0][0]=value
            with self.subTest(value=value),self.assertRaises(ValueError):self.verify(inp,bad)
        bad=deepcopy(obj);bad['gram'][0][1]='1'
        with self.assertRaisesRegex(ValueError,'symmetric'):self.verify(inp,bad)
        bad=deepcopy(obj);bad['gram'].pop()
        with self.assertRaisesRegex(ValueError,'dimensions'):self.verify(inp,bad)

    def test_reject_nonpositive_gram_despite_exact_identity(self):
        inp,obj=quaternion_fixture()
        obj['gram']=[[str(-s.Rational(v)) for v in row] for row in obj['gram']]
        obj['multipliers']=[f'-({h})' for h in obj['multipliers']]
        with self.assertRaisesRegex(ValueError,'positive definite'):self.verify(inp,obj)

    def test_reject_corrupted_identity(self):
        inp,obj=quaternion_fixture();obj['multipliers'][0]='0'
        with self.assertRaisesRegex(ValueError,'polynomial combination'):self.verify(inp,obj)

    def test_reject_invalid_multiplier_domain(self):
        inp,obj=quaternion_fixture()
        for value in ('sqrt(2)*x0','unknown*x0','0.5*x0','1/x0','x0**(-1)','1','x0**100',
                      '__import__("os").system("false")'):
            bad=deepcopy(obj);bad['multipliers'][0]=value
            with self.subTest(value=value),self.assertRaises(ValueError):self.verify(inp,bad)

    def test_reject_minor_metadata(self):
        inp,obj=quaternion_fixture();obj['minor_indices']=obj['minor_indices'][:-1]
        with self.assertRaisesRegex(ValueError,'minor-index count'):self.verify(inp,obj)

if __name__=='__main__':unittest.main(verbosity=2)
