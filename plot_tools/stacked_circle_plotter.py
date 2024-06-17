import circlify
import matplotlib.pyplot as plt
import pandas as pd
import argparse
from matplotlib.patches import Patch


class CirclePlotter:
    def __init__(
        self, datasets: list, names: list, save_path="./", ignore_hemispheres=False
    ):
        self.datasets = datasets
        self.names = names
        self.save_path = save_path
        self.ignore_hemispheres = ignore_hemispheres

    def process(self):
        dfs = self.handle_dataframes()
        data_dict = self.format_dfs(dfs)
        self.plot(data_dict, self.save_path)

    def handle_dataframes(self):
        dfs = []
        for dataset in self.datasets:
            df = pd.read_csv(dataset)
            dfs.append(df)

        return dfs

    def format_dfs(self, dfs):
        data_dict = []
        for index, df in enumerate(dfs):

            if self.ignore_hemispheres:
                exclusions = [
                    "left cerebral white matter",
                    "left cerebral cortex",
                    "right cerebral white matter",
                    "right cerebral cortex",
                    "void",
                ]
                df = df[~df["Labels"].isin(exclusions)]
            else:
                exclusions = ["void"]
                df = df[~df["Labels"].isin(exclusions)]

            datum_df = df["Tumor in region"].to_list()
            regions_df = df["Labels"].to_list()

            data_dict.append(
                {
                    "id": f"{self.names[index]}",
                    "datum": sum(datum_df),
                    "children": [
                        {"id": regions_df[i], "datum": datum_df[i]}
                        for i in range(len(regions_df))
                    ],
                }
            )
        return data_dict

    def plot(self, data_dict, save_path):

        # Define colors

        colors_regions = [
            "#FF0000",  # Red
            "#00FF00",  # Green
            "#0000FF",  # Blue
            "#FFFF00",  # Yellow
            "#00FFFF",  # Cyan
            "#FF00FF",  # Magenta
            "#00CED1",  # Dark Turquoise
            "#556B2F",  # Dark Olive Green
            "#8B4513",  # Saddle Brown
            "#800000",  # Maroon
            "#808000",  # Olive
            "#000080",  # Navy
            "#800080",  # Purple
            "#008080",  # Teal
            "#8B008B",  # Dark Magenta
            "#FFD700",  # Gold
            "#4B0082",  # Indigo
            "#FFC0CB",  # Pink
            "#FFDAB9",  # Peach
            "#9932CC",  # Dark Orchid
            "#FF7F50",  # Coral
            "#FFA07A",  # Light Salmon
        ]

        colors_dataset = [
            "#F0E68C",  # Khaki
            "#DC143C",  # Crimson
            "#00FF00",  # Lime
            "#FFA500",  # Orange
            "#CD853F",  # Peru
            "#FF6347",  # Tomato
            "#EE82EE",  # Violet
        ]

        sub_labels = [
            "void",
            "left cerebral white matter",
            "left cerebral cortex",
            "left lateral ventrical",
            "left thalamus",
            "left caudate",
            "left putamen",
            "left pallidum",
            "brain-stem",
            "left hippocampus",
            "left amygdala",
            "left accumbens",
            "right cerebral white matter",
            "right cerebral cortex",
            "right lateral ventricle",
            "right thalamus",
            "right caudate",
            "right putamen",
            "right pallidum",
            "right hippocampus",
            "right amygdala",
            "right accumbens",
        ]

        color_mapping_region = {}
        color_mapping_dataset = {}

        for index, name in enumerate(self.names):
            color_mapping_dataset[name] = colors_dataset[index]

        for index, name in enumerate(sub_labels):
            color_mapping_region[name] = colors_regions[index]

        circles = circlify.circlify(
            data_dict,
            show_enclosure=False,
            target_enclosure=circlify.Circle(x=0, y=0, r=1),
        )

        # Create just a figure and only one subplot
        fig, ax = plt.subplots(figsize=(30, 30))

        # Title
        ax.set_title("Tumor distibution in BRATS dataset", fontsize=20, y=1.0, pad=50)

        # Remove axes
        ax.axis("off")

        # Find axis boundaries
        lim = max(
            max(
                abs(circle.x) + circle.r,
                abs(circle.y) + circle.r,
            )
            for circle in circles
        )
        plt.xlim(-lim, lim)
        plt.ylim(-lim, lim)

        # Print circle the highest level datasets:
        for circle in circles:
            if circle.level == 1:
                x, y, r = circle
                dataset = circle.ex["id"]
                color_dataset = color_mapping_dataset[dataset]
                ax.add_patch(
                    plt.Circle(
                        (x, y),
                        r,
                        alpha=0.5,
                        linewidth=2,
                        color=color_dataset,
                    )
                )

        # Print circle and labels for the regions:
        for circle in circles:
            if circle.level == 2:
                x, y, r = circle
                label = circle.ex["id"]
                color = color_mapping_region[label]
                ax.add_patch(plt.Circle((x, y), r, alpha=1, linewidth=2, color=color))

        handles_dataset, labels_dataset = ax.get_legend_handles_labels()
        handles_region, labels_region = ax.get_legend_handles_labels()
        for key, value in color_mapping_dataset.items():
            handles_dataset.append(Patch(color=value, edgecolor=value))
            labels_dataset.append(key)

        legend_dataset = ax.legend(
            handles_dataset,
            labels_dataset,
            loc="lower left",
            title="Datasets",
            fontsize=15,
            title_fontsize=15,
        )

        for key, value in color_mapping_region.items():
            if (
                key == "void"
                or key == "left cerebral white matter"
                or key == "right cerebral white matter"
                or key == "left cerebral cortex"
                or key == "right cerebral cortex"
            ):
                continue
            handles_region.append(Patch(color=value, edgecolor=value))
            labels_region.append(key)

        legend_region = ax.legend(
            handles_region,
            labels_region,
            loc="lower right",
            title="Regions",
            fontsize=15,
            title_fontsize=15,
        )

        ax.add_artist(legend_dataset)
        ax.add_artist(legend_region)

        plt.savefig(save_path + f"/circle_plot.png")
        plt.close()


# Test the class

datasets = [
    "output_analysis/Brats-2023-SSA/per_dataset_dist/Brats-2023-SSA/subcortical_stats.csv",
    "output_analysis/Brats2021_wTumor/per_dataset_dist/Brats2021_wTumor/subcortical_stats.csv",
    "output_analysis/Burdenko-GBM-Progression/per_dataset_dist/Burdenko-GBM-Progression/subcortical_stats.csv",
    "output_analysis/LGG-1p19qDeletion/per_dataset_dist/LGG-1p19qDeletion/subcortical_stats.csv",
    "output_analysis/QIN/per_dataset_dist/QIN/subcortical_stats.csv",
    "output_analysis/RHUH_GBM/per_dataset_dist/RHUH_GBM/subcortical_stats.csv",
    "output_analysis/UCSF-PDGM-v3/per_dataset_dist/UCSF-PDGM-v3/subcortical_stats.csv",
]
names = [
    "Brats-2023-SSA",
    "Brats2021_wTumor",
    "Burdenko-GBM-Progression",
    "LGG-1p19qDeletion",
    "QIN",
    "RHUH_GBM",
    "UCSF-PDGM-v3",
]
save_path = "output_plots"
ignore_hemispheres = True

cpltr = CirclePlotter(datasets, names, save_path, ignore_hemispheres)
cpltr.process()


# def main(datasets, names, save_path):
#     cpltr = CirclePlotter(datasets, names, save_path)
#     cpltr.process()


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Calculate tumor per region")
#     parser.add_argument(
#         "--dirs", type=list, required=True, help="Directory containing the data"
#     )
#     parser.add_argument(
#         "--names", type=list, required=True, help="Name of the dataset for saving"
#     )
#     parser.add_argument(
#         "--save_path", type=str, required=False, help="Path to save the output files"
#     )
#     args = parser.parse_args()

#     main(args.dirs, args.names, args.save_path)
