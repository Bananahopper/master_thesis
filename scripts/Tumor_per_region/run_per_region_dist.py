from src.analysis.per_region_dist import PerRegionDist
import argparse
import logging


def main(name, mode):
    tpr = PerRegionDist(name, mode)
    tpr.process()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate tumor per region")
    parser.add_argument(
        "--name", type=str, required=True, help="Name of the dataset for saving"
    )
    parser.add_argument(
        "--mode",
        type=int,
        required=True,
        help="Mode = 1 for tumor in region / total tumor, Mode = 2 for tumor in region / total region",
    )
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        filename="per_region_stats.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    main(args.name, args.mode)
