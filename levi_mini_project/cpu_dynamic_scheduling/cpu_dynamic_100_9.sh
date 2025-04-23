#!/bin/bash
#BSUB -R "rusage[mem=1024MB] select[model==XeonGold6142] span[hosts=1]"
#BSUB -q hpc
#BSUB -W 60
#BSUB -J cpu_dynamic_100_9
#BSUB -n 9
#BSUB -o cpu_dynamic_100_9_%J.out
#BSUB -e cpu_dynamic_100_9_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613
time python sim.py 100 9
