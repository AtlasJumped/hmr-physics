import re,collections,statistics as st,math
W=collections.defaultdict(list); I=collections.defaultdict(list)
for l in open('dim_raw.txt'):
    kv=dict(x.split('=') for x in l.split()[1:] if '=' in x)
    if l.startswith('WHOLE'): W[(kv['rule'],kv['K'],kv['q'],int(kv['n']))].append(kv)
    elif l.startswith('INT'): I[(kv['rule'],kv['K'],kv['q'],int(kv['n']),int(kv['lo']))].append((float(kv['dmm']),int(kv['cnt'])))
def ms(v): return f"{st.mean(v):.2f}±{st.pstdev(v):.2f}"
rules=sorted({k[:3] for k in W},key=lambda k:"KLHMNCTU".index(k[0])*10+float(k[2])+float(k[1]))
print("A. Whole pattern, mean±sd over seeds. d_MM = Myrheim-Meyer from related share; d_h = chain-growth dimension between this size and the previous one = ln(n ratio)/ln(height ratio)")
print("rule K q | n | seeds | d_MM | height | d_h | direct parents (last tenth) | diamonds per 100 births | share of diamond tops stacked on a diamond | longest stack | Fano")
for r in rules:
    prev=None
    for n in (500,2000,8000,32000):
        v=W.get(r+(n,))
        if not v: print(f"{r[0]} {r[1]} {r[2]} | {n} | 0 | not run (timed out)"); continue
        h=st.mean(float(x['height']) for x in v)
        dh=f"{math.log(n/prev[0])/math.log(h/prev[1]):.2f}" if prev and h>prev[1] else "-"
        tops=sum(int(x['tops']) for x in v); stk=sum(int(x['stacked']) for x in v)
        print(f"{r[0]} {r[1]} {r[2]} | {n} | {len(v)} | {ms([float(x['dmm']) for x in v])} | {ms([float(x['height']) for x in v])} | {dh} | {ms([float(x['linkpar_last']) for x in v])} | {ms([float(x['diam_per100']) for x in v])} | {stk/max(tops,1):.2f} | {max(int(x['maxstack']) for x in v)} | {ms([float(x['fano']) for x in v])}")
        prev=(n,h)
print()
print("B. Inside intervals: d_MM by interval size bin, mean±sd over seeds (bins with at least 3 seeds having >=20 intervals). A space would give one value across bins and sizes.")
for r in rules:
    for n in (2000,8000,32000):
        out=[]
        for lo in (16,32,64,128,256,512,1024,2048):
            v=[d for d,c in I.get(r+(n,lo),[]) if c>=20]
            if len(v)>=3: out.append(f"{lo}:{st.mean(v):.2f}±{st.pstdev(v):.2f}")
        print(f"{r[0]} {r[1]} {r[2]} n={n}: "+"  ".join(out))
