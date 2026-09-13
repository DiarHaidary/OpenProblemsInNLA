#!/usr/bin/env python3
"""Build report tables and CSV from accepted certificates. Standard library only."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal, localcontext
import csv
import json

ROOT = Path(__file__).resolve().parents[1]


def tex_fraction(text):
    value = Fraction(text)
    sign = '-' if value < 0 else ''
    value = abs(value)
    if value.denominator == 1:
        return sign+str(value.numerator)
    return sign+r'\frac{'+str(value.numerator)+'}{'+str(value.denominator)+'}'


def lower_decimal(value, places=8):
    number = Fraction(value)
    integer = number.numerator*10**places//number.denominator
    sign = '-' if integer < 0 else ''
    integer = abs(integer)
    return f'{sign}{integer//10**places}.{integer%10**places:0{places}d}'


def main():
    rows = json.loads((ROOT/'results/verified.json').read_text())
    expected = list(range(2,65))+[80]
    assert [r['q'] for r in rows] == expected
    assert all(r['status']=='VERIFIED' for r in rows)
    table=[]; exported=[]
    for row in rows:
        q=row['q']; data=json.loads((ROOT/f'certificates/q{q:03d}.json').read_text())
        t=Fraction(int(row['t_numerator']),int(row['t_denominator']))
        with localcontext() as ctx:
            ctx.prec=35
            radius=(Decimal(t.numerator)/Decimal(t.denominator)).sqrt()
        record={
            'q':q, 't_numerator':t.numerator, 't_denominator':t.denominator,
            'sqrt_t_approx':str(radius),
            'r_numerical_NOT_PROOF':data['proposal_diagnostics_NOT_PROOF']['numerical_r'],
            'status':row['status'],
            'H_min_LDL_pivot_lower':row['H_min_LDL_pivot_lower'],
            'energy_min_LDL_pivot_lower':row['HB+B^T H_min_LDL_pivot_lower'],
            'Stein_min_LDL_pivot_lower':row['tH-N^T HN_min_LDL_pivot_lower'],
            'contraction_min_LDL_pivot_lower':row['I-N^T N_min_LDL_pivot_lower'],
            'Rayleigh_gap_lower':row['Rayleigh_gap_lower']}
        exported.append(record)
        if q in [2,3,4,8,16,32,48,64,80]:
            table.append(f'{q} & ${tex_fraction(str(t))}$ & {radius:.9f} & '
                         f"{row['HB+B^T H_min_LDL_pivot_lower']} \\\\")
    (ROOT/'tables/certificate_summary.tex').write_text(
        r'\begin{tabular}{@{}crrr@{}}'+'\n'+r'\toprule'+'\n'+
        r'$q$ & Exact $t_q$ & $\sqrt{t_q}$ (approx.) & Lower bound on energy pivot\\'+'\n'+
        r'\midrule'+'\n'+'\n'.join(table)+'\n'+r'\bottomrule'+'\n'+r'\end{tabular}'+'\n')
    with (ROOT/'results/certificates.csv').open('w',newline='') as out:
        writer=csv.DictWriter(out,fieldnames=list(exported[0]));writer.writeheader();writer.writerows(exported)
    exact=json.loads((ROOT/'results/exact_q3.json').read_text())
    names={'H':'H','HB+B^T H':'G','tH-N^T HN':'F','I-N^T N':'J'}
    table=[]
    for key, values in exact['leading_principal_minors'].items():
        for k,value in enumerate(values,1):
            table.append(f'${names[key]}$ & {k} & '
                         f"${tex_fraction(value['rational_part'])}$ & "
                         f"${tex_fraction(value['sqrt6_coefficient'])}$ & "
                         f"{lower_decimal(value['lower_rational_bound'])} \\\\")
    (ROOT/'tables/q3_minors.tex').write_text(
        r'\begin{tabular}{@{}ccrrr@{}}'+'\n'+r'\toprule'+'\n'+
        r'Matrix & Minor & $a$ & $b$ & Certified lower bound\\'+'\n'+
        r'\midrule'+'\n'+'\n'.join(table)+'\n'+r'\bottomrule'+'\n'+r'\end{tabular}'+'\n')


if __name__=='__main__':
    main()
