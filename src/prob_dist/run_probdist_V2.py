import glob
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import logging
import os

class ProcessNiftiData:
    def __init__(self,
                dataset_path : str,
                dataset_name : str,
                atlas_path : str, 
                save_path: str,
                array_size: tuple,
                labels: bool,
                necrotic_core = None,
                enhancing_region =None,
                edema = None):
        
        self.dataset_path = dataset_path
        self.save_path = save_path
        self.dataset_name = dataset_name
        self.atlas_path = atlas_path
        self.necrotic_core = necrotic_core
        self.enhancing_region = enhancing_region
        self.edema = edema
        self.labels = labels
        self.array_size = array_size
        
        logging.info(f"This is where the fun begins...")
        logging.info(f"Save path: {save_path}")
        logging.info(f"Dataset path: {dataset_path}")


    def process_data(self):
        # Get all the nifti files
        files = glob.glob(self.dataset_path)

        # Get the affine matrix
        sample = self.atlas_path
        sample_img = nib.load(sample)
        affine = sample_img.affine
        header = sample_img.header
        extra = sample_img.extra
        file_map = sample_img.file_map

        # Initialize result arrays
        result_array_whole_tumor = np.zeros((self.array_size[0], self.array_size[1], self.array_size[2]))
        result_array_necrotic_core = np.zeros((self.array_size[0], self.array_size[1], self.array_size[2]))
        result_array_enhancing_region = np.zeros((self.array_size[0], self.array_size[1], self.array_size[2]))
        result_array_edema = np.zeros((self.array_size[0], self.array_size[1], self.array_size[2]))

        if self.labels == True:
            # Whole tumor
            for file in files:
                img = nib.load(file)
                data = img.get_fdata()
                #get binary mask
                data[data > 0] = 1

                result_array_whole_tumor += data

            # Necrotic core
            for file in files:
                img = nib.load(file)
                data = img.get_fdata()
                # Get necrotic core
                data = data == self.necrotic_core
                data[data > 0] = 1

                result_array_necrotic_core += data

            # Enhancing region
            for file in files:
                img = nib.load(file)
                data = img.get_fdata()
                # Get enhancing region
                data = data == self.enhancing_region 
                data[data > 0] = 1

                result_array_enhancing_region += data

            # Edema
            for file in files:
                img = nib.load(file)
                data = img.get_fdata()
                # Get edema
                data = data == self.edema
                data[data > 0] = 1

                result_array_edema += data

        else:
            for file in files:
                img = nib.load(file)
                data = img.get_fdata()
                #get binary mask
                data[data > 0] = 1

                result_array_whole_tumor += data

        print(max(result_array_whole_tumor.flatten()))
        print(max(result_array_necrotic_core.flatten()))
        print(max(result_array_enhancing_region.flatten()))
        print(max(result_array_edema.flatten()))

        if self.labels == True:
            self.save_result_as_nifti(result_array_whole_tumor, 'whole_tumor', affine, header, extra, file_map)
            self.save_result_as_nifti(result_array_necrotic_core, 'necrotic_core', affine, header, extra, file_map)
            self.save_result_as_nifti(result_array_enhancing_region, 'enhancing_region', affine, header, extra, file_map)
            self.save_result_as_nifti(result_array_edema, 'edema', affine, header, extra, file_map)
        else:
            self.save_result_as_nifti(result_array_whole_tumor, 'whole_tumor', affine, header, extra, file_map)

        if self.labels == True:
            self.visualize_surface_plot(result_array_whole_tumor, 'whole_tumor')
            self.visualize_surface_plot(result_array_necrotic_core, 'necrotic_core')
            self.visualize_surface_plot(result_array_enhancing_region, 'enhancing_region')
            self.visualize_surface_plot(result_array_edema, 'edema')
        else:
            self.visualize_surface_plot(result_array_whole_tumor, 'whole_tumor')


    def save_result_as_nifti(self, result_array, name, affine):
        img = nib.Nifti1Image(result_array, affine)
        nib.save(img, f'{self.save_path}/probdist_{self.dataset_name}_{name}.nii')

    def visualize_surface_plot(self, result_array, name):
        collapsed_array = np.sum(result_array, axis=2)
        collapsed_array_sum = sum(collapsed_array.flatten())
        collapsed_array_plot = collapsed_array / collapsed_array_sum
        collapsed_array_plot = collapsed_array_plot 

        x = np.arange(0, collapsed_array.shape[1])
        y = np.arange(0, collapsed_array.shape[0])
        X, Y = np.meshgrid(x, y)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, collapsed_array, cmap='viridis')

        ax.set_title(f"Collapsed Array Surface Plot - {name}")
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        ax.set_zlabel("Values (10^3)")

        plt.savefig(f"{self.save_path}/{dataset_name}_surface_plot_{name}.png")


dataset_path = r'C:\Users\gaspa\Desktop\segmentation_test\Datasets\BRAIN-TUMO-PROGRESSION_DATASET\Brain-Tumor-Progression\sub-*\BraTSPipeline_sub*\brainTumorMask_SRI.nii'
save_path = r'C:\Users\gaspa\Desktop\segmentation_test\prob_dist_results\BRAIN-TUMOR-PROGRESSION_DATASET'
dataset_name = 'BTP'

process = ProcessNiftiData(dataset_path=dataset_path, dataset_name=dataset_name, atlas_path=atlas_path, save_path=save_path, array_size=(240,240,155), labels=True, necrotic_core=1, enhancing_region=3, edema=2)
process.process_data()