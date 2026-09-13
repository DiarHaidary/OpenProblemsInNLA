"""Exact finite checks for the fourth RA-01 note.

Run from any directory: python code/verify_exact.py
Only the Python standard library is used. These checks are not a formal proof.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from math import comb, factorial, prod
from pathlib import Path
import json
import time
from exact_rpcholesky import (Matrix, diagonal, householder_conjugate,
                             trace, update, spike, contraction, fraction_record)

ROOT = Path(__file__).resolve().parents[1]
COUNTS: Counter[str] = Counter()


def check(group: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(f"Exact check failed in {group}")
    COUNTS[group] += 1


def elementary(values: list[F]) -> list[F]:
    e = [F(1)] + [F(0)] * len(values)
    for x in values:
        for j in range(len(values), 0, -1):
            e[j] += x * e[j-1]
    return e


def levels(a: Matrix):
    """Actual RP probabilities, merging subsets after checking residual equality."""
    n = len(a)
    residuals = {0: a}
    probabilities = {0: F(1)}
    result = []
    for step in range(n+1):
        check('probability_normalization', sum(probabilities.values(), F(0)) == 1)
        result.append({s: (p, residuals[s]) for s, p in probabilities.items()})
        if step == n:
            break
        nxt: dict[int, F] = {}
        for mask, p in probabilities.items():
            r = residuals[mask]
            t = trace(r)
            if t == 0:
                check('termination', all(x == 0 for row in r for x in row))
                nxt[mask] = nxt.get(mask, F(0)) + p
                continue
            conditional = F(0)
            for j in range(n):
                if not r[j][j]:
                    continue
                b = update(r, j)
                sm = mask | (1 << j)
                if sm in residuals:
                    check('order_independence', b == residuals[sm])
                else:
                    residuals[sm] = b
                w = r[j][j]/t
                conditional += w*trace(b)
                nxt[sm] = nxt.get(sm, F(0)) + p*w
            trsquare = sum((x*x for row in r for x in row), F(0))
            check('one_step_trace_identity', conditional == t-trsquare/t)
        probabilities = nxt
    return result


def matrix_cases() -> list[dict]:
    specs = [
        ('geometric_rank_one_dense', 1, [F(10000)], [F(1, 2**j) for j in range(5)], 'geometric', True),
        ('geometric_rank_two_dense', 2, [F(10000), F(7)], [F(1, 2**j) for j in range(6)], 'geometric', True),
        ('geometric_rank_three_dense', 3, [F(10**6), F(100), F(2)], [F(1, 2**j) for j in range(5)], 'geometric', True),
        ('geometric_rank_two_diagonal', 2, [F(10000), F(7)], [F(1, 2**j) for j in range(6)], 'geometric', False),
        ('inverse_square_dense', 2, [F(100000), F(2)], [F(1, j*j) for j in range(1, 6)], 'square', True),
        ('inverse_cube_dense', 2, [F(10000), F(2)], [F(1, j**3) for j in range(1, 6)], 'cube', True),
        ('singular_dense', 2, [F(5), F(1)], [F(0)]*3, 'zero', True),
    ]
    records = []
    for name, rank, head, tail, kind, dense in specs:
        spectrum = head+tail
        n = len(spectrum)
        a = (householder_conjugate(spectrum, list(range(1, n+1))) if dense
             else diagonal(spectrum))
        lvls = levels(a)
        means = [sum((p*trace(R) for p, R in L.values()), F(0)) for L in lvls]
        taus = [sum(spectrum[j:], F(0)) for j in range(n+1)]
        e = elementary(spectrum)
        tau = taus[rank]
        for k, L in enumerate(lvls):
            for p, R in L.values():
                check('spectral_tail_lower_bound', trace(R) >= taus[k])
            if k:
                check('mean_monotonicity', means[k] <= means[k-1])
            if k >= rank and tau == 0:
                check('zero_tail_recovery', means[k] == 0)
            if k and tau:
                check('scalar_contraction', means[k] <= contraction(means[k-1], tau, rank))
            if k <= rank or not tau:
                continue
            m = k-rank
            den = prod(taus[:rank])
            M = F(factorial(k))*e[k]/(den*tau**m)
            for v in [F(1, 2), F(1), F(2), F(4)]:
                prob = sum((p for p,R in L.values() if trace(R)>v*tau), F(0))
                check('determinant_path_probability_bound', prob <= M/v**m)
            if m > 1:
                check('integrated_path_bound', (means[k]/tau)**m <= F(m,m-1)**m*M)
            if kind == 'geometric':
                Mgeo = F(4*factorial(k))*(1+F(1,2**m))**rank*F(1,2**(m*(m-1)//2))
                check('geometric_prefactor', M <= Mgeo)
                if m>1:
                    check('integrated_geometric_bound', (means[k]/tau)**m <= F(m,m-1)**m*Mgeo)
            if kind == 'square':
                Msq = F(factorial(k)*10**m, factorial(2*m+1))*(1+F(10,(2*m+2)**2))**rank
                check('inverse_square_prefactor', M <= Msq)
                if m>1:
                    check('integrated_inverse_square_bound', (means[k]/tau)**m <= F(m,m-1)**m*Msq)
        check('exact_recovery', means[-1] == 0)
        records.append({'name':name, 'dimension':n, 'target_rank':rank,
                        'tail_type':kind, 'eigenvalues':list(map(str,spectrum)),
                        'expected_traces':list(map(str,means)),
                        'nonzero_target_warm_start_test': bool(n>3*rank+1)})
        print(f"PASS matrix {name} (n={n}, r={rank})", flush=True)
    # Check the exchangeable spike trace formula against the actual chain.
    n=6; d=F(1,n-1); lvls=levels(spike(n,1,d))
    for k,L in enumerate(lvls):
        target=d*(n-k)*(1+1/(F(k)+d)) if k<n else F(0)
        for p,R in L.values():
            check('spike_trace_formula', trace(R)==target)
    records.append({'name':'clock_spike','dimension':n,'target_rank':1,
                    'expected_traces':[str(d*(n-k)*(1+1/(F(k)+d))) if k<n else '0' for k in range(n+1)]})
    return records


def spectral_coefficients() -> dict:
    checked = 0
    for length in [1,2,4,8,16,32,64]:
        geo=elementary([F(1,2**j) for j in range(length)])
        sq=elementary([F(1,j*j) for j in range(1,length+1)])
        for ell in range(1,min(length,16)+1):
            qprod=prod((1-F(1,2**j) for j in range(1,ell+1)))
            gexact=F(1,2**(ell*(ell-1)//2))/qprod
            check('geometric_coefficient_bound', geo[ell] <= gexact)
            check('geometric_product_constant', qprod > F(1,4))
            check('inverse_square_coefficient_bound', sq[ell] <= F(10**ell,factorial(2*ell+1)))
            checked+=1
    for p in [2,3,4]:
        D=F(p+1)+F(1,p-1); K=(3*D/p)**p
        for length in [5,12,32]:
            es=elementary([F(1,j**p) for j in range(1,length+1)])
            for ell in range(1,min(length,12)+1):
                check('algebraic_coefficient_bound', es[ell] <= (K/F(ell**p))**ell)
    return {'geometric_and_square_degree_cases':checked, 'algebraic_exponents':[2,3,4],
            'maximum_tail_length':64}


def scalar_constants() -> dict:
    base_geo=F(5*factorial(10),1)/F(384,35)**7
    check('geometric_factorial_base', base_geo<1)
    for r in range(3,101):
        F_r=F(8,5)*F(2*r,2*r+1)*2**r
        check('geometric_factorial_constant', 5*factorial(3*r+1) <= F_r**(2*r+1))
        check('geometric_prefactor_constant', 4*(1+F(1,2**(2*r+1)))**r < 5)
        b_r=F(2*r,5*(2*r+1))
        L_r=F(6*factorial(3*r+1),5*factorial(4*r+3))
        check('inverse_square_factorial_constant', L_r <= b_r**(2*r+1))
        check('inverse_square_prefactor_constant', (1+F(10,(4*r+4)**2))**r < F(6,5))
    check('square_induction_step_r3', F(11*12*13,16*17*18*19) < F(6,35)**2)
    check('square_induction_step_r_ge4', F(2197,81920) < F(6,35)**2)
    # An upper comparison chain; intermediate loosenings are deliberate.
    chain=[(F(4),F(23,8)),(F(23,8),F(16,7)),(F(16,7),F(2)),(F(2),F(7,4)),(F(7,4),F(89,56))]
    for x,y in chain:
        check('rank_two_scalar_chain', contraction(x,F(1),2)<=y)
    check('rank_two_warm_start', F(89,56)<F(8,5))
    eps_values=[F(1,100),F(1,10),F(1,2),F(2,3),F(3,4),F(7,8),F(9,10),F(99,100),F(1000,1001)]
    cases=0
    for r in [1,2,3,4,5,8,16,31,64,100]:
        for eps in eps_values:
            def ceiling(x:F)->int:return -(-x.numerator//x.denominator)
            k=ceiling(3*r/eps); t0=3*r+1; B=F(8,5)
            check('C3_ceiling', k>=t0 and F(k-t0)>=r*B*(1/eps-1/(B-1)))
            k=ceiling(4*r/eps)
            check('C4_ceiling', k>=t0 and F(k-t0)>=2*r*(1/eps-1))
            cases+=1
    return {'geometric_base_fraction':str(base_geo), 'factorial_ranks_checked':'3 through 100',
            'rank_two_upper_trace_at_7':'89/56','rank_epsilon_pairs':cases}


def clock_certificates() -> dict:
    for n in range(2,41):
        d=F(1,n-1)
        for k in range(n+1):
            T=d*(n-k)*(1+1/(F(k)+d)) if k<n else F(0)
            check('clock_lower_rate', T>=1+F(1,k+1)-F(k,n-1))
            if k>=1:
                check('clock_upper_rate_after_first', T<=2)
    records=[]
    for a in [F(0),F(1,2),F(1),F(2),F(10),F(100)]:
        x=4*(a+2); J=-(-x.numerator//x.denominator)
        t=2**J; n=t*t+t+2
        loss=F(t+t*t,n-1)
        lower=F(t)+F(J,4)-loss
        check('clock_finite_parameter', J>=4*(a+2) and loss<1 and lower>t+a)
        records.append({'a':str(a),'J':J,'time':str(t),'dimension':str(n),
                        'strict_analytic_lower_bound_for_mean_count':str(lower),
                        'proposed_upper_bound':str(F(t)+a),
                        'matrix_allocated':False})
    return {'small_dimensions_checked':'2 through 40', 'finite_certificates':records,
            'note':'The lower bound uses log(2)>1/2, proved analytically in the note. No large matrix is instantiated.'}



def path_bound_saturation() -> dict:
    records=[]
    M=N=10**6
    for r in range(1,7):
        head=[F(M**j) for j in range(r,0,-1)]
        eh=elementary(head)
        D=prod((sum(head[j:],F(1)) for j in range(r)))
        for c in [1,2,3]:
            m=c*r;k=r+m
            ek=sum((eh[r-s]*F(comb(N,m+s),N**(m+s)) for s in range(r+1)),F(0))
            ratio=ek*factorial(m)/D
            check('path_bound_saturation', F(999,1000)<ratio<F(1001,1000))
            records.append({'rank':r,'extra_pivots':m,'head_scale':M,'tail_count':N,
                            'ratio_to_limiting_prefactor':str(ratio),'matrix_allocated':False})
    return {'cases':records,'scope':'Scalar coefficients of an upper comparison, NOT measured algorithmic errors.'}


def main() -> None:
    start=time.perf_counter()
    records=matrix_cases()
    result={'status':'PASS','arithmetic':'fractions.Fraction; exact rational',
            'matrix_cases':records, 'spectral_coefficients':spectral_coefficients(),
            'scalar_constants':scalar_constants(), 'clock':clock_certificates(),
            'path_bound_saturation':path_bound_saturation(),
            'assertions_by_group':dict(sorted(COUNTS.items())),
            'explicit_assertions':sum(COUNTS.values()),
            'seconds':round(time.perf_counter()-start,3),
            'scope':'Finite checks only. No formal verification or unrestricted RA-01 solution is claimed.'}
    out=ROOT/'verification'/'exact_results.json';out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(f"PASS {len(records)} matrix cases; {result['explicit_assertions']} explicit checks; {result['seconds']} seconds")

if __name__=='__main__':main()
