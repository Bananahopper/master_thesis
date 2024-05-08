#!/bin/bash
#SBATCH -J Run_Per_Dataset_Dist
#SBATCH -N 1
#SBATCH -c 50
#SBATCH --time=1-00:00:00
#SBATCH -p batch
#SBATCH --qos=normal


module load tools/Singularity
source activate CaPTk

python scripts/Tumor_per_dataset/run_per_dataset_dist.py --cortical_pattern "$1" --subcortical_pattern "$2"