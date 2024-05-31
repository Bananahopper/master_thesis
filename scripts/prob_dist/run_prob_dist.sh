#!/bin/bash
#SBATCH -J ProbDist
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 128
#SBATCH --time=1-00:00:00
#SBATCH -p batch
#SBATCH --qos=normal

# Load env
source activate CaPTk

# RUN
python /scratch/users/ggaspar/CaPTk/scripts/prob_dist/run_prob_dist.py \
       --pattern "$1" \
       --dataset_name "$2" \
       --whole_tumor "$3" 