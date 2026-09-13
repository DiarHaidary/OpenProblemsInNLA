"""Confluent seed and division-free collocation determinant formulation."""
from __future__ import annotations
from math import factorial,comb
import mpmath as mp

def convolution(a,b,n):
 out=[mp.mpf(0)]*(n+1)
 for i in range(min(len(a),n+1)):
  for j in range(min(len(b),n-i+1)):out[i+j]+=a[i]*b[j]
 return out

def fcoeff(a,k):
 n=len(a);h=[mp.mpf(0)]+list(a);p=[mp.mpf(1)]+[mp.mpf(0)]*n
 for _ in range(k):p=convolution(p,h,n)
 return sum(p)/factorial(k)

def seed(n):
 if n<1:raise ValueError('n must be positive')
 a=[mp.mpf(0)]*n;a[0]=-mp.root(factorial(n),n)
 for j in range(2,n+1):
  k=n-j+1
  a[j-1]=(((-1)**k)*comb(n,k)-fcoeff(a,k))*factorial(k-1)/a[0]**(k-1)
 return a

def g_coefficients(a):
 """Coefficients in increasing powers of t of g(t)=-sum j*a_j*(1-t)^(j-1)."""
 n=len(a);g=[mp.mpf(0)]*n
 for j in range(1,n+1):
  for r in range(j):g[r]-=j*a[j-1]*comb(j-1,r)*((-1)**r)
 return g

def complete_homogeneous(c,m):
 h=[mp.mpf(1)]+[mp.mpf(0)]*m
 for t in c:
  for k in range(1,m+1):h[k]+=t*h[k-1]
 return h

def pencil(c,a):
 """Returns B0,B1; det(B0-lambda B1)/n! extends across node collisions."""
 n=len(c)
 if len(a)!=n:raise ValueError('n coefficients required')
 g=g_coefficients(a);B0=mp.zeros(n);B1=mp.zeros(n)
 for k in range(n):
  h=complete_homogeneous(c[:k+1],2*n)
  for j in range(1,n+1):
   if j-1>=k:B0[k,j-1]=j*h[j-1-k]
   B1[k,j-1]=sum(g[r]*h[r+j-k] for r in range(n) if r+j>=k)
 return B0,B1

def poly_at_one_seed(a):
 """p(t) = Taylor_n exp(integral_1^t g), coefficients in powers of t."""
 n=len(a);zz=[mp.mpf(1)]+[mp.mpf(0)]*n;power=zz.copy()
 for k in range(1,n+1):
  power=convolution(power,[mp.mpf(0)]+a,n)
  for j in range(n+1):zz[j]+=power[j]/factorial(k)
 tt=[mp.mpf(0)]*(n+1)
 for j in range(n+1):
  for k in range(j+1):tt[k]+=zz[j]*comb(j,k)*((-1)**k)
 return tt

if __name__=='__main__':
 mp.mp.dps=80
 for n in range(2,16):
  a=seed(n);er=max(abs(fcoeff(a,k)-(-1)**k*comb(n,k)) for k in range(1,n+1))
  p=poly_at_one_seed(a)
  print(n,'a_negative',all(x<0 for x in a),'p_coeff_positive',all(x>0 for x in p[1:]),'residual',mp.nstr(er,3),'a', [mp.nstr(x,6) for x in a],flush=True)
