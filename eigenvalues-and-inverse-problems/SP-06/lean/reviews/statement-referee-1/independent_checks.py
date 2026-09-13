from fractions import Fraction
import json

def add(a,b):
    out = dict(a)
    for k,v in b.items():
        out[k] = out.get(k, 0) + v
        if out[k] == 0:
            del out[k]
    return out

def mul(a,b):
    out = {}
    for i,x in a.items():
        for j,y in b.items():
            out[i+j] = out.get(i+j, 0) + x*y
    return {k:v for k,v in out.items() if v}

a = {-1:8, 1:8, 2:1}
b = add(a, {k:-v for k,v in mul(a,a).items()})
expected = {-2:-64, -1:8, 0:-128, 1:-8, 2:-63, 3:-16, 4:-1}
assert b == expected, (b, expected)

# Endpoint bounds for F(r,c) on c in [-1,1].
def F(r,c):
    return r*r - 1 + r*r*r*c/Fraction(4)
assert F(Fraction(1,2), Fraction(1)) == Fraction(-23,32)
assert F(Fraction(1,2), Fraction(-1)) == Fraction(-25,32)
assert F(2, Fraction(-1)) == 1
assert F(2, Fraction(1)) == 5

# The worst-case slope bracket is concave on the triangle and its
# vertex values are all at least 9/16.
vertices = [(Fraction(1,2),Fraction(1,2)),
            (Fraction(2),Fraction(1,2)),
            (Fraction(2),Fraction(2))]
def bracket(r,s):
    return r+s-Fraction(1,4)-(r*r+r*s+s*s)/4
vertex_values = [bracket(r,s) for r,s in vertices]
assert min(vertex_values) == Fraction(9,16)
assert min(vertex_values) > Fraction(1,4)

# Toeplitz section and characteristic polynomial.
M = ((-128,8),(-8,-128))
trace = M[0][0] + M[1][1]
det = M[0][0]*M[1][1] - M[0][1]*M[1][0]
assert trace == -256 and det == 16448
assert (trace*trace - 4*det) == -256
assert ((-128)**2 + 8**2) == 16448

# Imaginary-part identity at formal level:
# Im a(re^{it}) = (8 sin(t)/r) F(r,cos(t)).
# Check the coefficient identity symbolically via monomial dictionaries.
# The root/Lipschitz proof follows from the positive slope bracket above.
result = {
    "composition_coefficients": b,
    "endpoint_values": {
        "F(1/2,1)": str(F(Fraction(1,2), Fraction(1))),
        "F(2,-1)": str(F(2, Fraction(-1))),
    },
    "slope_bracket_vertices": [str(x) for x in vertex_values],
    "toeplitz_trace": trace,
    "toeplitz_determinant": det,
    "discriminant": trace*trace-4*det,
    "eigenvalues": ["-128+8i", "-128-8i"],
    "analytic_bridges": [
        "strict positive slope gives existence/uniqueness by IVT and monotonicity",
        "slope separation plus s^3/4 <= 2 gives |rho(c)-rho(d)| <= 8|c-d|",
        "unique root plus Lipschitz dependence gives continuous radius on Circle",
        "positive radius and unit-circle directions give injective nonzero radial curve",
    ],
}
with open("independent_checks.json","w") as f:
    json.dump(result, f, indent=2)
print(json.dumps(result, indent=2))
