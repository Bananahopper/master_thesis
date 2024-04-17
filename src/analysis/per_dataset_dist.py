import pandas as pd
import os
import glob
import logging
import argparse
from functools import reduce
import random
import matplotlib.pyplot as plt

from analysis import ANALYSIS_FOLDER

# Configure logging
logging.basicConfig(
    filename="per_dataset_stats.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class PerDatasetDist:
    def __init__(self, directory, name):
        self.directory = directory
        self.name = name

        self.SAVE_PATH = os.path.join(ANALYSIS_FOLDER, "per_dataset_dist")
        if not os.path.exists(self.SAVE_PATH):
            os.makedirs(self.SAVE_PATH)

    def process(self):
        added_dfs_cortical, added_dfs_subcortical = self.get_files()

        if added_dfs_cortical is None or added_dfs_subcortical is None:
            logging.error("Unable to obtain added dataframes. Exiting...")
            return

        merged_cortical, merged_subcortical = self.get_statistics(
            added_dfs_cortical, added_dfs_subcortical
        )
        self.save_statistics(merged_cortical, merged_subcortical)

    def get_files(self):
        added_dfs_cortical = []
        added_dfs_subcortical = []

        for root, dir, files in os.walk(self.directory):
            for subdir in dir:

                logging.info(f"Processing {subdir}")

                for file in glob.glob(os.path.join(root, subdir, "*_cortical.csv")):

                    if not os.path.exists(file):
                        logging.error(f"File {file} does not exist. Exiting...")
                        return None, None

                    df = pd.read_csv(file)

                    logging.info(f"Size of cortical df for {subdir} is {df.shape}")

                    added_dfs_cortical.append(df)

                for file in glob.glob(os.path.join(root, subdir, "*_subcortical.csv")):

                    if not os.path.exists(file):
                        logging.error(f"File {file} does not exist. Exiting...")
                        return None, None

                    df = pd.read_csv(file)

                    logging.info(f"Size of subcortical df for {subdir} is {df.shape}")

                    added_dfs_subcortical.append(df)

                logging.info(f"Processed {subdir}")

            return added_dfs_cortical, added_dfs_subcortical

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

    def save_statistics(self, merged_cortical, merged_subcortical):
        merged_cortical.to_csv(self.SAVE_PATH + f"/cortical_stats_for_{self.name}.csv")

        logging.info(f"Saved cortical stats for {self.name}")

        merged_subcortical.to_csv(
            self.SAVE_PATH + f"/subcortical_stats_for_{self.name}.csv"
        )

        logging.info(f"Saved subcortical stats for {self.name}")

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
            f"Percentage of tumor in each cortical region for {self.name} dataset"
        )
        plt.legend(loc="center left", bbox_to_anchor=(1.0, 0.5))
        plt.savefig(self.SAVE_PATH + f"/cortical_plot_for_{self.name}.png")
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
            f"Percentage of tumor in each subcortical region for {self.name} dataset"
        )
        plt.legend(loc="center left", bbox_to_anchor=(1.0, 0.5))
        plt.savefig(self.SAVE_PATH + f"/subcortical_plot_for_{self.name}.png")
        plt.close()

        logging.info(f"Saved plots for {self.name}")
