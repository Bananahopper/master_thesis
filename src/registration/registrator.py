import glob
import logging
import os
import subprocess
from common.io.path_operations import (
    create_registration_folder_for_subject_file_path,
    extract_subject_id_from_file_path,
    get_file_list_from_pattern,
)
from constants import AFFINE_NAME


class Registrator:
    """
    This class is used to register T1 images, and their tumor masks, to a normalized space atlas.
    """

    allowed_metrics = ["MI", "WNCC"]
    # allowed patch radius for arbitrary dimension
    allowed_patch_radius = [2]

    def __init__(
        self,
        target_atlas: str,
        max_iterations: list[int] = [100, 50, 10],
        metric: str = "MI",
        patch_radius: list[int] = [2, 2, 2],
        ia_image_centers: bool = True,
    ):

        if metric not in self.allowed_metrics:
            raise ValueError(
                "The metric must be one of the following: " + str(self.allowed_metrics)
            )

        # check for each patch_radius if it is allowed
        for i in range(len(patch_radius)):
            if patch_radius[i] not in self.allowed_patch_radius:
                raise ValueError(
                    "The patch radius must be one of the following: "
                    + str(self.allowed_patch_radius)
                )

        # check if paths are absolute paths
        if target_atlas[0] != os.path.sep:
            raise ValueError("Target is not an absolute path")

        logging.info("Running greedy registration with the following parameters:")
        logging.info("Target: " + target_atlas)
        logging.info("Max iterations: " + str(max_iterations))
        logging.info("Metric: " + metric)
        logging.info("Patch radius: " + str(patch_radius))
        logging.info("Align image centers first: " + str(ia_image_centers))

        self.target = target_atlas
        self.max_iterations = max_iterations
        self.metric = metric
        self.patch_radius = patch_radius
        self.ia_image_centers = ia_image_centers

    def run(self, source: str, label: str):
        """
        Runs the greedy algorithm for every file in the source.
        """
        file_list = get_file_list_from_pattern(source)
        label_list = get_file_list_from_pattern(label)

        if len(file_list) != len(label_list):
            raise ValueError("The number of files and labels must be the same")

        for idx, (file, label) in enumerate(zip(file_list, label_list)):
            logging.info(str(idx) + "/" + str(len(file_list)))
            self.register(file, label)

    def register(self, file: str, label: str):
        """
        Registers a single file to the target.
        Args:
            file (str): file to be registered
            label (str): label to be registered
        """
        logging.info("Registration for :" + file)

        output_folder, affine_folder, warp_folder, inverse_warp_folder = (
            create_registration_folder_for_subject_file_path(file)
        )

        affine_file_path = os.path.join(affine_folder, AFFINE_NAME)

        self.create_affine_command(file, self.target, affine_file_path)

    def create_affine_command(
        self, source_file: str, target_file: str, affine_file_path: str
    ):
        """
        Creates the command for the greedy algorithm.

        Args:
            source_file (str): file to be registered
            target_file (str): target file
            transformation_file_path (str): path to the transformation file
        """
        command_affine = (
            "greedy -d 3 -a -i "
            + target_file
            + " "
            + source_file
            + " -o "
            + affine_file_path
        )
        command_affine += (
            " -m "
            + self.metric
            + " "
            + str(self.patch_radius[0])
            + "x"
            + str(self.patch_radius[1])
            + "x"
            + str(self.patch_radius[2])
        )
        command_affine += (
            " -n "
            + str(self.max_iterations[0])
            + "x"
            + str(self.max_iterations[1])
            + "x"
            + str(self.max_iterations[2])
        )
        if self.ia_image_centers:
            command_affine += " -ia-image-centers "

        logging.info(
            "Calculating greedy registration with the following command: "
            + command_affine
        )
        return command_affine
