#!/bin/bash
# dimension, lineage, write cost: 5 seeds per size
cd /home/claude/council/compute_copy
cfg(){ case $1 in
 K0) echo "rule=K mu=0";; K) echo "rule=K";; A5) echo "rule=A q=0.5";; A9) echo "rule=A q=0.9";;
 F5) echo "rule=F q=0.5";; F9) echo "rule=F q=0.9";; F9f) echo "rule=F q=0.9 qa=0.5";;
 B) echo "rule=B W=100 eps=0.05 alpha=2";; G) echo "rule=G eps=0.05 alpha=2";;
 T) echo "rule=T thr=3 plo=0.1 phi=0.9";; T1) echo "rule=T thr=3 plo=0.1 phi=1.0";; D) echo "rule=D L=200 eps=0.05 theta=0.6 g=0.5";; esac; }
for tag in K0 K A5 A9 F5 F9 F9f B G T T1 D; do for n in 500 2000 8000 32000 128000; do for sd in 1 2 3 4 5; do
  [ $n = 128000 ] && [ $sd -gt 3 ] && continue
  ./copy mode=dim $(cfg $tag) n=$n seed=$sd | sed "s/^/$tag /"
done; done; done > dim_raw.txt
