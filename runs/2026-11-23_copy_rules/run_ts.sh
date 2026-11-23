#!/bin/bash
# multistability time series (free runs) and write pulses
cd /home/claude/council/compute_copy; mkdir -p ts pulse
free(){ tag=$1; shift; for sd in 1 2 3 4 5 6; do ./copy mode=ts n=128000 win=100 seed=$sd "$@" > ts/${tag}_s$sd.txt; done; }
free K rule=K
for W in 25 50 100 200 400; do for e in 0.05 0.10; do free B_W${W}_e$e rule=B W=$W eps=$e alpha=2; done; done
free Blin_W100_e0.05 rule=B W=100 eps=0.05 alpha=1
free G rule=G eps=0.05 alpha=2
free G_e0.01 rule=G eps=0.01 alpha=2
free F5 rule=F q=0.5
free F9 rule=F q=0.9
free F9f rule=F q=0.9 qa=0.5
free A9 rule=A q=0.9
free T rule=T thr=3 plo=0.1 phi=0.9
free T1 rule=T thr=3 plo=0.1 phi=1.0
free D rule=D L=200 eps=0.05 theta=0.6 g=0.5
free D_e0.15 rule=D L=200 eps=0.15 theta=0.6 g=0.5
free D_g0.8 rule=D L=200 eps=0.05 theta=0.6 g=0.8
# pulses: write D at 8000 for P births, then write C at 20000 for P births; n=32000, 20 seeds
pul(){ tag=$1; shift; for P in 0 25 50 100 150 200 400 800; do for sd in $(seq 1 20); do
  if [ $P = 0 ]; then ./copy mode=ts n=32000 win=100 seed=$sd "$@" > pulse/${tag}_P${P}_s$sd.txt
  else ./copy mode=ts n=32000 win=100 seed=$sd pulse=8000:$P:D pulse=20000:$P:C "$@" > pulse/${tag}_P${P}_s$sd.txt; fi; done; done; }
pul K rule=K
pul B rule=B W=100 eps=0.05 alpha=2
pul D rule=D L=200 eps=0.05 theta=0.6 g=0.5
pul G rule=G eps=0.05 alpha=2
pul F5 rule=F q=0.5
pul F9 rule=F q=0.9
pul A9 rule=A q=0.9
pul T rule=T thr=3 plo=0.1 phi=0.9
pul T1 rule=T thr=3 plo=0.1 phi=1.0
