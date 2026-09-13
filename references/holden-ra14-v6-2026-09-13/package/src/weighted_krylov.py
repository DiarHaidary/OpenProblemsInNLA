"""Components of the finite-dimensional weighted Krylov obstruction.

This is floating-point diagnostic code.  It neither proves an oracle lower
bound nor implements an unrestricted RA-14 solver.  The mathematical theorem
and its exact model restrictions are in report.pdf and PROOF_AUDIT.md.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Callable
import numpy as np
from numpy.typing import NDArray
from scipy.linalg import eigh, qr

Array = NDArray[np.float64]


def _positive_int(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return int(value)


def _accuracy(epsilon: float) -> float:
    e = float(epsilon)
    if not math.isfinite(e) or not 0 < e < 0.5:
        raise ValueError("epsilon must be finite and lie strictly between 0 and 1/2")
    return e


def log_cosh(value: float) -> float:
    x = abs(float(value))
    return x + math.log1p(math.exp(-2*x)) - math.log(2.0)


@dataclass(frozen=True)
class ChebyshevGeometry:
    degree: int
    epsilon: float
    nodes: Array
    tail_weights: Array      # tau^2 - x_j^2, not probability weights
    normalized_lagrange_abs: Array  # |ell_j(a)| / T_d(a)
    allocation_weights: Array
    log_chebyshev_at_spike: float
    weighted_lagrange_over_chebyshev: float  # L / T_d(a)
    harmonic_number: float


def chebyshev_geometry(degree: int, epsilon: float) -> ChebyshevGeometry:
    """Stable node/weight geometry, also when epsilon is much smaller than 1."""
    d = _positive_int(degree, "degree")
    e = _accuracy(epsilon)
    j = np.arange(d+1, dtype=float)
    theta = np.pi*j/d
    half_sine_sq = np.sin(theta/2)**2
    nodes = np.cos(theta)
    # Use (tau-x)(tau+x) and a-x directly to avoid cancellation near x=1.
    edge = (e + 2*half_sine_sq) * (2 + e - 2*half_sine_sq)
    # At -1, the second factor may still suffer cancellation for tiny e.
    edge[-1] = e*(2+e)
    edge[0] = e*(2+e)
    distance = 2*e + 2*half_sine_sq
    endpoint = np.ones(d+1)
    endpoint[[0, -1]] = 0.5
    raw = endpoint/distance
    lagrange = raw/raw.sum()
    scaled = lagrange*np.sqrt(edge)
    weighted = float(scaled.sum())
    allocation = scaled/weighted
    return ChebyshevGeometry(
        d, e, nodes, edge, lagrange, allocation,
        log_cosh(2*d*math.asinh(math.sqrt(e))), weighted,
        math.fsum(1/j for j in range(1, d+1)),
    )


@dataclass(frozen=True)
class HardSpectrum:
    n: int
    k: int
    width: int
    degree: int
    epsilon: float
    geometry: ChebyshevGeometry
    multiplicities: NDArray[np.int64]
    eigenvalues: Array
    allocation_condition: bool
    log_analytic_condition: float


def hard_spectrum(n: int, k: int, width: int, degree: int, epsilon: float) -> HardSpectrum:
    """Construct the proof's finite spectrum; reject an insufficient budget."""
    n = _positive_int(n, "n")
    k = _positive_int(k, "k")
    b = _positive_int(width, "width")
    d = _positive_int(degree, "degree")
    e = _accuracy(epsilon)
    if k >= n:
        raise ValueError("require k < n")
    if not 1 < 1+e < 1+2*e:
        raise ValueError("epsilon is too small to represent the diagnostic spectrum in float64; use the symbolic formulas instead")
    allocation_ok = 2*(8*b+1)*(d+1) <= n-k
    if not allocation_ok:
        raise ValueError("the theorem's multiplicity-budget condition is not satisfied")
    geo = chebyshev_geometry(d, e)
    half_budget = (n-k)/2
    multiplicities = 8*b + np.ceil(half_budget*geo.allocation_weights).astype(np.int64)
    remaining = n-k-int(multiplicities.sum())
    if remaining < 0:
        raise ArithmeticError("rounding violated the proved multiplicity budget")
    multiplicities[0] += remaining
    spectrum = np.concatenate([np.full(k, 1+2*e), np.repeat(geo.nodes, multiplicities)])
    log_condition = (
        math.log(1e9) + math.log((k+b)/(n-k))
        + 2*math.log(math.log(math.e*d)) + 4*d*math.sqrt(e)
    )
    return HardSpectrum(n,k,b,d,e,geo,multiplicities,spectrum,True,log_condition)


def split_gaussian(omega: Array, spectrum: HardSpectrum) -> tuple[Array, list[Array]]:
    om = np.asarray(omega, dtype=float)
    if om.shape != (spectrum.n, spectrum.width):
        raise ValueError("omega has the wrong shape")
    top = om[:spectrum.k]
    blocks = []
    first = spectrum.k
    for m in spectrum.multiplicities:
        blocks.append(om[first:first+int(m)])
        first += int(m)
    return top, blocks


def interpolation_budget(omega: Array, spectrum: HardSpectrum) -> dict[str, float]:
    """Evaluate S/T_d(a)^2 and the pathwise scalar cone upper bound."""
    top, blocks = split_gaussian(omega, spectrum)
    geo = spectrum.geometry
    gram_inverses = []
    for block in blocks:
        smallest = float(np.linalg.eigvalsh(block.T@block)[0])
        if smallest <= 0:
            raise np.linalg.LinAlgError("nonpositive Gram eigenvalue in floating-point computation")
        gram_inverses.append(1/smallest)
    lag = geo.normalized_lagrange_abs
    normalized_s = float(np.sum(lag**2*geo.tail_weights*np.asarray(gram_inverses)))
    top_norm_sq = float(np.linalg.norm(top, 2)**2)
    log_pathwise = math.log(top_norm_sq) + math.log(normalized_s) + 2*geo.log_chebyshev_at_spike
    delta = spectrum.epsilon*(2+3*spectrum.epsilon)
    mean_normalized_bound = 6000*geo.weighted_lagrange_over_chebyshev**2/(spectrum.n-spectrum.k)
    return {
        'normalized_S': normalized_s,
        'normalized_S_expectation_bound': mean_normalized_bound,
        'top_norm_squared': top_norm_sq,
        'log_pathwise_cone_upper': log_pathwise,
        'log_delta': math.log(delta),
        'pathwise_cone_certificate': float(log_pathwise < math.log(delta)),
        'markov_event': float(normalized_s <= 4*mean_normalized_bound),
        'top_norm_event': float(top_norm_sq <= 100*(spectrum.k+spectrum.width)),
    }


def chebyshev_feature_blocks(omega: Array, spectrum: HardSpectrum) -> tuple[Array, Array]:
    """Coefficient-space top and weighted-tail matrices for the whole prefix.

    Every coefficient vector c produces z_top=top@c and
    E^(-1/2)z_tail=tail@c.  The polynomial basis is Chebyshev, not monomials.
    """
    top, blocks = split_gaussian(omega, spectrum)
    d = spectrum.degree
    h = 2*math.asinh(math.sqrt(spectrum.epsilon))
    top_feature = np.concatenate([math.cosh(j*h)*top for j in range(d+1)], axis=1)
    tail = []
    for j, block in enumerate(blocks):
        angles = np.arange(d+1)*np.pi*j/d
        row_block = np.concatenate([math.cos(angle)*block for angle in angles], axis=1)
        tail.append(row_block/math.sqrt(spectrum.geometry.tail_weights[j]))
    return top_feature, np.vstack(tail)


def numerical_cone_optimum(omega: Array, spectrum: HardSpectrum) -> dict[str, float]:
    """Diagnostic maximum top/tail quotient over the full Krylov prefix.

    An eigenvalue computation in coefficient coordinates avoids searching over
    outputs.  This is a floating-point diagnostic, NOT an interval certificate.
    """
    top, tail = chebyshev_feature_blocks(omega, spectrum)
    _, r = qr(tail, mode='economic', check_finite=True)
    singular = np.linalg.svd(r, compute_uv=False)
    if singular[-1] <= 0:
        raise np.linalg.LinAlgError("numerically singular weighted-tail feature matrix")
    # c=R^{-1}y; the supremum is ||top R^{-1}||^2.
    transformed = np.linalg.solve(r.T, top.T).T
    optimum = float(np.linalg.norm(transformed, 2)**2)
    delta = spectrum.epsilon*(2+3*spectrum.epsilon)
    return {
        'max_top_over_weighted_tail': optimum,
        'delta': delta,
        'optimum_over_delta': optimum/delta,
        'tail_feature_condition': float(singular[0]/singular[-1]),
        'numerical_no_nonzero_cone_vector': float(optimum < delta),
    }


def graph_residual_and_cone(epsilon: float, tail_nodes: Array, graph: Array) -> dict[str, float]:
    """Check the exact residual/weighted-cone equivalence on a supplied graph."""
    e = _accuracy(epsilon)
    nodes = np.asarray(tail_nodes, dtype=float)
    f = np.asarray(graph, dtype=float)
    if f.ndim != 2 or nodes.shape != (f.shape[0],):
        raise ValueError("graph and tail dimensions do not agree")
    if np.max(np.abs(nodes)) > 1:
        raise ValueError("tail eigenvalues must lie in [-1,1]")
    k = f.shape[1]
    stack = np.vstack([np.eye(k), f])
    z = np.linalg.qr(stack, mode='reduced')[0]
    eig = np.concatenate([np.full(k,1+2*e),nodes])
    residual = float(np.linalg.norm(eig[:,None]*(np.eye(len(eig))-z@z.T),2))
    weights = ((1+e)-nodes)*((1+e)+nodes)
    delta = e*(2+3*e)
    cone_matrix = delta*f.T@(f/weights[:,None])
    cone_max = float(np.linalg.eigvalsh(cone_matrix)[-1])
    return {'residual':residual, 'threshold':1+e, 'cone_max':cone_max}


def global_scales(n: int, k: int, epsilon: float) -> tuple[float, float]:
    n = _positive_int(n,'n'); k = _positive_int(k,'k'); e = _accuracy(epsilon)
    if k >= n:
        raise ValueError("require k<n")
    s = math.sqrt(e); x=n/k; y=x*s
    lower = n*math.log1p(y)/y
    upper = min(float(n), (k/s)*math.log(math.e*x))
    return lower, upper


def full_block_upper_parameters(n: int, k: int, epsilon: float) -> dict[str, int | str]:
    n=_positive_int(n,'n'); k=_positive_int(k,'k'); e=_accuracy(epsilon)
    if k>=n:
        raise ValueError("require k<n")
    b=256*(2*k+1)
    if b>n:
        return {'branch':'exact_columns','queries':n,'width':n,'degree':0}
    s=math.sqrt(e)
    d1=math.ceil(math.log(16*n/((k+1)*e))/(2*s))
    d2=math.ceil(math.log(96*n/(k*e))/s)
    degree=max(d1+1,2*d2)
    budget=2*b*degree
    if n<=budget:
        return {'branch':'exact_columns','queries':n,'width':n,'degree':0}
    return {'branch':'full_block','queries':budget,'width':b,'degree':degree}


class CountingTwoSidedOracle:
    """A minimal query counter for testing the prescribed full-block prefix."""
    def __init__(self, matrix: Array):
        a=np.asarray(matrix,dtype=float)
        if a.ndim!=2 or a.shape[0]!=a.shape[1] or not np.all(np.isfinite(a)):
            raise ValueError('matrix must be a finite real square array')
        self._a=a.copy(); self.n=a.shape[0]; self.queries=0
    def product(self, block: Array, transpose: bool=False) -> Array:
        b=np.asarray(block,dtype=float)
        if b.ndim!=2 or b.shape[0]!=self.n:
            raise ValueError('a two-dimensional block of height n is required')
        self.queries+=b.shape[1]
        return (self._a.T if transpose else self._a)@b


def full_normal_prefix(oracle: CountingTwoSidedOracle, start: Array, degree: int) -> list[Array]:
    """Compute [Omega,M Omega,...,M^d Omega], M=A^T A, charging every column."""
    if not isinstance(degree,int) or degree<0:
        raise ValueError('degree must be a nonnegative integer')
    omega=np.asarray(start,dtype=float)
    if omega.ndim!=2 or omega.shape[0]!=oracle.n:
        raise ValueError('invalid starting block')
    blocks=[omega.copy()]
    for _ in range(degree):
        blocks.append(oracle.product(oracle.product(blocks[-1]),transpose=True))
    return blocks


def shifted_kernel_posterior_geometry(j: Array, b: Array, q: Array, shift: float) -> dict[str, Array | float]:
    """Algebra in the shifted hard-edge posterior; no sampling claim is made.

    Requires J > shift I. Q is an orthonormal residual-kernel frame. The
    omitted density factor is independent of Q. All quantities are diagnostic.
    """
    j=np.asarray(j,dtype=float); b=np.asarray(b,dtype=float); q=np.asarray(q,dtype=float)
    h=float(shift)
    if not math.isfinite(h) or h<0 or j.ndim!=2 or j.shape[0]!=j.shape[1]:
        raise ValueError('invalid shift or queried compression')
    t=j.shape[0]
    if b.ndim!=2 or b.shape[1]!=t or q.ndim!=2 or q.shape[0]!=b.shape[0]:
        raise ValueError('incompatible matrix dimensions')
    if t>0 and np.linalg.eigvalsh(j-h*np.eye(t))[0]<=0:
        raise ValueError('the posterior formula requires J > shift I')
    if not 0<q.shape[1]<q.shape[0]:
        raise ValueError('the residual kernel must have positive dimension and codimension')
    if not np.allclose(q.T@q,np.eye(q.shape[1]),rtol=1e-11,atol=1e-11):
        raise ValueError('Q must be orthonormal')
    invj=np.linalg.inv(j); invshift=np.linalg.inv(j-h*np.eye(t))
    k_matrix=b@invj@invj@b.T
    r_matrix=np.eye(b.shape[0])+b@invj@invshift@b.T
    from scipy.linalg import null_space
    v=null_space(q.T)
    qq=q.T@r_matrix@q
    short=v.T@r_matrix@v-v.T@r_matrix@q@np.linalg.solve(qq,q.T@r_matrix@v)
    c=q.T@k_matrix@q
    score=(1-q.shape[1])/2*np.linalg.slogdet(np.eye(q.shape[1])+c)[1]
    score+=h/2*np.trace(np.linalg.solve(qq,q.T@r_matrix@r_matrix@q))
    alternate=(1-q.shape[1])/2*np.linalg.slogdet(np.eye(q.shape[1])+c)[1]-h/2*np.trace(short)
    return {'K':k_matrix,'R':r_matrix,'shorted_R':short,'complement':v,
            'log_density_up_to_constant':float(score),
            'log_density_with_trace_constant':float(alternate)}


def shifted_rank_one_parameters(n: int, epsilon: float) -> dict[str, int | float | str]:
    """Budget for the averaged shifted-Wishart rank-one result only.

    This is NOT an all-input RA-14 algorithm with an F-scale guarantee.
    The polynomial branch assumes the specific shifted ensemble in the report.
    """
    if not isinstance(n,int) or isinstance(n,bool) or n<8:
        raise ValueError('n must be an integer at least eight')
    e=float(epsilon)
    if not math.isfinite(e) or not 0<e<=1/16:
        raise ValueError('epsilon must lie in (0, 1/16]')
    s=math.sqrt(e); y=n*s
    f=math.log1p(y)/s
    if y<2:
        return {'branch':'exact_columns','queries':n,'degree':0,'F_scale':f,'y':y}
    log_target=math.log(2e12)+math.log(y)+math.log1p(1/(2e12*y))
    degree=math.ceil(log_target/(8*s))
    if degree>=n:
        return {'branch':'exact_columns','queries':n,'degree':0,'F_scale':f,'y':y}
    return {'branch':'shifted_ensemble_polynomial','queries':degree,'degree':degree,
            'F_scale':f,'y':y,'tail_endpoint':1-4*e}


def shifted_rank_one_filter(oracle: CountingTwoSidedOracle, epsilon: float,
                           rng: np.random.Generator) -> tuple[Array, dict]:
    """Oracle-counted implementation of the shifted-ensemble rank-one method.

    No eigenvalues or hidden kernel are consulted. The exact branch is valid
    for every matrix; the polynomial branch has only the ensemble-average
    guarantee proved in the report. Floating point is not the exact-real model.
    """
    parameters=shifted_rank_one_parameters(oracle.n,epsilon)
    before=oracle.queries
    if parameters['branch']=='exact_columns':
        matrix=oracle.product(np.eye(oracle.n))
        _,_,vt=np.linalg.svd(matrix,full_matrices=False)
        z=vt[:1].T
    else:
        b=float(parameters['tail_endpoint']); degree=int(parameters['degree'])
        previous=rng.normal(size=(oracle.n,1))
        current=2*oracle.product(previous)/b-previous
        for _ in range(1,degree):
            following=4*oracle.product(current)/b-2*current-previous
            previous,current=current,following
        scale=float(np.max(np.abs(current)))
        if not math.isfinite(scale) or scale==0:
            raise FloatingPointError('polynomial vector is zero or non-finite')
        current=current/scale
        z=current/np.linalg.norm(current)
    metadata=dict(parameters)
    metadata['actual_queries']=oracle.queries-before
    if metadata['actual_queries']!=metadata['queries']:
        raise RuntimeError('query accounting mismatch')
    return z,metadata


def wishart_resolvent_terms(g: Array, shift: float) -> dict[str, float | Array]:
    """Pointwise terms in the Gaussian resolvent integration identity.

    The identity involving r is an expectation identity, not a pointwise one.
    The returned divergence is pointwise and can be checked by differentiation.
    """
    g=np.asarray(g,dtype=float); t=float(shift)
    if g.ndim!=2 or not np.all(np.isfinite(g)) or not math.isfinite(t) or t<=0:
        raise ValueError('a finite matrix and a positive shift are required')
    r,N=g.shape
    if r<1 or N<r+1:
        raise ValueError('the resolvent bound requires at least r+1 columns')
    w=g@g.T; resolvent=np.linalg.inv(w+t*np.eye(r))
    trace=float(np.trace(resolvent)); trace_square=float(np.trace(resolvent@resolvent))
    trace_wr=float(np.trace(w@resolvent))
    divergence=N*trace-float(np.trace(resolvent@w@resolvent))-trace_wr*trace
    return {'resolvent':resolvent,'trace':trace,'trace_resolvent_square':trace_square,
            'squared_trace':trace*trace,'trace_WR':trace_wr,
            'gaussian_field_divergence':divergence,
            'expectation_identity_rhs':(N-r-1+t)*trace+t*trace_square+t*trace*trace,
            'r':r,'N':N,'proved_mean_trace_upper':math.sqrt(r/t)}
