"""Exact rational enclosures for the two-line model integral.

Only Python's standard library is used. No floating-point value decides an
inequality. Each cell uses an integrated binomial polynomial and a geometric
remainder bound; square roots and final sums are rounded outward.
"""
from fractions import Fraction as F
from math import comb, isqrt
from typing import Sequence


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def floor_scaled(x: F, scale: int) -> int:
    return (x.numerator * scale) // x.denominator


def ceil_scaled(x: F, scale: int) -> int:
    return -((-x.numerator * scale) // x.denominator)


def sqrt_bounds(x: F, bits: int = 128) -> tuple[F, F]:
    require(x >= 0, 'Cannot enclose a negative square root')
    require(isinstance(bits, int) and bits >= 8, 'Invalid precision')
    scale = 1 << bits
    a = isqrt((x.numerator * scale * scale) // x.denominator)
    lo = F(a, scale)
    hi = lo if a*a*x.denominator == x.numerator*scale*scale else F(a+1, scale)
    require(lo*lo <= x <= hi*hi, 'Square-root enclosure failure')
    return lo, hi


def mul(a: Sequence[F], b: Sequence[F]) -> list[F]:
    out = [F(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    out[i+j] += x*y
    return out


def integrate_symmetric(a: Sequence[F]) -> F:
    return sum((2*a[j]/(j+1) for j in range(0,len(a),2)), F(0))


def atan_bounds(x: F, terms: int = 64) -> tuple[F,F]:
    require(0 < x < 1 and terms > 0, 'Invalid arctangent parameters')
    total = sum(((-1)**j*x**(2*j+1)/F(2*j+1) for j in range(terms)), F(0))
    next_term = (-1)**terms*x**(2*terms+1)/F(2*terms+1)
    return min(total,total+next_term),max(total,total+next_term)


def pi_bounds(bits: int = 128) -> tuple[F,F]:
    # Machin identity: tan(4 atan(1/5)-atan(1/239)) = 1.
    z=F(1,5); t2=2*z/(1-z*z); t4=2*t2/(1-t2*t2)
    require((t4-F(1,239))/(1+t4/F(239))==1, 'Machin rational identity failed')
    a0,a1=atan_bounds(z);b0,b1=atan_bounds(F(1,239))
    scale=1 << bits
    lo=F(floor_scaled(16*a0-4*b1,scale),scale)
    hi=F(ceil_scaled(16*a1-4*b0,scale),scale)
    require(F(3)<lo<hi<F(22,7),'Invalid pi enclosure')
    return lo,hi


def integral_bounds(b: F, c: F, cells: int=32, degree: int=12,
                    bits: int=128) -> tuple[F,F,dict]:
    require(b>=0 and c>=0 and b+c<1,'Require b,c>=0 and b+c<1')
    require(isinstance(cells,int) and 1<=cells<=4096,'Invalid cell count')
    require(isinstance(degree,int) and 1<=degree<=40,'Invalid series degree')
    require(isinstance(bits,int) and 32<=bits<=1024,'Invalid precision')
    # tan(u/2) substitution: I=2 integral_0^1 Q(t)^(-1/2) dt.
    q=[1-b*b,-4*c,2+4*c*c-2*b*b,-4*c,1-b*b]
    scale=1 << bits; sumlo=0; sumhi=0; maxr=F(0); maxtail=F(0)
    h=F(1,2*cells)
    for cell in range(cells):
        mid=F(2*cell+1,2*cells)
        shifted=[sum((q[j]*comb(j,k)*mid**(j-k)*h**k
                      for j in range(k,5)),F(0)) for k in range(5)]
        q0=shifted[0];require(q0>0,'Nonpositive cell center')
        u=[F(0)]+[z/q0 for z in shifted[1:]]
        r=sum((abs(z) for z in u),F(0));maxr=max(maxr,r)
        require(r<1,'Cell series does not converge; subdivide more finely')
        power=[F(1)];coeff=F(1);J=F(0)
        for k in range(degree+1):
            J += coeff*integrate_symmetric(power)
            if k<degree:
                power=mul(power,u)
                coeff *= -F(2*k+1,2*k+2)
        tail=2*r**(degree+1)/(1-r)
        maxtail=max(maxtail,tail)
        require(J>tail,'Integrated polynomial enclosure is not positive')
        rtlo,rthi=sqrt_bounds(q0,bits+32)
        require(rtlo>0,'Root precision too low')
        lo=2*h*(J-tail)/rthi;hi=2*h*(J+tail)/rtlo
        sumlo+=floor_scaled(lo,scale);sumhi+=ceil_scaled(hi,scale)
    lo=F(sumlo,scale);hi=F(sumhi,scale)
    require(0<lo<hi,'Invalid integral enclosure')
    return lo,hi,{'cells':cells,'binomial_degree':degree,'bits':bits,
                  'largest_relative_cell_variation':str(maxr),
                  'largest_integrated_series_tail':str(maxtail)}


def model_bounds(b: F,c: F,cells: int=32,degree: int=12,bits: int=128) -> dict:
    il,ih,detail=integral_bounds(b,c,cells,degree,bits)
    pl,ph=pi_bounds(bits)
    r2l=(b+c)**2+(pl/(2*ih))**2
    r2h=(b+c)**2+(ph/(2*il))**2
    rl,_=sqrt_bounds(r2l,bits);_,rh=sqrt_bounds(r2h,bits)
    # Actual infinite-ladder matching ratio, unlike the formal selected gap.
    actual2l=b*b+(pl/(2*ih))**2
    actual2h=b*b+(ph/(2*il))**2
    al,_=sqrt_bounds(actual2l,bits);_,ah=sqrt_bounds(actual2h,bits)
    return {'b':str(b),'c':str(c),'integral_lower':str(il),'integral_upper':str(ih),
            'pi_lower':str(pl),'pi_upper':str(ph),'T_lower':str(il/ph),'T_upper':str(ih/pl),
            'formal_ratio_lower':str(rl),'formal_ratio_upper':str(rh),
            'actual_infinite_ratio_lower':str(al),'actual_infinite_ratio_upper':str(ah),
            'quadrature':detail}
