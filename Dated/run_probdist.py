import numpy as np
import nibabel as nib
import glob
import matplotlib.pyplot as plt


# get all the nifti files
files = glob.glob(r'C:\Users\gaspa\Desktop\segmentation_test\Datasets\BRAIN-TUMO-PROGRESSION_DATASET\Brain-Tumor-Progression\sub-*\BraTSPipeline_sub*\brainTumorMask_SRI.nii')
dataset_name = 'RHUH_Dataset'

# Get the affine matrix
sample = files[0]
sample_img = nib.load(sample)
affine = sample_img.affine

# initialize result array
result_array_whole_tumor = np.zeros((240,240,155))
for file in files:
    img = nib.load(file)
    data = img.get_fdata()
    #get binary mask
    data[data > 0] = 1

    result_array_whole_tumor += data

result_array_necrotic_core = np.zeros((240,240,155))
for file in files:
    img = nib.load(file)
    data = img.get_fdata()
    # Get necrotic core
    data = data == 1
    data[data > 0] = 1

    result_array_necrotic_core += data

result_array_enhancing_region = np.zeros((240,240,155))
for file in files:
    img = nib.load(file)
    data = img.get_fdata()
    # Get enhancing region
    data = data == 4 
    data[data > 0] = 1

    result_array_enhancing_region += data

result_array_edema= np.zeros((240,240,155))
for file in files:
    img = nib.load(file)
    data = img.get_fdata()
    # Get edema
    data = data == 2
    data[data > 0] = 1

    result_array_edema += data




# Save result array as nifti file
img_whole_tumor = nib.Nifti1Image(result_array_whole_tumor, affine, header=img.header)
nib.save(img_whole_tumor, r'C:\Users\gaspa\Desktop\segmentation_test\prob_dist_results\BRAIN-TUMOR-PROGRESSION_DATASET\probdist_BTP_whole_tumor.nii')

img_edema = nib.Nifti1Image(result_array_edema, affine, header=img.header)
nib.save(img_edema, r'C:\Users\gaspa\Desktop\segmentation_test\prob_dist_results\BRAIN-TUMOR-PROGRESSION_DATASET\probdist_BTP_edema.nii')

img_necrotic_core = nib.Nifti1Image(result_array_necrotic_core, affine, header=img.header)
nib.save(img_necrotic_core, r'C:\Users\gaspa\Desktop\segmentation_test\prob_dist_results\BRAIN-TUMOR-PROGRESSION_DATASET\probdist_BTP_necrotic_core.nii')

img_enhancing_tumor = nib.Nifti1Image(result_array_enhancing_region, affine, header=img.header)
nib.save(img_enhancing_tumor, r'C:\Users\gaspa\Desktop\segmentation_test\prob_dist_results\BRAIN-TUMOR-PROGRESSION_DATASET\probdist_BTP_enhancing_region.nii')




# Visualize probability distribution as a 2D surface plot
collapsed_array = np.sum(result_array_whole_tumor, axis=2)
collapsed_array_plot = collapsed_array / sum(collapsed_array.flatten())
collapsed_array_plot = collapsed_array_plot * 1000

# Create X, Y grids for the surface plot
x = np.arange(0, collapsed_array.shape[1])
y = np.arange(0, collapsed_array.shape[0])
X, Y = np.meshgrid(x, y)

# Plot the surface
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, collapsed_array, cmap='viridis')

ax.set_title("Collapsed Array Surface Plot")
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Values (10^3)")

plt.savefig(r"C:\Users\gaspa\Desktop\segmentation_test\prob_dist_results\BRAIN-TUMOR-PROGRESSION_DATASET\BTP_surface_plot_whole_tumor.png")

# Visualize probability distribution as a 2D surface plot
collapsed_array = np.sum(result_array_edema, axis=2)
collapsed_array_plot = collapsed_array / sum(collapsed_array.flatten())
collapsed_array_plot = collapsed_array_plot * 1000

# Create X, Y grids for the surface plot
x = np.arange(0, collapsed_array.shape[1])
y = np.arange(0, collapsed_array.shape[0])
X, Y = np.meshgrid(x, y)

# Plot the surface
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, collapsed_array, cmap='viridis')

ax.set_title("Collapsed Array Surface Plot")
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Values (10^3)")

plt.savefig(r"C:\Users\gaspa\Desktop\segmentation_test\prob_dist_results\BRAIN-TUMOR-PROGRESSION_DATASET\BTP_surface_plot_edema.png")

collapsed_array = np.sum(result_array_enhancing_region, axis=2)
collapsed_array_plot = collapsed_array / sum(collapsed_array.flatten())
collapsed_array_plot = collapsed_array_plot * 1000

# Create X, Y grids for the surface plot
x = np.arange(0, collapsed_array.shape[1])
y = np.arange(0, collapsed_array.shape[0])
X, Y = np.meshgrid(x, y)

# Plot the surface
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, collapsed_array, cmap='viridis')

ax.set_title("Collapsed Array Surface Plot")
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Values (10^3)")

plt.savefig(r"C:\Users\gaspa\Desktop\segmentation_test\prob_dist_results\BRAIN-TUMOR-PROGRESSION_DATASET\BTP_surface_plot_enhancing_region.png")

collapsed_array = np.sum(result_array_necrotic_core, axis=2)
collapsed_array_plot = collapsed_array / sum(collapsed_array.flatten())
collapsed_array_plot = collapsed_array_plot * 1000

# Create X, Y grids for the surface plot
x = np.arange(0, collapsed_array.shape[1])
y = np.arange(0, collapsed_array.shape[0])
X, Y = np.meshgrid(x, y)

# Plot the surface
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, collapsed_array, cmap='viridis')

ax.set_title("Collapsed Array Surface Plot")
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Values (10^3)")

plt.savefig(r"C:\Users\gaspa\Desktop\segmentation_test\prob_dist_results\BRAIN-TUMOR-PROGRESSION_DATASET\BTP_surface_plot_necrotic_core.png")