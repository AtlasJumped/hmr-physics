copy.c                 all rules; modes mem (block statistics over many runs), ts (windowed time series, write pulses), dim (dimension, lineage, write cost)
                       build: gcc -O2 -o copy copy.c -lm   (binary not kept)
run_dim.sh, run_mem.sh, run_ts.sh, run_ts2.sh, run_front.sh   the exact commands used
conditions_check.py -> conditions_out.txt    exact check of conditions 2 and 3 on patterns up to 5 thoughts
dim_analyze.py  -> dim_out.txt   (raw: dim_raw.txt)          dimension, lineage, inheritance, write cost
mem_analyze.py  -> mem_out.txt   (raw: mem/*.txt.gz, gunzip first)   memory and retention
ts_analyze.py   -> ts_out.txt    (raw: ts_raw.tgz, folder ts/)       free runs, states, dwell
ts2_analyze.py  -> ts2_out.txt   (raw: ts_raw.tgz folder ts2/, pulse_raw.tgz folder pulse2/)   rule B dwell against W, V/C write tests
pulse_analyze.py-> pulse_out.txt (raw: pulse_raw.tgz, folder pulse/) write tests D then C, all rules
front_analyze.py-> front_out.txt (raw: front_raw.tgz, folder front/)   frontier-anchor follow-up
