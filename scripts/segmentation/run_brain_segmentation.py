import logging
import argparse
from src.segmentation.brain_segmentation import BrainExtractor


def main(
    pattern: str,
):

    brain_extractor = BrainExtractor()

    brain_extractor.run(pattern)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run brain segmentation")
    parser.add_argument(
        "--pattern", type=str, required=True, help="Pattern for the files"
    )
    args = parser.parse_args()

    # # Configure logging
    # logging.basicConfig(
    #     filename="brain_extraction.log",
    #     level=logging.INFO,
    #     format="%(asctime)s - %(levelname)s - %(message)s",
    # )

    main(
        args.pattern,
    )
