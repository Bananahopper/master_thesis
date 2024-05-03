from src.analysis.per_region_dist import PerRegionDist
import os
import argparse
import logging


def main(mode, original_seg, cortical_seg, subcortical_seg):
    per_region_dist = PerRegionDist(mode)
    per_region_dist.process(original_seg, cortical_seg, subcortical_seg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run per region distribution")
    parser.add_argument("--mode", type=str, required=True, help="Mode of the analysis")
    parser.add_argument(
        "--original_seg",
        type=str,
        required=True,
        help="Path to the original segmentation",
    )
    parser.add_argument(
        "--cortical_seg",
        type=str,
        required=True,
        help="Path to the cortical segmentation",
    )
    parser.add_argument(
        "--subcortical_seg",
        type=str,
        required=True,
        help="Path to the subcortical segmentation",
    )
    args = parser.parse_args()

    if os.path.exists(
        "scratch/users/ggaspar/CaPTk/output_analysis/per_region_stats.log"
    ):
        os.remove("scratch/users/ggaspar/CaPTk/output_analysis/per_region_stats.log")

    # Configure logging
    logging.basicConfig(
        filename="/scratch/users/ggaspar/CaPTk/output_analysis/per_region_stats.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    main(
        args.mode,
        args.original_seg,
        args.cortical_seg,
        args.subcortical_seg,
    )
