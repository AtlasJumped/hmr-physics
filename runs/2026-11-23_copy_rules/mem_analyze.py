# Early/late memory: correlations between internal statistics of block 1 and later blocks, with shuffled controls.
# Stats per block: R related pairs, Lk links, H longest chain, nC one-parent shapes, nD diamond-top shapes (internal to the block).
import numpy as np, os
rng=np.random.default_rng(0); names=['R','Lk','H','nC','nD']
TAGS=('K0','K','A5','A9','F5','F9','F9f','B','G','T','T1','D')
def cmat(X,Y):
    X=X-X.mean(0); Y=Y-Y.mean(0); sx=np.sqrt((X**2).sum(0)); sy=np.sqrt((Y**2).sum(0)); sx[sx==0]=np.inf; sy[sy==0]=np.inf
    return (X.T@Y)/np.outer(sx,sy)
def mi(x,y,nb=6):
    q=lambda v: (np.argsort(np.argsort(v+rng.random(len(v))*1e-6))*nb//len(v))
    a=q(x);b=q(y); J=np.zeros((nb,nb)); np.add.at(J,(a,b),1); J/=J.sum(); pa=J.sum(1,keepdims=True); pb=J.sum(0,keepdims=True); m=J>0
    return float((J[m]*np.log2(J[m]/(pa@pb)[m])).sum())
print("== block 1 vs last block (4 blocks). corr of R, nC, nD; shuffle sd; max|corr| over 25 pairs vs shuffled 99th pct; MI(nC_1;nC_last) bits minus shuffle mean ==")
for n in (200,2000):
    for tag in TAGS:
        f=f'mem/{tag}_{n}.txt'
        if not os.path.exists(f): continue
        d=np.loadtxt(f); runs=d.shape[0]; B=d.shape[1]//5; blk=[d[:,5*b:5*b+5] for b in range(B)]
        C=cmat(blk[0],blk[-1]); i,j=np.unravel_index(np.argmax(np.abs(C)),C.shape); nulR=[];nulmax=[];nulmi=[]
        for _ in range(200):
            Cs=cmat(blk[0],blk[-1][rng.permutation(runs)]); nulR.append(Cs[0,0]); nulmax.append(np.abs(Cs).max())
        for _ in range(30): nulmi.append(mi(blk[0][:,3],blk[-1][rng.permutation(runs),3]))
        m=mi(blk[0][:,3],blk[-1][:,3])
        lag=" ".join("%+.3f"%cmat(blk[0],blk[b])[3,3] for b in range(1,B))
        print(f"{tag:4s} n={n:5d} runs={runs:6d} | R {C[0,0]:+.4f} nC {C[3,3]:+.4f} nD {C[4,4]:+.4f} +- {np.std(nulR):.4f} | max {abs(C[i,j]):.4f} ({names[i]}1,{names[j]}last) vs {np.percentile(nulmax,99):.4f} | MI {m-np.mean(nulmi):+.5f} ({np.std(nulmi):.5f}) | nC block1 vs 2,3,4: {lag}")
print("\n== retention: corr of a block's count with a later block. Short: n=1600, blocks of 100, 20000 runs. Long: n=25600, blocks of 1600, 1500 runs. ==")
print("== reference block = block 3 (index 2); later blocks 4,5,6,8,11,16 => birth-time ratio 1.4,1.8,2.2,3.0,4.2,6.2 ; statistic nC (and nD, Lk) ==")
for tag in TAGS:
    for pre,lab in (('ret','short'),('retL','long ')):
        f=f'mem/{pre}_{tag}.txt'
        if not os.path.exists(f): continue
        d=np.loadtxt(f); out=[]
        for si,sn in ((3,'nC'),(4,'nD'),(1,'Lk')):
            X=d[:,si::5]; X=(X-X.mean(0))/(X.std(0)+1e-12)
            out.append(sn+" "+" ".join(f"{(X[:,2]*X[:,j]).mean():+.3f}" for j in (3,4,5,7,10,15)))
        print(f"{tag:4s} {lab} noise {1/np.sqrt(len(d)):.3f} | "+" | ".join(out))
print("\n== retention at fixed lag (short runs, blocks of 100): mean corr of nC over start blocks 5.., lag 100..1100 ==")
for tag in TAGS:
    f=f'mem/ret_{tag}.txt'
    if not os.path.exists(f): continue
    d=np.loadtxt(f); X=d[:,3::5]; X=(X-X.mean(0))/(X.std(0)+1e-12)
    print(f"{tag:4s} "+" ".join(f"{np.mean([(X[:,i]*X[:,i+l]).mean() for i in range(4,16-l)]):+.3f}" for l in (1,2,3,4,6,8,11)))
