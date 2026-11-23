# Free-run time series: are there two or more stable states, and does the system switch between them both ways?
# Windows of 100 births, n=128000, 6 seeds. State = shape whose smoothed share (5 windows) exceeds 0.5; held until another shape exceeds 0.5.
import numpy as np, glob, re, collections
names='CVD'
def load(f): return np.loadtxt(f,usecols=(1,2,3,4,5,6,7,8))
def states(fr,k=5):
    sm=np.vstack([np.convolve(fr[:,i],np.ones(k)/k,mode='valid') for i in range(3)]).T
    st=[];cur=-1
    for row in sm:
        j=int(np.argmax(row))
        if row[j]>0.5: cur=j
        st.append(cur)
    return np.array(st),sm
tags=[]
for f in sorted(glob.glob('ts/*_s1.txt')): tags.append(re.sub(r'_s1.txt$','',f[3:]))
print("config | per-seed mean shares C/V/D over second half | across-seed sd of C share | within-seed sd of C share (windows of 1000, second half) | switches total | mean dwell (births) | transitions (from>to:count) | time share in each state")
for tag in tags:
    means=[];within=[];sw=0;dw=[];tr=collections.Counter();occ=np.zeros(4);
    for f in sorted(glob.glob(f'ts/{tag}_s*.txt')):
        d=load(f); fr=d[:,1:4]; h=len(fr)//2; means.append(fr[h:].mean(0))
        c=fr[h:,0]; c=c[:len(c)//10*10].reshape(-1,10).mean(1); within.append(c.std())
        st,_=states(fr); st=st[50:]   # drop first 5000 births
        for s in st: occ[s]+=1
        idx=np.flatnonzero(np.diff(st)!=0); sw+=len(idx)
        for a,b in zip(st[idx],st[idx+1]): tr[names[a]+'>'+names[b]]+=1
        if len(idx)>1: dw+=list(np.diff(idx)*100)
    means=np.array(means); occ/=occ.sum()
    print(f"{tag:16s} | "+" ".join("%.2f/%.2f/%.2f"%tuple(m) for m in means)+f" | {means[:,0].std():.3f} | {np.mean(within):.3f} | {sw} | {np.mean(dw) if dw else float('nan'):.0f} | "+" ".join(f"{k}:{v}" for k,v in sorted(tr.items()))+" | "+" ".join(f"{names[i]}:{occ[i]:.2f}" for i in range(3)))
print("\n== barrier: histogram of the smoothed C share (pooled seeds, after first 5000 births), 10 bins from 0 to 1 ==")
for tag in tags:
    if not tag.startswith('B'): continue
    hs=np.zeros(10)
    for f in sorted(glob.glob(f'ts/{tag}_s*.txt')):
        st,sm=states(load(f)[:,1:4]); hs+=np.histogram(sm[50:,0],bins=10,range=(0,1))[0]
    hs/=hs.sum(); print(f"{tag:16s} "+" ".join(f"{x:.4f}" for x in hs))
print("\n== durable store of rule D (day reset): value of s per seed over time (share of days in C/V/D), number of changes ==")
for tag in tags:
    if not tag.startswith('D'): continue
    for f in sorted(glob.glob(f'ts/{tag}_s*.txt')):
        s=load(f)[:,7].astype(int); print(tag,f[-6:-4],"share s=C/V/D: %.2f/%.2f/%.2f"%tuple((s==k).mean() for k in (1,2,3)),"changes:",int((np.diff(s)!=0).sum()))
print("\n== write cost (bits of choice given up per birth, second half) and copy share ==")
for tag in tags:
    v=[load(f) for f in sorted(glob.glob(f'ts/{tag}_s*.txt'))]; print(f"{tag:16s} given up {np.mean([x[len(x)//2:,4].mean() for x in v]):6.2f} bits  copy share {np.mean([x[len(x)//2:,5].mean() for x in v]):.3f}")
