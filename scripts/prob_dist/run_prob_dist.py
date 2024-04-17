from src.analysis.prob_dist import ProbDist
import argparse
import logging


def main(
    dataset_path,
    dataset_name,
    atlas_path,
    labels,
    array_size,
    necrotic_core,
    enhancing_region,
    edema,
):
    prob = ProbDist(
        dataset_path,
        dataset_name,
        atlas_path,
        labels,
        array_size,
        necrotic_core,
        enhancing_region,
        edema,
    )
    prob.process_data()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate probability distribution")
    parser.add_argument(
        "--dataset_path", type=str, required=True, help="Path to the dataset"
    )
    parser.add_argument(
        "--dataset_name", type=str, required=True, help="Name of the dataset"
    )
    parser.add_argument(
        "--atlas_path", type=str, required=True, help="Path to the atlas"
    )
    parser.add_argument(
        "--labels", type=bool, required=True, help="Whether to use labels"
    )
    parser.add_argument(
        "--array_size", type=list, required=True, help="Size of the array"
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

    # Configure logging
    logging.basicConfig(
        filename="prob_dist.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    main(
        args.dataset_path,
        args.dataset_name,
        args.atlas_path,
        args.labels,
        args.array_size,
        args.necrotic_core,
        args.enhancing_region,
        args.edema,
    )
