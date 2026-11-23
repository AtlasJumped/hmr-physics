// COPY rules for the HMR council: smallest changes to V1's K=2 growth in which an existing local shape
// raises the chance that the same shape is made again nearby.
// Every rule: new thought m picks a focus set S (1 or 2 earlier thoughts) and is born after S and all S rests on.
// SHAPE (type) of a thought = its direct-parent set up to isomorphism, one step deep:
//   R root (no parents) | C one parent ("chain") | V two parents with no common direct parent | D two parents sharing a direct parent ("diamond top")
// make(X,a): build shape X on anchor a:  C: S={a}   D: S={a, a random sibling of a}   V: S={a, b}, b uniform among thoughts unrelated to a and not its sibling
// base(): with chance mu make(C,a), with chance mu make(D,a) (a uniform), else V1's K2 (two uniform draws). mu=0 is pure K2.
// Rules:
//  K : base only (control).
//  A : twin templating. w.p. q: template t uniform (non-root); S = parents of t (m becomes a twin of t). else base.
//  F : forward templating. w.p. q: template t = pick; make(type(t), t) (same shape, one layer up, on t). else base.
//  B : motif preferential attachment, global, saturating. leaky counts N_X (decay 1-1/W per birth) of realized shapes;
//      p_X = eps + (1-3eps) N_X^alpha / sum N_Y^alpha ; make(X, a), a = pick.
//  G : motif preferential attachment, local. as B but N_X counted over a's neighbourhood (a, its parents, its last 8 children, last 8 children of each parent).
//  T : lineage threshold. a = pick; r = run(a) = length of the same-shape chain ending at a. copy chance = phi if r>=theta else plo: make(type(a),a). else base on a.
//  D : threshold and overnight reset. days of L births. fast trace = today's counts (wiped each night). durable store s (a shape).
//      p_X = eps + (1-3eps) [ (1-g) 1(X=s) + g today_X^alpha / sum today_Y^alpha ]. At night: if today's top shape has share >= theta, s := that shape.
// pick: uniform over earlier thoughts; with chance qa instead uniform over thoughts nothing is built on yet (frontier). qa=0 by default.
// pulses: pulse=t0:P:X forces make(X,pick) for births t0..t0+P-1 (an external "write").
// modes: mem (block statistics over many runs), ts (windowed time series), dim (dimension, lineage, write cost)
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
enum{TR=0,TC=1,TV=2,TD=3};
int n; u64 **anc,*ancblk;
typedef struct{int *v;int c,cap;} vec;
static void push(vec*x,int a){if(x->c==x->cap){x->cap=x->cap?2*x->cap:4;x->v=realloc(x->v,sizeof(int)*x->cap);}x->v[x->c++]=a;}
vec *chi; int (*par)[2]; int *np,*h,*run,*gen,*maxl,*maxpos,nmax; unsigned char *type,*copied;
char rule='K'; double q=0.5,mu=0.05,eps=0.05,alpha=2,Wl=100,plo=0.1,phi=0.9,theta=0.6,g=0.5,qa=0; int thr=3,Lday=200;
int npulse=0,pt0[8],pP[8],pX[8];
static int S[2],ns; static double Hb; static int src; static int sdur=TV; static double Ng[4],today[4];
static inline int rel(int x,int y){return x==y?1:(x>y?BIT(anc[x],y):BIT(anc[y],x));}
static inline int share(int a,int b){for(int i=0;i<np[a];i++)for(int j=0;j<np[b];j++)if(par[a][i]==par[b][j])return 1;return 0;}
static int pick(int m){
  int a; if(qa>0&&uni()<qa)a=maxl[ri(nmax)]; else a=ri(m);
  double p=(1-qa)/m+(maxpos[a]>=0?qa/nmax:0); Hb-=log2(p); return a;
}
static void make(int X,int a,int m){
  S[0]=a; ns=1;
  if(X==TC||X==TR)return;
  if(X==TD){
    int el[2],ne=0; for(int i=0;i<np[a];i++)if(chi[par[a][i]].c>1)el[ne++]=par[a][i];
    if(ne){int p=el[ri(ne)],b; do{b=chi[p].v[ri(chi[p].c)];}while(b==a); Hb+=log2((double)ne)+log2((double)chi[p].c-1); S[1]=b; ns=2; return;}
    S[1]=ri(m); ns=2; Hb+=log2((double)m); return;
  }
  int b=-1; for(int t=0;t<64;t++){int c=ri(m); if(c==a||rel(a,c)||share(a,c))continue; b=c;break;}
  if(b<0)b=ri(m); S[1]=b; ns=2; Hb+=log2((double)m);
}
static void base(int m,int a){ // a<0: fresh anchor
  double u=uni();
  if(u<2*mu){ if(a<0)a=pick(m); Hb-=log2(mu); make(u<mu?TC:TD,a,m); return; }
  if(mu>0)Hb-=log2(1-2*mu);
  if(a<0){a=ri(m);Hb+=log2((double)m);} S[0]=a; S[1]=ri(m); ns=2; Hb+=log2((double)m);
}
static int drawtype(double*w,int m){ // p_X = eps + (1-3eps) w_X^alpha/sum
  double z=0,p[4]; for(int X=1;X<=3;X++){p[X]=w[X]>0?pow(w[X],alpha):0; z+=p[X];}
  for(int X=1;X<=3;X++)p[X]=eps+(1-3*eps)*(z>0?p[X]/z:1.0/3);
  double u=uni(); int X=u<p[1]?1:(u<p[1]+p[2]?2:3); Hb-=log2(p[X]); return X;
}
static void draw(int m){
  ns=0; Hb=0; src=-1;
  for(int i=0;i<npulse;i++) if(m>=pt0[i]&&m<pt0[i]+pP[i]){ make(pX[i],pick(m),m); return; }
  switch(rule){
  case 'K': base(m,-1); break;
  case 'A': if(m>1&&uni()<q){ int t=1+ri(m-1); Hb+=-log2(q)+log2((double)m-1); S[0]=par[t][0]; ns=1; if(np[t]==2){S[1]=par[t][1];ns=2;} src=t; }
            else { Hb-=log2(1-q); base(m,-1);} break;
  case 'F': if(uni()<q){ Hb-=log2(q); int t=pick(m); if(type[t]==TR){S[0]=t;S[1]=ri(m);ns=2;Hb+=log2((double)m);} else {make(type[t],t,m); src=t;} }
            else { Hb-=log2(1-q); base(m,-1);} break;
  case 'B': { int a=pick(m); make(drawtype(Ng,m),a,m);} break;
  case 'G': { int a=pick(m); double w[4]={0,0,0,0}; w[type[a]]+=1; for(int i=0;i<np[a];i++){int p=par[a][i]; w[type[p]]+=1; int c0=chi[p].c>9?chi[p].c-9:0; int k=0; for(int j=chi[p].c-1;j>=c0&&k<8;j--) if(chi[p].v[j]!=a){w[type[chi[p].v[j]]]+=1;k++;} }
              { int c0=chi[a].c>8?chi[a].c-8:0; for(int j=c0;j<chi[a].c;j++)w[type[chi[a].v[j]]]+=1; }
              make(drawtype(w,m),a,m);} break;
  case 'T': { int a=pick(m); double pc=(type[a]==TR)?0:(run[a]>=thr?phi:plo);
              if(uni()<pc){ Hb-=log2(pc); make(type[a],a,m); src=a; } else { Hb-=log2(1-pc); base(m,a);} } break;
  case 'D': { int a=pick(m); double w[4]={0,0,0,0},z=0,p[4]; for(int X=1;X<=3;X++){w[X]=today[X]>0?pow(today[X],alpha):0; z+=w[X];}
              for(int X=1;X<=3;X++)p[X]=eps+(1-3*eps)*(z>0?(1-g)*(X==sdur)+g*w[X]/z:(double)(X==sdur));
              double u=uni(); int X=u<p[1]?1:(u<p[1]+p[2]?2:3); Hb-=log2(p[X]); make(X,a,m);} break;
  }
}
static int tsmode=0;
static void grow(void){
  for(int i=0;i<n;i++)chi[i].c=0;
  nmax=0; sdur=TV; for(int X=0;X<4;X++){Ng[X]=0;today[X]=0;}
  double aH=0,aC=0,aR=0; double f[4]={0,0,0,0}; double lam=1-1.0/Wl;
  for(int m=0;m<n;m++){
    u64*am=anc[m]; int w=(m>>6)+1; memset(am,0,8*w); h[m]=1; np[m]=0; gen[m]=0; copied[m]=0; run[m]=1; type[m]=TR;
    if(m>0){
      if(rule=='D' && m%Lday==0){ int X=1; for(int Y=2;Y<=3;Y++)if(today[Y]>today[X])X=Y; double z=today[1]+today[2]+today[3]; if(z>0&&today[X]/z>=theta)sdur=X; today[1]=today[2]=today[3]=0; }
      draw(m);
      for(int i=0;i<ns;i++){u64*as=anc[S[i]]; int ws=(S[i]>>6)+1; for(int k=0;k<ws;k++)am[k]|=as[k]; am[S[i]>>6]|=1ULL<<(S[i]&63);}
      if(ns==2){ if(S[0]==S[1])ns=1; else if(rel(S[0],S[1])){ if(S[0]<S[1])S[0]=S[1]; ns=1; } }
      for(int i=0;i<ns;i++){int a=S[i]; par[m][np[m]++]=a; push(&chi[a],m); if(h[a]+1>h[m])h[m]=h[a]+1;
        if(maxpos[a]>=0){int pos=maxpos[a]; maxl[pos]=maxl[--nmax]; maxpos[maxl[pos]]=pos; maxpos[a]=-1;} }
      type[m]=np[m]==1?TC:(share(par[m][0],par[m][1])?TD:TV);
      for(int i=0;i<np[m];i++){int a=par[m][i]; if(type[a]==type[m]&&run[a]+1>run[m])run[m]=run[a]+1;}
      if(src>=0){copied[m]=1; gen[m]=gen[src]+1;}
      for(int X=1;X<=3;X++)Ng[X]*=lam; Ng[type[m]]+=1; today[type[m]]+=1;
    }
    maxpos[m]=nmax; maxl[nmax++]=m;
    if(tsmode && m>0){ aH+=2*log2((double)m)-Hb; aC+=copied[m]; aR+=run[m]; f[type[m]]+=1;
      if(m%tsmode==0){ printf("TS %d %.4f %.4f %.4f %.4f %.4f %.3f %d\n",m,f[1]/tsmode,f[2]/tsmode,f[3]/tsmode,aH/tsmode,aC/tsmode,aR/tsmode,sdur); aH=aC=aR=0; f[1]=f[2]=f[3]=0; } }
  }
}
static int pc(u64 x){return __builtin_popcountll(x);}
static double fd(double d){return exp(lgamma(d+1)+lgamma(d/2)-log(2)-lgamma(1.5*d));}
static double mmdim(double r){double lo=0.5,hi=80; for(int i=0;i<70;i++){double mid=(lo+hi)/2; if(fd(mid)>r)lo=mid; else hi=mid;} return (lo+hi)/2;}
static void runstats(unsigned char*ty,int*rn,double out[4][6]){ // per type: count, mean run, max run, P(run>=3), P(>=5), P(>=10)
  for(int X=0;X<4;X++)for(int k=0;k<6;k++)out[X][k]=0;
  for(int m=1;m<n;m++){ rn[m]=1; for(int i=0;i<np[m];i++){int a=par[m][i]; if(a>0&&ty[a]==ty[m]&&rn[a]+1>rn[m])rn[m]=rn[a]+1;}
    double*o=out[ty[m]]; o[0]++; o[1]+=rn[m]; if(rn[m]>o[2])o[2]=rn[m]; if(rn[m]>=3)o[3]++; if(rn[m]>=5)o[4]++; if(rn[m]>=10)o[5]++; }
  for(int X=1;X<4;X++)if(out[X][0]>0){out[X][1]/=out[X][0];out[X][3]/=out[X][0];out[X][4]/=out[X][0];out[X][5]/=out[X][0];}
}
static int cmpl(const void*a,const void*b){long x=*(const long*)a,y=*(const long*)b;return x<y?-1:x>y;}
int main(int argc,char**argv){
  char mode[16]="dim"; long sd=1; int runs=1,B=4;
  n=1000;
  for(int i=1;i<argc;i++){ char*e=strchr(argv[i],'='); if(!e){fprintf(stderr,"bad arg %s\n",argv[i]);return 1;} *e=0; char*k=argv[i],*v=e+1;
    if(!strcmp(k,"mode"))strncpy(mode,v,15); else if(!strcmp(k,"rule"))rule=v[0]; else if(!strcmp(k,"n"))n=atoi(v); else if(!strcmp(k,"seed"))sd=atol(v);
    else if(!strcmp(k,"q"))q=atof(v); else if(!strcmp(k,"mu"))mu=atof(v); else if(!strcmp(k,"eps"))eps=atof(v); else if(!strcmp(k,"alpha"))alpha=atof(v);
    else if(!strcmp(k,"W"))Wl=atof(v); else if(!strcmp(k,"plo"))plo=atof(v); else if(!strcmp(k,"phi"))phi=atof(v); else if(!strcmp(k,"thr"))thr=atoi(v);
    else if(!strcmp(k,"theta"))theta=atof(v); else if(!strcmp(k,"g"))g=atof(v); else if(!strcmp(k,"L"))Lday=atoi(v); else if(!strcmp(k,"qa"))qa=atof(v);
    else if(!strcmp(k,"runs"))runs=atoi(v); else if(!strcmp(k,"B"))B=atoi(v); else if(!strcmp(k,"win"))tsmode=atoi(v);
    else if(!strcmp(k,"pulse")){ char c; sscanf(v,"%d:%d:%c",&pt0[npulse],&pP[npulse],&c); pX[npulse]=c=='C'?TC:(c=='V'?TV:TD); npulse++; }
    else {fprintf(stderr,"unknown %s\n",k);return 1;} }
  size_t tot=0; for(int m=0;m<n;m++)tot+=(m>>6)+1; ancblk=malloc(8*tot); anc=malloc(sizeof(u64*)*n); tot=0; for(int m=0;m<n;m++){anc[m]=ancblk+tot; tot+=(m>>6)+1;}
  chi=calloc(n,sizeof(vec)); par=malloc(sizeof(int[2])*n); np=malloc(4*n); h=malloc(4*n); run=malloc(4*n); gen=malloc(4*n); maxl=malloc(4*n); maxpos=malloc(4*n); type=malloc(n); copied=malloc(n);
  if(!strcmp(mode,"mem")){
    int bs=n/B; int*hb=malloc(4*n);
    for(int r=0;r<runs;r++){ seed(sd*1000003ULL+r); grow();
      for(int b=0;b<B;b++){ int lo=b*bs,hi=lo+bs; long R=0,Lk=0,nC=0,nD=0; int H=0;
        for(int m=lo;m<hi;m++){ u64*am=anc[m]; int c=0; for(int k=lo>>6;k<=(m>>6);k++){u64 x=am[k]; if(k==(lo>>6))x&=~0ULL<<(lo&63); c+=pc(x);} R+=c;
          hb[m]=1; for(int i=0;i<np[m];i++){int a=par[m][i]; if(a>=lo){Lk++; if(hb[a]+1>hb[m])hb[m]=hb[a]+1;}} if(hb[m]>H)H=hb[m];
          nC+=type[m]==TC; nD+=type[m]==TD; }
        printf("%ld %ld %d %ld %ld ",R,Lk,H,nC,nD); }
      printf("\n"); }
    return 0; }
  if(!strcmp(mode,"ts")){ if(!tsmode)tsmode=100; seed(sd); grow(); return 0; }
  // dim mode
  seed(sd);
  // write cost accumulated over the second half
  double gH=0; { /* grow with entropy tally */ }
  tsmode=0; grow();
  // re-run identical growth to tally entropy is avoided: recompute cheaply by a second pass with same seed
  { seed(sd); double acc=0; int cnt=0; /* identical RNG stream => identical pattern */
    for(int i=0;i<n;i++)chi[i].c=0; nmax=0; sdur=TV; for(int X=0;X<4;X++){Ng[X]=0;today[X]=0;} double lam=1-1.0/Wl;
    for(int m=0;m<n;m++){ u64*am=anc[m]; int w=(m>>6)+1; memset(am,0,8*w); h[m]=1; np[m]=0; gen[m]=0; copied[m]=0; run[m]=1; type[m]=TR;
      if(m>0){ if(rule=='D' && m%Lday==0){ int X=1; for(int Y=2;Y<=3;Y++)if(today[Y]>today[X])X=Y; double z=today[1]+today[2]+today[3]; if(z>0&&today[X]/z>=theta)sdur=X; today[1]=today[2]=today[3]=0; }
        draw(m); if(m>=n/2){acc+=2*log2((double)m)-Hb;cnt++;}
        for(int i=0;i<ns;i++){u64*as=anc[S[i]]; int ws=(S[i]>>6)+1; for(int k=0;k<ws;k++)am[k]|=as[k]; am[S[i]>>6]|=1ULL<<(S[i]&63);}
        if(ns==2){ if(S[0]==S[1])ns=1; else if(rel(S[0],S[1])){ if(S[0]<S[1])S[0]=S[1]; ns=1; } }
        for(int i=0;i<ns;i++){int a=S[i]; par[m][np[m]++]=a; push(&chi[a],m); if(h[a]+1>h[m])h[m]=h[a]+1;
          if(maxpos[a]>=0){int pos=maxpos[a]; maxl[pos]=maxl[--nmax]; maxpos[maxl[pos]]=pos; maxpos[a]=-1;} }
        type[m]=np[m]==1?TC:(share(par[m][0],par[m][1])?TD:TV);
        for(int i=0;i<np[m];i++){int a=par[m][i]; if(type[a]==type[m]&&run[a]+1>run[m])run[m]=run[a]+1;}
        if(src>=0){copied[m]=1; gen[m]=gen[src]+1;}
        for(int X=1;X<=3;X++)Ng[X]*=lam; Ng[type[m]]+=1; today[type[m]]+=1; }
      maxpos[m]=nmax; maxl[nmax++]=m; }
    gH=acc/cnt; }
  int W=(n+63)>>6; u64*desc=calloc((size_t)n*W,8);
  #define Dm(m) (desc+(size_t)(m)*W)
  for(int m=n-1;m>0;m--){u64*dm=Dm(m); for(int i=0;i<np[m];i++){u64*dp=Dm(par[m][i]); for(int k=m>>6;k<W;k++)dp[k]|=dm[k]; dp[m>>6]|=1ULL<<(m&63);} }
  long R=0,links=0; int H=0,maxgen=0; double mgen=0; long ncop=0;
  for(int m=0;m<n;m++){u64*am=anc[m]; int c=0; for(int k=0;k<=(m>>6);k++)c+=pc(am[k]); R+=c; if(h[m]>H)H=h[m]; links+=np[m]; if(gen[m]>maxgen)maxgen=gen[m]; if(copied[m]){mgen+=gen[m];ncop++;} }
  double r=R/((double)n*(n-1)/2);
  printf("WHOLE rule=%c n=%d seed=%ld r=%.6f dmm=%.4f height=%d links=%ld maxs=%d given_up_bits=%.3f copies=%ld meangen=%.2f maxgen=%d\n",rule,n,sd,r,mmdim(r),H,links,nmax,gH,ncop,ncop?mgen/ncop:0,maxgen);
  // lineage: same-shape runs along links, against the same pattern with shapes shuffled among thoughts
  double o[4][6],sh[4][6]={{0}},t2[4][6]; int*rn=malloc(4*n); unsigned char*ty=malloc(n); int NS=20;
  runstats(type,rn,o); memcpy(ty,type,n);
  for(int it=0;it<NS;it++){ for(int i=n-1;i>1;i--){int j=1+ri(i); unsigned char t=ty[i];ty[i]=ty[j];ty[j]=t;} runstats(ty,rn,t2); for(int X=1;X<4;X++)for(int k=0;k<6;k++)sh[X][k]+=t2[X][k]/NS; }
  const char*nm="RCVD";
  for(int X=1;X<4;X++) printf("LIN rule=%c n=%d seed=%ld type=%c count=%.0f meanrun=%.3f maxrun=%.0f p3=%.5f p5=%.5f p10=%.5f | shuf meanrun=%.3f maxrun=%.1f p3=%.5f p5=%.5f p10=%.5f\n",rule,n,sd,nm[X],o[X][0],o[X][1],o[X][2],o[X][3],o[X][4],o[X][5],sh[X][1],sh[X][2],sh[X][3],sh[X][4],sh[X][5]);
  // shape inheritance: mutual information between a thought's shape and a parent's shape (over links, non-root parents)
  { double J[4][4]={{0}},z=0,pa[4]={0},pb[4]={0},mi=0; for(int m=1;m<n;m++)for(int i=0;i<np[m];i++){int a=par[m][i]; if(a>0){J[type[m]][type[a]]++;z++;}}
    for(int x=1;x<4;x++)for(int y=1;y<4;y++){J[x][y]/=z;pa[x]+=J[x][y];pb[y]+=J[x][y];}
    for(int x=1;x<4;x++)for(int y=1;y<4;y++)if(J[x][y]>0)mi+=J[x][y]*log2(J[x][y]/(pa[x]*pb[y]));
    // twin classes
    long*key=malloc(8*n); int nk=0; for(int m=1;m<n;m++){int a=par[m][0],b=np[m]==2?par[m][1]:-1; if(b>a){int t=a;a=b;b=t;} key[nk++]=(long)a*(n+1)+(b+1);} qsort(key,nk,8,cmpl);
    double sw=0; int mx=0; for(int i=0;i<nk;){int j=i; while(j<nk&&key[j]==key[i])j++; int c=j-i; sw+=(double)c*c; if(c>mx)mx=c; i=j;}
    printf("INH rule=%c n=%d seed=%ld MI_bits=%.5f twin_mean=%.3f twin_max=%d\n",rule,n,sd,mi,sw/nk,mx); }
  #define NB 8
  double sr[NB]={0}; int cn[NB]={0}; long tries=0; int done=0; u64*I=malloc(8*W);
  while(tries<400000 && done<1600){
    tries++; int b=n/2+ri(n-n/2); int a=1+ri(b-1); if(!BIT(anc[b],a))continue;
    u64*da=Dm(a),*ab=anc[b]; int k0=a>>6,k1=b>>6; int sz=0; for(int k=k0;k<=k1;k++){I[k]=da[k]&ab[k]; sz+=pc(I[k]);}
    if(sz<16||sz>4095)continue; int bin=(int)floor(log2(sz))-4; if(cn[bin]>=200)continue;
    long rl=0; for(int k=k0;k<=k1;k++){u64 x=I[k]; while(x){int i=k*64+__builtin_ctzll(x); x&=x-1; u64*ai=anc[i]; for(int kk=k0;kk<=(i>>6);kk++)rl+=pc(ai[kk]&I[kk]);}}
    sr[bin]+=rl/((double)sz*(sz-1)/2); cn[bin]++; done++;
  }
  for(int bI=0;bI<NB;bI++) if(cn[bI]) printf("INT rule=%c n=%d seed=%ld lo=%d cnt=%d r=%.5f dmm=%.3f\n",rule,n,sd,16<<bI,cn[bI],sr[bI]/cn[bI],mmdim(sr[bI]/cn[bI]));
  return 0;
}
