import re,glob,sys,statistics as st
keys=['rw','height','links','N1','N2','N3','mins','maxs','b0','b1','b2','b3','b4','c0','c1','c2','c3','c4']
def rows(f,tag):
    out=[]
    for l in open(f):
        if l.startswith(tag): out.append({k:float(v) for k,v in (x.split('=') for x in l.split()[1:])})
    return out
show=['height','links','N1','N2','N3','mins','maxs','c0','c1','c2','c3','c4']
for D,N in ((4,1000),(4,2000),(4,4000),(3,2000)):
    fs=sorted(glob.glob(f'bal/*_{D}D_{N}.txt'))
    if not fs: continue
    print(f"\n== {D}D, N={N}. Truth = mean±sd over scatters. Chains: mean of trace points in third quarter | last quarter of the run (agreement = stationary). c0..c4 = number of intervals in size bins 5-9,10-19,20-39,40-79,80-159")
    print("run | "+" | ".join(show)+" | bin shares b0..b4 (last quarter) | rw | acceptance")
    for f in fs:
        name=f.split('/')[-1].replace(f'_{D}D_{N}.txt','')
        if name=='truth':
            r=rows(f,'TRUTH'); print(f"truth ({len(r)} scatters) | "+" | ".join(f"{st.mean(x[k] for x in r):.0f}±{st.pstdev([x[k] for x in r]):.0f}" if k!='height' else f"{st.mean(x[k] for x in r):.1f}±{st.pstdev([x[k] for x in r]):.1f}" for k in show)+" | "+" ".join(f"{st.mean(x[k] for x in r):.3f}" for k in ['b0','b1','b2','b3','b4'])+f" | {st.mean(x['rw'] for x in r):.4f} | -")
            continue
        r=rows(f,'TRACE'); 
        if len(r)<40: print(name,"incomplete",len(r)); continue
        q3=r[20:30]; q4=r[30:40]
        print(f"{name} | "+" | ".join(f"{st.mean(x[k] for x in q3):.0f}|{st.mean(x[k] for x in q4):.0f}" if k!='height' else f"{st.mean(x[k] for x in q3):.1f}|{st.mean(x[k] for x in q4):.1f}" for k in show)+" | "+" ".join(f"{st.mean(x[k] for x in q4):.3f}" for k in ['b0','b1','b2','b3','b4'])+f" | {st.mean(x['rw'] for x in q4):.4f} | {r[-1]['acc']:.2f}")
