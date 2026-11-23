# Exact check (rational arithmetic) of which V1 conditions each candidate rule keeps, on all patterns up to N thoughts.
#  Cond 2 (order of unrelated births irrelevant / label independence): all birth orders of the same pattern have equal chance.
#  Cond 3 (Bell causality): odds between two births (pasts A, B) are the same in the full pattern and in the pattern cut down to A union B.
#  Cond 1 (nothing born into the past) and 4 (chances add to one) hold for every rule here by construction.
from fractions import Fraction as F
from itertools import permutations, combinations
import sys
N=int(sys.argv[1]) if len(sys.argv)>1 else 5
def info(st):
    m=len(st); par=[[] for _ in range(m)]; chi=[[] for _ in range(m)]; h=[1]*m
    for y in range(m):
        for a in range(y):
            if st[y]>>a&1 and not any((st[y]>>z&1) and (st[z]>>a&1) for z in range(a+1,y)):
                par[y].append(a); chi[a].append(y); h[y]=max(h[y],h[a]+1)
    below=0
    for y in range(m): below|=st[y]
    mx=[i for i in range(m) if not below>>i&1]
    return par,chi,h,mx
def add(d,k,p):
    if p: d[k]=d.get(k,0)+p
def pair_rule(first,second):
    def rule(st):
        m=len(st); out={}; I=info(st)
        for a,pa in first(st,I).items():
            for b,pb in second(st,I,a).items(): add(out,frozenset((a,b)),pa*pb)
        return out
    return rule
uni=lambda st,I,*_: {i:F(1,len(st)) for i in range(len(st))}
def win(st,I,*_,W=2):
    m=len(st); w=min(W,m); return {m-1-i:F(1,w) for i in range(w)}
def hdraw(st,I,*_):
    m=len(st); h=I[2]; d={}
    for c in range(m):
        for e in range(m): add(d,c if h[c]>=h[e] else e,F(1,m*m))
    return d
def mdraw(st,I,*_,q=F(1,2)):
    m=len(st); d={}
    for i in range(m): add(d,i,(1-q)/m)
    for i in I[3]: add(d,i,q/len(I[3]))
    return d
def nsec(st,I,a,q=F(1,2)):
    m=len(st); par,chi=I[0],I[1]; d={}; u=1-q
    if not par[a]: u=F(1)
    else:
        for p in par[a]:
            sib=[c for c in chi[p] if c!=a]
            if sib:
                for b in sib: add(d,b,q/len(par[a])/len(sib))
            else: u+=q/len(par[a])
    for i in range(m): add(d,i,u/m)
    return d
def csec(st,I,a,q=F(9,10)):
    m=len(st); par,chi,h=I[0],I[1],I[2]; d={}; u=1-q
    if m>1:
        dist={c:abs(len(par[c])-len(par[a]))+abs(len(chi[c])-len(chi[a]))+abs(h[c]-h[a]) for c in range(m) if c!=a}
        L=0
        for dv in sorted(set(dist.values())):
            cl=[c for c in dist if dist[c]==dv]; pk=F(m-L,m)**8-F(m-L-len(cl),m)**8
            for c in cl: add(d,c,q*pk/len(cl))
            L+=len(cl)
        u+=q*F(1,m)**8
    else: u=F(1)
    for i in range(m): add(d,i,u/m)
    return d
def urule(st,q=F(1,10)):
    m=len(st); par,chi,h,mx=info(st); out={}
    for a in range(m):
        sib=sorted({c for p in par[a] for c in chi[p] if c!=a})
        for r in range(len(sib)+1):
            for sub in combinations(sib,r): add(out,frozenset((a,)+sub),F(1,m)*q**r*(1-q)**(len(sib)-r))
    return out
RULES={'K2 (V1 family)':pair_rule(uni,uni),'L label window W=2':pair_rule(win,win),'H own-past height':pair_rule(hdraw,hdraw),
       'M frontier q=1/2':pair_rule(mdraw,mdraw),'N nearness q=1/2':pair_rule(uni,nsec),'C content attention q=9/10':pair_rule(uni,csec),'U unbounded nearness q=1/10':urule}
def trans(st,rule):
    out={}
    for S,p in rule(st).items():
        a=0
        for s in S: a|=st[s]|1<<s
        add(out,a,p)
    return out
def canon(st):
    m=len(st); best=None
    for pm in permutations(range(m)):
        rel=tuple(sorted((pm[a],pm[y]) for y in range(m) for a in range(m) if st[y]>>a&1)); 
        if best is None or rel<best: best=rel
    return (m,best)
def restrict(st,U):
    idx=[i for i in range(len(st)) if U>>i&1]; pos={i:k for k,i in enumerate(idx)}
    def rm(mask): return sum(1<<pos[i] for i in idx if mask>>i&1)
    return tuple(rm(st[i]) for i in idx),rm
for name,rule in RULES.items():
    level={(0,):F(1)}; allst=[(0,)]; gc_bad=0; gc_tot=0; gc_ex=None
    for m in range(1,N):
        nxt={}
        for st,p in level.items():
            for a,pt in trans(st,rule).items(): add(nxt,st+(a,),p*pt)
        cls={}
        for st,p in nxt.items(): cls.setdefault(canon(st),[]).append(p)
        for k,v in cls.items():
            gc_tot+=1
            if min(v)!=max(v):
                gc_bad+=1
                if gc_ex is None: gc_ex=(m+1,[str(x) for x in sorted(set(v))][:3])
        level=nxt; allst+=list(nxt)
    bc_bad=0; bc_tot=0; bc_ex=None
    for st in allst:
        if len(st)>=N: continue
        T=trans(st,rule); ks=sorted(T)
        for i in range(len(ks)):
            for j in range(i+1,len(ks)):
                A,B=ks[i],ks[j]; U=A|B
                if U==(1<<len(st))-1: continue
                if U==0: continue
                st2,rm=restrict(st,U); T2=trans(st2,rule); bc_tot+=1
                if T[A]*T2.get(rm(B),0)!=T[B]*T2.get(rm(A),0):
                    bc_bad+=1
                    if bc_ex is None: bc_ex=(len(st),)
    print(f"{name:30s} cond2 broken in {gc_bad}/{gc_tot} patterns (first at {gc_ex})   cond3 broken in {bc_bad}/{bc_tot} tests (first at size {bc_ex})")
