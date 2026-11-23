# Retention curve: correlation of a block's internal statistic with a block `lag` blocks later (blocks of 100 births, n=1600),
# averaged over starting blocks 4..(15-lag). Noise: same with runs shuffled.
import numpy as np
rng=np.random.default_rng(2)
lags=[1,2,3,4,6,8,11]
print("rule stat | "+" ".join(f"lag{100*l:5d}" for l in lags)+" | shuffle sd (lag 100)")
for tag in ('K2','M0.5','N0.9','C0.9','T0.9','U0.1','U0.14'):
    d=np.loadtxt(f'mem/ret_{tag}.txt'); B=16
    for si,sn in ((0,'R'),(1,'Lk')):
        X=d[:,si::5]; X=(X-X.mean(0))/ (X.std(0)+1e-12)
        out=[]
        for l in lags: out.append(np.mean([(X[:,i]*X[:,i+l]).mean() for i in range(4,B-l)]))
        p=rng.permutation(len(X)); nul=[np.mean([(X[:,i]*X[rng.permutation(len(X)),i+1]).mean() for i in range(4,B-1)]) for _ in range(20)]
        print(f"{tag:6s} {sn:2s} | "+" ".join(f"{v:+8.4f}" for v in out)+f" | {np.std(nul):.4f}")
