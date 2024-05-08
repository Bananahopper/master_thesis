from src.analysis.per_dataset_dist import PerDatasetDist
import argparse
import logging
import os


def main(cortical_pattern, subcortical_pattern):
    per_dataset_dist = PerDatasetDist()
    per_dataset_dist.process(cortical_pattern, subcortical_pattern)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Per dataset distance analysis.")
    parser.add_argument(
        "--cortical_pattern",
        type=str,
        help="Pattern for the cortical segmentations.",
    )
    parser.add_argument(
        "--subcortical_pattern",
        type=str,
        help="Pattern for the subcortical segmentations.",
    )

    args = parser.parse_args()

    if os.path.exists(
        "scratch/users/ggaspar/CaPTk/output_analysis/per_dataset_stats.log"
    ):
        os.remove("scratch/users/ggaspar/CaPTk/output_analysis/per_dataset_stats.log")

    # Configure logging
    logging.basicConfig(
        filename="/scratch/users/ggaspar/CaPTk/output_analysis/per_dataset_stats.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    main(args.cortical_pattern, args.subcortical_pattern)
