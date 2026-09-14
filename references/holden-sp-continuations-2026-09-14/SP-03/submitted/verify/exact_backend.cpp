// Exact dyadic contraction inequalities for the SP-03 polynomial system.
// Floating-point inputs are interpreted as exact binary rationals. No
// floating-point operation participates in a certificate acceptance decision.
#include <boost/multiprecision/cpp_int.hpp>
#include <vector>
#include <cstdint>
#include <cstring>
#include <cmath>
#include <algorithm>
#include <stdexcept>
#include <limits>
static_assert(sizeof(double)==8 && std::numeric_limits<double>::is_iec559,
              "The certificate decoder requires IEEE binary64 doubles");
using boost::multiprecision::cpp_int;
struct C { cpp_int r=0,i=0; };
static C add(const C&a,const C&b){return {a.r+b.r,a.i+b.i};}
static C neg(const C&a){return {-a.r,-a.i};}
static C sub(const C&a,const C&b){return {a.r-b.r,a.i-b.i};}
static C mul(const C&a,const C&b){return {a.r*b.r-a.i*b.i,a.r*b.i+a.i*b.r};}
static cpp_int ab(const cpp_int&a){return a<0?-a:a;}
static cpp_int norm(const C&a){return ab(a.r)+ab(a.i);}
struct Part{std::uint64_t mant;int exp;bool minus;};
static Part parts(double x){
 std::uint64_t bits;std::memcpy(&bits,&x,sizeof bits);
 unsigned e=(bits>>52)&2047;std::uint64_t mant=bits&((std::uint64_t(1)<<52)-1);
 if(e==2047)throw std::runtime_error("Non-finite input");
 if(e){mant|=std::uint64_t(1)<<52;return {mant,int(e)-1023-52,bool(bits>>63)};}
 return {mant,-1074,bool(bits>>63)};
}
static int common_exp(const double*x,int count){
 int E=0;for(int j=0;j<count;j++){auto p=parts(x[j]);if(p.mant)E=std::max(E,-p.exp);}return E;
}
static cpp_int scaled(double x,int E){auto p=parts(x);cpp_int v=p.mant;if(p.mant)v<<=(E+p.exp);return p.minus?-v:v;}
static std::vector<C> convert(const double*x,int count,int E){
 std::vector<C> v(count);for(int j=0;j<count;j++)v[j]={scaled(x[2*j],E),scaled(x[2*j+1],E)};return v;
}
struct Term{cpp_int num;int exp;};
static bool sum_less(const std::vector<Term>&t,int target_exp){
 int low=target_exp;for(auto &v:t)low=std::min(low,v.exp);
 cpp_int s=0;for(auto &v:t)s+=v.num<<(v.exp-low);
 cpp_int rhs=cpp_int(1)<<(target_exp-low);return s<rhs;
}
static double estimate(const cpp_int&n,int exponent){
 if(n==0)return 0.;
 unsigned k=boost::multiprecision::msb(n);
 int shift=k>52?int(k)-52:0;
 cpp_int high=n>>shift;
 return std::ldexp(high.convert_to<double>(),exponent+shift);
}
extern "C" const char* sp03_backend_version(){return "exact-dyadic-1";}
// Returns 0 on a passed contraction certificate, 1 if inequalities fail,
// -1 on invalid inputs. bounds[0..3] contain informational eta,z0,z2,r only.
extern "C" int sp03_verify(int n,const double*x0,const double*u0,const double*b0,int*radius_exponent,double*bounds){
 try{
  if(n<2 || n%2 || n>64)return -1;
  int m=n/2,d=n*n;
  int E=std::max(common_exp(x0,2*d),common_exp(u0,2*d));
  int Ey=common_exp(b0,2*d*d);
  auto x=convert(x0,d,E),u=convert(u0,d,E),B=convert(b0,d*d,Ey);
  std::vector<C> jx(d),xj(d),F(d),A(d*d);
  for(int a=0;a<n;a++)for(int b=0;b<n;b++){
   jx[a*n+b]=(a<m?x[(a+m)*n+b]:neg(x[(a-m)*n+b]));
   xj[a*n+b]=(b<m?neg(x[a*n+b+m]):x[a*n+b-m]);
  }
  int row=0;
  for(int i=0;i<n;i++)for(int j=i+1;j<n;j++){
   C v;
   for(int a=0;a<n;a++){
    v=add(v,mul(x[a*n+i],jx[a*n+j]));
    int ci=row*d+a*n+i,cj=row*d+a*n+j;
    A[ci]=add(A[ci],jx[a*n+j]);A[cj]=sub(A[cj],jx[a*n+i]);
   }
   if(i<m && j==i+m)v.r-=cpp_int(1)<<(2*E);
   F[row++]=v;
  }
  for(int i=0;i<n;i++)for(int j=i;j<n;j++){
   C v;int bj=j<m?j+m:j-m,bi=i<m?i+m:i-m;
   for(int a=0;a<n;a++){
    C ai=sub(u[a*n+i],x[a*n+i]),aj=sub(u[a*n+j],x[a*n+j]);
    v=add(v,add(mul(ai,xj[a*n+j]),mul(aj,xj[a*n+i])));
    A[row*d+a*n+i]=sub(A[row*d+a*n+i],xj[a*n+j]);
    A[row*d+a*n+j]=sub(A[row*d+a*n+j],xj[a*n+i]);
    A[row*d+a*n+bj]=add(A[row*d+a*n+bj],j<m?neg(ai):ai);
    A[row*d+a*n+bi]=add(A[row*d+a*n+bi],i<m?neg(aj):aj);
   }
   F[row++]=v;
  }
  cpp_int eta=0,z0=0,yn=0;
  std::vector<std::vector<int>> nz(d);
  for(int k=0;k<d;k++)for(int j=0;j<d;j++)if(A[k*d+j].r!=0 || A[k*d+j].i!=0)nz[k].push_back(j);
  for(int i=0;i<d;i++){
   C bf;cpp_int bn=0;std::vector<C> ba(d);
   for(int k=0;k<d;k++){
    const C&bk=B[i*d+k];bf=add(bf,mul(bk,F[k]));bn+=norm(bk);
    for(int j:nz[k])ba[j]=add(ba[j],mul(bk,A[k*d+j]));
   }
   ba[i].r-=cpp_int(1)<<(E+Ey);
   cpp_int zn=0;for(auto &v:ba)zn+=norm(v);
   cpp_int en=norm(bf);if(en>eta)eta=en;if(zn>z0)z0=zn;if(bn>yn)yn=bn;
  }
  cpp_int z2=yn*(4*n);
  int re=eta==0?-80:int(boost::multiprecision::msb(eta))+1-(Ey+2*E)+2;
  *radius_exponent=re;
  bounds[0]=estimate(eta,-Ey-2*E);bounds[1]=estimate(z0,-Ey-E);bounds[2]=estimate(z2,-Ey);bounds[3]=std::ldexp(1.,re);
  bool a=sum_less({{z0,-Ey-E},{z2,-Ey+re}},0);
  bool b=sum_less({{eta,-Ey-2*E},{z0,-Ey-E+re},{z2,-Ey+2*re-1}},re);
  return a&&b?0:1;
 }catch(...){return -1;}
}
