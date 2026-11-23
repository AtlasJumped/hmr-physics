# K-parent rule: each new thought builds on K earlier thoughts chosen evenly from all history.
# Measures (a) share of related pairs in the first n thoughts, (b) the same share inside intervals.
import random, sys, math
from math import lgamma, exp
def f(d): return exp(lgamma(d+1)+lgamma(d/2)-math.log(2)-lgamma(1.5*d))
def dim(r):
    lo,hi=1.0,60.0
    for _ in range(60):
        mid=(lo+hi)/2
        if f(mid)>r: lo=mid
        else: hi=mid
    return (lo+hi)/2
def run(K,N,seed):
    rng=random.Random(seed)
    par=[[] for _ in range(N)]; anc=[0]*N
    for m in range(1,N):
        ps=set(rng.randrange(m) for _ in range(K)) if m>=K else set(range(m))
        par[m]=list(ps); a=0
        for p in ps: a|=anc[p]|(1<<p)
        anc[m]=a
    desc=[0]*N
    for m in range(N-1,0,-1):
        d=desc[m]|(1<<m)
        for p in par[m]: desc[p]|=d
    cum=0; out=[]
    marks=set([500,1000,2000,4000,8000,16000,32000])
    for m in range(N):
        cum+=bin(anc[m]).count('1')
        n=m+1
        if n in marks:
            r=cum/(n*(n-1)/2); out.append((n,r,dim(r)))
    print(f"K={K} whole pattern: n, share related, dimension estimate")
    for n,r,d in out: print(f"  {n:6d}  {r:.4f}  {d:.2f}")
    # intervals
    res={}
    tries=0
    while tries<4000:
        tries+=1
        b=rng.randrange(N//2,N); 
        a=rng.randrange(1,b)
        if not (anc[b]>>a)&1: continue
        I=desc[a]&anc[b]; s=bin(I).count('1')
        if s<20 or s>3000: continue
        rel=0; x=I; 
        while x:
            low=x&-x; i=low.bit_length()-1; x^=low
            rel+=bin(anc[i]&I).count('1')
        r=rel/(s*(s-1)/2)
        k=int(math.log2(s))
        res.setdefault(k,[]).append(r)
    print(f"K={K} intervals: size bin, count, mean share related, dimension estimate")
    for k in sorted(res):
        v=res[k]; r=sum(v)/len(v)
        print(f"  {2**k:5d}-{2**(k+1)-1:5d}  {len(v):4d}  {r:.4f}  {dim(r):.2f}")
for K in (2,5,20):
    run(K,int(sys.argv[1]),1)
