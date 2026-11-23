# rule B: dwell time against W; write tests V then C
import numpy as np, glob
def states(fr,k=5):
    sm=np.vstack([np.convolve(fr[:,i],np.ones(k)/k,mode='valid') for i in range(3)]).T; st=[];cur=-1
    for row in sm:
        j=int(np.argmax(row))
        if row[j]>0.5: cur=j
        st.append(cur)
    return np.array(st)
print("== rule B eps=0.10 alpha=2, n=128000, 6 seeds: completed dwells in C and in V (births); censored dwells (run ended) not counted ==")
for W in (10,15,20,25,30,35,40,50):
    dw={0:[],1:[],2:[]}; nsw=0; occ=np.zeros(3)
    for f in sorted(glob.glob(f'ts2/B_W{W}_s*.txt')):
        st=states(np.loadtxt(f,usecols=(2,3,4)))[50:]; idx=np.flatnonzero(np.diff(st)!=0); nsw+=len(idx)
        for s in range(3): occ[s]+=(st==s).sum()
        for a,b in zip(idx[:-1],idx[1:]): dw[st[b]].append((b-a)*100)
    occ/=occ.sum()
    print(f"W={W:3d} switches={nsw:4d} | C: n={len(dw[0]):3d} mean dwell={np.mean(dw[0]) if dw[0] else float('nan'):8.0f} | V: n={len(dw[1]):3d} mean dwell={np.mean(dw[1]) if dw[1] else float('nan'):8.0f} | D: n={len(dw[2]):3d} mean dwell={np.mean(dw[2]) if dw[2] else float('nan'):6.0f} | time share C/V/D {occ[0]:.2f}/{occ[1]:.2f}/{occ[2]:.2f}")
print("\n== write tests, 20 seeds, n=32000: write V for P births at 8000, write C for P births at 20000. seeds with V majority at 16-20k; with C majority at 28-32k ==")
for cfg in ("W50_e0.10","W100_e0.05","W100_e0.10"):
    for P in (0,10,25,50,100,150,200,400,800):
        a=np.array([np.loadtxt(f,usecols=(2,3,4)) for f in sorted(glob.glob(f'pulse2/B_{cfg}_P{P}_s*.txt'))])
        print(f"B {cfg} P={P:4d}: before write (4-8k) C majority {(a[:,40:80,0].mean(1)>0.5).sum():2d}, V {(a[:,40:80,1].mean(1)>0.5).sum():2d} | after write 1: V majority {(a[:,160:200,1].mean(1)>0.5).sum():2d}/20 | after write 2: C majority {(a[:,280:320,0].mean(1)>0.5).sum():2d}/20")
