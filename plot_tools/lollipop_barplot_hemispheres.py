import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from src.common.io.path_operations import get_file_list_from_pattern


class HemisphereDifferencePlotter:
    def __init__(self):
        pass

    def process(self, file_pattern):
        files = get_file_list_from_pattern(file_pattern)
        print(files)
        dataset_names = []
        for file in files:
            dataset_name = file.split("/")[-2]
            dataset_names.append(dataset_name)

        self.add_hemispheres_and_plot(files, dataset_names)

    def add_hemispheres_and_plot(self, files, dataset_names):

        hemisphere_dict = {"Left Hemisphere": [], "Right Hemisphere": []}

        for file, name in zip(files, dataset_names):
            df = pd.read_csv(file)
            left_hemisphere = df[df["Labels"].str.contains("left")]
            right_hemisphere = df[df["Labels"].str.contains("right")]
            left_hemisphere_sum = left_hemisphere["Tumor in region"].sum()
            right_hemisphere_sum = right_hemisphere["Tumor in region"].sum()

            hemisphere_dict["Left Hemisphere"].append(left_hemisphere_sum)
            hemisphere_dict["Right Hemisphere"].append(right_hemisphere_sum)

        x = np.arange(len(dataset_names))
        width = 0.25
        multiplier = 0

        fig, ax = plt.subplots(layout="constrained", figsize=(15, 8))

        colors = ["#9932CC", "#FF6347"]

        for hemisphere, value in hemisphere_dict.items():
            offset = width * multiplier
            rects = ax.bar(
                x + offset, value, width, label=hemisphere, color=colors[multiplier]
            )
            ax.bar_label(rects, padding=3)
            multiplier += 1

        ax.set_xticks(x + width / 2)
        ax.set_xticklabels(dataset_names)
        ax.title.set_text(
            "Percentage of tumors attaining a specific hemisphere of the brain in each dataset",
        )
        ax.set_xlabel("Dataset", fontsize="large")
        ax.set_ylabel("Percentage (%) of tumors in hemisphere", fontsize="large")
        ax.legend(
            fontsize="large",
        )

        plt.savefig("hemisphere_difference.png")


x = HemisphereDifferencePlotter().process(
    "output_analysis/*/per_dataset_dist/*/subcortical_stats.csv"
)
