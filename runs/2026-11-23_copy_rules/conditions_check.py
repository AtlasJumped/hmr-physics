# Exact check (rational arithmetic) of which V1 conditions each COPY rule keeps, on all patterns up to N thoughts.
#  Cond 2 (birth order irrelevant): all birth orders of the same pattern have equal chance.
#  Cond 3 (odds depend only on the two pasts): odds between two births (pasts A, B) are the same in the full pattern
#         and in the pattern cut down to A union B.
#  Cond 1 and 4 hold for every rule here by construction. Driver reused from compute_rules/conditions_check.py.
from fractions import Fraction as F
from itertools import permutations
import sys
N=int(sys.argv[1]) if len(sys.argv)>1 else 5
R,C,V,D=0,1,2,3
def info(st):
    m=len(st); par=[[] for _ in range(m)]; chi=[[] for _ in range(m)]
    for y in range(m):
        for a in range(y):
            if st[y]>>a&1 and not any((st[y]>>z&1) and (st[z]>>a&1) for z in range(a+1,y)):
                par[y].append(a); chi[a].append(y)
    share=lambda a,b: any(p in par[b] for p in par[a])
    ty=[R if not par[y] else C if len(par[y])==1 else (D if any(share(par[y][i],par[y][j]) for i in range(len(par[y])) for j in range(i)) else V) for y in range(m)]
    run=[1]*m
    for y in range(m):
        for a in par[y]:
            if ty[a]==ty[y]: run[y]=max(run[y],run[a]+1)
    rel=lambda a,b: a==b or bool(st[max(a,b)]>>min(a,b)&1)
    return dict(m=m,par=par,chi=chi,ty=ty,run=run,share=share,rel=rel)
def add(d,k,p):
    if p: d[k]=d.get(k,0)+p
def make(I,X,a,out,w):
    m=I['m']
    if X in (C,R): add(out,frozenset((a,)),w); return
    if X==D:
        el=[p for p in I['par'][a] if len(I['chi'][p])>1]
        if el:
            for p in el:
                sib=[c for c in I['chi'][p] if c!=a]
                for b in sib: add(out,frozenset((a,b)),w/len(el)/len(sib))
        else:
            for b in range(m): add(out,frozenset((a,b)),w/m)
        return
    cand=[c for c in range(m) if c!=a and not I['rel'](a,c) and not I['share'](a,c)]
    if not cand: cand=list(range(m))
    for b in cand: add(out,frozenset((a,b)),w/len(cand))
def base(I,out,w,mu,a=None):
    m=I['m']; anchors=[(a,F(1))] if a is not None else [(x,F(1,m)) for x in range(m)]
    for x,px in anchors:
        make(I,C,x,out,w*mu*px); make(I,D,x,out,w*mu*px)
        for b in range(m): add(out,frozenset((x,b)),w*(1-2*mu)*px/m)
MU=F(1,20)
def ruleK(st,mu=MU):
    I=info(st); out={}; base(I,out,F(1),mu); return out
def ruleA(st,q=F(1,2),mu=MU):
    I=info(st); m=I['m']; out={}
    if m>1:
        for t in range(1,m): add(out,frozenset(I['par'][t]),q/(m-1))
        base(I,out,1-q,mu)
    else: base(I,out,F(1),mu)
    return out
def ruleF(st,q=F(1,2),mu=MU):
    I=info(st); m=I['m']; out={}
    for t in range(m):
        if I['ty'][t]==R:
            for b in range(m): add(out,frozenset((t,b)),q/m/m)
        else: make(I,I['ty'][t],t,out,q/m)
    base(I,out,1-q,mu); return out
def ptype(w,eps):
    z=sum(w[X]**2 for X in (C,V,D))
    return {X: eps+(1-3*eps)*(F(w[X]**2,1)/z if z else F(1,3)) for X in (C,V,D)}
def ruleB(st,W=2,eps=F(1,20)):
    I=info(st); m=I['m']; out={}; lam=1-F(1,W); Ng=[F(0)]*4
    for i in range(1,m): Ng=[x*lam for x in Ng]; Ng[I['ty'][i]]+=1
    p=ptype(Ng,eps)
    for a in range(m):
        for X in (C,V,D): make(I,X,a,out,p[X]/m)
    return out
def ruleG(st,eps=F(1,20)):
    I=info(st); m=I['m']; out={}
    for a in range(m):
        w=[F(0)]*4; w[I['ty'][a]]+=1
        for p in I['par'][a]:
            w[I['ty'][p]]+=1
            for c in I['chi'][p]:
                if c!=a: w[I['ty'][c]]+=1
        for c in I['chi'][a]: w[I['ty'][c]]+=1
        p=ptype(w,eps)
        for X in (C,V,D): make(I,X,a,out,p[X]/m)
    return out
def ruleT(st,thr=2,plo=F(1,10),phi=F(9,10),mu=MU):
    I=info(st); m=I['m']; out={}
    for a in range(m):
        pc=F(0) if I['ty'][a]==R else (phi if I['run'][a]>=thr else plo)
        if pc: make(I,I['ty'][a],a,out,pc/m)
        base(I,out,(1-pc)/m,mu,a)
    return out
def ruleD(st,L=2,eps=F(1,20),theta=F(3,5),g=F(1,2)):
    I=info(st); m=I['m']; out={}; s=V; today=[0]*4
    def night():
        nonlocal s,today
        X=max((C,V,D),key=lambda Y:(today[Y],-Y)); z=sum(today[1:])
        if z and F(today[X],z)>=theta: s=X
        today=[0]*4
    for i in range(1,m+1):
        if i%L==0: night()
        if i<m: today[I['ty'][i]]+=1
    z=sum(today[X]**2 for X in (C,V,D))
    p={X: eps+(1-3*eps)*(((1-g)*(X==s)+g*F(today[X]**2,z)) if z else F(int(X==s))) for X in (C,V,D)}
    for a in range(m):
        for X in (C,V,D): make(I,X,a,out,p[X]/m)
    return out
RULES={'K (K2 + spontaneous shapes, mu=1/20)':ruleK,'K0 (pure K2)':lambda st:ruleK(st,F(0)),
 'A twin templating q=1/2':ruleA,'A0 twin templating q=1/2, mu=0':lambda st:ruleA(st,F(1,2),F(0)),
 'F forward templating q=1/2':ruleF,'F0 forward templating q=1/2, mu=0':lambda st:ruleF(st,F(1,2),F(0)),
 'B global motif liking W=2':ruleB,'G local motif liking':ruleG,'T lineage threshold thr=2':ruleT,'D day reset L=2':ruleD}
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
        rel=tuple(sorted((pm[a],pm[y]) for y in range(m) for a in range(m) if st[y]>>a&1))
        if best is None or rel<best: best=rel
    return (m,best)
def restrict(st,U):
    idx=[i for i in range(len(st)) if U>>i&1]; pos={i:k for k,i in enumerate(idx)}
    def rm(mask): return sum(1<<pos[i] for i in idx if mask>>i&1)
    return tuple(rm(st[i]) for i in idx),rm
for name,rule in RULES.items():
    level={(0,):F(1)}; allst=[(0,)]; gc_bad=0; gc_tot=0; gc_ex=None; tot=F(0)
    for m in range(1,N):
        nxt={}
        for st,p in level.items():
            T=trans(st,rule); assert sum(T.values())==1, (name,st,sum(T.values()))
            for a,pt in T.items(): add(nxt,st+(a,),p*pt)
        cls={}
        for st,p in nxt.items(): cls.setdefault(canon(st),[]).append(p)
        for k,v in cls.items():
            gc_tot+=1
            if min(v)!=max(v):
                gc_bad+=1
                if gc_ex is None: gc_ex=m+1
        level=nxt; allst+=list(nxt)
    bc_bad=0; bc_tot=0; bc_ex=None
    for st in allst:
        if len(st)>=N: continue
        T=trans(st,rule); ks=sorted(T)
        for i in range(len(ks)):
            for j in range(i+1,len(ks)):
                A,B=ks[i],ks[j]; U=A|B
                if U==(1<<len(st))-1 or U==0: continue
                st2,rm=restrict(st,U); T2=trans(st2,rule); bc_tot+=1
                if T[A]*T2.get(rm(B),0)!=T[B]*T2.get(rm(A),0):
                    bc_bad+=1
                    if bc_ex is None: bc_ex=len(st)
    print(f"{name:40s} cond2 broken in {gc_bad}/{gc_tot} patterns (first at {gc_ex} thoughts)   cond3 broken in {bc_bad}/{bc_tot} tests (first at size {bc_ex})")
