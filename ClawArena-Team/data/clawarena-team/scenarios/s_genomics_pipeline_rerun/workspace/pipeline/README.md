# varcall-2026q2 Pipeline

Three-stage variant calling pipeline:
1. `align.py` — BWA-MEM2 alignment to reference genome
2. `call.py` — GATK HaplotypeCaller variant calling
3. `filter.py` — VQSR filtration

**Current run**: reference genome GRCh38.p15 (upgraded from GRCh38.p14).

Launch: `bash run_varcall.sh`

Expected runtime: 6–12 hours for 127 samples (ETL-heavy; schedule as background task).
