#!/bin/bash/

python scripts/segmentation/run_tumor_segmentation.py \
       --t1_pattern "$1" \
       --t1ce_pattern "$2" \
       --t2_pattern "$3" \
       --flair_pattern "$4" 