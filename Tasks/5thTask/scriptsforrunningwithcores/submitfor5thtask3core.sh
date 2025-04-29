#!/bin/bash

# -- -- -- Start of LSF options -- -- --
### General options 
### -- specify queue -- 
#BSUB -q hpc
### -- set the job Name -- 
#BSUB -J 5thtask3
### -- ask for number of cores (default: 1) -- 
#BSUB -n 3 
### -- specify that the cores must be on the same host -- 
#BSUB -R "span[hosts=1]"
### -- specify that we need 4GB of memory per core/slot -- 
#BSUB -R "rusage[mem=4GB]"
#BSUB -R "select[model == XeonE5_2660v3]"
### -- specify that we want the job to get killed if it exceeds 5 GB per core/slot -- 
#BSUB -M 5GB
### -- set walltime limit: hh:mm -- 
#BSUB -W 24:00  
### -- send notification at start -- 
#BSUB -B 
### -- send notification at completion -- 
#BSUB -N 
### -- Specify the output and error file. %J is the job-id -- 
### -- -o and -e mean append, -oo and -eo mean overwrite -- 
#BSUB -o 5thtask3_%J.out 
#BSUB -e 5thtask3_%J.err 
# -- -- -- end of LSF options -- -- --


source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613
lscpu
time python task5.py 100 3