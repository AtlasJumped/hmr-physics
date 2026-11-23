#!/bin/bash
# memory runs: per-block internal statistics, many independent runs
cd /home/claude/council/compute_rules; mkdir -p mem
for spec in "24 2 200000 0.1 6" "200 4 100000 0.02 25" "2000 4 20000 0.002 250"; do
  set -- $spec; n=$1;B=$2;runs=$3;pp=$4;w=$5
  ./grow mem K $n 7 2 0.5 $w $runs $B > mem/K2_$n.txt
  ./grow mem P $n 7 2 $pp $w $runs $B > mem/P_$n.txt
  ./grow mem L $n 7 2 0.5 $w $runs $B > mem/L_$n.txt
  ./grow mem H $n 7 2 0.5 $w $runs $B > mem/H_$n.txt
  ./grow mem M $n 7 2 0.5 $w $runs $B > mem/M0.5_$n.txt
  ./grow mem N $n 7 2 0.5 $w $runs $B > mem/N0.5_$n.txt
  ./grow mem N $n 7 2 0.9 $w $runs $B > mem/N0.9_$n.txt
  ./grow mem C $n 7 2 0.9 $w $runs $B > mem/C0.9_$n.txt
  ./grow mem T $n 7 2 0.9 $w $runs $B > mem/T0.9_$n.txt
  ./grow mem U $n 7 2 0.1 $w $runs $B > mem/U0.1_$n.txt
  r2=$((runs/5)); ./grow mem U $n 7 2 0.2 $w $r2 $B > mem/U0.2_$n.txt
done
