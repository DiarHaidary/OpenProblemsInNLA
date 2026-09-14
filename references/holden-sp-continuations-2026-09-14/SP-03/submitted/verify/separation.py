"""Exact disjointness of closed complex maximum-norm balls.

The first real coordinate is swept using integer interval endpoints. For
intervals that overlap in that coordinate, a floating-point calculation may
propose another separating coordinate, but acceptance of separation is
always checked using exact Python integers and Fraction arithmetic.
"""
from __future__ import annotations
from fractions import Fraction
import heapq
import numpy as np


def pow2(exponent: int) -> Fraction:
    e=int(exponent)
    return Fraction(1<<e,1) if e>=0 else Fraction(1,1<<(-e))


def exact_gap(a: float, b: float) -> Fraction:
    ar,ad=float(a).as_integer_ratio(); br,bd=float(b).as_integer_ratio()
    return Fraction(abs(ar*bd-br*ad),ad*bd)


def check_disjoint(centers, radius_exponents):
    centers=np.asarray(centers,dtype=np.complex128)
    exponents=np.asarray(radius_exponents,dtype=np.int64)
    if centers.ndim!=2 or exponents.shape!=(len(centers),):
        raise ValueError('Expected a matrix of centers and one exponent per center')
    if not np.isfinite(centers).all(): raise ValueError('Centers must be finite')
    if len(centers)<2:
        return {'distinct':True,'balls':len(centers),'overlap_pairs_checked':0}
    ratios=[float(x).as_integer_ratio() for x in centers[:,0].real]
    E=max(max(d.bit_length()-1 for _,d in ratios),int(-np.min(exponents)),0)
    intervals=[]
    for i,((num,den),re) in enumerate(zip(ratios,exponents)):
        z=num<<(E-(den.bit_length()-1)); r=1<<(E+int(re))
        intervals.append((z-r,z+r,i))
    intervals.sort()
    active={}; heap=[]; checked=0
    for lo,hi,i in intervals:
        while heap and heap[0][0]<lo:
            _,j=heapq.heappop(heap);active.pop(j,None)
        for j in active:
            checked+=1
            # This proposal is never itself trusted as a proof inequality.
            differences=centers[i]-centers[j]
            real=abs(differences.real); imag=abs(differences.imag)
            ri=int(np.argmax(real)); ii=int(np.argmax(imag))
            if real[ri]>=imag[ii]:
                a=float(centers[i,ri].real);b=float(centers[j,ri].real)
            else:
                a=float(centers[i,ii].imag);b=float(centers[j,ii].imag)
            if exact_gap(a,b)<=pow2(exponents[i])+pow2(exponents[j]):
                return {'distinct':False,'balls':len(centers),
                        'overlap_pairs_checked':checked,'unseparated_pair':[i,j]}
        active[i]=hi;heapq.heappush(heap,(hi,i))
    return {'distinct':True,'balls':len(centers),'overlap_pairs_checked':checked,
            'arithmetic':'exact Python integers and fractions'}


def select_disjoint(centers, radius_exponents, mandatory_count=0):
    """Conservatively select exactly disjoint balls, preserving a prefix.

    This is a selection helper, not a root certificate. The mandatory prefix
    must already consist of pairwise disjoint balls. A later mandatory ball
    can revoke an earlier tentative nonmandatory ball. Rejected balls need
    not represent duplicate roots; failure to separate is treated cautiously.
    The returned subset should still be passed to check_disjoint separately.
    """
    centers=np.asarray(centers,dtype=np.complex128)
    exponents=np.asarray(radius_exponents,dtype=np.int64)
    if centers.ndim!=2 or exponents.shape!=(len(centers),):
        raise ValueError('Invalid ball arrays')
    if not isinstance(mandatory_count,int) or not 0<=mandatory_count<=len(centers):
        raise ValueError('Invalid mandatory prefix size')
    if not np.isfinite(centers).all():raise ValueError('Nonfinite centers')
    if not len(centers):return [],[]
    ratios=[float(x).as_integer_ratio() for x in centers[:,0].real]
    E=max(max(d.bit_length()-1 for _,d in ratios),int(-np.min(exponents)),0)
    intervals=[]
    for i,((a,b),re) in enumerate(zip(ratios,exponents)):
        x=a<<(E-(b.bit_length()-1));r=1<<(E+int(re))
        intervals.append((x-r,x+r,i))
    intervals.sort();active={};heap=[];keep=np.zeros(len(centers),dtype=bool);rejected=[]
    def separated(i,j):
        delta=centers[i]-centers[j];dr=abs(delta.real);di=abs(delta.imag)
        a=int(np.argmax(dr));b=int(np.argmax(di))
        if dr[a]>=di[b]:x,y=float(centers[i,a].real),float(centers[j,a].real)
        else:x,y=float(centers[i,b].imag),float(centers[j,b].imag)
        return exact_gap(x,y)>pow2(exponents[i])+pow2(exponents[j])
    for lo,hi,i in intervals:
        while heap and heap[0][0]<lo:
            _,j=heapq.heappop(heap);active.pop(j,None)
        accept=True
        for j in list(active):
            if separated(i,j):continue
            if i<mandatory_count:
                if j<mandatory_count:raise AssertionError('Mandatory balls cannot be separated')
                keep[j]=False;active.pop(j,None);rejected.append([j,i])
            else:
                accept=False;rejected.append([i,j]);break
        if accept:
            keep[i]=True;active[i]=hi;heapq.heappush(heap,(hi,i))
    if not np.all(keep[:mandatory_count]):raise AssertionError('Mandatory prefix was not preserved')
    return list(map(int,np.flatnonzero(keep))),rejected
