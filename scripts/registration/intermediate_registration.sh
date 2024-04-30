#!/bin/bash/

python scripts/registration/run_registration.py \
       --principal_atlas_path "$1" \
       --cortical_atlas_path "$2" \
       --subcortical_atlas_path "$3" \
       --t1_path_pattern "$4" \
       --seg_path_pattern "$5" 