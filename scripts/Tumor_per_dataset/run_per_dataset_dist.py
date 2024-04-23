from src.analysis.per_dataset_dist import PerDatasetDist
import argparse
import logging


def main(name):
    perdata = PerDatasetDist(name)
    perdata.process()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate tumor per region")
    parser.add_argument(
        "--name", type=str, required=True, help="Name of the dataset for saving"
    )
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        filename="per_dataset_stats.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    main(args.name)
