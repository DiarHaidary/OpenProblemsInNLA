#!/usr/bin/env python3
"""Fresh independent exact arithmetic, parsed from the actual reviewed Lean arrays.

This is a Python diagnostic, never a Lean theorem or imported certificate.
No author checking code or recorded numerical result is imported.
"""
import ast, json, re
from fractions import Fraction as F
from audit import E, sha, write_json

s=(E/'inputs/NLA/IE05/Definitions.lean').read_text()
assert sha(s.encode())=='aa9a18994bb8d1889af8b30290cb71846af5424436d720afaf15a54184164dfa'

def arrays(name):
    body=re.search(r'^def '+name+r'\b.*?(?=^def |^end )',s,re.M|re.S).group()
    out={}
    for branch,b in re.findall(r'\| (false|true) => (.*?)(?=\n  \| |\Z)',body,re.S):
        out[branch]=ast.literal_eval(b.replace('![','[').strip())
    assert set(out)=={'true','false'}
    return out

H,D,T=(arrays(x) for x in ['integerH','integerD','integerT'])
lower=re.search(r'^def integerLower\b.*?(?=^/--)',s,re.M|re.S).group()
assert 'if i = j then 1 else if j < i then' in lower
assert 'if b = true ∧ i = 7 ∧ j = 1 then 0 else -1 else 0' in lower
L={b:[[1 if i==j else 0 if i<j or (b=='true' and (i,j)==(7,1)) else -1
       for j in range(8)] for i in range(8)] for b in ['false','true']}
assert [(i+1,j+1) for i in range(8) for j in range(8) if L['true'][i][j]!=L['false'][i][j]]==[(8,2)]
assert L['true'][6][1]==-1 and L['true'][7][1]==0

def matmul(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]

def transpose(A): return list(map(list,zip(*A)))

def forward(A,B):
    X=[]
    for i,row in enumerate(B):
        assert A[i][i]==1
        X.append([v-sum(A[i][k]*X[k][j] for k in range(i)) for j,v in enumerate(row)])
    return X

def manuscript_data(text):
    ms=[]
    for body in re.findall(r'\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}',text,re.S):
        ms.append([[int(v.strip()) for v in row.split('&')] for row in body.strip().split('\\\\')])
    ds=[[int(v) for v in row.split(',')] for row in re.findall(r'D(?:_0)?=\\operatorname\{diag\}\(([^)]+)\)',text)]
    assert len(ms)==3 and len(ds)==2
    return ms,ds

source_paths=['linear-systems-and-elimination/IE-05/solution.md',
              'linear-systems-and-elimination/IE-05/solution.tex',
              'references/stepaniants-ie05-2026-09-11/full-proof.md']
bindings={}
for rel in source_paths:
    p=E/'inputs/verification/original-sources'/rel
    matrices,diagonals=manuscript_data(p.read_text())
    assert matrices==[H['true'],T['true'],H['false']],rel
    assert diagonals==[D['true'],D['false']],rel
    assert forward(L['false'],H['false'])==T['false']
    bindings[rel]=dict(sha256=sha(p.read_bytes()),exact_displayed_array_match=True,candidate_T_forward_solved=True)

cases={}
reduced_witness=[]
reduced_candidate=[]
for b in ['false','true']:
    assert matmul(transpose(H[b]),H[b])==[[D[b][i] if i==j else 0 for j in range(8)] for i in range(8)]
    assert matmul(L[b],T[b])==H[b]
    assert forward(L[b],H[b])==T[b]
    assert all(L[b][i][i]==1 and T[b][i][i]>0 and D[b][i]>0 for i in range(8))
    assert all(T[b][i][j]==0 for i in range(8) for j in range(i))
    assert all(abs(L[b][i][j])<=1 for i in range(8) for j in range(i))
    S=[[F(v) for v in row] for row in H[b]]
    input_sq=max(F(H[b][i][j]**2,D[b][j]) for i in range(8) for j in range(8))
    stages=[]
    for k in range(8):
        tail=[[sum(L[b][i][r]*T[b][r][j] for r in range(k,8)) if i>=k and j>=k else 0
               for j in range(8)] for i in range(8)]
        assert S==tail,(b,k)
        # Pivot selection on H has the same order as on H_ij/sqrt(D_j)
        # because only one fixed positive column scaling enters that comparison.
        column_max=max(abs(S[i][k]) for i in range(k,8))
        ties=[i for i in range(k,8) if abs(S[i][k])==column_max]
        p=k
        for i in range(8):
            if k<=i and abs(S[p][k])<abs(S[i][k]): p=i
        assert p==min(ties)==k and S[p][k]!=0
        multipliers=[S[i][k]/S[k][k] for i in range(k+1,8)]
        assert multipliers==[L[b][i][k] for i in range(k+1,8)]
        sq={(i,j):S[i][j]**2/D[b][j] for i in range(k,8) for j in range(k,8)}
        maximum=max(sq.values())
        stages.append(dict(k=k,chosen_row=p,tied_rows=ties,
            active_numerators=[[str(S[i][j]) for j in range(k,8)] for i in range(k,8)],
            multipliers=list(map(str,multipliers)),max_squared=str(maximum),
            max_locations=[list(ij) for ij,v in sq.items() if v==maximum],
            equal_to_independent_tail=True))
        if b=='false':
            for i,j in sq:
                lhs=tail[i][j]**2; rhs=5462*D[b][j]
                assert lhs<=rhs
                reduced_candidate.append(dict(k=k,i=i,j=j,lhs=lhs,rhs=rhs,slack=rhs-lhs))
        S=[[S[i][j]-S[i][k]/S[k][k]*S[k][j] if i>k and j>k else F(0)
            for j in range(8)] for i in range(8)]
    assert S==[[0]*8 for _ in range(8)]
    growth_sq=max(F(t['max_squared']) for t in stages)/input_sq
    cases[b]=dict(gram_identity=True,LU_identity=True,upper_and_unit_lower=True,
        positive_T_diagonal=[T[b][i][i] for i in range(8)],positive_D=D[b],
        input_max_squared=str(input_sq),growth_squared=str(growth_sq),stages=stages,
        final_zero_tail=True)

for i in range(8):
    for j in range(8):
        lhs=5272*H['true'][i][j]**2; rhs=3969*D['true'][j]
        assert lhs<=rhs
        reduced_witness.append(dict(i=i,j=j,lhs=lhs,rhs=rhs,slack=rhs-lhs))
assert len(reduced_candidate)==204 and len(reduced_witness)==64
assert H['false'][2][2]==51 and D['false'][2]==3286
assert D['true'][7]==5272 and T['true'][7][7]==5272
assert F(cases['false']['growth_squared'])==F(17948132,2601)
assert F(cases['true']['growth_squared'])==F(5272,63)**2
gap=F(5272,63)**2-F(17948132,2601)
assert gap==F(117335164,1147041)>0
write_json(E/'numerical-result.json',dict(pass_=True,not_a_Lean_theorem=True,
    construction='one-based (8,2), excluding recovered (7,2)',source_array_bindings=bindings,
    actual_Lean_arrays_sha256=sha(s.encode()),cases=cases,
    witness_input_certificates=reduced_witness,candidate_active_certificates=reduced_candidate,
    one_candidate_entry=[2,2,51,3286],witness_final_pivot_numerator=5272,
    exact_gap=str(gap),reduced_certificate_counts=[64,204]))
print('PASS: independently parsed canonical and Lean arrays, exact Gram/LU and all pivot ties; 64+204 reduced bounds; gap '+str(gap)+'. Python diagnostic only.')
