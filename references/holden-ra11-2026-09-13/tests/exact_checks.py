"""Exact rational / Gaussian-rational identities. No floating-point assertions."""
from __future__ import annotations
import itertools
import json
from pathlib import Path
import random
import time
import sympy as s

ROOT = Path(__file__).resolve().parents[1]


def kron(vectors):
    out = s.Matrix([1])
    for v in vectors:
        out = s.kronecker_product(out, v)
    return out


def contract_except(y, vectors, keep):
    n, q = len(vectors[0]), len(vectors)
    out = s.zeros(n, 1)
    for index in itertools.product(range(n), repeat=q):
        flat, weight = 0, s.Integer(1)
        for j, a in enumerate(index):
            flat = flat*n + a
            if j != keep:
                weight *= vectors[j][a]
        out[index[keep]] += weight*y[flat]
    return out


def complex_interpolation():
    rng = random.Random(1701)
    cases = []
    for n, q in [(2,2),(2,3),(2,4),(2,5),(2,6),(3,2),(3,3)]:
        a = [s.Matrix([rng.randint(-3,3) for _ in range(n)]) for _ in range(q)]
        b = [s.Matrix([rng.randint(-3,3) for _ in range(n)]) for _ in range(q)]
        expected = kron([x+s.I*y for x,y in zip(a,b)]).expand()
        got = s.zeros(n**q,1)
        for j in range(q+1):
            weight = s.prod((s.I-k)/s.Integer(j-k) for k in range(q+1) if k != j)
            got += weight*kron([x+j*y for x,y in zip(a,b)])
        assert all(s.expand(v) == 0 for v in got-expected)
        cases.append({"n":n,"q":q,"real_queries":q+1})
    return cases


def conjecture_counterexample():
    cases = []
    unit_pairs = [(s.Rational(3,5),s.Rational(4,5)),
                  (s.Rational(5,13),s.Rational(12,13)),
                  (s.Rational(-8,17),s.Rational(15,17))]
    for q in range(2,9):
        N = 2**q
        d = s.zeros(N,q+1)
        for a in range(N):
            d[a,a.bit_count()] = 1
        vandermonde = s.Matrix([[s.Integer(j)**k for j in range(q+1)] for k in range(q+1)])
        assert vandermonde.det() != 0
        # V = D * Vandermonde consists only of real product-vector columns.
        for j in [0,1,q]:
            assert d*vandermonde[:,j] == kron([s.Matrix([1,j])]*q)
        z = s.Matrix([s.I**a.bit_count() for a in range(N)])
        real, imag = s.re(z), s.im(z)
        assert (real.T*real)[0] == 2**(q-1)
        assert (imag.T*imag)[0] == 2**(q-1)
        assert (real.T*imag)[0] == 0
        gram_inv = s.diag(*[s.Rational(1,s.binomial(q,k)) for k in range(q+1)])
        assert d*gram_inv*d.T*real == real
        assert d*gram_inv*d.T*imag == imag
        u = kron([s.Matrix(unit_pairs[j%3]) for j in range(q)])
        phase_identity = (real.T*u)[0]**2+(imag.T*u)[0]**2
        assert s.factor(phase_identity) == 1
        projection_sq = ((d.T*u).T*gram_inv*(d.T*u))[0]
        bound = s.Rational(1,2**(q-1))
        assert projection_sq >= bound
        cases.append({"q":q,"span_dimension":q+1,"guaranteed_projection_sq":str(bound),
                      "checked_projection_sq":str(projection_sq)})
    return cases


def exact_product_recovery():
    rng = random.Random(1711)
    cases = []
    for n,q,singular in [(2,2,False),(3,2,False),(3,3,False),(4,2,False),(3,3,True),(3,1,False)]:
        factors = []
        for i in range(q):
            cols = n-1 if singular else n
            c = s.Matrix(n,cols,[rng.randint(-2,3) for _ in range(n*cols)])
            a = c*c.T
            if not singular:
                a += s.eye(n)
            if a == s.zeros(n):
                a[0,0] = 1
            factors.append(a)
        M = s.kronecker_product(*factors)
        g = [s.Matrix([1+j+i for j in range(n)]) for i in range(q)]
        # If a reference happens to lie in a factor kernel, change it deterministically.
        for i in range(q):
            if (g[i].T*factors[i]*g[i])[0] == 0:
                j = next(j for j in range(n) if factors[i][j,j] != 0)
                g[i] = s.eye(n)[:,j]
        calls = 0
        def oracle(vectors):
            nonlocal calls
            calls += 1
            return M*kron(vectors)
        y = oracle(g)
        gamma = (kron(g).T*y)[0]
        b = [contract_except(y,g,i)/gamma for i in range(q)]
        actual_B = [a/(v.T*a*v)[0] for a,v in zip(factors,g)]
        assert all(bi == B*gi for bi,B,gi in zip(b,actual_B,g))
        pivots = [next(j for j in reversed(range(n)) if gi[j] != 0) for gi in g]
        indices = [[j for j in range(n) if j != p] for p in pivots]
        input_columns = [[gi] for gi in g]
        output_columns = [[bi] for bi in b]
        for j in range(n-1):
            targets = [s.eye(n)[:,indices[i][j]] for i in range(q)]
            alpha = [1-(bi.T*v)[0] for bi,v in zip(b,targets)]
            w = [v+c*gi for v,c,gi in zip(targets,alpha,g)]
            assert all((bi.T*wi)[0] == 1 for bi,wi in zip(b,w))
            yy = oracle(w)
            values = [contract_except(yy,g,i)/gamma-alpha[i]*b[i] for i in range(q)]
            for i in range(q):
                assert values[i] == actual_B[i]*targets[i]
                input_columns[i].append(targets[i]); output_columns[i].append(values[i])
        recovered = [s.Matrix.hstack(*output_columns[i])*s.Matrix.hstack(*input_columns[i]).inv()
                     for i in range(q)]
        assert recovered == actual_B
        assert gamma*s.kronecker_product(*recovered) == M
        trace = gamma*s.prod(s.trace(B) for B in recovered)
        assert trace == s.trace(M)
        assert calls == n
        cases.append({"n":n,"q":q,"singular_factors":singular,"queries":calls,"trace":str(trace)})
    return cases



def exact_shift_edge_cases():
    """The shift must work when targets or local contractions are zero."""
    n, q = 3, 3
    factors = [s.diag(1, 0, 2), s.Matrix([[2,1,0],[1,3,0],[0,0,1]]), s.diag(0,4,0)]
    g = [s.ones(n,1) for _ in range(q)]
    M = s.kronecker_product(*factors)
    gamma = (kron(g).T*M*kron(g))[0]
    B = [a/(gi.T*a*gi)[0] for a,gi in zip(factors,g)]
    b = [a*gi for a,gi in zip(B,g)]
    targets = [s.zeros(n,1), s.Matrix([b[1][1],-b[1][0],0]), s.Matrix([1,0,-1])]
    assert all((bi.T*v)[0] == 0 for bi,v in zip(b,targets))
    alpha = [1-(bi.T*v)[0] for bi,v in zip(b,targets)]
    w = [v+a*gi for v,a,gi in zip(targets,alpha,g)]
    y = M*kron(w)
    recovered = [contract_except(y,g,i)/gamma-alpha[i]*b[i] for i in range(q)]
    assert recovered == [a*v for a,v in zip(B,targets)]
    return {"n":n,"q":q,"zero_targets_and_contractions":"passed",
            "singular_PSD_factors":"passed","additional_queries":1}


def exact_low_rank():
    rng = random.Random(1901)
    n,q,N = 2,3,8
    cases=[]
    for rank in range(1,5):
        c = s.Matrix(N,rank,[rng.randint(-3,3) for _ in range(N*rank)])
        assert c.rank() == rank
        M = c*c.T
        for attempt in range(100):
            X = s.Matrix.hstack(*[kron([s.Matrix([rng.randint(-4,4) for _ in range(n)])
                                       for _ in range(q)]) for _ in range(rank)])
            K = X.T*M*X
            if K.det() != 0:
                break
        else:
            raise AssertionError("Test data generator failed.")
        Y=M*X
        assert Y*K.inv()*Y.T == M
        cases.append({"rank":rank,"queries_in_identity":rank,"trace":str(s.trace(M))})
    return cases


def analytic_log_density_derivative():
    y,a,k = s.symbols('y a k',positive=True)
    logf = y + (k/2-1)*s.log(s.exp(y)-a) - (s.exp(y)-a)/2
    expected = -(k/2-1)*a*s.exp(y)/(s.exp(y)-a)**2-s.exp(y)/2
    assert s.simplify(s.diff(logf,y,2)-expected) == 0
    return "Second derivative identity verified symbolically; it is nonpositive for k >= 2."


def main():
    started=time.perf_counter()
    results={"arithmetic":"SymPy exact rational and Gaussian-rational arithmetic",
             "interpolation":complex_interpolation(),
             "conjecture_counterexample":conjecture_counterexample(),
             "parallel_product_recovery":exact_product_recovery(),
             "shift_edge_cases":exact_shift_edge_cases(),
             "low_rank_reconstruction":exact_low_rank(),
             "log_density":analytic_log_density_derivative()}
    results['all_checks_passed']=True
    results['elapsed_seconds']=round(time.perf_counter()-started,3)
    (ROOT/'results'/'exact_checks.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__':
    main()
