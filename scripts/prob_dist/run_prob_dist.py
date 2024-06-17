import os
from src.constants import WORK_PATH_CAPTK
from src.analysis.prob_dist import ProbDist
import argparse
import logging


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


def main(
    pattern,
    dataset_name,
    whole_tumor,
):
    prob = ProbDist(
        dataset_name,
        whole_tumor,
    )
    prob.run(pattern)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate probability distribution")
    parser.add_argument(
        "--pattern",
        type=str,
        required=True,
        help="Pattern for the registered tumor segmentations",
    )
    parser.add_argument(
        "--dataset_name", type=str, required=True, help="Name of the dataset"
    )
    parser.add_argument(
        "--whole_tumor",
        type=str2bool,
        required=True,
        help="Whether to consider the whole tumor, or consider only the tumor core without the edema.",
    )
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        filename="/scratch/users/ggaspar/CaPTk/logs/prob_dist.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    logging.info(f"Running ProbDist with the following parameters: {args}")

    main(
        args.pattern,
        args.dataset_name,
        args.whole_tumor,
    )
