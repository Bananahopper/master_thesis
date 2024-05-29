import logging
import argparse
import os
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

    if os.path.exists("logs/brain_extraction.log"):
        os.remove("logs/brain_extraction.log")

    logging.basicConfig(
        filename="logs/brain_extraction.log",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    main(
        args.pattern,
    )
