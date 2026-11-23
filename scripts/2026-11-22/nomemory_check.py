# Check: in sequential growth rules written as "attention" (pick a set S, size-weighted, uniform within size),
# is the internal order of late-born thoughts independent of the internal order of early-born thoughts?
# Statistic: R_early = related pairs among first k thoughts; R_late = related pairs among last n-k. Correlation over runs.
import random, math
def grow(n, rule, rng):
    anc=[0]*n
    for m in range(1,n):
        if rule[0]=='perc':
            S=[j for j in range(m) if rng.random()<rule[1]]
        else:
            K=rule[1]; S=list(set(rng.randrange(m) for _ in range(K)))
        a=0
        for p in S: a|=anc[p]|(1<<p)
        anc[m]=a
    return anc
def stats(anc,k,n):
    early=(1<<k)-1; late=((1<<n)-1)^early
    Re=sum(bin(anc[i]&early).count('1') for i in range(k))
    Rl=sum(bin(anc[i]&late).count('1') for i in range(k,n))
    Rx=sum(bin(anc[i]&early).count('1') for i in range(k,n))
    return Re,Rl,Rx
def corr(x,y):
    n=len(x); mx=sum(x)/n; my=sum(y)/n
    sx=math.sqrt(sum((a-mx)**2 for a in x)); sy=math.sqrt(sum((b-my)**2 for b in y))
    return sum((a-mx)*(b-my) for a,b in zip(x,y))/(sx*sy)
rng=random.Random(7)
for rule in (('perc',0.1),('perc',0.3),('K',2),('K',4)):
    E=[];L=[];X=[]
    for _ in range(20000):
        a=grow(24,rule,rng); e,l,x=stats(a,12,24); E.append(e);L.append(l);X.append(x)
    print(rule, "corr(R_early,R_late)=%.4f  corr(R_early,R_cross)=%.4f  (noise ~ %.4f)"%(corr(E,L),corr(E,X),1/math.sqrt(len(E))))
