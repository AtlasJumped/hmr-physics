#!/bin/bash
# dimension + motif runs: 11 rule settings x 4 sizes x 5 seeds
cd /home/claude/council/compute_rules
: > dim_raw.txt
for cfg in "K 2 0.5" "K 5 0.5" "L 2 0.5" "H 2 0.5" "M 2 0.5" "N 2 0.5" "N 2 0.9" "C 2 0.9" "T 2 0.9" "U 2 0.1" "U 2 0.2"; do
  set -- $cfg
  for n in 500 2000 8000 32000; do for s in 1 2 3 4 5; do
    timeout 600 ./grow dim $1 $n $s $2 $3 50 >> dim_raw.txt || echo "FAIL rule=$1 K=$2 q=$3 n=$n seed=$s" >> dim_raw.txt
  done; done
done
echo DONE >> dim_raw.txt
