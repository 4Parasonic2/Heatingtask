#!/bin/bash
#BSUB -R "rusage[mem=4096MB] span[hosts=1]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -q c02613
#BSUB -W 00:50
#BSUB -J gpu_numba
#BSUB -n 4
#BSUB -o gpu_numba_%J.out
#BSUB -e gpu_numba_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

time python sim.py 100
