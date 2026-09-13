"""Reproduce all checks recorded in the manuscript.

Run from any directory: python path/to/code/verify.py
By default results are written to ../results relative to this file.
"""
from __future__ import annotations
import argparse
import csv
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction
from itertools import combinations
import json
import math
from pathlib import Path
import platform

import mpmath
import numpy as np
import scipy
import sympy as sp

from ra18 import (family, trine_lift, structural_basis, exhaustive_spectra,
                  predicted_spectrum, sample_basis, scalar_recurrence,
                  H, invsqrt, weighted_dual, select_grouped_real,
                  sharp_real_example)


def symbolic_checks():
    g, x = sp.symbols("g x", real=True)
    h = sp.Matrix([[1+g, sp.sqrt(g), sp.sqrt(1-g)],
                   [sp.sqrt(g), 2, 0], [sp.sqrt(1-g), 0, 1]])/3
    A = x*(3*x-2)**2
    D = 3*x*x-3*x+1
    expected = (A-g*D)/9
    assert sp.simplify((x*sp.eye(3)-h).det()-expected) == 0
    R = A/D
    derivative = (3*x-2)*(3*x-1)*(3*x*x-3*x+2)/D**2
    assert sp.simplify(sp.diff(R,x)-derivative) == 0
    assert sp.simplify(R-4*x+3*x**3/D) == 0
    assert sp.simplify(h.det()-g/9) == 0
    omega = (-1+sp.I*sp.sqrt(3))/2
    U1 = sp.Matrix([[1/sp.sqrt(6), phase/sp.sqrt(3), 0]
                    for phase in [1,omega,omega**2]] +
                   [[1/sp.sqrt(6), 0, phase/sp.sqrt(3)]
                    for phase in [1,omega,omega**2]])
    orth = (U1.conjugate().T*U1-sp.eye(3)).applyfunc(sp.simplify)
    assert orth == sp.zeros(3)
    realification = U1.applyfunc(sp.re).row_join(-U1.applyfunc(sp.im)).col_join(
        U1.applyfunc(sp.im).row_join(U1.applyfunc(sp.re)))
    selected_real = realification[[3,4,5,6,7,8],:]
    assert (selected_real.T*selected_real-sp.eye(6)/2).applyfunc(sp.simplify) == sp.zeros(6)
    q1 = (x-sp.Rational(1,2))*(x*x-x+sp.Rational(1,9))
    singular = 0
    valid = 0
    for I in combinations(range(6),3):
        S = U1[list(I),:]
        if sp.simplify(S.det()) == 0:
            singular += 1
        else:
            G = (S.conjugate().T*S).applyfunc(sp.simplify)
            cp = (x*sp.eye(3)-G).det()
            assert sp.simplify(cp-q1) == 0
            valid += 1
    assert (singular,valid) == (2,18)
    q0 = x-sp.Rational(1,2)
    assert sp.factor(D/9*q0.subs(x,R)-q1) == 0
    q2 = sp.cancel((D/9)**3*q1.subs(x,R))
    poly = sp.Poly(q2,x)
    assert poly.degree() == 9 and poly.LC() == 1
    assert poly.TC() == -sp.Rational(1,13122)
    return {"identities_passed": True, "U1_realification_orthogonal_basis_verified": True, "exact_U1_square_subsets": 20,
            "exact_U1_nonsingular_subsets": valid,
            "exact_U1_singular_subsets": singular,
            "q1": str(sp.factor(q1)), "q2": str(q2),
            "characteristic_identity": str(expected),
            "R_derivative": str(derivative)}


def exhaustive_family_check(level):
    U = family(level)
    n,r = U.shape
    reference = predicted_spectrum(level)
    valid=singular=mismatch=0
    largest_spectrum_error=0.0
    max_singular_abs_min=0.0
    beta=-np.inf
    min_valid=np.inf
    for idx, eigs in exhaustive_spectra(U):
        for indices, ev in zip(idx,eigs):
            structural = structural_basis(level,indices)
            numeric = ev[0] > 1e-9
            mismatch += int(structural != numeric)
            beta = max(beta,float(ev[0]))
            if structural:
                valid += 1
                min_valid=min(min_valid,float(ev[0]))
                largest_spectrum_error=max(largest_spectrum_error,float(np.max(np.abs(ev-reference))))
            else:
                singular += 1
                max_singular_abs_min=max(max_singular_abs_min,float(abs(ev[0])))
    expected_count=2*3**(3**level-1)
    assert valid == expected_count
    assert mismatch == 0
    assert largest_spectrum_error < 2e-12
    assert max_singular_abs_min < 2e-12
    return {"level":level,"n":n,"r":r,"total_subsets":math.comb(n,r),
            "nonsingular_subsets":valid,"singular_subsets":singular,
            "structural_numerical_classification_mismatches":mismatch,
            "column_orthogonality_error_2norm":float(np.linalg.norm(U.conj().T@U-np.eye(r),2)),
            "maximum_row_leverage_error":float(np.max(abs(np.sum(abs(U)**2,axis=1)-.5))),
            "maximum_full_spectrum_error":largest_spectrum_error,
            "maximum_abs_smallest_eigenvalue_singular_subsets":max_singular_abs_min,
            "minimum_beta_over_nonsingular_subsets":min_valid,
            "maximum_beta_over_all_subsets":beta,
            "best_inverse_norm":float(1/np.sqrt(beta)),
            "ratio_to_sqrt_n":float(1/np.sqrt(n*beta))}


def random_lift_checks(rng):
    worst_phase_error=0.0
    min_amplification_slack=np.inf
    spectra_error=0.0
    checks=0
    # Includes an unbalanced dimension: the amplification lemma is not
    # restricted to n=2r. These are tests, not an exhaustive theorem proof.
    for n,r in [(3,1),(4,2),(5,2),(6,3)]:
        for _ in range(5):
            A=rng.normal(size=(n,r))+1j*rng.normal(size=(n,r))
            U=np.linalg.qr(A)[0]
            T=trine_lift(U)
            for _ in range(25):
                I=np.sort(rng.choice(n,size=r,replace=False))
                is_I=np.zeros(n,dtype=bool);is_I[I]=True
                idx=[];s=[]
                omega=complex(-.5,np.sqrt(3)/2)
                for i in range(n):
                    j=int(rng.integers(3))
                    js=[p for p in range(3) if p!=j] if is_I[i] else [j]
                    idx.extend(3*i+p for p in js)
                    s.append(sum(omega**p for p in js))
                s=np.array(s)
                S=T[idx]; gram=S.conj().T@S
                phase=np.concatenate((np.ones(r),np.conj(s)))
                canonical=phase.conj()[:,None]*gram*phase[None,:]
                G=U[I].conj().T@U[I]
                D=np.diag(1+is_I.astype(float))
                expected=np.block([[np.eye(r)+G,U.conj().T],[U,D]])/3
                worst_phase_error=max(worst_phase_error,float(np.max(abs(canonical-expected))))
                g=np.linalg.eigvalsh(G)[0]
                mu=np.linalg.eigvalsh(gram)[0]
                slack=1/mu-(4/g-1.5)
                min_amplification_slack=min(min_amplification_slack,float(slack))
                assert slack>-1e-6
                if n==2*r:
                    prediction=np.sort(np.concatenate([np.linalg.eigvalsh(H(v)) for v in np.linalg.eigvalsh(G)]))
                    spectra_error=max(spectra_error,float(np.max(abs(np.linalg.eigvalsh(gram)-prediction))))
                checks += 1
    assert worst_phase_error<1e-12 and spectra_error<1e-12
    return {"selected_bases_tested":checks,"maximum_phase_conjugacy_error":worst_phase_error,
            "minimum_squared_inverse_amplification_slack":min_amplification_slack,
            "maximum_half_rank_full_spectrum_error":spectra_error}


def real_checks(rng):
    margins=[];duality_mismatches=0;duality_tests=0
    for _ in range(80):
        r=int(rng.integers(2,7));s=int(rng.integers(0,3));q=r+s
        A=rng.normal(size=(q,r));V=A@invsqrt(A.T@A)
        m=rng.integers(1,6,size=q)
        rows=[];labels=[]
        for i,mi in enumerate(m):
            weights=rng.normal(size=mi);weights/=np.linalg.norm(weights)
            rows.extend(weights[:,None]*V[i]);labels.extend([i]*mi)
        U=np.vstack(rows+[np.zeros((3,r))]);labels.extend([-1]*3)
        selected=select_grouped_real(U,labels)
        margin=np.linalg.eigvalsh(U[selected].T@U[selected])[0]-1/len(U)
        assert margin>-1e-10
        margins.append(float(margin))
        if s:
            # Test both fields and arbitrary admissible thresholds in the
            # equivalence, not only the threshold used by the selector.
            for complex_field in (False,True):
                B=rng.normal(size=(q,r))
                if complex_field:
                    B=B+1j*rng.normal(size=(q,r))
                Q=np.linalg.qr(B)[0]
                eta=float(rng.uniform(.2,.85)/m.max())
                Z,_=weighted_dual(Q,m,eta)
                for I in combinations(range(q),r):
                    J=[j for j in range(q) if j not in I]
                    X=Q[list(I)]/np.sqrt(m[list(I)])[:,None]
                    Y=Z[J]/np.sqrt(m[J])[:,None]
                    left=np.linalg.eigvalsh(X.conj().T@X)[0]-eta
                    right=np.linalg.eigvalsh(Y.conj().T@Y)[0]-eta
                    if abs(left)>1e-9 and abs(right)>1e-9:
                        duality_mismatches+=int((left>=0)!=(right>=0))
                        duality_tests+=1
    assert duality_mismatches==0
    fixtures=[]
    for m in [[1,1],[1,2,3],[2,3,1,4],[1,2,1,3,2]]:
        U=sharp_real_example(m);N,r=U.shape
        maxerr=0.0;valid=0
        for idx,eigs in exhaustive_spectra(U):
            for ev in eigs:
                if ev[0]>1e-9:
                    maxerr=max(maxerr,abs(float(ev[0])-1/N));valid+=1
        assert maxerr<1e-12
        fixtures.append({"multiplicities":m,"n":N,"r":r,
                         "nonsingular_subsets":valid,"max_beta_error":maxerr})
    return {"grouped_real_instances":len(margins),
            "minimum_selection_margin_above_1_over_n":min(margins),
            "weighted_duality_equivalence_tests":duality_tests,
            "weighted_duality_mismatches":duality_mismatches,
            "sharp_real_fixtures":fixtures}


def rigorous_limit_interval(level=20, bits=220):
    """Enclose L using exact rational bisection and the proved geometric tail."""
    def R(x):
        return x*(2-3*x)**2/(1-3*x+3*x*x)
    def inverse_bracket(target):
        lo,hi=Fraction(0),Fraction(1,3)
        for _ in range(bits):
            mid=(lo+hi)/2
            if R(mid)<=target:
                lo=mid
            else:
                hi=mid
        assert R(lo)<=target<=R(hi)
        return lo,hi
    low=high=Fraction(1,2)
    for _ in range(level):
        low=inverse_bracket(low)[0]
        high=inverse_bracket(high)[1]
    low*=4**level;high=high*4**level+Fraction(2,45*16**level)
    def decimal_bound(value,rounding):
        with localcontext() as ctx:
            ctx.prec=60;ctx.rounding=rounding
            return str(Decimal(value.numerator)/Decimal(value.denominator))
    return {"level":level,"bisection_steps_per_inverse":bits,
            "method":"exact rational interval propagation plus tail (2/45)*16**(-level)",
            "L_lower_rational":str(low),"L_upper_rational":str(high),
            "L_lower_decimal_outward":decimal_bound(low,ROUND_FLOOR),
            "L_upper_decimal_outward":decimal_bound(high,ROUND_CEILING)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir",type=Path,default=Path(__file__).resolve().parents[1]/"results")
    args=parser.parse_args();args.out_dir.mkdir(parents=True,exist_ok=True)
    rng=np.random.default_rng(20260913)
    print("Checking exact symbolic identities and all 20 first-level minors ...",flush=True)
    result={"seed":20260913,"verification_kind":"symbolic identities plus floating-point checks; not formal proof",
            "environment":{"python":platform.python_version(),"numpy":np.__version__,
                           "scipy":scipy.__version__,"sympy":sp.__version__,"mpmath":mpmath.__version__},
            "symbolic":symbolic_checks()}
    result["exhaustive_family"]=[]
    for level in [0,1,2]:
        print(f"Exhaustively checking every square row subset of level {level} ...",flush=True)
        result["exhaustive_family"].append(exhaustive_family_check(level))
    print("Checking random lift identities and third-level spectra ...",flush=True)
    result["random_lift"]=random_lift_checks(rng)
    U=family(3);pred=predicted_spectrum(3);sample_error=0.0
    for _ in range(200):
        idx=sample_basis(3,rng);assert structural_basis(3,idx)
        S=U[idx];ev=np.linalg.eigvalsh(S.conj().T@S)
        sample_error=max(sample_error,float(np.max(abs(ev-pred))))
    assert sample_error<1e-12
    result["level_three_samples"]={"sampled_bases":200,"exhaustive":False,
                                    "maximum_full_spectrum_error":sample_error}
    print("Checking weighted duality, grouped real selection, and equality fixtures ...",flush=True)
    result["real_checks"]=real_checks(rng)
    print("Computing 80-digit scalar recurrence through level 12 ...",flush=True)
    table=scalar_recurrence(12,80)
    with (args.out_dir/"recurrence.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(table[0]));writer.writeheader();writer.writerows(table)
    print("Enclosing the asymptotic limit with exact rational arithmetic ...",flush=True)
    result["rigorous_limit_interval"]=rigorous_limit_interval()
    result["all_checks_passed"]=True
    (args.out_dir/"verification.json").write_text(json.dumps(result,indent=2)+"\n")
    (args.out_dir/"recurrence.json").write_text(json.dumps(table,indent=2)+"\n")
    print(json.dumps(result,indent=2))
    print("ALL CHECKS PASSED",flush=True)


if __name__=="__main__":
    main()
