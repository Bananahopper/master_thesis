import os
from typing import List

# from tqdm import tqdm
import argparse
from src.analysis import WORK_PATH
from src.common.io.command_operations import run_commands
from src.common.io.path_operations import get_file_list_from_pattern


class ConnectomeRegistrator:
    def __init__(
        self,
        target_atlas: str,
        max_iterations: List[int] = [100, 50, 10],
        metric: str = "MI",
        patch_radius: List[int] = [2, 2, 2],
        ia_image_centers: bool = True,
    ):

        self.target_atlas = target_atlas
        self.max_iterations = max_iterations
        self.metric = metric
        self.patch_radius = patch_radius
        self.ia_image_centers = ia_image_centers

    def run(self, source: str, label: str, patient_id_number: int):

        file_list = get_file_list_from_pattern(source)
        label_list = get_file_list_from_pattern(label)

        print(file_list[0])

        for idx, (file, label) in enumerate(zip(file_list, label_list)):
            self.register(file, label, patient_id_number)

    def register(self, source: str, label: str, patient_id_number: int):

        registration_folder, affine_folder, warp_folder, subject_id = (
            self.create_folder_structure(source, patient_id_number)
        )

        patient_output_t1_affine = os.path.join(
            registration_folder, subject_id + "_connectome_aff_reg_t1.nii.gz"
        )
        patient_output_label_affine = os.path.join(
            registration_folder, subject_id + "_connectome_aff_reg_label.nii.gz"
        )

        patient_output_t1_warp = os.path.join(
            registration_folder, subject_id + "_connectome_warp_reg_t1.nii.gz"
        )
        patient_output_label_warp = os.path.join(
            registration_folder, subject_id + "_connectome_warp_reg_label.nii.gz"
        )

        affine_file = os.path.join(affine_folder, "affine.mat")
        warp_file = os.path.join(warp_folder, "warp.nii.gz")

        commands_to_run = []

        affine_command = self.create_affine_command(
            source, self.target_atlas, affine_file
        )
        apply_affine_command = self.create_apply_affine_command(
            source,
            self.target_atlas,
            affine_file,
            patient_output_t1_affine,
            label,
            patient_output_label_affine,
        )
        affine_commands = [affine_command, apply_affine_command]

        warp_command = self.create_warp_command(
            source, self.target_atlas, affine_file, warp_file
        )
        apply_warp_command = self.create_apply_warp_command(
            source,
            self.target_atlas,
            warp_file,
            affine_file,
            patient_output_t1_warp,
            label,
            patient_output_label_warp,
        )
        warp_commands = [warp_command, apply_warp_command]

        commands_to_run.extend(affine_commands)
        commands_to_run.extend(warp_commands)

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

        return command_apply_warp

    def create_folder_structure(self, source: str, patient_id_number: int):

        connectome_output_folder = os.path.join(
            WORK_PATH, "output_registration_connectome"
        )
        if not os.path.exists(connectome_output_folder):
            os.makedirs(connectome_output_folder)

        dataset_name = source.split("/")[1]
        subject_id = source.split("/")[-patient_id_number]

        registration_folder = os.path.join(
            connectome_output_folder, dataset_name, subject_id
        )
        if not os.path.exists(registration_folder):
            os.makedirs(registration_folder)

        affine_folder = os.path.join(registration_folder, "affine")
        if not os.path.exists(affine_folder):
            os.makedirs(affine_folder)

        warp_folder = os.path.join(registration_folder, "warp")
        if not os.path.exists(warp_folder):
            os.makedirs(warp_folder)

        return registration_folder, affine_folder, warp_folder, subject_id


def main(source, label, target_atlas, patient_id_number):
    registrator = ConnectomeRegistrator(target_atlas)
    registrator.run(source, label, patient_id_number)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Register connectome data")
    parser.add_argument(
        "--source", type=str, required=True, help="Pattern for source files"
    )
    parser.add_argument(
        "--label", type=str, required=True, help="Pattern for label files"
    )
    parser.add_argument(
        "--target_atlas", type=str, required=True, help="Target atlas file"
    )
    parser.add_argument(
        "--patient_id_number",
        type=int,
        help="Number of folders to go back to get the patient id",
    )

    args = parser.parse_args()

    main(args.source, args.label, args.target_atlas, args.patient_id_number)
