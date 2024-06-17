import os
import numpy as np
from src.common.io.path_operations import get_file_list_from_pattern
import nibabel as nib
from src.constants import CONNECTOME_BUNDCOUNT
import argparse
import matplotlib.pyplot as plt
import tqdm as tqdm
import math
import pandas as pd


class ConnectomeAnalyzer:
    def __init__(
        self,
        label: str,
    ):

        self.label = label
        self.mni_connectome = CONNECTOME_BUNDCOUNT

    def run(self):

        label_files = get_file_list_from_pattern(self.label)
        dataset_name = label_files[0].split("/")[1]
        number_of_patients = len(label_files)

        dataset_connectome_dict = {}

        for idx, label_file in tqdm.tqdm(enumerate(label_files)):
            patient_name = label_file.split("/")[-2]
            self.analyze(label_file)
            dataset_connectome_dict[patient_name] = self.analyze(label_file)

        self.plot_dict(dataset_connectome_dict, dataset_name, number_of_patients)

    def analyze(self, label_file: str):

        label = nib.load(label_file)
        label_data = label.get_fdata()

        mni_connectome = nib.load(self.mni_connectome)
        mni_connectome_data = mni_connectome.get_fdata()

        # Consider only the tumor core, Edema is 2
        label_data[label_data == 2] = 0
        label_data[label_data > 0] = 1

        masks_overlap = np.logical_and(label_data, mni_connectome_data)
        mni_overlap_voxels = np.where(masks_overlap, mni_connectome_data, 0)
        mni_voxels_to_sum = mni_overlap_voxels[mni_overlap_voxels > 0].flatten()

        if len(mni_voxels_to_sum) == 0:
            mni_voxel_sum = 0
        else:
            mni_voxel_sum = np.sum(mni_voxels_to_sum) / len(mni_voxels_to_sum)

        if math.isnan(mni_voxel_sum):
            mni_voxel_sum = 0

        return int(mni_voxel_sum)

    def plot_dict(
        self, dataset_connectome_dict: dict, dataset_name: str, number_of_patients: int
    ):

        df = pd.DataFrame(
            dataset_connectome_dict.items(), columns=["Patient", "Connectome overlap"]
        )
        df["Severity"] = df["Connectome overlap"].apply(
            lambda x: (
                "High connectome attainment"
                if x > 250
                else (
                    "Medium connectome attainment"
                    if x > 100
                    else "Low connectome attainment"
                )
            )
        )
        df = df.sort_values(by="Connectome overlap", ascending=True)

        severity_count = (
            df["Severity"]
            .value_counts()
            .reindex(
                [
                    "Low connectome attainment",
                    "Medium connectome attainment",
                    "High connectome attainment",
                ]
            )
        )
        severity_count = severity_count / sum(severity_count)

        colors = {
            "High connectome attainment": "red",
            "Medium connectome attainment": "orange",
            "Low connectome attainment": "green",
        }

        fig, (ax1, ax2) = plt.subplots(2, figsize=(20, 10))

        fig.suptitle(
            f"Analysis of connectome attainment by tumor in the {dataset_name} dataset. Number of patients: {number_of_patients}"
        )

        ax1.bar(df["Patient"], df["Connectome overlap"])
        ax1.set_xlabel("Patients")
        ax1.set_ylabel("Number of white matter bundles attained")
        ax1.set_title(
            f"Averge number of white matter bundles attained by the tumor for each patient in the {dataset_name} dataset"
        )
        ax1.set_xticks([])

        ax2.bar(
            severity_count.index,
            severity_count,
            color=[colors[i] for i in severity_count.index],
        )
        ax2.set_xlabel("Severity")
        ax2.set_ylabel("Proportion of attainment severity")
        ax2.set_title(
            f"Proportion of patients in the {dataset_name} dataset with different levels of white matter bundle attainment"
        )
        ax2.bar_label(ax2.containers[0], label_type="edge")
        ax2.margins(y=0.1)

        plt.savefig(f"connectome_overlap_{dataset_name}.png")


def main(label_path: str):
    analyzer = ConnectomeAnalyzer(label_path)
    analyzer.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze the overlap with the MNI connectome"
    )
    parser.add_argument(
        "--label_path",
        type=str,
        help="Path to the label file",
    )

    args = parser.parse_args()
    main(args.label_path)
