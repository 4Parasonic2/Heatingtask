#!/bin/bash
#BSUB -R "rusage[mem=1024MB] select[model==XeonGold6126]"
#BSUB -q hpc
#BSUB -W 60
#BSUB -J sim_20
#BSUB -n 1
#BSUB -o sim_20_%J.out
#BSUB -e sim_20_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613
time python ../simulate.py 20
