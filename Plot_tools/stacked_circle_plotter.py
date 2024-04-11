import circlify
import matplotlib.pyplot as plt
import pandas as pd
import argparse

class CirclePlotter():
    def __init__(self, 
                 datasets: list,
                 names: list,
                 save_path = "./"):
        self.datasets = datasets
        self.names = names
        self.save_path = save_path

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
            datum_df = df['Tumor in region'].to_list()
            regions_df = df['Labels'].to_list()

            data_dict.append({'id': f'{self.names[index]}', 'datum': sum(datum_df), 
                              'children': [{'id': regions_df[i], 
                                            'datum': datum_df[i]} for i in range(len(regions_df))]})
        return data_dict
    
    def plot(self, data_dict, save_path):

        # Define colors

        colors = [
                    "#FF0000",  # Red
                    "#00FF00",  # Green
                    "#0000FF",  # Blue
                    "#FFFF00",  # Yellow
                    "#00FFFF",  # Cyan
                    "#FF00FF",  # Magenta
                    "#000000",  # Black
                    "#FFFFFF",  # White
                    "#808080",  # Gray
                    "#800000",  # Maroon
                    "#808000",  # Olive
                    "#000080",  # Navy
                    "#800080",  # Purple
                    "#008080",  # Teal
                    "#C0C0C0",  # Silver
                    "#FFD700",  # Gold
                    "#4B0082",  # Indigo
                    "#FFC0CB",  # Pink
                    "#FFDAB9",  # Peach
                    "#E6E6FA",  # Lavender
                    "#FF7F50",   # Coral
                    "#FFA07A"  # Light Salmon
                ]
        
        sub_labels = ["void", "left cerebral white matter", "left cerebral cortex", "left lateral ventrical", "left thalamus", "left caudate", "left putamen", "left pallidum", "brain-stem", "left hippocampus", "left amygdala", "left accumbens", "right cerebral white matter", "right cerebral cortex", "right lateral ventricle", "right thalamus", "right caudate", "right putamen", "right pallidum", "right hippocampus", "right amygdala", "right accumbens"]

        color_mapping = {}

        for index, name in enumerate(sub_labels):
            color_mapping[name] = colors[index]
        
        circles = circlify.circlify(
            data_dict,
            show_enclosure=False,
            target_enclosure=circlify.Circle(x=0, y=0, r=1)
        )

        # Create just a figure and only one subplot
        fig, ax = plt.subplots(figsize=(30, 30))

        # Title
        ax.set_title('Tumor distibution in BRATS dataset')

        # Remove axes
        ax.axis('off')

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

        # Print circle the highest level (continents):
        for circle in circles:
            if circle.level ==1:
                x, y, r = circle
                ax.add_patch(plt.Circle((x, y), r, alpha=0.5,
                             linewidth=2, color="#bc5090"))

        # Print circle and labels for the highest level:
        for circle in circles:
            if circle.level == 2:
                x, y, r = circle
                label = circle.ex["id"]
                color = color_mapping[label]
                ax.add_patch(plt.Circle((x, y), r, alpha=0.5,
                            linewidth=2, color=color))
                plt.annotate(label, (x, y), ha='center', color="black")

        # Print labels for the continents
        for circle in circles:
            if circle.level == 1:
                x, y, r = circle
                label = circle.ex["id"]
                bbox_props = {'facecolor':'wheat', 'boxstyle': 'round', 'color': 'white'}
                plt.annotate(label, (x, y), va='center', ha='center', bbox=bbox_props)
        
        plt.savefig(save_path + f"/circle_plot.png")
        plt.close()


# Test the class
        
datasets = ["per_dataset_BRATS/subcortical_stats_for_BRATS.csv", "per_dataset_BTP/subcortical_stats_for_BTP.csv", "per_dataset_QIN/subcortical_stats_for_QIN.csv", "per_dataset_RHUH/subcortical_stats_for_RHUH.csv"]
names = ["BRATS", "BTP", "QIN", "RHUH"]
save_path = "test"

cpltr = CirclePlotter(datasets, names, save_path)
cpltr.process()


def main(datasets, names, save_path):
    cpltr = CirclePlotter(datasets, names, save_path)
    cpltr.process()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate tumor per region")
    parser.add_argument("--dirs", type=list, required=True, help="Directory containing the data")
    parser.add_argument("--names", type=list, required=True, help="Name of the dataset for saving")
    parser.add_argument("--save_path", type=str, required=False, help="Path to save the output files")
    args = parser.parse_args()

    main(args.dirs, args.names, args.save_path)
