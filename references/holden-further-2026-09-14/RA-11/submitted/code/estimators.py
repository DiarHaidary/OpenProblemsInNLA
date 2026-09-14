"""Numerical references. No floating-point stability or exact-bit theorem is implied.

The diagonal algorithm implements the explicit query design in the manuscript.
The probability-bound routine returns floating-point log bounds, not certified
outward-rounded integer guarantees. Exact mathematical formulas are in the note.
"""
from __future__ import annotations
from dataclasses import dataclass
import hashlib
import math
from typing import Sequence
import numpy as np


@dataclass
class ProductOracle:
    matrix: np.ndarray
    n: int
    q: int
    budget: int | None = None

    def __post_init__(self):
        self.matrix=np.asarray(self.matrix,dtype=float)
        if self.n<2 or self.q<1 or self.matrix.shape!=(self.n**self.q,)*2:
            raise ValueError('Incompatible dimensions.')
        self.calls=0
        self._hash=hashlib.sha256()

    def __call__(self, factors: Sequence[np.ndarray]) -> np.ndarray:
        if len(factors)!=self.q:
            raise ValueError('A call must supply exactly q local factors.')
        if self.budget is not None and self.calls>=self.budget:
            raise RuntimeError('Oracle budget exhausted before issuing this call.')
        vector=np.ones(1)
        for factor in factors:
            raw=np.asarray(factor)
            if np.iscomplexobj(raw) or raw.shape!=(self.n,) or not np.all(np.isfinite(raw)):
                raise ValueError('Actual oracle inputs must be finite real local vectors.')
            raw=np.asarray(raw,dtype=np.float64)
            self._hash.update(raw.tobytes())
            vector=np.kron(vector,raw)
        self.calls+=1
        return self.matrix@vector

    @property
    def query_hash(self):
        return self._hash.hexdigest()


def coordinate_factors(index:int,n:int,q:int):
    if not 0<=index<n**q: raise ValueError('Coordinate out of range.')
    digits=[0]*q
    for j in range(q-1,-1,-1):
        index,digits[j]=divmod(index,n)
    return [np.eye(n)[d] for d in digits]


def diagonal_control(oracle:ProductOracle,epsilon:float,seed:int=0,
                     force_training_count:int|None=None):
    if not 0<epsilon<0.5: raise ValueError('epsilon must be in (0,1/2).')
    n,q=oracle.n,oracle.q; N=n**q
    power_two=(N&(N-1))==0
    reciprocal_bound=N if power_two else 2*N
    m=math.ceil(math.sqrt(3*reciprocal_bound)/epsilon)
    if force_training_count is not None:
        if force_training_count<1: raise ValueError('Training count must be positive.')
        m=int(force_training_count)
    start=oracle.calls
    if force_training_count is None and 2*m>=N:
        if oracle.budget is not None and oracle.budget-start<N:
            raise RuntimeError('Insufficient budget for the selected basis branch.')
        value=0.0
        for i in range(N): value+=oracle(coordinate_factors(i,n,q))[i]
        return {'estimate':value,'calls':oracle.calls-start,'branch':'exact_basis','m':0,
                'query_hash':oracle.query_hash}
    if oracle.budget is not None and oracle.budget-start<2*m:
        raise RuntimeError('Insufficient budget before any estimator call.')
    B=(N-1).bit_length()
    if B>=63: raise ValueError('This numerical reference limits integer sampling to B<63.')
    rng=np.random.default_rng(seed)
    # Draw the ENTIRE query design before observing any responses.
    training=rng.integers(0,2,size=(m,q,n),dtype=np.int8)*2-1
    draws=rng.integers(0,1<<B,size=m,dtype=np.int64)
    indices=draws%N
    denom=1<<B; quotient,remainder=divmod(denom,N)
    probs=(quotient+(indices<remainder).astype(int))/denom
    a=np.zeros(N)
    for factors in training:
        x=np.ones(1)
        for factor in factors: x=np.kron(x,factor)
        a+=x*oracle(factors)
    a/=m
    corrections=[]
    for index,p in zip(indices,probs):
        i=int(index)
        d=oracle(coordinate_factors(i,n,q))[i]
        corrections.append((d-a[i])/p)
    value=float(a.sum()+np.mean(corrections))
    return {'estimate':value,'calls':oracle.calls-start,'branch':'diagonal_control',
            'm':m,'query_hash':oracle.query_hash,
            'relative_variance_bound':reciprocal_bound/(m*m),
            'forced_diagnostic_count':force_training_count is not None}


def log_fractional_bound(n:int,q:int,epsilon:float,finite_bits:bool=True):
    """Grid-refined log query count, useful for comparison, not certified rounding."""
    if n<2 or q<1 or not 0<epsilon<0.5: raise ValueError('Invalid parameters.')
    def objective(t):
        f=t*math.log(n)-math.fsum(math.log1p(t/k) for k in range(2,n+1))
        return math.log(q+1)+(math.log(6)+q*f-(1+t)*math.log(epsilon))/t
    # Convex-in-1/t style one-dimensional search, including t=1.
    lo,hi=1e-8,1.0
    phi=(math.sqrt(5)-1)/2
    a=hi-phi*(hi-lo); b=lo+phi*(hi-lo)
    for _ in range(100):
        if objective(a)<objective(b):
            hi=b; b=a; a=hi-phi*(hi-lo)
        else:
            lo=a; a=b; b=lo+phi*(hi-lo)
    t=min([1.0,(lo+hi)/2],key=objective)
    log_count=objective(t)+(math.log(2) if finite_bits else 0)
    D=math.log(n)-math.fsum(1/k for k in range(2,n+1))
    return {'n':n,'q':q,'epsilon':epsilon,'p':1+t,'log_unrounded_query_bound':log_count,
            'D_n':D,'finite_bit_factor_included':finite_bits,
            'note':'Floating-point evaluation; final ceilings not included.'}
