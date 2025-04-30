#!/bin/bash
#BSUB -R "rusage[mem=4096MB] span[hosts=1]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -q c02613
#BSUB -W 3:00
#BSUB -J task12_join
#BSUB -n 4
#BSUB -o task12_join%J_%I.out
#BSUB -e task12_join%J_%I.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

time python task12_join.py
