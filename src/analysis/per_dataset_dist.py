import pandas as pd
import logging
from functools import reduce
import random
import matplotlib.pyplot as plt
import os
from src.common.io.path_operations import (
    extract_fsd_from_output_analysis_path,
    get_file_list_from_pattern,
)
from src.analysis import ANALYSIS_FOLDER_CAPTK


class PerDatasetDist:
    def __init__(self):
        pass

    def process(self, cortical_pattern: str, subcortical_pattern: str):

        subject_id, _, dataset_name = extract_fsd_from_output_analysis_path(
            cortical_pattern
        )

        save_folder = os.path.join(
            ANALYSIS_FOLDER_CAPTK, dataset_name, "per_dataset_dist"
        )
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        dataset_save_folder = os.path.join(save_folder, dataset_name)
        if not os.path.exists(dataset_save_folder):
            os.makedirs(dataset_save_folder)

        cortical_df_list = get_file_list_from_pattern(cortical_pattern)
        subcortical_df_list = get_file_list_from_pattern(subcortical_pattern)

        if len(cortical_df_list) != len(subcortical_df_list):
            logging.error("Number of cortical and subcortical images do not match.")
            logging.error(
                f"Number of cortical images: {len(cortical_df_list)}, Number of subcortical images: {len(subcortical_df_list)}"
            )

        cortical_df_merged_list = []
        subcortical_df_merged_list = []

        for cortical_df_file, subcortical_df_file in zip(
            cortical_df_list, subcortical_df_list
        ):

            cortical_df = pd.read_csv(cortical_df_file)
            subcortical_df = pd.read_csv(subcortical_df_file)

            cortical_df_merged_list.append(cortical_df)
            subcortical_df_merged_list.append(subcortical_df)

        merged_cortical, merged_subcortical = self.get_statistics(
            cortical_df_merged_list,
            subcortical_df_merged_list,
        )

        # There should be an error here. The merged cortical and merged subcortical might be empty ############################################################################

        self.save_statistics(
            merged_cortical, merged_subcortical, dataset_save_folder, dataset_name
        )

    def get_statistics(self, added_dfs_cortical, added_dfs_subcortical):
        for df_list in [added_dfs_cortical, added_dfs_subcortical]:
            for df in df_list:
                df.drop("Values", axis=1, inplace=True)
                df.set_index("Labels", inplace=True)

        x = random.randint(0, 5000)
        y = random.randint(0, 5000)

        merged_df = reduce(
            lambda left, right: pd.merge(
                left, right, on=["Labels"], how="outer", suffixes=(None, x)
            ),
            added_dfs_cortical,
        ).fillna(0)
        summed_df = merged_df.sum(axis=1)
        divided_df = summed_df / len(added_dfs_cortical)
        divided_df = divided_df * 100
        merged_cortical = pd.DataFrame(divided_df, columns=["Tumor in region"])

        merged_df = reduce(
            lambda left, right: pd.merge(
                left, right, on=["Labels"], how="outer", suffixes=(None, y)
            ),
            added_dfs_subcortical,
        ).fillna(0)
        summed_df = merged_df.sum(axis=1)
        divided_df = summed_df / len(added_dfs_subcortical)
        divided_df = divided_df * 100
        merged_subcortical = pd.DataFrame(divided_df, columns=["Tumor in region"])

        return merged_cortical, merged_subcortical

    def save_statistics(
        self, merged_cortical, merged_subcortical, dataset_save_folder, dataset_name
    ):
        merged_cortical.to_csv(dataset_save_folder + f"/cortical_stats.csv")

        merged_subcortical.to_csv(dataset_save_folder + f"/subcortical_stats.csv")

        df_cortical = merged_cortical.drop("void")
        df_cortical_sorted = df_cortical.sort_values(
            by="Tumor in region", axis=0, ascending=False
        )

        plt.figure()
        df_cortical_sorted.plot(
            kind="barh", figsize=(25, 20), edgecolor="black", colormap="tab20b"
        )
        plt.xlabel("Percentage of tumor in region")
        plt.title(
            f"Percentage of tumor in each cortical region for {dataset_name} dataset"
        )
        plt.legend(loc="center left", bbox_to_anchor=(1.0, 0.5))
        plt.savefig(dataset_save_folder + f"/cortical_plot.png")
        plt.close()

        df_subcortical = merged_subcortical.drop("void")
        df_subcortical_sorted = df_subcortical.sort_values(
            by="Tumor in region", axis=0, ascending=False
        )

        plt.figure()
        df_subcortical_sorted.plot(
            kind="barh", figsize=(25, 20), edgecolor="black", colormap="tab20b"
        )
        plt.xlabel("Percentage of tumor in region")
        plt.title(
            f"Percentage of tumor in each subcortical region for {dataset_name} dataset"
        )
        plt.legend(loc="center left", bbox_to_anchor=(1.0, 0.5))
        plt.savefig(dataset_save_folder + f"/subcortical_plot.png")
        plt.close()

        logging.info(f"Saved plots for {dataset_name}")


# class PerDatasetDist:
#     def __init__(self, name):

#         self.name = name

#         self.SAVE_PATH = os.path.join(ANALYSIS_FOLDER_CAPTK, "per_dataset_dist")
#         if not os.path.exists(self.SAVE_PATH):
#             os.makedirs(self.SAVE_PATH)

#     def process(self):
#         added_dfs_cortical, added_dfs_subcortical = self.get_files()

#         if added_dfs_cortical is None or added_dfs_subcortical is None:
#             logging.error("Unable to obtain added dataframes. Exiting...")
#             return

#         merged_cortical, merged_subcortical = self.get_statistics(
#             added_dfs_cortical, added_dfs_subcortical
#         )
#         self.save_statistics(merged_cortical, merged_subcortical)

#     def get_files(self):
#         added_dfs_cortical = []
#         added_dfs_subcortical = []

#         for root, dir, files in os.walk(REGISTRATION_FOLDER_CAPTK):
#             for subdir in dir:

#                 logging.info(f"Processing {subdir}")

#                 for file in glob.glob(os.path.join(root, subdir, "*_cortical.csv")):

#                     if not os.path.exists(file):
#                         logging.error(f"File {file} does not exist. Exiting...")
#                         return None, None

#                     df = pd.read_csv(file)

#                     logging.info(f"Size of cortical df for {subdir} is {df.shape}")

#                     added_dfs_cortical.append(df)

#                 for file in glob.glob(os.path.join(root, subdir, "*_subcortical.csv")):

#                     if not os.path.exists(file):
#                         logging.error(f"File {file} does not exist. Exiting...")
#                         return None, None

#                     df = pd.read_csv(file)

#                     logging.info(f"Size of subcortical df for {subdir} is {df.shape}")

#                     added_dfs_subcortical.append(df)

#                 logging.info(f"Processed {subdir}")

#             return added_dfs_cortical, added_dfs_subcortical

#     def get_statistics(self, added_dfs_cortical, added_dfs_subcortical):
#         for df_list in [added_dfs_cortical, added_dfs_subcortical]:
#             for df in df_list:
#                 df.drop("Values", axis=1, inplace=True)
#                 df.set_index("Labels", inplace=True)

#         x = random.randint(0, 5000)
#         y = random.randint(0, 5000)

#         merged_df = reduce(
#             lambda left, right: pd.merge(
#                 left, right, on=["Labels"], how="outer", suffixes=(None, x)
#             ),
#             added_dfs_cortical,
#         ).fillna(0)
#         summed_df = merged_df.sum(axis=1)
#         divided_df = summed_df / len(added_dfs_cortical)
#         divided_df = divided_df * 100
#         merged_cortical = pd.DataFrame(divided_df, columns=["Tumor in region"])

#         merged_df = reduce(
#             lambda left, right: pd.merge(
#                 left, right, on=["Labels"], how="outer", suffixes=(None, y)
#             ),
#             added_dfs_subcortical,
#         ).fillna(0)
#         summed_df = merged_df.sum(axis=1)
#         divided_df = summed_df / len(added_dfs_subcortical)
#         divided_df = divided_df * 100
#         merged_subcortical = pd.DataFrame(divided_df, columns=["Tumor in region"])

#         return merged_cortical, merged_subcortical

#     def save_statistics(self, merged_cortical, merged_subcortical):
#         merged_cortical.to_csv(self.SAVE_PATH + f"/cortical_stats_for_{self.name}.csv")

#         logging.info(f"Saved cortical stats for {self.name}")

#         merged_subcortical.to_csv(
#             self.SAVE_PATH + f"/subcortical_stats_for_{self.name}.csv"
#         )

#         logging.info(f"Saved subcortical stats for {self.name}")

#         df_cortical = merged_cortical.drop("void")
#         df_cortical_sorted = df_cortical.sort_values(
#             by="Tumor in region", axis=0, ascending=False
#         )

#         plt.figure()
#         df_cortical_sorted.plot(
#             kind="barh", figsize=(25, 20), edgecolor="black", colormap="tab20b"
#         )
#         plt.xlabel("Percentage of tumor in region")
#         plt.title(
#             f"Percentage of tumor in each cortical region for {self.name} dataset"
#         )
#         plt.legend(loc="center left", bbox_to_anchor=(1.0, 0.5))
#         plt.savefig(self.SAVE_PATH + f"/cortical_plot_for_{self.name}.png")
#         plt.close()

#         df_subcortical = merged_subcortical.drop("void")
#         df_subcortical_sorted = df_subcortical.sort_values(
#             by="Tumor in region", axis=0, ascending=False
#         )

#         plt.figure()
#         df_subcortical_sorted.plot(
#             kind="barh", figsize=(25, 20), edgecolor="black", colormap="tab20b"
#         )
#         plt.xlabel("Percentage of tumor in region")
#         plt.title(
#             f"Percentage of tumor in each subcortical region for {self.name} dataset"
#         )
#         plt.legend(loc="center left", bbox_to_anchor=(1.0, 0.5))
#         plt.savefig(self.SAVE_PATH + f"/subcortical_plot_for_{self.name}.png")
#         plt.close()

#         logging.info(f"Saved plots for {self.name}")
