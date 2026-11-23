# Early/late shape memory: correlations between internal statistics of block 1 and later blocks, with shuffled controls.
# Stats per block: R related pairs, Lk links, H longest chain, Dm link-diamonds, Mn minimal thoughts (all internal to the block).
import numpy as np, glob, os, sys
rng=np.random.default_rng(0)
names=['R','Lk','H','Dm','Mn']
def cmat(X,Y):
    X=(X-X.mean(0)); Y=(Y-Y.mean(0)); sx=np.sqrt((X**2).sum(0)); sy=np.sqrt((Y**2).sum(0))
    sx[sx==0]=np.inf; sy[sy==0]=np.inf
    return (X.T@Y)/np.outer(sx,sy)
def mi(x,y,nb=6):
    def q(v):
        r=np.argsort(np.argsort(v+rng.random(len(v))*1e-6)); return (r*nb//len(v))
    a=q(x);b=q(y); J=np.zeros((nb,nb)); np.add.at(J,(a,b),1); J/=J.sum(); pa=J.sum(1,keepdims=True); pb=J.sum(0,keepdims=True)
    m=J>0; return float((J[m]*np.log2(J[m]/(pa@pb)[m])).sum())
print("rule n runs | corr(R_1,R_last) +- shuffle sd | max|corr| over 25 stat pairs (which) vs shuffle 99th pct | MI(R_1;R_last) bits minus shuffle mean (shuffle sd) | corr(R_1,R_b) for b=2..B")
for n in (24,200,2000):
    for tag in ('K2','P','L','H','M0.5','N0.5','N0.9','C0.9','T0.9','U0.1','U0.2'):
        f=f'mem/{tag}_{n}.txt'
        if not os.path.exists(f): continue
        d=np.loadtxt(f); runs=d.shape[0]; B=d.shape[1]//5; blk=[d[:,5*b:5*b+5] for b in range(B)]
        C=cmat(blk[0],blk[-1]); i,j=np.unravel_index(np.argmax(np.abs(C)),C.shape)
        nullR=[];nullmax=[];nullmi=[]
        for _ in range(300):
            p=rng.permutation(runs); Cs=cmat(blk[0],blk[-1][p]); nullR.append(Cs[0,0]); nullmax.append(np.abs(Cs).max())
        for _ in range(40): nullmi.append(mi(blk[0][:,0],blk[-1][rng.permutation(runs),0]))
        m=mi(blk[0][:,0],blk[-1][:,0])
        lag=" ".join("%+.3f"%cmat(blk[0],blk[b])[0,0] for b in range(1,B))
        print(f"{tag:5s} {n:5d} {runs:6d} | {C[0,0]:+.4f} +- {np.std(nullR):.4f} | {abs(C[i,j]):.4f} ({names[i]}1,{names[j]}last) vs {np.percentile(nullmax,99):.4f} | {m-np.mean(nullmi):+.5f} ({np.std(nullmi):.5f}) | {lag}")
