"""Verifier for a chosen-parameter stationary-model integral enclosure."""
from fractions import Fraction as F
from rational_quadrature import model_bounds,require,floor_scaled,ceil_scaled


def verify_spec(spec):
    require(isinstance(spec,dict),'Certificate must be an object')
    require(spec.get('schema')=='sp07.stationary-model.v1','Unknown certificate schema')
    b=F(spec['b']);c=F(spec['c'])
    lower=F(spec['formal_lower']);upper=F(spec['formal_upper'])
    require(0<lower<upper,'Invalid requested formal interval')
    out=model_bounds(b,c,spec['cells'],spec['degree'],spec['bits'])
    require(F(out['formal_ratio_lower'])>lower,'Formal lower comparison failed')
    require(F(out['formal_ratio_upper'])<upper,'Formal upper comparison failed')
    require(F(out['actual_infinite_ratio_upper'])<1,'Infinite matching comparison failed')
    scale=10**20
    il=F(floor_scaled(F(out['integral_lower']),scale),scale)
    ih=F(ceil_scaled(F(out['integral_upper']),scale),scale)
    pl=F(floor_scaled(F(out['pi_lower']),scale),scale)
    ph=F(ceil_scaled(F(out['pi_upper']),scale),scale)
    require(lower*lower<(b+c)**2+(pl/(2*ih))**2,'Paper lower squared comparison failed')
    require(upper*upper>(b+c)**2+(ph/(2*il))**2,'Paper upper squared comparison failed')
    out.update(paper_integral_lower=str(il),paper_integral_upper=str(ih),
               paper_pi_lower=str(pl),paper_pi_upper=str(ph))
    out.update(status='PASS',verified_strict_formal_lower=str(lower),
               verified_strict_formal_upper=str(upper),
               scope='Chosen stationary-model parameters only; not a finite SP-07 bound')
    return out
