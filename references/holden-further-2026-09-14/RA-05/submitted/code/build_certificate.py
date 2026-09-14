#!/usr/bin/env python3
"""Construct an exact cubic tensor-support certificate. Standard library only."""
from __future__ import annotations
from fractions import Fraction as Q
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELECTED = [0, 1, 14, 15, 50, 51, 60, 84, 85, 91, 103, 105, 104, 90, 61, 102, 21]

def dot(a, b):
    return sum(x*y for x,y in zip(a,b))

def fstr(x):
    return str(Q(x))

def build():
    h = 8
    signs = [[1-2*((x >> j)&1) for j in range(h)] for x in range(1<<h)]
    H = [[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]]
    core = [[2*int(i==j) for j in range(4)] for i in range(4)] + H + [[1-2*int(i==j) for j in range(4)] for i in range(4)]
    subsets = list(combinations(range(h), h//2))
    chars = []
    for S in subsets:
        row=[]
        for sx in signs:
            v=1
            for j in S: v*=sx[j]
            row.append(v)
        chars.append(row)
    Gnum = [[abs(dot(a,b))**3 for b in core] for a in core]  # denominator 64
    Fnum = [[abs(dot(x, signs[t]))**3 for t in SELECTED] for x in signs] # denominator 512
    Csel = [[row[t] for t in SELECTED] for row in chars]
    gram = [[sum(row[i]*row[j] for row in Csel) for j in range(17)] for i in range(17)]
    A = [[a*b for a in c for b in signs[t]] for c in core for t in SELECTED]
    weights = [17 if t==0 else 0 for _ in core for t in range(17)]
    # Evaluate all product hyperplanes using their unit data/query factors.
    Ssum = sum(Q(sum(row),512)**2 for row in Fnum) * sum(Q(sum(row),64)**2 for row in Gnum)
    winner=None
    for i,c in enumerate(core):
        for x,sx in enumerate(signs):
            normal=[a*b for a in c for b in sx]
            orig=sum(abs(dot(a,normal))**3 for a in A)
            weighted=sum(w*abs(dot(a,normal))**3 for a,w in zip(A,weights))
            rel=Q(abs(weighted-orig),orig) if orig else Q(0)
            if winner is None or rel > winner[0]:
                winner=(rel,i,x,normal,orig,weighted)
    rel,i,x,normal,orig,weighted=winner
    Pnum=[[32*int(a==b)-normal[a]*normal[b] for b in range(32)] for a in range(32)]
    # Exact unpivoted LDL certificate for Gram - 32 I > 0.
    B=[[Q(gram[i][j]-32*int(i==j)) for j in range(17)] for i in range(17)]
    L=[[Q(int(i==j)) for j in range(17)] for i in range(17)]
    piv=[]
    for j in range(17):
        dj=B[j][j]-sum(L[j][t]**2*piv[t] for t in range(j))
        if dj<=0: raise ArithmeticError('Positive definiteness certificate failed')
        piv.append(dj)
        for i2 in range(j+1,17):
            L[i2][j]=(B[i2][j]-sum(L[i2][t]*L[j][t]*piv[t] for t in range(j)))/dj
    payload={
        'description':'Exact cubic original-row support certificate from core x Boolean middle spectrum',
        'p':3,'core_dimension':4,'noise_dimension':8,'ambient_dimension':32,'query_rank':31,
        'core_numerators_denominator_2':core,
        'noise_selected_cube_indices':SELECTED,
        'input_integer_rows':A,
        'middle_character_subsets':[list(S) for S in subsets],
        'middle_selected_gram':gram,
        'gram_minus_32I_ldl_diagonal':[fstr(d) for d in piv],
        'gram_minus_32I_ldl_lower':[[fstr(v) for v in row] for row in L],
        'core_min_squared_singular_value':'1/4',
        'noise_min_squared_singular_value':'1/8',
        'sum_squared_normalized_original_query_costs':fstr(Ssum),
        'universal_support_bound':{'number_rows':204,'epsilon_squared_coefficient':fstr(32*Ssum)},
        'support_examples':[
            {'epsilon':'1/100','real_threshold':fstr(Q(204)-32*Ssum*Q(1,100)**2),'integer_lower_bound':150},
            {'epsilon':'1/1000','real_threshold':fstr(Q(204)-32*Ssum*Q(1,1000)**2),'integer_lower_bound':204}
        ],
        'candidate':{
            'weights':weights,'support':12,
            'witness':{
                'core_test_index':i,'cube_test_index':x,'integer_normal':normal,
                'normal_squared_norm':dot(normal,normal),
                'projector_denominator':32,'projector_numerator':Pnum,
                'original_cost_rational_coefficient_of_sqrt2':fstr(Q(orig,256)),
                'weighted_cost_rational_coefficient_of_sqrt2':fstr(Q(weighted,256)),
                'relative_error':fstr(rel),
                'violated_epsilon':'1/100'
            }
        }
    }
    out=ROOT/'results/cubic_tensor_certificate.json'
    out.write_text(json.dumps(payload,indent=2)+'\n')
    print(json.dumps({'path':str(out),'support_coefficient':str(32*Ssum),'witness':payload['candidate']['witness']['relative_error'],'original_cost_coefficient':payload['candidate']['witness']['original_cost_rational_coefficient_of_sqrt2'],'weighted_cost_coefficient':payload['candidate']['witness']['weighted_cost_rational_coefficient_of_sqrt2']},indent=2))

if __name__=='__main__': build()
