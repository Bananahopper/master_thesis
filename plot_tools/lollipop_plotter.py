import matplotlib.pyplot as plt
import pandas as pd
import argparse

class LollipopPlotter():
    def __init__(self, 
                 datasets: list,
                 names: list,
                 save_path: str) -> None:
        
        self.datasets = datasets
        self.names = names
        self.save_path = save_path

    def process(self) -> None:
        for name, dataset in zip(self.names, self.datasets):
            self.access_data_and_plot(dataset, name)

    def access_data_and_plot(self, 
                             data_path: str,
                             name: str) -> None:
        print(data_path)
        df = pd.read_csv(data_path, index_col=0)
        df = df.drop(index='void')
        ordered_df = df.sort_values(by='Tumor in region', ascending=False)
        x_range = range(0,len(df.index))

        # Make the plot
        plt.figure(figsize=(20,10))
        plt.hlines(y=x_range, xmin=0, xmax=ordered_df['Tumor in region'], color='#ff6361')
        plt.plot(ordered_df['Tumor in region'], x_range, "o", c='#bc5090')

        # Add titles and axis names
        plt.yticks(x_range, ordered_df.index)
        plt.title(f"Regions affected by tumors in the {name} dataset", loc='left')
        plt.xlabel(f'Percentages of tumors affecting specific region in the {name} dataset')
        plt.ylabel(f'Locations affected by tumors in the {name} dataset')

        # Save the plot
        plt.savefig(self.save_path + f"/lollipop_plot_for_{name}.png")
        plt.close()


# RUN THE CODE

datasets = ["per_dataset_BRATS/subcortical_stats_for_BRATS.csv", "per_dataset_BTP/subcortical_stats_for_BTP.csv", "per_dataset_QIN/subcortical_stats_for_QIN.csv", "per_dataset_RHUH/subcortical_stats_for_RHUH.csv"]
names = ["BRATS", "BTP", "QIN", "RHUH"]
save_path = "test"

lpop = LollipopPlotter(datasets, names, save_path)
lpop.process()
# def main(datasets, names, save_path):
#     lpop = LollipopPlotter(datasets, names, save_path)
#     lpop.process()


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Plot the datasets as lollipop plots")
#     parser.add_argument("--dirs", type=list, required=True, help="Directory containing the data")
#     parser.add_argument("--names", type=list, required=True, help="Name of the dataset for saving")
#     parser.add_argument("--save_path", type=str, required=True, help="Path to save the output files")
#     args = parser.parse_args()

#     main(args.dirs, args.names, args.save_path)