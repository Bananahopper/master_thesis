import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import glob
import tqdm
import numpy as np
from multiprocessing import Pool
import logging
from src.common.io.path_operations import (
    extract_file_name_from_path,
    extract_subject_id_from_file_path,
    get_file_list_from_pattern,
)
from src.analysis import ANALYSIS_FOLDER_CAPTK
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

            logging.info(f"Processing {original_seg_file}")

            patient_id, _, dataset_name = extract_subject_id_from_file_path(
                original_seg_file
            )

            save_folder = os.path.join(
                ANALYSIS_FOLDER_CAPTK, dataset_name, "per_region_dist"
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

        logging.info(f"Cortical labels: {cort_labels}")
        logging.info(f"Subcortical labels: {sub_labels}")
        logging.info(f"Cortical values: {cort_values}")
        logging.info(f"Subcortical values: {subcort_values}")

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

        if self.mode == 1:
            for region in cort_values:
                region_mask = np.zeros_like(original_seg_data)
                region_mask[cortical_seg_data == region] = 1
                tumor_overlap = original_seg_data * region_mask
                sum_tumor = np.sum(original_seg_data)
                sum_tumor_overlap = np.sum(tumor_overlap)
                # Append to dataframe
                cort_df.loc[cort_df["Values"] == region, "Tumor in region"] = (
                    sum_tumor_overlap / sum_tumor
                )

            for region in subcort_values:
                region_mask = np.zeros_like(original_seg_data)
                region_mask[subcortical_seg_data == region] = 1
                tumor_overlap = original_seg_data * region_mask
                sum_tumor = np.sum(original_seg_data)
                sum_tumor_overlap = np.sum(tumor_overlap)
                # Append to dataframe
                sub_df.loc[sub_df["Values"] == region, "Tumor in region"] = (
                    sum_tumor_overlap / sum_tumor
                )

            return cort_df, sub_df

        # Get tumor in region / total region
        elif self.mode == 2:
            for region in cort_values:
                region_mask = np.zeros_like(original_seg_data)
                region_mask[cortical_seg_data == region] = 1
                tumor_overlap = original_seg_data * region_mask
                sum_region = np.sum(region_mask)
                sum_tumor_overlap = np.sum(tumor_overlap)
                # Append to dataframe
                cort_df.loc[cort_df["Values"] == region, "Tumor in region"] = (
                    sum_tumor_overlap / sum_region
                )

            for region in subcort_values:
                region_mask = np.zeros_like(original_seg_data)
                region_mask[subcortical_seg_data == region] = 1
                tumor_overlap = original_seg_data * region_mask
                sum_region = np.sum(region_mask)
                sum_tumor_overlap = np.sum(tumor_overlap)
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
        # Save the data
        tumor_per_region_cortical.to_csv(
            subject_folder + f"/{patient_id}_cortical.csv",
            index=False,
        )
        tumor_per_region_subcortical.to_csv(
            subject_folder + f"/{patient_id}_subcortical.csv",
            index=False,
        )


# class PerRegionDist:
#     def __init__(self, name: str, mode: int, basedir: str):

#         self.name = name
#         self.mode = mode
#         self.basedir = basedir

#         self.SAVE_PATH = os.path.join(ANALYSIS_FOLDER_CAPTK, "per_region_dist")
#         if not os.path.exists(self.SAVE_PATH):
#             os.makedirs(self.SAVE_PATH)

#     def process(self):
#         logging.info(f"Processing {self.name} data")
#         # Get the data
#         basedir = os.listdir(self.basedir)
#         basedir.sort()

#         origdir = os.listdir("/scratch/users/ggaspar/CaPTk/datasets/BraTS2021_wTumor")
#         origdir.sort()

#         basedir = zip(basedir, origdir)
#         # Create a pool of worker processes
#         pool = Pool()

#         # Process the data in parallel with progress bar

#         results = list(
#             tqdm.tqdm(
#                 pool.starmap(self.process_subdir, [(subdir,) for subdir in basedir]),
#                 total=len(basedir),
#             )
#         )

#         # Close the pool
#         pool.close()
#         pool.join()

#     def process_subdir(self, subdir):
#         subdir_path = os.path.join(self.basedir, subdir)


#         print(subdir_path)

#         # Extract patient number from the subdirectory name

#         patient_number = extract_file_name_from_path(subdir_path)

#         os.makedirs(self.SAVE_PATH + f"/patient_{patient_number}", exist_ok=True)
#         logging.info(f"Processing subdirectory: {subdir_path}")

#         # Get the data
#         original_seg_data, cortical_seg_data, subcortical_seg_data = self.get_data(
#             subdir_path
#         )

#         if (
#             original_seg_data is None
#             or cortical_seg_data is None
#             or subcortical_seg_data is None
#         ):
#             logging.warning(
#                 f"Skipping subdirectory due to missing or invalid data: {subdir_path}"
#             )
#             return

#         logging.info(f"Data loaded successfully for subdirectory: {subdir_path}")
#         logging.info(f"Original segmentation data shape: {original_seg_data.shape}")
#         logging.info(f"Cortical segmentation data shape: {cortical_seg_data.shape}")
#         logging.info(
#             f"Subcortical segmentation data shape: {subcortical_seg_data.shape}"
#         )

#         # Get the tumor per region
#         tumor_per_region_cortical, tumor_per_region_subcortical = (
#             self.get_tumor_per_region(
#                 original_seg_data, cortical_seg_data, subcortical_seg_data
#             )
#         )

#         if tumor_per_region_cortical is None or tumor_per_region_subcortical is None:
#             logging.warning(
#                 f"Skipping subdirectory due to error in tumor per region calculation: {subdir_path}"
#             )
#             return

#         logging.info(
#             f"Tumor per region calculated successfully for subdirectory: {subdir_path}"
#         )

#         # Save the data
#         self.save_data(
#             self.name,
#             patient_number,
#             tumor_per_region_cortical,
#             tumor_per_region_subcortical,
#         )

#     def get_data(self, subdir):
#         # Construct the file path patterns
#         original_seg_pattern = os.path.join(subdir, "affine", "*_aff_reg_seg.nii.gz")
#         cortical_seg_pattern = os.path.join(
#             subdir, "inverse_warp", "*_seg_reg_cort.nii.gz"
#         )
#         subcortical_seg_pattern = os.path.join(
#             subdir, "inverse_warp", "*_seg_reg_sub.nii.gz"
#         )

#         # Find the file paths using glob.glob()
#         original_seg_paths = glob.glob(original_seg_pattern)
#         cortical_seg_paths = glob.glob(cortical_seg_pattern)
#         subcortical_seg_paths = glob.glob(subcortical_seg_pattern)

#         # Check if the required files exist
#         if not original_seg_paths:
#             logging.warning(
#                 f"Original segmentation file not found: {original_seg_pattern}"
#             )
#             return None, None, None
#         if not cortical_seg_paths:
#             logging.warning(
#                 f"Cortical segmentation file not found: {cortical_seg_pattern}"
#             )
#             return None, None, None
#         if not subcortical_seg_paths:
#             logging.warning(
#                 f"Subcortical segmentation file not found: {subcortical_seg_pattern}"
#             )
#             return None, None, None

#         try:
#             # Load the NIfTI files
#             original_seg = nib.load(original_seg_paths[0])
#             cortical_seg = nib.load(cortical_seg_paths[0])
#             subcortical_seg = nib.load(subcortical_seg_paths[0])

#             # Get the data and convert to appropriate data type
#             original_seg_data = original_seg.get_fdata().astype(np.int16)
#             original_seg_data[original_seg_data > 0] = 1
#             cortical_seg_data = cortical_seg.get_fdata().astype(np.int16)
#             subcortical_seg_data = subcortical_seg.get_fdata().astype(np.int16)

#             # Check if the data shapes match
#             if (
#                 original_seg_data.shape != cortical_seg_data.shape
#                 or original_seg_data.shape != subcortical_seg_data.shape
#             ):
#                 logging.warning(f"Data shapes do not match for files in {subdir}")
#                 return None, None, None

#             return original_seg_data, cortical_seg_data, subcortical_seg_data

#         except Exception as e:
#             logging.error(f"Error loading files in {subdir}: {str(e)}")
#             return None, None, None

#     def get_tumor_per_region(
#         self, original_seg_data, cortical_seg_data, subcortical_seg_data
#     ):
#         logging.info("Calculating tumor per region")

#         # Get the unique values in the segmentation data and convert to int
#         cort_values = list(set(cortical_seg_data.flatten()))
#         cort_values = [int(x) for x in cort_values]
#         subcort_values = list(set(subcortical_seg_data.flatten()))
#         subcort_values = [int(x) for x in subcort_values]

#         # Filter out regions that are not contained in the image
#         cort_labels = [CORT_LABELS[i] for i in cort_values]
#         sub_labels = [SUB_LABELS[i] for i in subcort_values]

#         logging.info(f"Cortical labels: {cort_labels}")
#         logging.info(f"Subcortical labels: {sub_labels}")
#         logging.info(f"Cortical values: {cort_values}")
#         logging.info(f"Subcortical values: {subcort_values}")

#         # Create a dictionary to store the values and their corresponding labels
#         cort_dict = {"Values": cort_values, "Labels": cort_labels}
#         subcort_dict = {"Values": subcort_values, "Labels": sub_labels}

#         # Check if dataframe is valid
#         try:
#             cort_df = pd.DataFrame(cort_dict)
#             sub_df = pd.DataFrame(subcort_dict)
#         except ValueError as e:
#             logging.error(f"Error creating DataFrames: {str(e)}")
#             return None, None

#         logging.info("DataFrames created successfully")

#         # Get tumor in region / total tumor
#         if self.mode == 1:
#             for region in cort_values:
#                 region_mask = np.zeros_like(original_seg_data)
#                 region_mask[cortical_seg_data == region] = 1
#                 tumor_overlap = original_seg_data * region_mask
#                 sum_tumor = np.sum(original_seg_data)
#                 sum_tumor_overlap = np.sum(tumor_overlap)
#                 # Append to dataframe
#                 cort_df.loc[cort_df["Values"] == region, "Tumor in region"] = (
#                     sum_tumor_overlap / sum_tumor
#                 )

#             for region in subcort_values:
#                 region_mask = np.zeros_like(original_seg_data)
#                 region_mask[subcortical_seg_data == region] = 1
#                 tumor_overlap = original_seg_data * region_mask
#                 sum_tumor = np.sum(original_seg_data)
#                 sum_tumor_overlap = np.sum(tumor_overlap)
#                 # Append to dataframe
#                 sub_df.loc[sub_df["Values"] == region, "Tumor in region"] = (
#                     sum_tumor_overlap / sum_tumor
#                 )

#             return cort_df, sub_df

#         # Get tumor in region / total region
#         elif self.mode == 2:
#             for region in cort_values:
#                 region_mask = np.zeros_like(original_seg_data)
#                 region_mask[cortical_seg_data == region] = 1
#                 tumor_overlap = original_seg_data * region_mask
#                 sum_region = np.sum(region_mask)
#                 sum_tumor_overlap = np.sum(tumor_overlap)
#                 # Append to dataframe
#                 cort_df.loc[cort_df["Values"] == region, "Tumor in region"] = (
#                     sum_tumor_overlap / sum_region
#                 )

#             for region in subcort_values:
#                 region_mask = np.zeros_like(original_seg_data)
#                 region_mask[subcortical_seg_data == region] = 1
#                 tumor_overlap = original_seg_data * region_mask
#                 sum_region = np.sum(region_mask)
#                 sum_tumor_overlap = np.sum(tumor_overlap)
#                 # Append to dataframe
#                 sub_df.loc[sub_df["Values"] == region, "Tumor in region"] = (
#                     sum_tumor_overlap / sum_region
#                 )

#             return cort_df, sub_df

#     def save_data(
#         self,
#         names,
#         counter,
#         tumor_per_region_cortical,
#         tumor_per_region_subcortical,
#     ):
#         # Save the data
#         tumor_per_region_cortical.to_csv(
#             self.SAVE_PATH
#             + f"/patient_{counter}/df_patient_{counter}_{names}_cortical.csv",
#             index=False,
#         )
#         tumor_per_region_subcortical.to_csv(
#             self.SAVE_PATH
#             + f"/patient_{counter}/df_patient_{counter}_{names}_subcortical.csv",
#             index=False,
#         )

#         logging.info(f"Data saved successfully for patient {counter}")
