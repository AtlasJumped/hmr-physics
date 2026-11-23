grow.c / grow          growth rules; modes mem (block statistics over many runs) and dim (dimension, motifs)
grow2.c / grow2        same rules (identical output checked) plus mode ts: windowed parents, diamonds, choice entropy
balance.c / balance    Task 2 MCMC with incremental interval tables
run_*.sh               the exact commands used
*_analyze.py, retention.py, doob_check.py, conditions_check.py   analysis; outputs in *_out.txt
mem/*.txt.gz           raw per-run block statistics (gunzip before re-running the analysis scripts)
dim_raw.txt, multi_raw.txt, entropy_raw.txt, bal/*.txt           raw outputs
