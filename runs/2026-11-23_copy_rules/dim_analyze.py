# dimension, lineage, inheritance, write cost: mean (sd) over seeds
import re, collections, numpy as np
W=collections.defaultdict(list); I=collections.defaultdict(list); L=collections.defaultdict(list); H=collections.defaultdict(list)
kv=lambda s: {k:v for k,v in re.findall(r'(\w+)=([-\w.]+)',s)}
for line in open('dim_raw.txt'):
    tag,kind,rest=line.split(' ',2); d=kv(rest); n=int(d['n'])
    if kind=='WHOLE': W[tag,n].append([float(d[k]) for k in ('dmm','height','links','given_up_bits','copies','meangen','maxgen','maxs')])
    elif kind=='INT': I[tag,n,int(d['lo'])].append(float(d['dmm']))
    elif kind=='LIN':
        a,b=rest.split('|'); da=kv(a); db=kv(b)
        L[tag,n,da['type']].append([float(da[k]) for k in ('count','meanrun','maxrun','p5','p10')]+[float(db[k]) for k in ('meanrun','maxrun','p5','p10')])
    elif kind=='INH': H[tag,n].append([float(d[k]) for k in ('MI_bits','twin_mean','twin_max')])
tags=[]; [tags.append(t) for t,_ in W if t not in tags]; ns=sorted({n for _,n in W})
print("== whole-pattern Myrheim-Meyer dimension, mean (sd) over seeds ==")
print("rule  "+"  ".join(f"n={n:<10d}" for n in ns)+" | log2(n) slope of d, last two sizes")
for t in tags:
    m=[np.mean(W[t,n],0)[0] for n in ns]; s=[np.std(W[t,n],0)[0] for n in ns]
    print(f"{t:5s} "+"  ".join(f"{a:5.2f} ({b:4.2f})" for a,b in zip(m,s))+f" | {(m[-1]-m[-2])/2:+.3f} per doubling")
print("\n== height (longest chain) and exponent height~n^x from last two sizes; links per birth; frontier share ==")
for t in tags:
    hh=[np.mean(W[t,n],0)[1] for n in ns]
    print(f"{t:5s} height "+" ".join(f"{h:7.1f}" for h in hh)+f" | x={np.log(hh[-1]/hh[-2])/np.log(ns[-1]/ns[-2]):.3f} | links/birth at {ns[-1]}: {np.mean(W[t,ns[-1]],0)[2]/ns[-1]:.3f} | frontier share {np.mean(W[t,ns[-1]],0)[7]/ns[-1]:.3f}")
print("\n== dimension inside intervals by size bin (n=32000 and 128000) ==")
for n in (32000,128000):
    for t in tags:
        los=sorted({lo for (tt,nn,lo) in I if tt==t and nn==n})
        print(f"{t:5s} n={n} "+" ".join(f"{lo}:{np.mean(I[t,n,lo]):.2f}" for lo in los))
print("\n== write cost: bits of free choice given up per birth relative to K2 (second half of run), copies, copy generations ==")
for t in tags:
    for n in (2000,32000):
        w=np.array(W[t,n]); print(f"{t:5s} n={n:6d} given_up={w[:,3].mean():6.2f} (sd {w[:,3].std():.2f})  copy share={w[:,4].mean()/n:.3f}  mean copy generation={w[:,5].mean():.2f}  max={w[:,6].mean():.1f}")
print("\n== lineage: same-shape runs along links vs the same pattern with shapes shuffled (n=32000; mean over seeds) ==")
print("rule shape share | mean run (shuffled) | max run (shuffled) | P(run>=5) (shuffled) | P(run>=10) (shuffled)")
for t in tags:
    for X in 'CVD':
        a=np.mean(L[t,32000,X],0); sd=np.std(L[t,32000,X],0)
        print(f"{t:5s} {X} {a[0]/32000:.3f} (sd {sd[0]/32000:.3f}) | {a[1]:6.2f} ({a[5]:5.2f}) | {a[2]:5.1f} ({a[6]:5.1f}) | {a[3]:.4f} ({a[7]:.4f}) | {a[4]:.4f} ({a[8]:.4f})")
print("\n== max run by n (does the longest lineage grow?), shape C then D; observed/shuffled ==")
for t in tags:
    print(f"{t:5s} "+" | ".join(X+" "+" ".join(f"{np.mean(L[t,n,X],0)[2]:.0f}/{np.mean(L[t,n,X],0)[6]:.0f}" for n in ns) for X in 'CD'))
print("\n== shape inheritance (bits between a thought's shape and a parent's shape) and twin classes, n=32000 ==")
for t in tags:
    h=np.array(H[t,32000]); print(f"{t:5s} MI={h[:,0].mean():.4f} (sd {h[:,0].std():.4f})  twin class size (size-weighted mean)={h[:,1].mean():.2f}  max={h[:,2].mean():.0f}")
