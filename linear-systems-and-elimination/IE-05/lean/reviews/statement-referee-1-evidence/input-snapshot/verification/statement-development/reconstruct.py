#!/usr/bin/env python3
"""Independent exact transcription/finite arithmetic diagnostic, not a Lean proof.

Parse the actual draft's integer arrays, solve L*T=H independently by forward
substitution, and check exactly the reduced certificates proposed for Lean.
No floating-point square root, external library, network, or source write.
"""
from __future__ import annotations
import datetime, hashlib, json, pathlib, re
from fractions import Fraction as F

PROJECT=pathlib.Path(__file__).resolve().parents[2]
SOURCE=PROJECT/'NLA/IE05/Definitions.lean'

def matrices(text,name,next_name):
    block=text.split('def '+name+' ',1)[1].split('def '+next_name+' ',1)[0]
    parts=block.split('| true =>')
    assert len(parts)==2
    result=[]
    for part in parts:
        rows=[[int(x.strip()) for x in row.split(',')]
              for row in re.findall(r'!\[([^\[\]]*)\]',part)]
        assert len(rows)==8 and all(len(row)==8 for row in rows)
        result.append(rows)
    return result

def transpose(a):return list(map(list,zip(*a)))
def mmul(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in transpose(b)] for row in a]
def solve_unit_lower(l,h):
    t=[[0]*8 for _ in range(8)]
    for i in range(8):
        for j in range(8):t[i][j]=h[i][j]-sum(l[i][r]*t[r][j] for r in range(i))
    return t
def tail(l,t,k,i,j):return sum(l[i][r]*t[r][j] for r in range(k,8))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    text=SOURCE.read_text()
    hs=matrices(text,'integerH','integerD');ts=matrices(text,'integerT','castIntegerMatrix')
    ds=[[int(x.strip()) for x in row.split(',')] for row in re.findall(
        r'!\[([^\[\]]*)\]',text.split('def integerD ',1)[1].split('def integerT ',1)[0])]
    assert len(ds)==2 and all(len(d)==8 for d in ds)
    lower=[[[1 if i==j else -1 if j<i else 0 for j in range(8)] for i in range(8)] for _ in range(2)]
    lower[1][7][1]=0 # canonical witness, NOT the recovered (7,2) variant
    printed=json.loads((PROJECT/'verification/original-sources/references/stepaniants-ie05-2026-09-11/independent-review/exact_matrix_review.json').read_text())
    results=[]
    for b in range(2):
        h,t,d,l=hs[b],ts[b],ds[b],lower[b]
        assert mmul(transpose(h),h)==[[d[i] if i==j else 0 for j in range(8)] for i in range(8)]
        assert all(x>0 for x in d)
        assert solve_unit_lower(l,h)==t and mmul(l,t)==h
        assert all(t[i][i]>0 for i in range(8))
        assert all(t[i][j]==0 for i in range(8) for j in range(i))
        assert all(abs(l[i][j])<=1 for i in range(8) for j in range(i))
        assert t==printed['counterexample' if b else 'canonical']['upper']
        results.append({'case':'witness' if b else 'candidate','H':h,'D':d,'L':l,'T':t,
                        'gram_diagonal':True,'positive_diagonal':True,'independent_forward_solve':True,
                        'all_lower_multipliers_abs_le_one':True})
    initial=[]
    for i in range(8):
        for j in range(8):
            lhs=5272*hs[1][i][j]**2;rhs=3969*ds[1][j]
            assert lhs<=rhs
            initial.append({'i':i,'j':j,'lhs':lhs,'rhs':rhs})
    active=[]
    for k in range(8):
        for i in range(k,8):
            for j in range(k,8):
                a=tail(lower[0],ts[0],k,i,j)
                assert a*a<=5462*ds[0][j]
                active.append({'k':k,'i':i,'j':j,'numerator':a,'lhs':a*a,'rhs':5462*ds[0][j]})
    assert hs[0][2][2]==51 and ds[0][2]==3286 and ds[1][7]==5272
    last=tail(lower[1],ts[1],7,7,7);assert last==5272
    gap=F(5272,63)**2-F(17948132,2601)
    assert gap==F(117335164,1147041)>0
    result={'phase':'statement-only arithmetic diagnostic','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'source_sha256':sha(SOURCE),'script_sha256':sha(pathlib.Path(__file__)),
        'matrix_cases':results,'witness_initial_checks':initial,'candidate_active_checks':active,
        'witness_initial_count':len(initial),'candidate_active_count':len(active),
        'witness_final_pivot_numerator':last,'candidate_selected_input_numerator':hs[0][2][2],
        'positive_squared_gap':str(gap),'all_checks_pass':True,
        'no_witness_intermediate_maximum_claim':True,'no_candidate_input_maximum_upper_check':True,
        'mathematical_proof_assistant_verification':False}
    out=PROJECT/'verification/statement-development/reconstruction.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'pass':True,'witness_initial':len(initial),'candidate_active':len(active),
                      'gap':str(gap),'sha256':sha(out)}))

if __name__=='__main__':main()
