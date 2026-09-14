# Continuation proof notes

These are supporting results, not an evaluation of the unrestricted SP-07 constant.

## Polygon completion theorem

Let p>=3 be odd, omega=exp(2 pi i/p), D_s=R diag(omega^j).
Let X be a Hermitian circulant contraction with X 1=1 and Fourier eigenvalues
lambda_0=1, lambda_j in [-1,1]. Set theta_j=acos(lambda_j)/2 for j=1,...,p-1.
Over all Hermitian-unitary completions U of X and arbitrary square complementary
matrices C (not required normal), the exact infimum of
||{D_s directsum C,U}|| is

2R max(cos(theta_1), cos(theta_{p-1}),
        max_{1<=j<=p-2}|cos(theta_j+theta_{j+1})|).

Proof: compress any completion to the selected space plus the defect space;
this reduces U. Add zero dummy complementary coordinates for endpoint eigenvalues
if needed. In Fourier coordinates the selected D_s is a cyclic shift. A cyclic
phase average, commuting with U and rotating D_s back to itself, eliminates all
complementary entries except the forward broken shift. Pinching into U's positive
and negative eigenspaces leaves two weighted shifts. Each complementary edge z
minimizes max(|RA+zB|,|RB+zA|) at z=-R, with value R|A-B|.
Here A=cos(theta_j)cos(theta_{j+1}), B=sin(theta_j)sin(theta_{j+1}).

Minimizing over the angles gives sin(pi/(2p)). If M=sin(gamma), endpoints force
both end angles >=pi/2-gamma. The alternating sum of the p-2 internal angle sums
bounds their sum by pi/2+(p-2)gamma, hence gamma>=pi/(2p). Equality occurs at
j odd: theta_j=pi/2-j*pi/(2p); j even: theta_j=j*pi/(2p).
Thus every such completion has norm >=2R sin(pi/(2p)), the selected pair-sum gap.
The relaxed infimum is attained by a broken shift C=-R S, normally nonnormal.

For the compressed-optimal overlap lambda_j=(-1)^j(1-2j/p), the compressed norm
is exactly 2R/p. Odd alternating telescoping proves this is the minimum. Its
full relaxed completion norm is exactly 2R/sqrt(p). The selected compressed ratio
is p sin(pi/(2p)) -> pi/2, but the completed selected ratio is
sqrt(p) sin(pi/(2p)) ->0.

## Remove the circulant restriction from the obstruction (not the exact formula)

Suppose an arbitrary Hermitian contraction X is the leading block of U and has
a unit vector v with Xv=v. Rotate p copies of the pair by the cyclic permutation
of selected polygon coordinates, multiplying the diagonal matrix by the inverse
spectral phase to keep each selected block D_s unchanged. Norms are unchanged.
The direct sum has common vector w=(rotated v)/sqrt(p), fixed by the direct-sum U.
For each distinct selected eigenvalue, its spectral projection of w has norm
1/sqrt(p). Their normalized vectors define a p-dimensional reducing subspace for
D. In this basis the compressed reflection block is Hermitian circulant with
constant eigenvector of eigenvalue 1: its entries are cyclic sums
sum_g conjugate(v_{i-g}) X_{i-g,j-g} v_{j-g}.
The remaining block of D is arbitrary, so the proved circulant-completion theorem
applies. Thus the polygon selected gap is <= the full norm even for arbitrary X
with eigenvalue 1. No assertion is made that this is the full matching distance
of the extended normal pair. A -1 eigenvector is handled by replacing U by -U.

## Two-line stationary model

On periodic vector functions, D=-i d/dtheta +1/4+i diag(y_s,y_c).
For V=e^{-i theta/2}(i sin(phi) I+cos(phi) sigma_x), and reflection of the angular
variable J, U=V J is a self-adjoint unitary when phi is odd and increases by pi
under theta->theta+2pi. Its anticommutator is a bounded multiplier times J.
Writing B=y_s+y_c, C=y_s-y_c>=0, its exact norm is
sup_theta [sqrt(phi'(theta)^2+B^2)+C|sin(phi(theta))|].
For B,C>0 and phi(0)=0, phi(pi)=pi/2, the minimal cost T is the unique T>B+C with
integral_0^{pi/2} ((T-C sin u)^2-B^2)^(-1/2) du=pi.
An integral primitive proves the lower bound even for nonmonotone paths; the
positive ODE saturates the norm and attains it.

Normalize b=B/T, c=C/T. Then T=I(b,c)/pi and the formal selected-gap quotient is
sqrt((b+c)^2+(pi/(2I))^2). Its numerically optimized value is near 1.03730541764.
This is NOT a finite normal-matrix bound: both infinite spectral ladders have
infinite multiplicity count and no finite Hall deficit. No norm-controlled finite
approximation or unrestricted extremality theorem is supplied.

## Final audit clarifications

The orbit dilation in Theorem 3.2 of the final report proves the constant-one
polygon obstruction for arbitrary overlaps with an eigenvalue +1 or -1, not
merely for circulant overlaps. The exact fixed-overlap formula itself retains
the circulant hypothesis.

The actual matching between the two bilateral infinite spectral ladders is
explicit: exchange the channels and send index m to -m. Its bottleneck is
sqrt(1/4+B^2), strictly smaller than the optimal phase norm when C>0. Thus the
formal selected gap is not the actual infinite matching distance. The final
report and rational certificate keep these quantities separate.
