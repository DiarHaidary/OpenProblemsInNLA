// Optional high-precision Newton proposals. This file is NOT a proof checker.
// All returned binary64 centers must pass exact_backend.cpp independently.
#include <quadmath.h>
#include <vector>
#include <cmath>
#include <algorithm>
struct Z { __float128 r=0,i=0; };
static Z operator+(Z a,Z b){return {a.r+b.r,a.i+b.i};}
static Z operator-(Z a,Z b){return {a.r-b.r,a.i-b.i};}
static Z operator-(Z a){return {-a.r,-a.i};}
static Z operator*(Z a,Z b){return {a.r*b.r-a.i*b.i,a.r*b.i+a.i*b.r};}
static Z operator/(Z a,Z b){__float128 d=b.r*b.r+b.i*b.i;return {(a.r*b.r+a.i*b.i)/d,(a.i*b.r-a.r*b.i)/d};}
static __float128 square(Z a){return a.r*a.r+a.i*a.i;}
extern "C" int sp03_refine_quad(int n,const double* xin,const double* uin,double* out,int iterations){
 try{
  if(n<2||n%2||n>32||iterations<1||iterations>20)return -1;
  int m=n/2,d=n*n;
  std::vector<Z>x(d),u(d);
  for(int j=0;j<d;j++){x[j]={(__float128)xin[2*j],(__float128)xin[2*j+1]};u[j]={(__float128)uin[2*j],(__float128)uin[2*j+1]};}
  for(int it=0;it<iterations;it++){
   std::vector<Z>jx(d),xj(d),f(d),a(d*d);
   for(int i=0;i<n;i++)for(int j=0;j<n;j++){
    jx[i*n+j]=i<m?x[(i+m)*n+j]:-x[(i-m)*n+j];
    xj[i*n+j]=j<m?-x[i*n+j+m]:x[i*n+j-m];
   }
   int row=0;
   for(int i=0;i<n;i++)for(int j=i+1;j<n;j++){
    Z v;
    for(int k=0;k<n;k++){
     v=v+x[k*n+i]*jx[k*n+j];
     a[row*d+k*n+i]=a[row*d+k*n+i]+jx[k*n+j];
     a[row*d+k*n+j]=a[row*d+k*n+j]-jx[k*n+i];
    }
    if(i<m&&j==i+m)v.r-=1;
    f[row++]=v;
   }
   for(int i=0;i<n;i++)for(int j=i;j<n;j++){
    Z v;int bi=i<m?i+m:i-m,bj=j<m?j+m:j-m;
    for(int k=0;k<n;k++){
     Z ai=u[k*n+i]-x[k*n+i],aj=u[k*n+j]-x[k*n+j];
     v=v+ai*xj[k*n+j]+aj*xj[k*n+i];
     a[row*d+k*n+i]=a[row*d+k*n+i]-xj[k*n+j];
     a[row*d+k*n+j]=a[row*d+k*n+j]-xj[k*n+i];
     a[row*d+k*n+bj]=a[row*d+k*n+bj]+(j<m?-ai:ai);
     a[row*d+k*n+bi]=a[row*d+k*n+bi]+(i<m?-aj:aj);
    }
    f[row++]=v;
   }
   for(int k=0;k<d;k++){
    int pivot=k;__float128 best=square(a[k*d+k]);
    for(int i=k+1;i<d;i++){__float128 q=square(a[i*d+k]);if(q>best){best=q;pivot=i;}}
    if(best==0||isnanq(best)||isinfq(best))return 1;
    if(pivot!=k){for(int j=k;j<d;j++)std::swap(a[k*d+j],a[pivot*d+j]);std::swap(f[k],f[pivot]);}
    for(int i=k+1;i<d;i++){
     Z z=a[i*d+k]/a[k*d+k];a[i*d+k]={0,0};
     for(int j=k+1;j<d;j++)a[i*d+j]=a[i*d+j]-z*a[k*d+j];
     f[i]=f[i]-z*f[k];
    }
   }
   std::vector<Z>delta(d);
   for(int i=d-1;i>=0;i--){Z z=f[i];for(int j=i+1;j<d;j++)z=z-a[i*d+j]*delta[j];delta[i]=z/a[i*d+i];}
   for(int i=0;i<d;i++)x[i]=x[i]-delta[i];
  }
  for(int j=0;j<d;j++){
   out[2*j]=(double)x[j].r;out[2*j+1]=(double)x[j].i;
   if(!std::isfinite(out[2*j])||!std::isfinite(out[2*j+1]))return 1;
  }
  return 0;
 }catch(...){return -1;}
}
