import numpy as np
import nibabel as nib
import math
import multiprocessing as mp

fileRHUH = nib.load('prob_dist_results/RHUH_DATASET/probdist_RHUH.nii')
imgRHUH = fileRHUH.get_fdata()
fileBTP = nib.load('prob_dist_results/BRAIN-TUMOR-PROGRESSION_DATASET/probdist_BTP.nii')
imgBTP = fileBTP.get_fdata()

# Iterate over every voxel and calculate the probability of the voxel being a tumor voxel

result_array = np.zeros_like(imgRHUH, dtype=float)

for (x_RHUH,y_RHUH,z_RHUH), valueRHUH in np.ndenumerate(imgRHUH):
    for (x_BTP,y_BTP,z_BTP), valueBTP in np.ndenumerate(imgBTP):
        a = int(valueRHUH)
        b = int(valueBTP)
        c = 39 - a
        d = 20 - b
        n = 2
         
        p = (math.factorial(a + b)*math.factorial(c + d)*math.factorial(a + c)*math.factorial(b + d)) / (math.factorial(a)*math.factorial(b)*math.factorial(c)*math.factorial(d)*math.factorial(n))

        result_array[x_RHUH, y_RHUH, z_RHUH] = p


# Save the result
img = nib.Nifti1Image(result_array, affine=imgBTP.affine)
nib.save(img, 'prob_dist_results/combined_prob_dist.nii')