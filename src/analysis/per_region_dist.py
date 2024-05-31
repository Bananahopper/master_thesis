import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import numpy as np
import logging
from src.constants.utils import get_edema_value
from src.analysis.utils.utils import pad_or_trim_to_match
from src.common.io.path_operations import (
    extract_subject_id_from_file_path,
    get_file_list_from_pattern,
)
from src.analysis import ANALYSIS_FOLDER, ANALYSIS_FOLDER_CAPTK
from src.constants.analysis__constants.cort_sub_labels import CORT_LABELS, SUB_LABELS


class PerRegionDist:
    """
    This class calculates the tumor per region distribution for the cortical and subcortical regions. Depending on the mode, the distribution can be calculated as the tumor in region / total tumor or tumor in region / total region.
    """

    def __init__(self, mode: int):

        if not os.path.exists(ANALYSIS_FOLDER_CAPTK):
            os.makedirs(ANALYSIS_FOLDER_CAPTK)

        self.mode = int(mode)

    def process(self, original_seg: str, cortical_seg: str, subcortical_seg: str):

        try:
            original_seg_list = get_file_list_from_pattern(original_seg)
            cortical_seg_list = get_file_list_from_pattern(cortical_seg)
            subcortical_seg_list = get_file_list_from_pattern(subcortical_seg)
        except:
            logging.error("Error getting file list from pattern.")
            return

        self.edema = get_edema_value(original_seg_list[0])

        if len(original_seg_list) != len(cortical_seg_list) or len(
            original_seg_list
        ) != len(subcortical_seg_list):
            logging.error(
                "Number of original, cortical and subcortical images do not match."
            )
            logging.error(
                f"Number of original images: {len(original_seg_list)}, Number of cortical images: {len(cortical_seg_list)}, Number of subcortical images: {len(subcortical_seg_list)}"
            )

        for original_seg_file, cortical_seg_file, subcortical_seg_file in zip(
            original_seg_list, cortical_seg_list, subcortical_seg_list
        ):

            print(original_seg_file)
            print(cortical_seg_file)
            print(subcortical_seg_file)

            logging.info(f"Processing {original_seg_file}")

            patient_id, _, dataset_name = extract_subject_id_from_file_path(
                original_seg_file
            )

            if os.path.exists(ANALYSIS_FOLDER_CAPTK):
                save_folder = os.path.join(
                    ANALYSIS_FOLDER_CAPTK, dataset_name, "per_region_dist"
                )
            else:
                save_folder = os.path.join(
                    ANALYSIS_FOLDER, dataset_name, "per_region_dist"
                )
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)

            subject_folder = os.path.join(save_folder, patient_id)
            if not os.path.exists(subject_folder):
                os.makedirs(subject_folder)

            original_seg_data, cortical_seg_data, subcortical_seg_data = (
                self.convert_data_to_nib_data(
                    original_seg_file, cortical_seg_file, subcortical_seg_file
                )
            )

            tumor_per_region_cortical, tumor_per_region_subcortical = (
                self.get_tumor_per_region(
                    original_seg_data, cortical_seg_data, subcortical_seg_data
                )
            )

            self.save_data(
                subject_folder,
                patient_id,
                tumor_per_region_cortical,
                tumor_per_region_subcortical,
            )

    def convert_data_to_nib_data(
        self, original_seg_file, cortical_seg_file, subcortical_seg_file
    ):

        original_seg = nib.load(original_seg_file)
        cortical_seg = nib.load(cortical_seg_file)
        subcortical_seg = nib.load(subcortical_seg_file)

        original_seg_data = original_seg.get_fdata().astype(np.int16)
        original_seg_data[original_seg_data == self.edema] = 0
        original_seg_data[original_seg_data > 0] = 1
        cortical_seg_data = cortical_seg.get_fdata().astype(np.int16)
        subcortical_seg_data = subcortical_seg.get_fdata().astype(np.int16)

        return original_seg_data, cortical_seg_data, subcortical_seg_data

    def get_tumor_per_region(
        self, original_seg_data, cortical_seg_data, subcortical_seg_data
    ):
        logging.info("Calculating tumor per region")

        # Get the unique values in the segmentation data and convert to int
        cort_values = list(set(cortical_seg_data.flatten()))
        cort_values = [int(x) for x in cort_values]
        subcort_values = list(set(subcortical_seg_data.flatten()))
        subcort_values = [int(x) for x in subcort_values]

        # Filter out regions that are not contained in the image
        cort_labels = [CORT_LABELS[i] for i in cort_values]
        sub_labels = [SUB_LABELS[i] for i in subcort_values]

        # Create a dictionary to store the values and their corresponding labels
        cort_dict = {"Values": cort_values, "Labels": cort_labels}
        subcort_dict = {"Values": subcort_values, "Labels": sub_labels}

        # Check if dataframe is valid
        try:
            cort_df = pd.DataFrame(cort_dict)
            sub_df = pd.DataFrame(subcort_dict)
        except ValueError as e:
            logging.error(f"Error creating DataFrames: {str(e)}")
            return None, None

        # Get tumor in region / total tumor

        for region in cort_values:
            region_mask = np.zeros_like(original_seg_data)

            if region_mask.shape != cortical_seg_data.shape:

                logging.info("Shapes do not match. Padding or trimming.")
                logging.info(f"Region mask before cut: {region_mask.shape}")
                logging.info(f"Cortical seg data before cut: {cortical_seg_data.shape}")
                print("Shapes do not match. Padding or trimming.")
                print(f"Region mask before cut: {region_mask.shape}")
                print(f"Cortical seg data before cut: {cortical_seg_data.shape}")

                cortical_seg_data = pad_or_trim_to_match(
                    region_mask, cortical_seg_data, [8, 13]
                )

            print(f"Region mask after cut : {region_mask.shape}")
            print(f"Cortical seg data after cut : {cortical_seg_data.shape}")

            region_mask[cortical_seg_data == region] = 1
            tumor_overlap = original_seg_data * region_mask
            sum_tumor_overlap = np.sum(tumor_overlap)

            if self.mode == 1:
                sum_tumor = np.sum(original_seg_data)
                # Append to dataframe
                cort_df.loc[cort_df["Values"] == region, "Tumor in region"] = (
                    sum_tumor_overlap / sum_tumor
                )
            elif self.mode == 2:
                sum_region = np.sum(region_mask)
                # Append to dataframe
                cort_df.loc[cort_df["Values"] == region, "Tumor in region"] = (
                    sum_tumor_overlap / sum_region
                )

        for region in subcort_values:
            region_mask = np.zeros_like(original_seg_data)

            if region_mask.shape != subcortical_seg_data.shape:

                subcortical_seg_data = pad_or_trim_to_match(
                    region_mask, subcortical_seg_data, [8, 13]
                )

            region_mask[subcortical_seg_data == region] = 1
            tumor_overlap = original_seg_data * region_mask
            sum_tumor_overlap = np.sum(tumor_overlap)

            if self.mode == 1:
                sum_tumor = np.sum(original_seg_data)
                # Append to dataframe
                sub_df.loc[sub_df["Values"] == region, "Tumor in region"] = (
                    sum_tumor_overlap / sum_tumor
                )
            elif self.mode == 2:
                sum_region = np.sum(region_mask)
                # Append to dataframe
                sub_df.loc[sub_df["Values"] == region, "Tumor in region"] = (
                    sum_tumor_overlap / sum_region
                )

        return cort_df, sub_df

    def save_data(
        self,
        subject_folder,
        patient_id,
        tumor_per_region_cortical,
        tumor_per_region_subcortical,
    ):

        logging.info(f"Saving data to: {subject_folder}")

        # Save the data
        tumor_per_region_cortical.to_csv(
            subject_folder + f"/{patient_id}_cortical.csv",
            index=False,
        )
        tumor_per_region_subcortical.to_csv(
            subject_folder + f"/{patient_id}_subcortical.csv",
            index=False,
        )
