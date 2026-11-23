#!/bin/bash
# multistability test for rule U near its densification threshold: per-window mean direct parents, 30 seeds per q
cd /home/claude/council/compute_rules; : > multi_raw.txt
for qq in 0.10 0.12 0.14 0.16 0.18; do for s in $(seq 1 30); do
  timeout 120 ./grow2 ts U 8001 $s 2 $qq 50 500 | sed "s/^/q=$qq seed=$s /" >> multi_raw.txt
done; done
echo DONE >> multi_raw.txt
