#!/bin/bash
# memory (early/late block statistics) and retention
cd /home/claude/council/compute_copy; mkdir -p mem
cfg(){ case $1 in
 K0) echo "rule=K mu=0";; K) echo "rule=K";; A5) echo "rule=A q=0.5";; A9) echo "rule=A q=0.9";;
 F5) echo "rule=F q=0.5";; F9) echo "rule=F q=0.9";; F9f) echo "rule=F q=0.9 qa=0.5";;
 B) echo "rule=B W=100 eps=0.05 alpha=2";; G) echo "rule=G eps=0.05 alpha=2";;
 T) echo "rule=T thr=3 plo=0.1 phi=0.9";; T1) echo "rule=T thr=3 plo=0.1 phi=1.0";; D) echo "rule=D L=200 eps=0.05 theta=0.6 g=0.5";; esac; }
for tag in K0 K A5 A9 F5 F9 F9f B G T T1 D; do
  ./copy mode=mem $(cfg $tag) n=200 runs=100000 B=4 seed=7 > mem/${tag}_200.txt
  ./copy mode=mem $(cfg $tag) n=2000 runs=20000 B=4 seed=7 > mem/${tag}_2000.txt
  ./copy mode=mem $(cfg $tag) n=1600 runs=20000 B=16 seed=9 > mem/ret_${tag}.txt
  ./copy mode=mem $(cfg $tag) n=25600 runs=1500 B=16 seed=11 > mem/retL_${tag}.txt
done
