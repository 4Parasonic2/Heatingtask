#!/bin/bash
#BSUB -R "rusage[mem=1024MB] select[model==XeonGold6126] span[hosts=1]"
#BSUB -q hpc
#BSUB -W 60
#BSUB -J cpu_static
#BSUB -n 6
#BSUB -o cpu_static_100_6_%J.out
#BSUB -e cpu_static_100_6_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613
time python sim.py 100 6
