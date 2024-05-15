import logging
import os
from src.common.debugging import check_sub_with_missing_files
from src.common.io.command_operations import run_commands
from src.common.io.path_operations import (
    create_registration_folder_for_subject_file_path,
    extract_subject_id_from_file_path,
    get_file_list_from_pattern,
)
from src.constants import AFFINE_NAME, INVERSE_WARP_NAME, WARP_NAME
from typing import List


class Registrator:
    """
    This class is used to register T1 images, and their tumor masks, to a normalized space atlas.
    """

    allowed_metrics = ["MI"]
    # allowed patch radius for arbitrary dimension
    allowed_patch_radius = [2]

    def __init__(
        self,
        target_atlas: str,
        target_cortical_atlas: str,
        target_subcortical_atlas: str,
        max_iterations: List[int] = [100, 50, 10],
        metric: str = "MI",
        patch_radius: List[int] = [2, 2, 2],
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
        if target_cortical_atlas[0] != os.path.sep:
            raise ValueError("Target is not an absolute path")
        if target_subcortical_atlas[0] != os.path.sep:
            raise ValueError("Target is not an absolute path")

        logging.info("Running greedy registration with the following parameters:")
        logging.info("Target: " + target_atlas)
        logging.info("Target cortical: " + target_cortical_atlas)
        logging.info("Target subcortical: " + target_subcortical_atlas)
        logging.info("Max iterations: " + str(max_iterations))
        logging.info("Metric: " + metric)
        logging.info("Patch radius: " + str(patch_radius))
        logging.info("Align image centers first: " + str(ia_image_centers))

        self.target = target_atlas
        self.target_cortical = target_cortical_atlas
        self.target_subcortical = target_subcortical_atlas
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

            sub_missing_modality = check_sub_with_missing_files(file_list, label_list)

            logging.error(
                f"The number of files and labels must be the same. Images: {len(file_list)}, Labels: {len(label_list)}. Missing modality or label in {sub_missing_modality}"
            )
            raise ValueError(
                f"The number of files and labels must be the same. Images: {len(file_list)}, Labels: {len(label_list)}. Missing modality or label in {sub_missing_modality}"
            )

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

        _, affine_folder, warp_folder, inverse_warp_folder = (
            create_registration_folder_for_subject_file_path(file)
        )

        output_subject_id, _, _ = extract_subject_id_from_file_path(file)
        output_affine_subject_file_path = os.path.join(
            affine_folder, output_subject_id + "_aff_reg_t1.nii.gz"
        )
        output_affine_subject_label_path = os.path.join(
            affine_folder, output_subject_id + "_aff_reg_seg.nii.gz"
        )
        output_deformable_subject_file_path = os.path.join(
            warp_folder, output_subject_id + "_def_reg_t1.nii.gz"
        )
        output_deformable_subject_label_file_path = os.path.join(
            warp_folder, output_subject_id + "_def_reg_seg.nii.gz"
        )
        output_inverse_deformable_subject_label_file_path_cort = os.path.join(
            inverse_warp_folder, output_subject_id + "_seg_reg_cort.nii.gz"
        )
        output_inverse_deformable_subject_label_file_path_sub = os.path.join(
            inverse_warp_folder, output_subject_id + "_seg_reg_sub.nii.gz"
        )

        commands_to_run = []

        affine_file_path = os.path.join(affine_folder, AFFINE_NAME)
        command_affine = self.create_affine_command(file, self.target, affine_file_path)
        command_apply_affine = self.create_apply_affine_command(
            file,
            self.target,
            affine_file_path,
            output_affine_subject_file_path,
            label,
            output_affine_subject_label_path,
        )
        affine_commands = [command_affine, command_apply_affine]

        warp_file_path = os.path.join(warp_folder, WARP_NAME)
        command_warp = self.create_warp_command(
            file, self.target, affine_file_path, warp_file_path
        )
        command_apply_warp = self.create_apply_warp_command(
            file,
            self.target,
            warp_file_path,
            affine_file_path,
            output_deformable_subject_file_path,
            label,
            output_deformable_subject_label_file_path,
        )
        deformable_commands = [command_warp, command_apply_warp]

        inverse_warp_file_path = os.path.join(inverse_warp_folder, INVERSE_WARP_NAME)
        command_inverse_warp = self.create_inverse_warp_command(
            file, self.target, affine_file_path, warp_file_path, inverse_warp_file_path
        )
        command_apply_inverse_warp_cort, command_apply_inverse_warp_sub = (
            self.create_apply_inverse_warp_command(
                file,
                self.target_cortical,
                self.target_subcortical,
                affine_file_path,
                inverse_warp_file_path,
                output_inverse_deformable_subject_label_file_path_cort,
                output_inverse_deformable_subject_label_file_path_sub,
            )
        )
        inverse_deformable_commands = [
            command_inverse_warp,
            command_apply_inverse_warp_cort,
            command_apply_inverse_warp_sub,
        ]

        commands_to_run.extend(affine_commands)
        commands_to_run.extend(deformable_commands)
        commands_to_run.extend(inverse_deformable_commands)

        run_commands(commands_to_run)

    def create_affine_command(
        self, source_file: str, target_file: str, affine_file_path: str
    ):
        """
        Creates the command for the greedy algorithm.

        Args:
            source_file (str): file to beq registered
            target_file (str): target file
            transformation_file_path (str): path to the transformation file

        Returns:
            str: affine command
        """
        command_affine = (
            "/work/CaPTk/bin/install/appdir/usr/bin/greedy -d 3 -a -i "
            + target_file
            + " "
            + source_file
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
        if self.ia_image_centers:
            command_affine += " -ia-image-centers "

        logging.info(
            "Calculating greedy registration with the following command: "
            + command_affine
        )
        return command_affine

    def create_apply_affine_command(
        self,
        source_file: str,
        target_file: str,
        affine_file_path: str,
        output_affine_subject_file_path: str,
        label_file: str,
        output_affine_subject_label_path: str,
    ):
        """
        Creates the command for the greedy algorithm.

        Args:
            source_file (str): file to be registered
            target_file (str): target file
            affine_file_path (str): path to the affine file
            output_file_path (str): path to the output file
            label_file (str): label file
            output_label_file_path (str): path to the output label file

        Returns:
            str: apply affine command
        """

        command_apply_affine = (
            "/work/CaPTk/bin/install/appdir/usr/bin/greedy -d 3"
            + " -rf "
            + target_file
            + " -rm "
            + source_file
            + " "
            + output_affine_subject_file_path
            + " -ri LABEL 0.2vox"
            + " -rm "
            + label_file
            + " "
            + output_affine_subject_label_path
            + " -r "
            + affine_file_path
        )

        logging.info(
            "Calculating greedy registration with the following command: "
            + command_apply_affine
        )
        return command_apply_affine

    def create_warp_command(
        self,
        source_file: str,
        target_file: str,
        affine_file_path: str,
        warp_file_path: str,
    ):
        """
        Creates the command for the greedy algorithm.

        Args:
            source_file (str): file to be registered
            target_file (str): target file
            affine_file_path (str): path to the affine file
            warp_file_path (str): path to the warp file

        Returns:
            str: warp command
        """

        command_warp = (
            "/work/CaPTk/bin/install/appdir/usr/bin/greedy -d 3"
            + " -m "
            + self.metric
            + " -i "
            + target_file
            + " "
            + source_file
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

        logging.info(
            "Calculating greedy registration with the following command: "
            + command_warp
        )

        return command_warp

    def create_apply_warp_command(
        self,
        source_file: str,
        target_file: str,
        warp_file_path: str,
        affine_file_path: str,
        output_subject_file_path: str,
        label_file: str,
        output_subject_label_path: str,
    ):
        """
        Creates the command for the greedy algorithm.

        Args:
            source_file (str): file to be registered
            target_file (str): target file
            warp_file_path (str): path to the warp file
            affine_file_path (str): path to the affine file
            output_file_path (str): path to the output file
            label_file (str): label file
            output_label_file_path (str): path to the output label file

        Returns:
            str: apply warp command
        """

        command_apply_warp = (
            "/work/CaPTk/bin/install/appdir/usr/bin/greedy -d 3"
            + " -rf "
            + target_file
            + " -rm "
            + source_file
            + " "
            + output_subject_file_path
            + " -ri LABEL 0.2vox"
            + " -rm "
            + label_file
            + " "
            + output_subject_label_path
            + " -r "
            + warp_file_path
            + " "
            + affine_file_path
        )

        logging.info(
            "Calculating greedy registration with the following command: "
            + command_apply_warp
        )
        return command_apply_warp

    def create_inverse_warp_command(
        self,
        source_file: str,
        target_file: str,
        affine_file_path: str,
        warp_file_path: str,
        inverse_warp_file_path: str,
    ):
        """
        Creates the inverse warp command for the greedy algorithm.

        Args:
            source_file (str): file to be registered
            target_file (str): target file
            warp_file_path (str): path to the warp file
            inverse_warp_file_path (str): path to the inverse warp file

        Returns:
            str: inverse warp command
        """

        command_inverse_warp = (
            "/work/CaPTk/bin/install/appdir/usr/bin/greedy -d 3"
            + " -m "
            + self.metric
            + " -i "
            + target_file
            + " "
            + source_file
            + " -it "
            + affine_file_path
            + " -o "
            + warp_file_path
            + " -oinv "
            + inverse_warp_file_path
            + " -sv"
        )

        command_inverse_warp += (
            " -n "
            + str(self.max_iterations[0])
            + "x"
            + str(self.max_iterations[1])
            + "x"
            + str(self.max_iterations[2])
        )

        logging.info(
            "Calculating greedy registration with the following command: "
            + command_inverse_warp
        )

        return command_inverse_warp

    def create_apply_inverse_warp_command(
        self,
        source_file: str,
        target_cortical_file: str,
        target_subcortical_file: str,
        affine_file_path: str,
        inverse_warp_file_path: str,
        output_subject_file_path_cort: str,
        output_subject_file_path_sub: str,
    ):
        """
        Creates the command for the greedy algorithm.

        Args:
            source_file (str): file to be registered
            target_file (str): target file
            inverse_warp_file_path (str): path to the inverse warp file
            affine_file_path (str): path to the affine file
            output_file_path (str): path to the output file
            label_file (str): label file
            output_label_file_path (str): path to the output label file

        Returns:
            str, str: apply inverse warp command
        """

        command_apply_inverse_warp_cort = (
            "/work/CaPTk/bin/install/appdir/usr/bin/greedy -d 3"
            + " -rf "
            + source_file
            + " -ri LABEL 0.2vox"
            + " -rm "
            + target_cortical_file
            + " "
            + output_subject_file_path_cort
            + " -r "
            + affine_file_path
            + ",-1 "
            + inverse_warp_file_path
        )

        command_apply_inverse_warp_sub = (
            "/work/CaPTk/bin/install/appdir/usr/bin/greedy -d 3"
            + " -rf "
            + source_file
            + " -ri LABEL 0.2vox"
            + " -rm "
            + target_subcortical_file
            + " "
            + output_subject_file_path_sub
            + " -r "
            + affine_file_path
            + ",-1 "
            + inverse_warp_file_path
        )

        logging.info(
            "Calculating greedy registration with the following command: "
            + command_apply_inverse_warp_cort
        )

        logging.info(
            "Calculating greedy registration with the following command: "
            + command_apply_inverse_warp_sub
        )
        return command_apply_inverse_warp_cort, command_apply_inverse_warp_sub
