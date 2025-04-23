#!/bin/bash
#BSUB -R "rusage[mem=1024MB] select[model==XeonGold6142]"
#BSUB -q hpc
#BSUB -W 60
#BSUB -J sim_100
#BSUB -n 1
#BSUB -o sim_100_%J.out
#BSUB -e sim_100_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613
time python ../simulate.py 100
