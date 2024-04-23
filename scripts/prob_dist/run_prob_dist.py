import os
from constants import WORK_PATH_CAPTK
from src.analysis.prob_dist import ProbDist
import argparse
import logging


def main(
    pattern,
    dataset_name,
    labels,
    necrotic_core,
    enhancing_region,
    edema,
):
    prob = ProbDist(
        dataset_name,
        labels,
        necrotic_core,
        enhancing_region,
        edema,
    )
    prob.run(pattern)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate probability distribution")
    parser.add_argument(
        "--pattern", type=str, required=True, help="Pattern for the files"
    )
    parser.add_argument(
        "--dataset_name", type=str, required=True, help="Name of the dataset"
    )
    parser.add_argument(
        "--labels", type=bool, required=True, help="Whether to use labels"
    )
    parser.add_argument(
        "--necrotic_core",
        type=bool,
        required=False,
        help="Whether to use necrotic core",
    )
    parser.add_argument(
        "--enhancing_region",
        type=bool,
        required=False,
        help="Whether to use enhancing region",
    )
    parser.add_argument(
        "--edema", type=bool, required=False, help="Whether to use edema"
    )
    args = parser.parse_args()

    if not os.path.exists(WORK_PATH_CAPTK, "logs/"):
        os.makedirs(WORK_PATH_CAPTK, "logs")

    # Configure logging
    logging.basicConfig(
        filename="logs/prob_dist.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    main(
        args.pattern,
        args.dataset_name,
        args.labels,
        args.necrotic_core,
        args.enhancing_region,
        args.edema,
    )
