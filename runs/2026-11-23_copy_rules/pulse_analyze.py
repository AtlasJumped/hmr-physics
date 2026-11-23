# Write test. n=32000, 20 seeds. Write 1: force shape D for P births from birth 8000. Write 2: force shape C for P births from birth 20000.
# Reported: share of new births with the written shape in later windows, minus the same windows of the no-write control (P=0),
# and the number of seeds (of 20) in which the written shape holds the majority (>0.5) of births long after the write.
import numpy as np, glob
def load(tag,P): return np.array([np.loadtxt(f,usecols=(2,3,4,8)) for f in sorted(glob.glob(f'pulse/{tag}_P{P}_s*.txt'))])  # seeds x windows x (C,V,D,s)
def w(a,lo,hi,col): return a[:,lo//100:hi//100,col].mean(1)
print("rule P | excess D share at births 9-10k, 12-13k, 16-17k, 19-20k (sem) | seeds with D majority at 16-20k | excess C share at 21-22k, 24-25k, 31-32k | seeds with C majority at 28-32k | seeds with D majority at 28-32k")
for tag in ('K','F5','F9','A9','T','T1','G','B','D'):
    c=load(tag,0)
    for P in (25,50,100,150,200,400,800):
        a=load(tag,P)
        e=[(w(a,lo,lo+1000,2)-w(c,lo,lo+1000,2)) for lo in (9000,12000,16000,19000)]
        e2=[(w(a,lo,lo+1000,0)-w(c,lo,lo+1000,0)) for lo in (21000,24000,31000)]
        print(f"{tag:3s} {P:4d} | "+" ".join(f"{x.mean():+.3f}" for x in e)+f" ({e[1].std()/np.sqrt(len(a)):.3f}) | {(w(a,16000,20000,2)>0.5).sum():2d} | "+" ".join(f"{x.mean():+.3f}" for x in e2)+f" | {(w(a,28000,32000,0)>0.5).sum():2d} | {(w(a,28000,32000,2)>0.5).sum():2d}")
    print(f"{tag:3s} control: C majority at 16-20k in {(w(c,16000,20000,0)>0.5).sum()} seeds, V majority in {(w(c,16000,20000,1)>0.5).sum()}, D majority in {(w(c,16000,20000,2)>0.5).sum()}; at 28-32k C {(w(c,28000,32000,0)>0.5).sum()}, V {(w(c,28000,32000,1)>0.5).sum()}, D {(w(c,28000,32000,2)>0.5).sum()}")
print("\n== rule D (day reset, L=200, theta=0.6): durable store s after each write. seeds with s=D at birth 19900; s=C at 31900 ==")
for P in (25,50,100,150,200,400,800):
    a=load('D',P); print(f"P={P:4d}: s=D after write 1 in {(a[:,198,3]==3).sum():2d}/20; s=C after write 2 in {(a[:,318,3]==1).sum():2d}/20")
print("\n== decay of a written excess (rule F and A, P=800): excess D share by window after write 1, births 9k..20k in 1k steps ==")
for tag in ('F5','F9','A9','T','G'):
    c=load(tag,0); a=load(tag,800); print(tag," ".join(f"{(w(a,lo,lo+1000,2)-w(c,lo,lo+1000,2)).mean():+.3f}" for lo in range(9000,20000,1000)))
