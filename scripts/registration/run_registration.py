from src.registration.registrator import Registrator
import argparse
import os
import logging


def main(
    principal_atlas_path,
    cortical_atlas_path,
    subcortical_atlas_path,
    t1_path_pattern,
    seg_path_pattern,
):

    registrator = Registrator(
        principal_atlas_path, cortical_atlas_path, subcortical_atlas_path
    )
    registrator.run(t1_path_pattern, seg_path_pattern)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the registration.")
    parser.add_argument(
        "--principal_atlas_path",
        type=str,
        required=True,
        help="Path to the principal atlas.",
    )
    parser.add_argument(
        "--cortical_atlas_path",
        type=str,
        required=True,
        help="Path to the cortical atlas.",
    )
    parser.add_argument(
        "--subcortical_atlas_path",
        type=str,
        required=True,
        help="Path to the subcortical atlas.",
    )
    parser.add_argument(
        "--t1_path_pattern", type=str, required=True, help="Pattern to the T1 files."
    )
    parser.add_argument(
        "--seg_path_pattern",
        type=str,
        required=True,
        help="Pattern to the segmentation files.",
    )

    args = parser.parse_args()

    if os.path.exists("logs/registration.log"):
        os.remove("logs/registration.log")

    logging.basicConfig(
        filename="logs/registration.log",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    main(
        args.principal_atlas_path,
        args.cortical_atlas_path,
        args.subcortical_atlas_path,
        args.t1_path_pattern,
        args.seg_path_pattern,
    )

# registrator = Registrator(
#     "/atlases/mni_icbm152_t1_tal_nlin_asym_09a_brain_only.nii",
#     "/atlases/HarvardOxford-cort-maxprob-thr25-2mm.nii",
#     "/atlases/HarvardOxford-sub-maxprob-thr25-2mm.nii",
# )

# registrator.run(
#     "/datasets/Brats2021_wTumor/*/*_t1.nii.gz",
#     "/datasets/Brats2021_wTumor/*/*_seg.nii.gz",
# )
