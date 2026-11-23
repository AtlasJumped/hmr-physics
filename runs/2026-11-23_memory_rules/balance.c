// Task 2: multi-scale balance test (R2_phys section 8) at size, compiled, with incremental updates.
// State: a partial order on N thoughts with a fixed birth labeling (i before j only if i<j).
// Move: pick a pair i<j. If i-j is a link (related, nothing between), propose removing the relation.
//       If unrelated and adding i<j needs no other new relation (past(i) in past(j), future(j) in future(i)), propose adding it.
//       Symmetric proposals, Metropolis on beta*E. At beta=0 this samples labeled orders uniformly.
// E_multi = (r_whole-RT)^2 + sum over interval-size bins (mean related share in bin - T_bin)^2, empty bin counts as share 0.
// E_null  = (r_whole-RT)^2.
// Indicators NOT in E: longest chain, links, pairs with 1,2,3 between, first and last thoughts.
// usage: balance DIM N mode(truth|multi|null) start(scatter|perc) steps seed Bfac [T_0..T_4]
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
typedef uint64_t u64;
static u64 s[4];
static inline u64 rotl(u64 x,int k){return (x<<k)|(x>>(64-k));}
static inline u64 rnd(void){u64 r=rotl(s[1]*5,7)*9,t=s[1]<<17;s[2]^=s[0];s[3]^=s[1];s[1]^=s[2];s[0]^=s[3];s[2]^=t;s[3]=rotl(s[3],45);return r;}
static void seed(u64 x){for(int i=0;i<4;i++){x+=0x9E3779B97F4A7C15ULL;u64 z=x;z=(z^(z>>30))*0xBF58476D1CE4E5B9ULL;z=(z^(z>>27))*0x94D049BB133111EBULL;s[i]=z^(z>>31);}}
static inline double uni(void){return (rnd()>>11)*(1.0/9007199254740992.0);}
static inline int ri(int n){return (int)(((rnd()>>32)*(u64)n)>>32);}
#define NBIN 5
static const int BLO[NBIN]={5,10,20,40,80}, BHI[NBIN]={9,19,39,79,159};
int N,W,DIM; u64 *anc,*desc; int *sz,*rl; long R; double bsum[NBIN]; long bcnt[NBIN]; double RT,T[NBIN]; int multi;
#define A(m) (anc+(size_t)(m)*W)
#define D(m) (desc+(size_t)(m)*W)
#define SZ(a,b) sz[(size_t)(a)*N+(b)]
#define RL(a,b) rl[(size_t)(a)*N+(b)]
#define BIT(row,i) (((row)[(i)>>6]>>((i)&63))&1)
static inline int pc(u64 x){return __builtin_popcountll(x);}
static inline int binof(int sv){ if(sv<5||sv>159)return -1; return sv<10?0:sv<20?1:sv<40?2:sv<80?3:4; }
static inline void bupd(int sv,int rv,int sign){int k=binof(sv); if(k<0)return; bsum[k]+=sign*(rv/(0.5*sv*(sv-1))); bcnt[k]+=sign;}
static double energy(void){ double d=R/(0.5*N*(N-1))-RT, E=d*d; if(multi)for(int k=0;k<NBIN;k++){double m=bcnt[k]>0?bsum[k]/bcnt[k]:0.0; E+=(m-T[k])*(m-T[k]);} return E; }
static void build_tables(void){ // from anc: desc, sz, rl, bins
  memset(desc,0,sizeof(u64)*(size_t)N*W); R=0; for(int k=0;k<NBIN;k++){bsum[k]=0;bcnt[k]=0;}
  for(int j=0;j<N;j++){u64*aj=A(j); for(int k=0;k<W;k++){u64 x=aj[k]; while(x){int i=k*64+__builtin_ctzll(x); x&=x-1; D(i)[j>>6]|=1ULL<<(j&63); R++;}}}
  u64*I=malloc(8*W);
  for(int a=0;a<N;a++)for(int b=a+1;b<N;b++){
    if(!BIT(A(b),a)){SZ(a,b)=-1;RL(a,b)=0;continue;}
    int sv=0; for(int k=0;k<W;k++){I[k]=D(a)[k]&A(b)[k]; sv+=pc(I[k]);}
    int rv=0; if(sv>=2) for(int k=0;k<W;k++){u64 x=I[k]; while(x){int i=k*64+__builtin_ctzll(x); x&=x-1; u64*ai=A(i); for(int kk=0;kk<=k;kk++)rv+=pc(ai[kk]&I[kk]);}}
    SZ(a,b)=sv; RL(a,b)=rv; bupd(sv,rv,+1);
  }
  free(I);
}
static int *la,*lb;
static void apply(int i,int j,int add){
  int na=0,nb=0;
  for(int k=0;k<W;k++){u64 x=A(i)[k]; while(x){la[na++]=k*64+__builtin_ctzll(x); x&=x-1;}}
  for(int k=0;k<W;k++){u64 x=D(j)[k]; while(x){lb[nb++]=k*64+__builtin_ctzll(x); x&=x-1;}}
  int sg=add?1:-1;
  for(int y=0;y<nb;y++){int b=lb[y]; int sv=SZ(i,b),rv=RL(i,b); bupd(sv,rv,-1); sv+=sg; rv+=sg*SZ(j,b); SZ(i,b)=sv; RL(i,b)=rv; bupd(sv,rv,+1);}
  for(int x=0;x<na;x++){int a=la[x]; int sv=SZ(a,j),rv=RL(a,j); bupd(sv,rv,-1); sv+=sg; rv+=sg*SZ(a,i); SZ(a,j)=sv; RL(a,j)=rv; bupd(sv,rv,+1);}
  for(int x=0;x<na;x++){int a=la[x]; int*srow=sz+(size_t)a*N,*rrow=rl+(size_t)a*N;
    for(int y=0;y<nb;y++){int b=lb[y]; int sv=srow[b]; if(sv>=5&&sv<=159){ double den=0.5*sv*(sv-1); bsum[binof(sv)]+=sg/den; } rrow[b]+=sg; } }
  if(add){A(j)[i>>6]|=1ULL<<(i&63); D(i)[j>>6]|=1ULL<<(j&63); SZ(i,j)=0; RL(i,j)=0; R++;}
  else   {A(j)[i>>6]&=~(1ULL<<(i&63)); D(i)[j>>6]&=~(1ULL<<(j&63)); SZ(i,j)=-1; RL(i,j)=0; R--;}
}
static void sprinkle(int dim){
  double (*p)[4]=malloc(sizeof(double)*4*N); int c=0;
  while(c<N){ double t=2*uni()-1,r2=0,x[3]={0,0,0}; for(int d=0;d<dim-1;d++){x[d]=2*uni()-1; r2+=x[d]*x[d];} if(fabs(t)+sqrt(r2)<1){p[c][0]=t;p[c][1]=x[0];p[c][2]=x[1];p[c][3]=x[2];c++;} }
  for(int i=1;i<N;i++){double v[4]; memcpy(v,p[i],32); int j=i-1; while(j>=0&&p[j][0]>v[0]){memcpy(p[j+1],p[j],32);j--;} memcpy(p[j+1],v,32);}
  memset(anc,0,sizeof(u64)*(size_t)N*W);
  for(int j=0;j<N;j++)for(int i=0;i<j;i++){double dt=p[j][0]-p[i][0],dx=p[j][1]-p[i][1],dy=p[j][2]-p[i][2],dz=p[j][3]-p[i][3]; if(dt*dt>dx*dx+dy*dy+dz*dz)A(j)[i>>6]|=1ULL<<(i&63);}
  free(p);
}
static double perc(double p){ memset(anc,0,sizeof(u64)*(size_t)N*W); long r=0;
  for(int j=1;j<N;j++){u64*aj=A(j); for(int i=0;i<j;i++) if(uni()<p){u64*ai=A(i); for(int k=0;k<=(i>>6);k++)aj[k]|=ai[k]; aj[i>>6]|=1ULL<<(i&63);} for(int k=0;k<W;k++)r+=pc(aj[k]);}
  return r/(0.5*N*(N-1)); }
static int *hh;
static void report(const char*tag,long step,double beta,double acc){
  long links=0,n1=0,n2=0,n3=0; int H=0,mins=0,maxs=0;
  for(int j=0;j<N;j++){u64*aj=A(j); int best=0,any=0; for(int k=0;k<W;k++){u64 x=aj[k]; while(x){int i=k*64+__builtin_ctzll(x); x&=x-1; any=1; if(hh[i]>best)best=hh[i]; int sv=SZ(i,j); if(sv==0)links++; else if(sv==1)n1++; else if(sv==2)n2++; else if(sv==3)n3++;}}
    hh[j]=best+1; if(hh[j]>H)H=hh[j]; if(!any)mins++; int dn=0; for(int k=0;k<W;k++)if(D(j)[k]){dn=1;break;} if(!dn)maxs++; }
  int sm=multi; multi=1; double Em=energy(); multi=sm;
  printf("%s step=%ld beta=%.3g acc=%.4f E=%.3e Emulti=%.3e rw=%.4f height=%d links=%ld N1=%ld N2=%ld N3=%ld mins=%d maxs=%d",tag,step,beta,acc,energy(),Em,R/(0.5*N*(N-1)),H,links,n1,n2,n3,mins,maxs);
  for(int k=0;k<NBIN;k++)printf(" b%d=%.4f c%d=%ld",k,bcnt[k]?bsum[k]/bcnt[k]:0.0,k,bcnt[k]);
  printf("\n"); fflush(stdout);
}
int main(int argc,char**argv){
  DIM=atoi(argv[1]); N=atoi(argv[2]); char*mode=argv[3]; char*start=argv[4]; long steps=atol(argv[5]); long sd=atol(argv[6]); double Bfac=atof(argv[7]);
  RT=DIM==2?0.5:DIM==3?8.0/35:0.1; for(int k=0;k<NBIN;k++)T[k]=argc>8+k?atof(argv[8+k]):RT;
  W=(N+63)>>6; anc=malloc(sizeof(u64)*(size_t)N*W); desc=malloc(sizeof(u64)*(size_t)N*W); sz=malloc(sizeof(int)*(size_t)N*N); rl=malloc(sizeof(int)*(size_t)N*N); la=malloc(4*N); lb=malloc(4*N); hh=malloc(4*N);
  seed(sd); multi=1; int hot=!strcmp(start,"scatter"); /* scatter start: constant final beta, no melting */
  if(!strcmp(mode,"truth")){ for(long r=0;r<steps;r++){sprinkle(DIM); build_tables(); report("TRUTH",r,0,0);} return 0; }
  multi=!strcmp(mode,"multi");
  if(!strcmp(start,"scatter"))sprinkle(DIM);
  else { double lo=0,hi=0.2,p=0.01; for(int it=0;it<25;it++){p=(lo+hi)/2; double r=perc(p); if(r>RT)hi=p; else lo=p;} }
  build_tables(); report("START",0,0,0);
  double b1=Bfac*(double)N*N,b0=b1/300; double E=energy(); long acc=0,prop=0; long every=steps/40; if(every<1)every=1;
  for(long st=1;st<=steps;st++){
    double f=st/(0.4*steps); if(f>1||hot)f=1; double beta=b0*pow(b1/b0,f);
    int j=1+ri(N-1),i=ri(j); int add;
    if(BIT(A(j),i)){ if(SZ(i,j)!=0) goto skip; add=0; }
    else { u64*ai=A(i),*aj=A(j),*di=D(i),*dj=D(j); int ok=1; for(int k=0;k<W&&ok;k++) if((ai[k]&~aj[k])||(dj[k]&~di[k]))ok=0; if(!ok)goto skip; add=1; }
    prop++; apply(i,j,add); { double E2=energy(); if(E2<=E||uni()<exp(-beta*(E2-E))){E=E2;acc++;} else apply(i,j,!add); }
    skip:
    if(st%every==0){ report("TRACE",st,beta,prop?(double)acc/prop:0); fprintf(stderr,"useful proposals %ld of %ld\n",prop,st); }
    if(st==steps/2||st==steps){ // drift check of the incremental tables against a full rebuild
      double bs[NBIN]; long bc[NBIN],R0=R; memcpy(bs,bsum,sizeof bs); memcpy(bc,bcnt,sizeof bc); build_tables(); double md=0; for(int k=0;k<NBIN;k++){ if(bc[k]!=bcnt[k])md=1e9; if(fabs(bs[k]-bsum[k])>md)md=fabs(bs[k]-bsum[k]); }
      printf("CHECK step=%ld incremental-vs-rebuild max diff in bin sums=%.3e R diff=%ld\n",st,md,R0-R); E=energy(); }
  }
  return 0;
}
