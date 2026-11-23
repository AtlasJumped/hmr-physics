// Growth rules for the HMR council "rule with memory" search.
// Every rule: the new thought m picks a focus set S of earlier thoughts and is born after S and all S rests on.
// Rules differ only in how S is drawn.
//  K : V1 family. K iid uniform draws from all earlier thoughts.               (par1=K)
//  P : V1 family. each earlier thought with chance p (transitive percolation)  (par2=p)
//  L : label-only. K iid uniform draws from the last W thoughts by birth order (par1=K, par3=W)
//  H : sees own-past shape. K draws, each the higher (longest chain below) of two uniform draws (par1=K)
//  M : sees future. K draws, each w.p. q uniform over maximal thoughts (nothing after them), else uniform (par1=K, par2=q)
//  N : closure by nearness. a uniform; w.p. q b = a sibling of a (other direct child of a random direct parent of a), else b uniform (par2=q)
//  C : content-addressed attention. a uniform; w.p. q b = of 8 uniform candidates the one whose local shape
//      (direct parents, direct children, height) is most similar to a's; else b uniform            (par2=q)
//  T : attention keyed on recent context. as C, but the key is the shape of the thought the PREVIOUS birth attended to first (par2=q)
//  U : nearness, unbounded focus. a uniform; plus every sibling of a (via any direct parent), each w.p. q (par2=q)
// modes: mem  -> many runs, per-block internal statistics (for early/late correlation)
//        dim  -> one run, dimension estimators and motif counts
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
#define BIT(row,i) (((row)[(i)>>6]>>((i)&63))&1)
int n,W; u64 *anc,*desc; 
#define A(m) (anc+(size_t)(m)*W)
#define D(m) (desc+(size_t)(m)*W)
typedef struct{int *v;int c,cap;} vec;
static void push(vec*x,int a){if(x->c==x->cap){x->cap=x->cap?2*x->cap:4;x->v=realloc(x->v,sizeof(int)*x->cap);}x->v[x->c++]=a;}
vec *par,*chi; int *h,*maxl,*maxpos,nmax; int *ndia,*lstack; long totdia,totlinks;
char rule; int K=2,Wn=50; double q=0.5;
#define SMAX 4096
static int S[SMAX],ns;
static void adds(int a){for(int i=0;i<ns;i++)if(S[i]==a)return; if(ns<SMAX)S[ns++]=a;}
static int prevA=0;
static inline int sdist(int x,int y){return abs(par[x].c-par[y].c)+abs(chi[x].c-chi[y].c)+abs(h[x]-h[y]);}
static void draw(int m){
  ns=0;
  switch(rule){
  case 'K': for(int k=0;k<K;k++)adds(ri(m)); break;
  case 'P': { double lg=log(1-q); int j=-1; for(;;){ j+=1+(int)floor(log(1-uni())/lg); if(j>=m)break; adds(j);} } break;
  case 'L': { int w=m<Wn?m:Wn; for(int k=0;k<K;k++)adds(m-1-ri(w)); } break;
  case 'H': for(int k=0;k<K;k++){int a=ri(m),b=ri(m); adds(h[a]>=h[b]?a:b);} break;
  case 'M': for(int k=0;k<K;k++){ if(uni()<q)adds(maxl[ri(nmax)]); else adds(ri(m)); } break;
  case 'N': { int a=ri(m); adds(a); int b=-1;
      if(uni()<q && par[a].c>0){ int p=par[a].v[ri(par[a].c)]; if(chi[p].c>1){ do{b=chi[p].v[ri(chi[p].c)];}while(b==a);} }
      if(b<0)b=ri(m); adds(b);} break;
  case 'C': case 'T': { int a=ri(m); adds(a); int key=(rule=='C')?a:prevA; int b=-1;
      if(uni()<q && m>1){ int best=1<<30; for(int t=0;t<8;t++){int c=ri(m); if(c==a)continue; int d=sdist(c,key); if(d<best){best=d;b=c;}} }
      if(b<0)b=ri(m); adds(b); prevA=a; } break;
  case 'U': { int a=ri(m); adds(a);
      for(int i=0;i<par[a].c;i++){int p=par[a].v[i]; for(int j=0;j<chi[p].c;j++){int b=chi[p].v[j]; if(b!=a){ int seen=0; for(int t=0;t<ns;t++)if(S[t]==b)seen=1; if(!seen && uni()<q)adds(b);} } } } break;
  }
}
static void grow(void){
  memset(anc,0,sizeof(u64)*(size_t)n*W);
  for(int i=0;i<n;i++){par[i].c=0;chi[i].c=0;}
  nmax=0; totdia=0; totlinks=0; prevA=0;
  for(int m=0;m<n;m++){
    u64*am=A(m); h[m]=1; ndia[m]=0; lstack[m]=0;
    if(m>0){
      draw(m);
      int w=(m+63)>>6;
      for(int i=0;i<ns;i++){u64*as=A(S[i]); for(int k=0;k<w;k++)am[k]|=as[k]; am[S[i]>>6]|=1ULL<<(S[i]&63);}
      // links = members of S not below another member of S
      for(int i=0;i<ns;i++){int a=S[i],ok=1; for(int j=0;j<ns&&ok;j++) if(j!=i && BIT(A(S[j]),a))ok=0;
        if(ok){push(&par[m],a);push(&chi[a],m); if(h[a]+1>h[m])h[m]=h[a]+1; totlinks++;
          if(maxpos[a]>=0){int pos=maxpos[a]; maxl[pos]=maxl[--nmax]; maxpos[maxl[pos]]=pos; maxpos[a]=-1;} } }
      // diamonds p<a,b<m with all four relations links
      if(par[m].c<=40) for(int i=0;i<par[m].c;i++)for(int j=i+1;j<par[m].c;j++){int a=par[m].v[i],b=par[m].v[j];
        for(int x=0;x<par[a].c;x++)for(int y=0;y<par[b].c;y++) if(par[a].v[x]==par[b].v[y]){int p=par[a].v[x]; ndia[m]++; totdia++; if(lstack[p]+1>lstack[m])lstack[m]=lstack[p]+1; } }
      if(ndia[m]==0)lstack[m]=0;
    }
    maxpos[m]=nmax; maxl[nmax++]=m;
  }
}
static int pc(u64 x){return __builtin_popcountll(x);}
static double fd(double d){return exp(lgamma(d+1)+lgamma(d/2)-log(2)-lgamma(1.5*d));}
static double mmdim(double r){double lo=0.5,hi=80; for(int i=0;i<70;i++){double mid=(lo+hi)/2; if(fd(mid)>r)lo=mid; else hi=mid;} return (lo+hi)/2;}
int main(int argc,char**argv){
  if(argc<8){fprintf(stderr,"grow mode rule n seed K q W [runs blocks]\n");return 1;}
  char*mode=argv[1]; rule=argv[2][0]; n=atoi(argv[3]); long sd=atol(argv[4]); K=atoi(argv[5]); q=atof(argv[6]); Wn=atoi(argv[7]);
  W=(n+63)>>6; anc=malloc(sizeof(u64)*(size_t)n*W);
  par=calloc(n,sizeof(vec)); chi=calloc(n,sizeof(vec)); h=malloc(4*n); maxl=malloc(4*n); maxpos=malloc(4*n); ndia=malloc(4*n); lstack=malloc(4*n);
  if(!strcmp(mode,"mem")){
    int runs=atoi(argv[8]),B=atoi(argv[9]); int bs=n/B; int *hb=malloc(4*n);
    for(int r=0;r<runs;r++){
      seed(sd*1000003ULL+r); grow();
      for(int b=0;b<B;b++){
        int lo=b*bs,hi=lo+bs; long R=0,Lk=0,Dm=0,Mn=0; int H=0;
        for(int m=lo;m<hi;m++){
          u64*am=A(m); int c=0;
          for(int k=lo>>6;k<=(m>>6);k++){u64 x=am[k]; if(k==(lo>>6))x&=~0ULL<<(lo&63); c+=pc(x);}
          R+=c; if(c==0)Mn++;
          hb[m]=1; for(int i=0;i<par[m].c;i++){int a=par[m].v[i]; if(a>=lo){Lk++; if(hb[a]+1>hb[m])hb[m]=hb[a]+1;}}
          if(hb[m]>H)H=hb[m];
          for(int i=0;i<par[m].c;i++)for(int j=i+1;j<par[m].c;j++){int a=par[m].v[i],bb=par[m].v[j];
            for(int x=0;x<par[a].c;x++)for(int y=0;y<par[bb].c;y++) if(par[a].v[x]==par[bb].v[y] && par[a].v[x]>=lo)Dm++; }
        }
        printf("%ld %ld %d %ld %ld ",R,Lk,H,Dm,Mn);
      }
      printf("\n");
    }
    return 0;
  }
  // dim mode
  seed(sd); grow();
  desc=calloc((size_t)n*W,sizeof(u64));
  for(int m=n-1;m>0;m--){u64*dm=D(m); for(int i=0;i<par[m].c;i++){u64*dp=D(par[m].v[i]); for(int k=m>>6;k<W;k++)dp[k]|=dm[k]; dp[m>>6]|=1ULL<<(m&63);} }
  long R=0; int H=0; int tops=0,stacked=0,maxstack=0; long mins=0;
  for(int m=0;m<n;m++){u64*am=A(m); int c=0; for(int k=0;k<=(m>>6);k++)c+=pc(am[k]); R+=c; if(!c)mins++; if(h[m]>H)H=h[m]; if(ndia[m]){tops++; if(lstack[m]>1)stacked++;} if(lstack[m]>maxstack)maxstack=lstack[m];}
  double r=R/((double)n*(n-1)/2);
  // Fano factor of diamond births in windows of 100 over the last half
  int nw=0; double sm=0,sq=0; for(int lo=n/2;lo+100<=n;lo+=100){int c=0; for(int m=lo;m<lo+100;m++)c+=ndia[m]; sm+=c; sq+=(double)c*c; nw++;}
  double mu=sm/nw, var=sq/nw-mu*mu;
  // mean direct parents in last tenth (is focus bounded?)
  double lp=0; for(int m=n-n/10;m<n;m++)lp+=par[m].c; lp/=(n/10);
  printf("WHOLE rule=%c K=%d q=%g W=%d n=%d seed=%ld r=%.6f dmm=%.4f height=%d links=%ld linkpar_last=%.3f mins=%ld maxs=%d diamonds=%ld tops=%d stacked=%d maxstack=%d fano=%.3f diam_per100=%.3f\n",
    rule,K,q,Wn,n,sd,r,mmdim(r),H,totlinks,lp,mins,nmax,totdia,tops,stacked,maxstack,mu>0?var/mu:0.0,mu);
  // intervals by size bin
  #define NB 8
  double sr[NB]={0}; int cn[NB]={0}; long tries=0; int done=0; u64*I=malloc(8*W);
  while(tries<400000 && done<1600){
    tries++; int b=n/2+ri(n-n/2); int a=1+ri(b-1); if(!BIT(A(b),a))continue;
    u64*da=D(a),*ab=A(b); int k0=a>>6,k1=b>>6; int sz=0; for(int k=k0;k<=k1;k++){I[k]=da[k]&ab[k]; sz+=pc(I[k]);}
    if(sz<16||sz>4095)continue; int bin=(int)floor(log2(sz))-4; if(cn[bin]>=200)continue;
    long rel=0; for(int k=k0;k<=k1;k++){u64 x=I[k]; while(x){int i=k*64+__builtin_ctzll(x); x&=x-1; u64*ai=A(i); for(int kk=k0;kk<=(i>>6);kk++)rel+=pc(ai[kk]&I[kk]);}}
    sr[bin]+=rel/((double)sz*(sz-1)/2); cn[bin]++; done++;
  }
  for(int bI=0;bI<NB;bI++) if(cn[bI]) printf("INT rule=%c K=%d q=%g n=%d seed=%ld lo=%d cnt=%d r=%.5f dmm=%.3f\n",rule,K,q,n,sd,16<<bI,cn[bI],sr[bI]/cn[bI],mmdim(sr[bI]/cn[bI]));
  return 0;
}
