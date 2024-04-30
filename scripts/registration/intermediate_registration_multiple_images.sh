#!/bin/bash/

python scripts/registration/run_registration_multiple_images.py \
       --atlas "$1" \
       --t1_pattern "$2" \
       --t2_pattern "$3" \
       --t1ce_pattern "$4" \
       --flair_pattern "$5" 