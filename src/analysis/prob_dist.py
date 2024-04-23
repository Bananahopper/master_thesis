import glob
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import os
import logging
from analysis import ANALYSIS_FOLDER
from common.io.path_operations import (
    extract_srf_from_prob_dist_path,
    get_file_list_from_pattern,
)
from constants import MNI_ATLAS_PATH


class ProbDist:
    def __init__(
        self,
        dataset_name: str,
        labels=False,
        necrotic_core=None,
        enhancing_region=None,
        edema=None,
    ):

        self.dataset_name = dataset_name
        self.necrotic_core = necrotic_core
        self.enhancing_region = enhancing_region
        self.edema = edema
        self.labels = labels
        self.SAVE_PATH = os.path.join(ANALYSIS_FOLDER, f"{dataset_name}/prob_dist")

        if not os.path.exists(self.SAVE_PATH):
            os.makedirs(self.SAVE_PATH)

        logging.info(
            f"""Running ProbDist with the following parameters:
                     Dataset name: {self.dataset_name},
                     Labels: {self.labels},
                     Necrotic core: {self.necrotic_core},
                     Enhancing region: {self.enhancing_region},
                     Edema: {self.edema},
                     Save path: {self.SAVE_PATH}"""
        )

    def run(self, pattern: str):

        if not pattern.endswith("*_seg.nii.gz"):
            logging.error("Pattern must end with *_seg.nii.gz")
            return None

        file_list = get_file_list_from_pattern(pattern)
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
        result_array_necrotic_core = np.zeros(
            (sample_img.shape[0], sample_img.shape[1], sample_img.shape[2])
        )
        result_array_enhancing_region = np.zeros(
            (sample_img.shape[0], sample_img.shape[1], sample_img.shape[2])
        )
        result_array_edema = np.zeros(
            (sample_img.shape[0], sample_img.shape[1], sample_img.shape[2])
        )

        if self.labels == True:
            for file in file_list:

                logging.info(f"Processing file: {file}")

                # Whole tumor
                img = nib.load(file)
                data = img.get_fdata()
                # get binary mask
                data[data > 0] = 1

                result_array_whole_tumor += data

            for file in file_list:
                # Necrotic core
                img = nib.load(file)
                data = img.get_fdata()
                # Get necrotic core
                data = data == self.necrotic_core
                data[data > 0] = 1

                result_array_necrotic_core += data
            for file in file_list:
                # Enhancing region
                img = nib.load(file)
                data = img.get_fdata()
                # Get enhancing region
                data = data == self.enhancing_region
                data[data > 0] = 1

                result_array_enhancing_region += data
            for file in file_list:
                # Edema
                img = nib.load(file)
                data = img.get_fdata()
                # Get edema
                data = data == self.edema
                data[data > 0] = 1

                result_array_edema += data

        elif self.labels == False:
            for file in file_list:
                img = nib.load(file)
                data = img.get_fdata()
                # get binary mask
                data[data > 0] = 1

                result_array_whole_tumor += data

        logging.info(
            f"Max value in whole tumor: {max(result_array_whole_tumor.flatten())}"
        )

        if self.labels == True:
            self.save_result_as_nifti(
                result_array_whole_tumor,
                registration_modality,
                "whole_tumor",
                affine,
                header,
                extra,
                file_map,
            )
            self.save_result_as_nifti(
                result_array_necrotic_core,
                registration_modality,
                "necrotic_core",
                affine,
                header,
                extra,
                file_map,
            )
            self.save_result_as_nifti(
                result_array_enhancing_region,
                registration_modality,
                "enhancing_region",
                affine,
                header,
                extra,
                file_map,
            )
            self.save_result_as_nifti(
                result_array_edema,
                registration_modality,
                "edema",
                affine,
                header,
                extra,
                file_map,
            )
        elif self.labels == False:
            self.save_result_as_nifti(
                result_array_whole_tumor,
                registration_modality,
                "whole_tumor",
                affine,
                header,
                extra,
                file_map,
            )

        if self.labels == True:
            self.visualize_surface_plot(
                result_array_whole_tumor,
                registration_modality,
                "whole_tumor",
                self.dataset_name,
            )
            self.visualize_surface_plot(
                result_array_necrotic_core,
                registration_modality,
                "necrotic_core",
                self.dataset_name,
            )
            self.visualize_surface_plot(
                result_array_enhancing_region,
                registration_modality,
                "enhancing_region",
                self.dataset_name,
            )
            self.visualize_surface_plot(
                result_array_edema, registration_modality, "edema", self.dataset_name
            )
        elif self.labels == False:
            self.visualize_surface_plot(
                result_array_whole_tumor,
                registration_modality,
                "whole_tumor",
                self.dataset_name,
            )

    def save_result_as_nifti(
        self, result_array, registration_modality, name, affine, header, extra, file_map
    ):
        img = nib.Nifti1Image(result_array, affine, header, extra, file_map)

        logging.info(
            f"Saving to path: {self.SAVE_PATH}/{registration_modality}/probdist_{self.dataset_name}_{name}.nii"
        )

        if not os.path.exists(f"{self.SAVE_PATH}/{registration_modality}"):
            os.makedirs(f"{self.SAVE_PATH}/{registration_modality}")

        nib.save(
            img,
            f"{self.SAVE_PATH}/{registration_modality}/probdist_{self.dataset_name}_{name}.nii",
        )

    def visualize_surface_plot(
        self, result_array, registration_modality, name, dataset_name
    ):
        collapsed_array = np.sum(result_array, axis=2)
        collapsed_array_sum = sum(collapsed_array.flatten())
        collapsed_array_plot = collapsed_array / collapsed_array_sum
        collapsed_array_plot = collapsed_array_plot

        x = np.arange(0, collapsed_array.shape[1])
        y = np.arange(0, collapsed_array.shape[0])
        X, Y = np.meshgrid(x, y)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.plot_surface(X, Y, collapsed_array, cmap="viridis")

        ax.set_title(f"Collapsed Array Surface Plot - {name}")
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        ax.set_zlabel("Values (10^3)")

        if not os.path.exists(f"{self.SAVE_PATH}/{registration_modality}"):
            os.makedirs(f"{self.SAVE_PATH}/{registration_modality}")

        plt.savefig(
            f"{self.SAVE_PATH}/{registration_modality}/{dataset_name}_surface_plot_{name}.png"
        )
