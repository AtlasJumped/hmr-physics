#!/bin/bash
# follow-up: dwell time against window W for rule B (eps=0.10), and write tests between its two stable states (V and C)
cd /home/claude/council/compute_copy; mkdir -p ts2 pulse2
for W in 10 15 20 25 30 35 40 50; do for sd in 1 2 3 4 5 6; do ./copy mode=ts n=128000 win=100 seed=$sd rule=B W=$W eps=0.10 alpha=2 > ts2/B_W${W}_s$sd.txt; done; done
for cfg in "50 0.10" "100 0.05" "100 0.10"; do set -- $cfg; for P in 0 10 25 50 100 150 200 400 800; do for sd in $(seq 1 20); do
  if [ $P = 0 ]; then ./copy mode=ts n=32000 win=100 seed=$sd rule=B W=$1 eps=$2 > pulse2/B_W$1_e$2_P${P}_s$sd.txt
  else ./copy mode=ts n=32000 win=100 seed=$sd rule=B W=$1 eps=$2 pulse=8000:$P:V pulse=20000:$P:C > pulse2/B_W$1_e$2_P${P}_s$sd.txt; fi; done; done; done
