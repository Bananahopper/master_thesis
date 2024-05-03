import logging
import argparse
import os
from src.segmentation.tumor_segmentation import TumorSegmentor


def main(t1_pattern: str, t1ce_pattern: str, t2_pattern: str, flair_pattern: str):

    tumor_segmentor = TumorSegmentor()

    tumor_segmentor.run(t1_pattern, t1ce_pattern, t2_pattern, flair_pattern)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run tumor segmentation")
    parser.add_argument(
        "--t1_pattern", type=str, required=True, help="Pattern for the T1 files"
    )
    parser.add_argument(
        "--t1ce_pattern", type=str, required=True, help="Pattern for the T1ce files"
    )
    parser.add_argument(
        "--t2_pattern", type=str, required=True, help="Pattern for the T2 files"
    )
    parser.add_argument(
        "--flair_pattern", type=str, required=True, help="Pattern for the FLAIR files"
    )
    args = parser.parse_args()

    if os.path.exists("output_registration/tumor_segmentation.log"):
        os.remove("output_registration/tumor_segmentation.log")

    logging.basicConfig(
        filename="output_registration/tumor_segmentation.log",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    main(
        args.t1_pattern,
        args.t1ce_pattern,
        args.t2_pattern,
        args.flair_pattern,
    )
