"""Fresh rational check of actual Lean tables against original manuscript and QR."""
from pathlib import Path
from fractions import Fraction as F
import ast, hashlib, json, re

OWN=Path(__file__).resolve().parent
ROOT=OWN.parents[1]
source=ROOT/'NLA/IE05/Definitions.lean'
original=ROOT/'verification/original-sources/linear-systems-and-elimination/IE-05/solution.md'
data=json.loads((ROOT/'verification/original-sources/references/stepaniants-ie05-2026-09-11/verification/integer_counterexample.json').read_text())
s=source.read_text(); text=original.read_text()

def tables(name,next_name):
    block=s.split('def '+name,1)[1].split('def '+next_name,1)[0]
    return {b:ast.literal_eval(re.search(r'\| '+b+r' => (.*?)(?=\n  \||\n\n|\Z)',block,re.S)[1].replace('!','')) for b in ['false','true']}

hs=tables('integerH','integerD'); ds=tables('integerD','integerT'); ts=tables('integerT','castIntegerMatrix')
printed=[[[int(v.strip()) for v in row.split('&')] for row in body.strip().split(r'\\')]
         for body in re.findall(r'\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}',text,re.S)]
assert len(printed)==3 and printed==[hs['true'],ts['true'],hs['false']]
diag=re.findall(r'D(?:_0)?=\\operatorname\{diag\}\(([^)]*)\)',text)
assert len(diag)==2 and [list(map(int,x.split(','))) for x in diag]==[ds['true'],ds['false']]
assert 'if b = true ∧ i = 7 ∧ j = 1 then 0 else -1' in s

def mul(a,b): return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def tail(l,t,k): return [[sum(l[i][q]*t[q][j] for q in range(k,8)) if i>=k and j>=k else 0 for j in range(8)] for i in range(8)]

results={}; inequalities=[]
for b in ['false','true']:
    H,D,T=hs[b],ds[b],ts[b]
    L=[[1 if i==j else -1 if i>j else 0 for j in range(8)] for i in range(8)]
    if b=='true': L[7][1]=0
    old=data['perturbed' if b=='true' else 'original']
    assert L==[[F(x) for x in row] for row in old['lower']]
    assert mul(list(zip(*H)),H)==[[D[i] if i==j else 0 for j in range(8)] for i in range(8)]
    assert mul(L,T)==H
    assert all(T[i][j]==0 for i in range(8) for j in range(i))
    assert all(T[i][i]>0 and D[i]>0 for i in range(8))
    # Independent exact Gram--Schmidt, with the Euclidean dot product and positive rescaling.
    residuals=[]; norms=[]; factors=[]
    for j in range(8):
        v=[F(L[i][j]) for i in range(8)]
        w=v[:]
        for u,n in zip(residuals,norms):
            c=dot(u,v)/n; w=[x-c*y for x,y in zip(w,u)]
        norm=dot(w,w); assert norm>0
        nonzero=next(i for i,x in enumerate(w) if x)
        factor=F(H[nonzero][j])/w[nonzero]
        assert factor>0 and [factor*x for x in w]==[H[i][j] for i in range(8)]
        assert factor*factor*norm==D[j]
        assert w==[F(x) for x in old['rational_columns'][j]]
        assert norm==F(old['squared_column_norms'][j])
        residuals.append(w); norms.append(norm); factors.append(str(factor))
    # Independent forward substitution recovers exactly the supplied upper factor.
    U=[list(map(F,row)) for row in H]
    for i in range(8):
        for j in range(8): U[i][j]-=sum(L[i][k]*U[k][j] for k in range(i))
    assert U==T
    S=[list(map(F,row)) for row in H]; stages=[]
    for k in range(8):
        assert S==tail(L,T,k)
        column=[abs(S[i][k]) for i in range(k,8)]
        p=k+column.index(max(column)); assert p==k and S[p][k]>0
        ties=[i for i in range(k,8) if abs(S[i][k])==abs(S[p][k])]
        stages.append({'stage_zero_based':k,'chosen_row':p,'all_tied_rows':ties,'integer_pivot':str(S[k][k]),
                       'active_entries':(8-k)**2})
        if b=='false':
            for i in range(k,8):
                for j in range(k,8):
                    lhs=S[i][j]**2; rhs=5462*D[j]; assert lhs<=rhs
                    inequalities.append({'k':k,'i':i,'j':j,'lhs':int(lhs),'rhs':rhs})
        nextS=[[F(0) for _ in range(8)] for _ in range(8)]
        for i in range(k+1,8):
            ell=S[i][k]/S[k][k]; assert ell==L[i][k] and abs(ell)<=1
            for j in range(k+1,8): nextS[i][j]=S[i][j]-ell*S[k][j]
        S=nextS
    assert S==tail(L,T,8)==[[0]*8 for _ in range(8)]
    results[b]={'H':H,'D':D,'L':L,'T':T,'positive_GS_integer_scales':factors,'stages':stages}

witness=[]
for i in range(8):
    for j in range(8):
        lhs=5272*hs['true'][i][j]**2; rhs=3969*ds['true'][j]; assert lhs<=rhs
        witness.append({'i':i,'j':j,'lhs':lhs,'rhs':rhs})
assert len(witness)==64 and len(inequalities)==204
assert hs['false'][2][2]==51 and ds['false'][2]==3286
assert tail(results['true']['L'],ts['true'],7)[7][7]==ds['true'][7]==5272
gap=F(5272,63)**2-F(17948132,2601)
assert gap==F(117335164,1147041)>0
report={'status':'PASS','arithmetic':'Python integers and fractions.Fraction; no floating point or author checker execution',
        'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'original_manuscript_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),
        'constructions':results,'witness_input_inequalities':witness,'candidate_active_inequalities':inequalities,
        'witness_count':64,'candidate_count':204,'gap':str(gap),
        'scope':'Both QR conventions, exact table transcription, genuine padded Schur recurrences and first-tie paths; only reduced one-sided numerical bounds.'}
(OWN/'exact-result.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print('Exact independent PASS: both QR conventions, literal Gram/LU tables and eight Schur stages; 64 witness + 204 candidate inequalities; positive gap '+str(gap))
