#!/bin/bash
#SBATCH -J CaPTk_connectome_registration
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 128
#SBATCH --time=1-00:00:00
#SBATCH -p batch
#SBATCH --qos=normal

singularity exec  --no-home \
                  --bind datasets/:/datasets \
                  --bind output_registration_connectome/:/output_registration_connectome \
                  --bind src/:/src \
                  --bind scripts:/scripts \
                  --bind atlases/:/atlases \
                  --bind logs/:/logs \
                  captk_latest.sif \
                  python src/registration/connectome_registrator.py --source "$1" --label "$2" --target_atlas "$3" --patient_id_number "$4"