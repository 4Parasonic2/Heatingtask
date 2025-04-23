#!/bin/bash
#BSUB -R "rusage[mem=1024MB] select[model==XeonGold6142] span[hosts=1]"
#BSUB -q hpc
#BSUB -W 60
#BSUB -J cpu_numba
#BSUB -n 1
#BSUB -o cpu_numba_100%J.out
#BSUB -e cpu_numba_100%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613
time python sim.py 100
