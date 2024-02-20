import argparse
import logging
import os

from prob_dist.run_probdist_V2 import ProcessNiftiData

def main(arg: dict):
    processNiftiData = ProcessNiftiData(dataset_path=arg['dataset_path'],
                                        dataset_name=arg['dataset_name'],
                                        save_path=arg['save_path'],
                                        labels=arg['labels'],
                                        necrotic_core=arg['necrotic_core'],
                                        enhancing_region=arg['enhancing_region'],
                                        edema=arg['edema'],
                                        dimensions=arg['dimensions'])
    processNiftiData.process_data()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='Process Nifti data')
    parser.add_argument('--dataset_path', type=str, help='Path to the dataset')
    parser.add_argument('--dataset_name', type=str, help='Name of the dataset')
    parser.add_argument('--save_path', type=str, help='Path to save the processed data')
    parser.add_argument('--labels', type=bool, help='Whether to use labels or not')
    parser.add_argument('--necrotic_core', type=int, help='Value for necrotic core')
    parser.add_argument('--enhancing_region', type=int, help='Value for enhancing region')
    parser.add_argument('--edema', type=int, help='Value for edema')
    parser.add_argument('--dimensions', type=tuple, help='Dimensions of the array')

    args = parser.parse_args()
    arg = vars(args)
    
    main(arg)