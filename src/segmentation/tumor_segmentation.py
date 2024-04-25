import logging
import os
from src.common.io.command_operations import run_commands
from src.common.io.path_operations import (
    extract_save_dir_from_path,
    get_file_list_from_pattern,
)


class TumorSegmentor:
    def __init__(self):
        pass

    def run(
        self, t1_pattern: str, t1ce_pattern: str, t2_pattern: str, flair_pattern: str
    ):
        """
        Run CaPTk tumor segmentation on a skull stripped MRI images

        Args:
            t1_pattern (str): pattern to get the list of T1 images
            t1ce_pattern (str): pattern to get the list of T1ce images
            t2_pattern (str): pattern to get the list of T2 images
            flair_pattern (str): pattern to get the list of FLAIR images
        """

        t1_path_list = get_file_list_from_pattern(t1_pattern)
        t1ce_path_list = get_file_list_from_pattern(t1ce_pattern)
        t2_path_list = get_file_list_from_pattern(t2_pattern)
        flair_path_list = get_file_list_from_pattern(flair_pattern)

        if (
            len(t1_path_list) != len(t1ce_path_list)
            or len(t1_path_list) != len(t2_path_list)
            or len(t1_path_list) != len(flair_path_list)
        ):
            logging.error("Number of T1, T1ce, T2 and FLAIR images do not match.")
            return

        commands = []

        for t1_path, t1ce_path, t2_path, flair_path in zip(
            t1_path_list, t1ce_path_list, t2_path_list, flair_path_list
        ):

            logging.info(
                "Creating command for:"
                + t1_path
                + " "
                + t1ce_path
                + " "
                + t2_path
                + " "
                + flair_path
            )

            command = self.create_CaPTk_tumor_segmentation_command(
                t1_path, t1ce_path, t2_path, flair_path
            )

            logging.info("Command:" + command)

            commands.append(command)

        run_commands(commands)

        logging.info("Tumor segmentation was successful.")

    def create_CaPTk_tumor_segmentation_command(
        self, t1_path: str, t1ce_path: str, t2_path: str, flair_path: str
    ):
        """
        Create a CaPTk Skull strip command for a T1 image.

        Args:
            t1_path (str): path to the T1 image
            t1ce_path (str): path to the T1ce image
            t2_path (str): path to the T2 image
            flair_path (str): path to the FLAIR image

        Returns:
            str: command
        """

        save_directory = extract_save_dir_from_path(t1_path)

        output_folder = os.path.join(save_directory, "tumor_segmentation_outputs")

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        logging.info("Output folder:" + output_folder)

        command = (
            "/work/CaPTk/bin/install/appdir/usr/bin/DeepMedic"
            + " -md "
            + "/work/CaPTk/bin/install/appdir/usr/data/deepMedic/saved_models/brainTumorSegmentation"
            + " -i "
            + t1_path
            + ","
            + t1ce_path
            + ","
            + t2_path
            + ","
            + flair_path
            + " -o "
            + output_folder
        )

        return command
