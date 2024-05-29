import argparse
import logging
import os
from src.registration.registrator_multiple_images import RegistratorMultipleImages


def main(
    atlas,
    t1_pattern,
    t2_pattern,
    t1ce_pattern,
    flair_pattern,
):
    registrator = RegistratorMultipleImages(atlas)
    registrator.run(t1_pattern, t2_pattern, t1ce_pattern, flair_pattern)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the registration.")
    parser.add_argument(
        "--atlas",
        type=str,
        required=True,
        help="Path to the atlas.",
    )
    parser.add_argument(
        "--t1_pattern",
        type=str,
        required=True,
        help="Pattern to the T1 files.",
    )
    parser.add_argument(
        "--t2_pattern",
        type=str,
        required=True,
        help="Pattern to the T2 files.",
    )
    parser.add_argument(
        "--t1ce_pattern",
        type=str,
        required=True,
        help="Pattern to the T1CE files.",
    )
    parser.add_argument(
        "--flair_pattern",
        type=str,
        required=True,
        help="Pattern to the FLAIR files.",
    )

    args = parser.parse_args()

    if os.path.exists("logs/registration_multiple_images.log"):
        os.remove("logs/registration_multiple_images.log")

    logging.basicConfig(
        filename="logs/registration_multiple_images.log",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    main(
        args.atlas,
        args.t1_pattern,
        args.t2_pattern,
        args.t1ce_pattern,
        args.flair_pattern,
    )
