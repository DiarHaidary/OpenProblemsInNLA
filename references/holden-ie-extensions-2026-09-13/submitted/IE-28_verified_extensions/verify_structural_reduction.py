"""Exact, finite checks; this script is not a general-existence proof."""
import itertools
import json
import sympy as s

def check_nodes(nodes):
    c = [s.Rational(x) for x in nodes]
    n = len(c)
    V = s.Matrix([[x**k for k in range(n)] for x in c])
    Q = s.diag(*c) * V * s.diag(*[s.Rational(1,k) for k in range(1,n+1)]) * V.inv()
    w = [1/s.prod(c[i]-c[j] for j in range(n) if j != i) for i in range(n)]
    T = s.diag(*[c[i]/w[i] for i in range(n)])
    B = s.Matrix(n,n,lambda i,j: 1/(c[i]-c[j]) if i != j else
                 1/c[i] + sum(1/(c[i]-c[k]) for k in range(n) if k != i))
    assert (T.inv()*Q.inv()*T-B).applyfunc(s.simplify) == s.zeros(n)
    assert s.simplify(B.det()-s.factorial(n)/s.prod(c)) == 0
    x = s.symbols('x0:'+str(n))
    van = s.prod(x)*s.prod(x[j]-x[i] for i in range(n) for j in range(i+1,n))
    sub = dict(zip(x,c))
    for k in range(n+1):
        for S in itertools.combinations(range(n),k):
            rhs = van
            for i in S: rhs = s.diff(rhs,x[i])
            rhs = rhs.subs(sub)/van.subs(sub)
            lhs = B.extract(S,S).det() if S else s.Integer(1)
            assert s.simplify(lhs-rhs) == 0
    return {'nodes':[str(v) for v in c], 'all_exact_checks_passed':True}

cases = [check_nodes(v) for v in [(1,), (1,2), (1,2,4),
                                  (s.Rational(1,7),s.Rational(2,5),s.Rational(3,4),1)]]
B0 = s.Matrix([[1,4,4],[-4,1,4],[-4,-4,1]])
assert B0+B0.T == 2*s.eye(3)
assert B0.det() == 49
for S in itertools.combinations(range(3),2):
    assert B0.extract(S,S).det() == 17
assert 17**3 > 49**2
print(json.dumps({'collocation_checks':cases,
                  'auxiliary_counterexample_verified':True,
                  'counterexample_is_to_IE28':False,
                  'global_IE28_existence_proved':False},indent=2))
