#!/bin/bash
#SBATCH -J Run_Per_Region_Dist
#SBATCH -N 1
#SBATCH -c 50
#SBATCH --time=1-00:00:00
#SBATCH -p batch
#SBATCH --qos=normal


python scripts/Tumor_per_region/run_per_region_dist.py --mode "$1" --original_seg "$2" --cortical_seg "$3" --subcortical_seg "$4"