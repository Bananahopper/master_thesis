import glob
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import os
import logging
from analysis import ANALYSIS_FOLDER, ANALYSIS_FOLDER_CAPTK
from common.io.path_operations import (
    extract_srf_from_prob_dist_path,
    get_file_list_from_pattern,
)
from constants import MNI_ATLAS_PATH
from src.constants.utils import get_edema_value


class ProbDist:
    def __init__(
        self,
        dataset_name: str,
        whole_tumor: bool,
    ):

        self.dataset_name = dataset_name
        self.whole_tumor = whole_tumor
        self.SAVE_PATH = os.path.join(
            ANALYSIS_FOLDER_CAPTK, f"{dataset_name}/prob_dist"
        )

        if not os.path.exists(self.SAVE_PATH):
            os.makedirs(self.SAVE_PATH)

        logging.info(
            f"""Running ProbDist with the following parameters:
                     Dataset name: {self.dataset_name},
                     Whole tumor: {self.whole_tumor},
                     Save path: {self.SAVE_PATH}"""
        )

    def run(self, pattern: str):

        if not pattern.endswith("*_seg.nii.gz"):
            logging.error("Pattern must end with *_seg.nii.gz")
            return None

        file_list = get_file_list_from_pattern(pattern)
        self.edema = get_edema_value(file_list[0])
        _, _, registration_modality, _ = extract_srf_from_prob_dist_path(file_list[0])

        self.process_data(file_list, registration_modality)

    def process_data(self, file_list: list, registration_modality: str):

        # Get the affine matrix
        sample = MNI_ATLAS_PATH
        sample_img = nib.load(sample)
        affine = sample_img.affine
        header = sample_img.header
        extra = sample_img.extra
        file_map = sample_img.file_map

        # Initialize result arrays
        result_array_whole_tumor = np.zeros(
            (sample_img.shape[0], sample_img.shape[1], sample_img.shape[2])
        )

        if self.whole_tumor == True:
            for file in file_list:
                img = nib.load(file)
                data = img.get_fdata()
                # get binary mask
                data[data > 0] = 1

                result_array_whole_tumor += data

        else:
            for file in file_list:
                img = nib.load(file)
                data = img.get_fdata()

                try:
                    if self.edema != None:
                        data[data == self.edema] = 0
                except:
                    logging.error(
                        "Edema has to have a value to run when whole_tumor = False."
                    )
                    return None

                data[data > 0] = 1

                result_array_whole_tumor += data

        logging.info(
            f"Max value in whole tumor: {max(result_array_whole_tumor.flatten())}"
        )

        self.save_result_as_nifti(
            result_array_whole_tumor,
            registration_modality,
            affine,
            header,
            extra,
            file_map,
        )

        result_probability_mask_whole_tumor = self.create_tumor_probability_mask(
            result_array_whole_tumor
        )

        self.save_result_as_nifti(
            result_probability_mask_whole_tumor,
            registration_modality,
            affine,
            header,
            extra,
            file_map,
            probability_mask=True,
        )

        len_files = len(file_list)

        self.visualize_surface_plot(
            result_array_whole_tumor,
            registration_modality,
            self.dataset_name,
            len_files,
        )

    def save_result_as_nifti(
        self,
        result_array,
        registration_modality,
        affine,
        header,
        extra,
        file_map,
        probability_mask=False,
    ):
        img = nib.Nifti2Image(result_array, affine, header, extra, file_map)

        if not os.path.exists(f"{self.SAVE_PATH}/{registration_modality}"):
            os.makedirs(f"{self.SAVE_PATH}/{registration_modality}")

        if self.whole_tumor == True:
            nib.save(
                img,
                f"{self.SAVE_PATH}/{registration_modality}/probdist_{self.dataset_name}_whole_tumor.nii",
            )
            if probability_mask == True:
                nib.save(
                    img,
                    f"{self.SAVE_PATH}/{registration_modality}/probdist_{self.dataset_name}_whole_tumor_probability_mask.nii",
                )

            logging.info(
                f"Saving to path: {self.SAVE_PATH}/{registration_modality}/probdist_{self.dataset_name}_whole_tumor.nii"
            )
        else:
            nib.save(
                img,
                f"{self.SAVE_PATH}/{registration_modality}/probdist_{self.dataset_name}.nii",
            )
            if probability_mask == True:
                nib.save(
                    img,
                    f"{self.SAVE_PATH}/{registration_modality}/probdist_{self.dataset_name}_probability_mask.nii",
                )

            logging.info(
                f"Saving to path: {self.SAVE_PATH}/{registration_modality}/probdist_{self.dataset_name}.nii"
            )

    def create_tumor_probability_mask(self, result_array):
        result_probability_mask_array = result_array / np.sum(result_array)

        mask = (result_probability_mask_array >= 0) & (
            result_probability_mask_array <= 0.5
        )

        result_probability_mask = result_probability_mask_array[mask]

        return result_probability_mask

    def visualize_surface_plot(
        self, result_array, registration_modality, dataset_name, len_files
    ):
        collapsed_array = np.sum(result_array, axis=2)
        collapsed_array_sum = len_files
        collapsed_array_plot = collapsed_array / collapsed_array_sum
        collapsed_array_plot = collapsed_array_plot

        x = np.arange(0, collapsed_array.shape[1])
        y = np.arange(0, collapsed_array.shape[0])
        X, Y = np.meshgrid(x, y)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.plot_surface(X, Y, collapsed_array, cmap="viridis")

        ax.set_title(
            f"Collapsed Array Surface Plot - {self.dataset_name} - {'whole_tumor' if self.whole_tumor == True else 'no_edema'}"
        )
        ax.set_xlabel("Left View")
        ax.set_ylabel("Posterior View")
        ax.set_zlabel("Values")

        if not os.path.exists(f"{self.SAVE_PATH}/{registration_modality}"):
            os.makedirs(f"{self.SAVE_PATH}/{registration_modality}")

        if self.whole_tumor == True:
            plt.savefig(
                f"{self.SAVE_PATH}/{registration_modality}/{dataset_name}_surface_plot_whole_tumor.png"
            )
        else:
            plt.savefig(
                f"{self.SAVE_PATH}/{registration_modality}/{dataset_name}_surface_plot.png"
            )
