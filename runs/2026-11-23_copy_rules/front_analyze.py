# frontier-anchor follow-up (untar front_raw.tgz first): per-seed shares, write tests, dimension
import numpy as np, glob, re
for tag in ("G_qa0.5","G_qa1.0","T_qa1.0","F_qa1.0"):
    for P in (0,100,800):
        a=np.array([np.loadtxt(f,usecols=(2,3,4)) for f in sorted(glob.glob(f'front/{tag}_P{P}_s*.txt'),key=lambda s:int(re.search(r's(\d+)\.txt',s).group(1)))])
        c=[a[:,lo:hi,0].mean(1) for lo,hi in ((80,160),(320,400),(560,640))]; v=[a[:,lo:hi,1].mean(1) for lo,hi in ((80,160),(320,400),(560,640))]
        print(f"{tag} P={P:3d} C share by seed: "+" | ".join(" ".join(f"{x:.2f}" for x in cc) for cc in c))
        print(f"{tag} P={P:3d} mean V share {v[0].mean():.3f} -> {v[1].mean():.3f} -> {v[2].mean():.3f}; mean C share {c[0].mean():.3f} -> {c[1].mean():.3f} -> {c[2].mean():.3f}")
for tag in ("G_qa0.5","G_qa1.0","T_qa1.0","F_qa1.0"):
    d={}
    for line in open(f'front/dim_{tag}.txt'):
        k=dict(re.findall(r'(\w+)=([-\w.]+)',line)); d.setdefault(int(k['n']),[]).append((float(k['dmm']),float(k['height'])))
    print(tag," ".join(f"{np.mean(d[n],0)[0]:.2f} (sd {np.std(d[n],0)[0]:.2f}, h={np.mean(d[n],0)[1]:.0f})" for n in sorted(d)))
