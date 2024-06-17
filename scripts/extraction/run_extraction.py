from src.constants import WORK_PATH_CAPTK
from src.extraction.extraction import Extractor
import argparse
import logging
import os


def main(image_pattern, mask_pattern):
    extraction = Extractor(image_pattern, mask_pattern)

    extraction.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract brain from image")
    parser.add_argument(
        "--image_pattern", type=str, required=True, help="Pattern for T1 files"
    )
    parser.add_argument(
        "--mask_pattern", type=str, required=True, help="Pattern for mask files"
    )

    if os.getcwd() == WORK_PATH_CAPTK:
        if not os.path.exists(WORK_PATH_CAPTK, "logs"):
            os.makedirs(WORK_PATH_CAPTK, "logs")

        logging.basicConfig(
            filename="/scratch/users/ggaspar/CaPTk/logs/extraction.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

    args = parser.parse_args()

    main(args.image_pattern, args.mask_pattern)
