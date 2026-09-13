#!/usr/bin/env python3
"""Generate a path-complete counterexample query and test its LU identities.

The generated SMT-LIB file has NOT been certified UNSAT. Generating a complete
model is not a solution of IE-11. The model includes no candidate active equalities.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
from candidate import eliminate,constraints
ROOT=Path(__file__).resolve().parents[1]

def smt_int(n):return str(n) if n>=0 else f'(- {-n})'
def mul(*terms):
    a=[t for t in terms if t!='1'];return '1' if not a else a[0] if len(a)==1 else '(* '+' '.join(a)+')'
def add(*terms):
    a=[t for t in terms if t!='0'];return '0' if not a else a[0] if len(a)==1 else '(+ '+' '.join(a)+')'

def generate():
    L={(i,j):('1' if i==j else f'l{i}{j}') for i in range(1,6) for j in range(1,i+1)}
    U={(i,j):('1' if i==j==1 else f'u{i}{j}') for i in range(1,6) for j in range(i,6)}
    variables=[v for v in L.values() if v!='1']+[v for v in U.values() if v!='1']
    assert len(variables)==24
    text=['; IE-11: existence of a normalized positive-pivot CP matrix with p5 > alpha.',
          '; No solver result or global certificate is supplied for this query.',
          '; Coefficients of P5 from Chen--Edelman--Urschel (2026), Eq. 2.15.',
          '(set-logic QF_NRA)','(declare-fun alpha () Real)']
    text += [f'(declare-fun {v} () Real)' for v in variables]
    text += ['(assert (> alpha 4))','(assert (< alpha 5))']
    pp=[int(a) for a in (ROOT/'data'/'reference_P5_ascending.txt').read_text().split()]
    polynomial=smt_int(pp[-1])
    for a in reversed(pp[:-1]):polynomial=add(mul(polynomial,'alpha'),smt_int(a))
    text.append(f'(assert (= {polynomial} 0))')
    for k in range(2,6):text.append(f'(assert (> {U[k,k]} 0))')
    count=0
    for k in range(1,5):
        p=U[k,k]
        for i in range(k,6):
            for j in range(k,6):
                if i==j==k:continue
                s=add(*[mul(L[i,t],U[t,j]) for t in range(k,min(i,j)+1)])
                text.append(f'(assert (<= {s} {p}))')
                text.append(f'(assert (>= {s} (- {p})))');count+=2
    assert count==100
    text += ['(assert (> u55 alpha))','(check-sat)']
    path=ROOT/'data'/'global_counterexample.smt2';path.write_text('\n'.join(text)+'\n')
    return path

def check_lu():
    data=json.loads((ROOT/'data'/'rational_witness.json').read_text());D=int(data['denominator'])
    A=[[Q(int(a),D) for a in row] for row in data['numerators']]
    L=[[Q(int(i==j)) for j in range(5)] for i in range(5)]
    U=[[Q(0) for _ in range(5)] for _ in range(5)];S=[row[:] for row in A]
    for k in range(5):
        for j in range(k,5):U[k][j]=S[k][j]
        assert U[k][k]>0
        for i in range(k+1,5):
            L[i][k]=S[i][k]/U[k][k]
            for j in range(k+1,5):S[i][j]-=L[i][k]*U[k][j]
    product=[[sum(L[i][k]*U[k][j] for k in range(5)) for j in range(5)] for i in range(5)]
    assert product==A
    stages=eliminate(A);checks=0
    for k,T in enumerate(stages):
        for i in range(k,5):
            for j in range(k,5):
                value=sum(L[i][t]*U[t][j] for t in range(k,min(i,j)+1))
                assert value==T[i-k][j-k];checks+=1
    assert checks==55
    assert all(abs(L[i][j])<=1 for i in range(5) for j in range(i))
    assert all(v>0 for _,v in constraints(stages))
    result=dict(status='PASS: exact LU/Schur identity test',global_solution=False,
        entries_compared=checks,cp_inequalities=100,query_status='NOT SOLVED; no UNSAT certificate',
        lower_variables=10,upper_variables=14)
    (ROOT/'results'/'global_model_check.json').write_text(json.dumps(result,indent=2)+'\n')
    return result
if __name__=='__main__':
    path=generate();r=check_lu();print(r['status']);print('Generated',path.name,'; query NOT solved.')
