#!/bin/bash
#BSUB -R "rusage[mem=4096MB] span[hosts=1]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -q c02613
#BSUB -W 00:50
#BSUB -J cupy_fixed_100
#BSUB -n 4
#BSUB -o cupy_fixed_100_%J.out
#BSUB -e cupy_fixed_100_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

time python sim_fixed_iter.py 100
