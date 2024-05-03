import os
import logging
from typing import List

from src.common.io.command_operations import run_commands
from src.common.io.path_operations import (
    create_registration_folder_for_subject_file_path_multiple_images,
    extract_subject_id_from_file_path,
    get_file_list_from_pattern,
)
from src.constants import AFFINE_NAME, WARP_NAME


class RegistratorMultipleImages:
    """
    This class registers multiple MRI modalities to a target atlas.
    """

    def __init__(
        self,
        target_atlas: str,
        max_iterations: List[int] = [100, 50, 10],
        metric: str = "MI",
        patch_radius: List[int] = [2, 2, 2],
        ia_image_centers: bool = True,
    ):

        if target_atlas[0] != os.path.sep:
            raise ValueError("target_atlas should be an absolute path")

        logging.info("Initializing RegistratorMultipleImages")
        logging.info(f"target_atlas: {target_atlas}")
        logging.info(f"max_iterations: {max_iterations}")
        logging.info(f"metric: {metric}")
        logging.info(f"patch_radius: {patch_radius}")
        logging.info(f"ia_image_centers: {ia_image_centers}")

        self.target_atlas = target_atlas
        self.max_iterations = max_iterations
        self.metric = metric
        self.patch_radius = patch_radius
        self.ia_image_centers = ia_image_centers

    def run(
        self,
        t1_pattern: str = None,
        t2_pattern: str = None,
        t1ce_pattern: str = None,
        flair_pattern: str = None,
    ):

        if (
            t1_pattern is None
            and t2_pattern is None
            and t1ce_pattern is None
            and flair_pattern is None
        ):
            raise ValueError("At least one modality should be provided!")

        if t1_pattern is not None:
            t1_list = get_file_list_from_pattern(t1_pattern)

            logging.info(f"t1_list: {t1_list}")

        if t2_pattern is not None:
            t2_list = get_file_list_from_pattern(t2_pattern)

            logging.info(f"t2_list: {t2_list}")

        if t1ce_pattern is not None:
            t1ce_list = get_file_list_from_pattern(t1ce_pattern)

            logging.info(f"t1ce_list: {t1ce_list}")

        if flair_pattern is not None:
            flair_list = get_file_list_from_pattern(flair_pattern)

            logging.info(f"flair_list: {flair_list}")

        for t1, t2, t1ce, flair in zip(t1_list, t2_list, t1ce_list, flair_list):
            for idx, file in enumerate((t1, t2, t1ce, flair)):

                modality = (
                    "T1"
                    if idx == 0
                    else "T2" if idx == 1 else "T1CE" if idx == 2 else "FLAIR"
                )

                _, affine_folder, warp_folder, _ = (
                    create_registration_folder_for_subject_file_path_multiple_images(
                        file, modality
                    )
                )

                subject_id, _ = extract_subject_id_from_file_path(file)

                commands_to_run = []

                # Affine commands

                if modality == "T1":
                    affine_file_path = os.path.join(affine_folder, AFFINE_NAME)
                    t1_affine_file_path = affine_file_path
                elif modality != "T1":
                    affine_file_path = t1_affine_file_path

                output_affine_subject_file_path = os.path.join(
                    affine_folder, subject_id + f"_aff_reg_{modality}.nii.gz"
                )

                if modality == "T1":
                    command_affine = self.create_affine_command(
                        self.target_atlas, file, affine_file_path
                    )

                    commands_to_run.append(command_affine)

                command_apply_affine = self.create_apply_affine_command(
                    file,
                    self.target_atlas,
                    affine_file_path,
                    output_affine_subject_file_path,
                )
                commands_to_run.append(command_apply_affine)

                # Deformable commands

                if modality == "T1":
                    warp_file_path = os.path.join(warp_folder, WARP_NAME)
                    t1_warp_file_path = warp_file_path
                elif modality != "T1":
                    warp_file_path = t1_warp_file_path

                output_warp_subject_file_path = os.path.join(
                    warp_folder, subject_id + f"_def_reg_{modality}.nii.gz"
                )

                if modality == "T1":
                    deformable_command = self.create_warp_command(
                        file, self.target_atlas, affine_file_path, warp_file_path
                    )

                    commands_to_run.append(deformable_command)

                deformable_apply_commands = self.create_apply_warp_command(
                    file,
                    self.target_atlas,
                    warp_file_path,
                    affine_file_path,
                    output_warp_subject_file_path,
                )
                commands_to_run.append(deformable_apply_commands)

                run_commands(commands_to_run)

    def create_affine_command(
        self, target_atlas: str, file: str, affine_file_path: str
    ):
        """
        Creates the command for the affine registration.

        Args:
            file (str): file to register
            target_atlas (str): target atlas
            affine_file_path (str): path to the affine.mat file
        Returns:
            str: affine command
        """
        command_affine = (
            "/work/CaPTk/bin/install/appdir/usr/bin/greedy -d 3 -a -i "
            + target_atlas
            + " "
            + file
            + " -o "
            + affine_file_path
        )

        command_affine += " -m " + self.metric

        command_affine += (
            " -n "
            + str(self.max_iterations[0])
            + "x"
            + str(self.max_iterations[1])
            + "x"
            + str(self.max_iterations[2])
        )

        command_affine += " -ia-image-centers" if self.ia_image_centers else ""

        # logging.info(
        #     f"Creating affine registration with the following command: {command_affine}"
        # )

        return command_affine

    def create_apply_affine_command(
        self,
        file: str,
        target_atlas: str,
        affine_file_path: str,
        output_affine_subject_file_path: str,
    ):
        """
        Creates the apply command for the greedy algorithm.

        Args:
            file (str): file to register
            target_atlas (str): target atlas
            affine_file_path (str): path to the affine.mat file
            output_affine_subject_file_path (str): path to the output file

        Returns:
            str: apply affine command
        """

        command_apply_affine = (
            "/work/CaPTk/bin/install/appdir/usr/bin/greedy -d 3"
            + " -rf "
            + target_atlas
            + " -rm "
            + file
            + " "
            + output_affine_subject_file_path
            + " -r "
            + affine_file_path
        )

        # logging.info(
        #     f"Applying affine registration with the following command: {command_apply_affine}"
        # )
        return command_apply_affine

    def create_warp_command(
        self,
        file: str,
        target_atlas: str,
        affine_file_path: str,
        warp_file_path: str,
    ):
        """
        Creates the command for the greedy algorithm.

        Args:
            file (str): file to register
            target_atlas (str): target atlas
            affine_file_path (str): path to the affine.mat file
            warp_file_path (str): path to the warp.nii.gz file

        Returns:
            str: warp command
        """

        command_warp = (
            "/work/CaPTk/bin/install/appdir/usr/bin/greedy -d 3"
            + " -m "
            + self.metric
            + " -i "
            + target_atlas
            + " "
            + file
            + " -it "
            + affine_file_path
            + " -o "
            + warp_file_path
        )

        command_warp += (
            " -n "
            + str(self.max_iterations[0])
            + "x"
            + str(self.max_iterations[1])
            + "x"
            + str(self.max_iterations[2])
        )

        # logging.info(
        #     f"Creating deformable registration with the following command: {command_warp}"
        # )

        return command_warp

    def create_apply_warp_command(
        self,
        file: str,
        target_atlas: str,
        warp_file_path: str,
        affine_file_path: str,
        output_subject_file_path: str,
    ):
        """
        Creates the apply deformable command for the greedy algorithm.

        Args:
            file (str): file to register
            target_atlas (str): target atlas
            warp_file_path (str): path to the warp.nii.gz file
            affine_file_path (str): path to the affine.mat file
            output_subject_file_path (str): path to the output file

        Returns:
            str: apply warp command
        """

        command_apply_warp = (
            "/work/CaPTk/bin/install/appdir/usr/bin/greedy -d 3"
            + " -rf "
            + target_atlas
            + " -rm "
            + file
            + " "
            + output_subject_file_path
            + " -r "
            + warp_file_path
            + " "
            + affine_file_path
        )

        # logging.info(
        #     f"Applying deformable registration with the following command: {command_apply_warp}"
        # )

        return command_apply_warp
