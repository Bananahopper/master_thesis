import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import glob
import argparse
import tqdm
from multiprocessing import Pool
import logging
import re

# Configure logging
logging.basicConfig(filename='tumor_per_region.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class tumor_per_region():
    def __init__(self,
                 dir: str,
                 name: str,
                 save_path: str,
                 mode: int):

        self.dir = dir
        self.name = name
        self.save_path = save_path
        self.mode = mode

    def process(self):
        print("Processing data")
        # Get the data
        basedir = os.listdir(self.dir)
        
        # Create a pool of worker processes
        pool = Pool()
        
        # Process the data in parallel with progress bar
        results = list(tqdm.tqdm(pool.starmap(self.process_subdir, [(subdir,) for subdir in basedir]), total=len(basedir)))
        
        # Close the pool
        pool.close()
        pool.join()

    def process_subdir(self, subdir):
        subdir_path = os.path.join(self.dir, subdir)

        # Extract patient number from the subdirectory name
        pattern = r"/(?P<number>\d+)"
        patient_number = re.findall(pattern, subdir_path)
        patient_number = patient_number[0]


        os.makedirs(self.save_path + f"/patient_{patient_number}", exist_ok=True)
        logging.info(f"Processing subdirectory: {subdir_path}")

        # Get the data
        original_seg_data, cortical_seg_data, subcortical_seg_data = self.get_data(subdir_path)

        if original_seg_data is None or cortical_seg_data is None or subcortical_seg_data is None:
            logging.warning(f"Skipping subdirectory due to missing or invalid data: {subdir_path}")
            return

        logging.info(f"Data loaded successfully for subdirectory: {subdir_path}")
        logging.info(f"Original segmentation data shape: {original_seg_data.shape}")
        logging.info(f"Cortical segmentation data shape: {cortical_seg_data.shape}")
        logging.info(f"Subcortical segmentation data shape: {subcortical_seg_data.shape}")

        # Get the tumor per region
        tumor_per_region_cortical, tumor_per_region_subcortical = self.get_tumor_per_region(original_seg_data, cortical_seg_data, subcortical_seg_data)

        if tumor_per_region_cortical is None or tumor_per_region_subcortical is None:
            logging.warning(f"Skipping subdirectory due to error in tumor per region calculation: {subdir_path}")
            return

        logging.info(f"Tumor per region calculated successfully for subdirectory: {subdir_path}")

        # Save the data
        self.save_data(self.save_path, self.name, patient_number, tumor_per_region_cortical, tumor_per_region_subcortical)

    def get_data(self, subdir):
        # Construct the file path patterns
        original_seg_pattern = os.path.join(subdir, "*_seg.nii.gz")
        cortical_seg_pattern = os.path.join(subdir, "*_cort.nii.gz")
        subcortical_seg_pattern = os.path.join(subdir, "*_sub.nii.gz")

        # Find the file paths using glob.glob()
        original_seg_paths = glob.glob(original_seg_pattern)
        cortical_seg_paths = glob.glob(cortical_seg_pattern)
        subcortical_seg_paths = glob.glob(subcortical_seg_pattern)

        # Check if the required files exist
        if not original_seg_paths:
            logging.warning(f"Original segmentation file not found: {original_seg_pattern}")
            return None, None, None
        if not cortical_seg_paths:
            logging.warning(f"Cortical segmentation file not found: {cortical_seg_pattern}")
            return None, None, None
        if not subcortical_seg_paths:
            logging.warning(f"Subcortical segmentation file not found: {subcortical_seg_pattern}")
            return None, None, None

        try:
            # Load the NIfTI files
            original_seg = nib.load(original_seg_paths[0])
            cortical_seg = nib.load(cortical_seg_paths[0])
            subcortical_seg = nib.load(subcortical_seg_paths[0])

            # Get the data and convert to appropriate data type
            original_seg_data = original_seg.get_fdata().astype(np.int16)
            original_seg_data[original_seg_data > 0] = 1
            cortical_seg_data = cortical_seg.get_fdata().astype(np.int16)
            subcortical_seg_data = subcortical_seg.get_fdata().astype(np.int16)

            # Check if the data shapes match
            if original_seg_data.shape != cortical_seg_data.shape or original_seg_data.shape != subcortical_seg_data.shape:
                logging.warning(f"Data shapes do not match for files in {subdir}")
                return None, None, None

            return original_seg_data, cortical_seg_data, subcortical_seg_data

        except Exception as e:
            logging.error(f"Error loading files in {subdir}: {str(e)}")
            return None, None, None


    def get_tumor_per_region(self, original_seg_data, cortical_seg_data, subcortical_seg_data):
        logging.info("Calculating tumor per region")

        # Get the pandas table
        cort_labels = ["void", "frontal pole", "insular cortex", "superior frontal gyrus", "middle frontal gyrus", "inferior frontal gyrus, pars triangularis", "inferior frontal gyrus, pars opercularis", "precentral gyrus", "temporal pole", "superior temporal gyrus, anterior division", "superior temporal gyrus, posterior division", "middle temporal gyrus, anterior division", "middle temporal gyrus, posterior division", "middle temporal gyrus, temporooccipital part", "inferior temporal gyrus, anterior division", "inferior temporal gyrus, posterior division", "inferior temporal gyrus, temporooccipital part", "postcentral gyrus", "superior parietal lobule", "supramarginal gyrus, anterior division", "supramarginal gyrus, posterior division", "angular gyrus", "lateral occipital cortex, superior division", "lateral occipital cortex, inferior division", "intracalcarine cortex", "frontal medial cortex", "juxtapositional lobule cortex", "subcallosal cortex", "paracingulate gyrus", "cingulate gyrus, anterior division", "cingulate gyrus, posterior division", "precuneous cortex", "cuneal cortex", "frontal oribtal cortex", "parahippocampal gyrus, anterior division", "parahippocampal gyrus, posterior division", "lingual gyrus", "temporal fusiform cortex, anterior division", "temporal fusiform cortex, posterior division", "temporal occipital fusiform cortex", "occipital fusiform gyrus", "frontal operculum cortex", "central opercular cortex", "parietal operculum cortex", "planum polare", "heschls gyrus", "planum temporale", "supracalcarine cortex", "occipital pole"]
        sub_labels = ["void", "left cerebral white matter", "left cerebral cortex", "left lateral ventrical", "left thalamus", "left caudate", "left putamen", "left pallidum", "brain-stem", "left hippocampus", "left amygdala", "left accumbens", "right cerebral white matter", "right cerebral cortex", "right lateral ventricle", "right thalamus", "right caudate", "right putamen", "right pallidum", "right hippocampus", "right amygdala", "right accumbens"]

        cort_values = list(set(cortical_seg_data.flatten()))
        cort_values = [int(x) for x in cort_values]
        subcort_values = list(set(subcortical_seg_data.flatten()))
        subcort_values = [int(x) for x in subcort_values]

        # Filter out cort_labels based on values
        cort_labels = [cort_labels[i] for i in cort_values]
        sub_labels = [sub_labels[i] for i in subcort_values] 

        logging.info(f"Cortical labels: {cort_labels}")
        logging.info(f"Subcortical labels: {sub_labels}")
        logging.info(f"Cortical values: {cort_values}")
        logging.info(f"Subcortical values: {subcort_values}")

        cort_dict = {            
            'Values': cort_values,
            'Labels': cort_labels
        }
        subcort_dict = {
            'Values': subcort_values,
            'Labels': sub_labels       
        }

        try:
            cort_df = pd.DataFrame(cort_dict)
            sub_df = pd.DataFrame(subcort_dict)
        except ValueError as e:
            logging.error(f"Error creating DataFrames: {str(e)}")
            return None, None

        logging.info("DataFrames created successfully")

        if self.mode == 1:
        # Get the tumor per region
            for region in cort_values:
                region_mask = np.zeros_like(original_seg_data)
                region_mask[cortical_seg_data == region] = 1
                tumor_overlap = original_seg_data * region_mask
                sum_tumor = np.sum(original_seg_data)
                sum_tumor_overlap = np.sum(tumor_overlap)
                # Append to dataframe
                cort_df.loc[cort_df["Values"] == region, "Tumor in region"] = sum_tumor_overlap / sum_tumor

            for region in subcort_values:
                region_mask = np.zeros_like(original_seg_data)
                region_mask[subcortical_seg_data == region] = 1
                tumor_overlap = original_seg_data * region_mask
                sum_tumor = np.sum(original_seg_data)
                sum_tumor_overlap = np.sum(tumor_overlap)
                # Append to dataframe
                sub_df.loc[sub_df["Values"] == region, "Tumor in region"] = sum_tumor_overlap / sum_tumor

            return cort_df, sub_df
        
        elif self.mode == 2:
            for region in cort_values:
                region_mask = np.zeros_like(original_seg_data)
                region_mask[cortical_seg_data == region] = 1
                tumor_overlap = original_seg_data * region_mask
                sum_region = np.sum(region_mask)
                sum_tumor_overlap = np.sum(tumor_overlap)
                # Append to dataframe
                cort_df.loc[cort_df["Values"] == region, "Tumor in region"] = sum_tumor_overlap / sum_region

            for region in subcort_values:
                region_mask = np.zeros_like(original_seg_data)
                region_mask[subcortical_seg_data == region] = 1
                tumor_overlap = original_seg_data * region_mask
                sum_region = np.sum(region_mask)
                sum_tumor_overlap = np.sum(tumor_overlap)
                # Append to dataframe
                sub_df.loc[sub_df["Values"] == region, "Tumor in region"] = sum_tumor_overlap / sum_region

            return cort_df, sub_df

    def save_data(self, save_path, names, counter, tumor_per_region_cortical, tumor_per_region_subcortical):
        # Save the data
        tumor_per_region_cortical.to_csv(save_path + f"/patient_{counter}/df_patient_{counter}_{names}_cortical.csv", index=False)
        tumor_per_region_subcortical.to_csv(save_path + f"/patient_{counter}/df_patient_{counter}_{names}_subcortical.csv", index=False)

        print("Data saved")



def main(dir, name, save_path, mode):
    tpr = tumor_per_region(dir, name, save_path, mode)
    tpr.process()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate tumor per region")
    parser.add_argument("--dir", type=str, required=True, help="Directory containing the data")
    parser.add_argument("--name", type=str, required=True, help="Name of the dataset for saving")
    parser.add_argument("--save_path", type=str, required=True, help="Path to save the output files")
    parser.add_argument("--mode", type=int, required=True, help="Mode = 1 for tumor in region / total tumor, Mode = 2 for tumor in region / total region")
    args = parser.parse_args()

    main(args.dir, args.name, args.save_path, args.mode)
