#!/bin/bash
# follow-up: local rules with the anchor drawn from the frontier (thoughts nothing is built on yet) with chance qa
cd /home/claude/council/compute_copy; mkdir -p front
for cfg in "G 0.5" "G 1.0" "T 1.0" "F 1.0"; do set -- $cfg; r=$1; qa=$2
  for P in 0 100 800; do for sd in $(seq 1 10); do
   if [ $P = 0 ]; then ./copy mode=ts n=64000 win=100 seed=$sd rule=$r qa=$qa q=0.9 eps=0.05 > front/${r}_qa${qa}_P${P}_s$sd.txt
   else ./copy mode=ts n=64000 win=100 seed=$sd rule=$r qa=$qa q=0.9 eps=0.05 pulse=16000:$P:V pulse=40000:$P:C > front/${r}_qa${qa}_P${P}_s$sd.txt; fi; done; done
  for n in 2000 8000 32000 128000; do for sd in 1 2 3; do ./copy mode=dim rule=$r qa=$qa q=0.9 eps=0.05 n=$n seed=$sd | grep WHOLE | sed "s/^/${r}_qa$qa /"; done; done > front/dim_${r}_qa$qa.txt
done
