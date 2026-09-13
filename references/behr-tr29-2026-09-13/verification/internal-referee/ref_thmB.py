# Referee checks for REPORT.md §4 (Theorem B): non-monomial instances, ingredients (i),(iii), hypothesis necessity
import sympy as sp
exec(open('ref_check.py').read().split('print("== Lemma 2')[0])
X,Y=sp.symbols('x y')
def binary_ann(F,var0,var1,d):
    # returns list of (degree, dim Ann_deg, basis forms in a0,a1 or b0,b1)
    out={}
    for i in range(d+2):
        ms=[(i-s,s) for s in range(i+1)]
        imgs=[sp.expand(sp.diff(F,var0,m[0],var1,m[1])) if i<=d else 0 for m in ms]
        if i>d: out[i]=(i+1,None); continue
        tg=[(d-i-s,s) for s in range(d-i+1)]
        M=sp.Matrix([[sp.Poly(im,var0,var1).coeff_monomial(var0**t[0]*var1**t[1]) if im!=0 else 0 for im in imgs] for t in tg])
        out[i]=(len(ms)-M.rank(), M.nullspace(), ms)
    return out
def rs(F,var0,var1,d,s0,s1):
    ann=binary_ann(F,var0,var1,d)
    r=min(i for i in ann if ann[i][0]>0); s=d+2-r
    info=ann[r]
    phi=None
    if r<=d and info[1]:
        phi=sp.factor(sum(c*s0**m[0]*s1**m[1] for c,m in zip(info[1][0],info[2])))
    return r,s,phi
cases=[("x^4y+y^5",x**4*y+y**5,5),("x^3y^2+y^5",x**3*y**2+y**5,5),("x^5+y^5",x**5+y**5,5),("x^2y^2",x**2*y**2,4),("x^3y+x y^3",x**3*y+x*y**3,4),("(x+y)^3 y^2 + x^5", (x+y)**3*y**2+x**5,5)]
Gcases=[("u^3v+v^4",u**3*v+v**4,4),("u^2v",u**2*v,3),("u^2v^2+u^4",u**2*v**2+u**4,4),("u^4+v^4",u**4+v**4,4)]
for fn,F,A in cases:
    r,s,phi=rs(F,x,y,A,a0,a1)
    for gn,G,B in Gcases:
        r2,s2,phi2=rs(G,u,v,B,b0,b1)
        T=sp.expand(F*G)
        # ingredient (i): dims of Ann(F⊗G)_(i,k), i<=r-1, k<=s'-1 equal (i+1)*max(0,k-r'+1) if r'<s' else 0
        ok_i=True
        for i in range(r):
            for k in range(s2):
                rk,forms=kernel_forms(T,i,k,A,B)
                exp=(i+1)*max(0,k-r2+1) if r2<s2 else 0
                if len(forms)!=exp: ok_i=False
                if r2<s2 and forms and not all(sp.rem(sp.Poly(f,b0,b1,a0,a1).as_expr(),phi2,b0)==0 or sp.div(f,phi2,b0,b1)[1]==0 for f in forms): ok_i=False
        rc,_=kernel_forms(T,r-1,s2-1,A,B)
        HF = (r==s) or (phi is not None and any(e>=2 and sp.Poly(fac,a0,a1).total_degree()==1 for fac,e in sp.factor_list(phi)[1]))
        HG = (r2==s2) or (phi2 is not None and any(e>=2 and sp.Poly(fac,b0,b1).total_degree()==1 for fac,e in sp.factor_list(phi2)[1]))
        bound=r*s2+s*r2-r*r2
        RF = s if HF else r; RG = s2 if HG else r2
        print(f"F={fn} (r={r},s={s},phi={phi},H_F={HF}) G={gn} (r'={r2},s'={s2},phi'={phi2},H_G={HG}): "
              f"(i) ok={ok_i}; (iii) rankCat={rc} vs r*r'={r*r2}; ThmB bound={bound}; R(F)R(G)={RF*RG}"
              + ("" if (HF and HG) else f"  [hyp fails; naive bound {'> R(F)R(G) FALSE' if bound>RF*RG else '<= R(F)R(G)'}]"))
