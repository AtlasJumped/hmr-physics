# Label-independent candidate: V1 rule K2 reweighted by a liking of the FINAL pattern (Doob transform with terminal weight).
# Keeps conditions 1, 2, 4 exactly (weight depends only on the unlabeled final pattern); breaks 3; depends on the horizon N.
# Weighted early/late correlation of internal related-pair counts; noise by shuffling the late block together with... (see below).
import numpy as np
rng=np.random.default_rng(1)
def wcorr(x,y,w):
    w=w/w.sum(); mx=(w*x).sum(); my=(w*y).sum(); return (w*(x-mx)*(y-my)).sum()/np.sqrt((w*(x-mx)**2).sum()*(w*(y-my)**2).sum())
for n,B in ((24,2),(200,4)):
    d=np.loadtxt(f'mem/K2_{n}.txt'); t=np.loadtxt(f'mem/K2_{n}_whole.txt')
    Re,Rl=d[:,0],d[:,5*(B-1)]; De,Dl=d[:,3],d[:,5*(B-1)+3]
    for name,stat,thetas in (('diamonds',t[:,3],(0.5,1.0,2.0)),('related pairs',t[:,0],(0.02,0.05,-0.05) if n==24 else (0.0005,0.001,-0.001))):
        for th in thetas:
            w=np.exp(th*(stat-stat.mean())); ess=w.sum()**2/(w**2).sum()
            c=wcorr(Re,Rl,w)
            # control: same weights, late block shuffled among runs (destroys any early/late link, keeps weight spread)
            null=[wcorr(Re,Rl[rng.permutation(len(Rl))],w) for _ in range(200)]
            print(f"n={n} first vs last block  liking=exp({th:+g} x {name} in final pattern)  effective runs={ess:9.0f}  corr(R_first,R_last)={c:+.4f}  shuffle sd={np.std(null):.4f}  unweighted={np.corrcoef(Re,Rl)[0,1]:+.4f}")
