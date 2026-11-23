#!/bin/bash
# usage: run_balance.sh DIM N STEPS
cd /home/claude/council/compute_rules; mkdir -p bal; D=$1; N=$2; S=$3
./balance $D $N truth scatter $4 99 100 > bal/truth_${D}D_$N.txt
run(){ ./balance $D $N $1 $2 $S $3 100 > bal/${1}_${2}_s$3_${D}D_$N.txt 2>/dev/null; }
run multi perc 1 & run multi scatter 1 & wait
run multi perc 2 & run multi scatter 2 & wait
run null perc 1 & run null scatter 1 & wait
echo done
