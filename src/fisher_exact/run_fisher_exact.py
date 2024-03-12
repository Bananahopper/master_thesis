import numpy as np
import nibabel as nib
import math

def perform_fisher_test(dataset1_path: str, 
                        dataset2_path: str,
                        save_path: str,
                        size1: int, 
                        size2: int):
    """
    Perform Fisher's exact test between two datasets.

    Args:
        dataset1_path (str): Path to the first dataset.
        dataset2_path (str): Path to the second dataset.
        save_path (str): Path to save the result.
        size1 (int): Size of the first dataset.
        size2 (int): Size of the second dataset.
    """
    # Load datasets
    file_ds1 = nib.load(dataset1_path)
    img_ds1 = file_ds1.get_fdata()
    file_ds2 = nib.load(dataset2_path)
    img_ds2 = file_ds2.get_fdata()

    # Initialize result array
    result_array = np.zeros_like(img_ds1, dtype=float)
    shape = result_array.shape

    # Flatten datasets
    x = img_ds1.flatten()
    y = img_ds2.flatten()
    z = result_array.flatten()

    # Perform Fisher's exact test for each voxel
    for i, value in enumerate(x):
        a = int(value)
        b = int(y[i])
        c = size1 - a
        d = size2 - b
        n = size1 + size2
         
        # Calculate p-value using Fisher's exact test formula
        p = ((math.factorial(a + b)) * (math.factorial(c + d)) * 
             (math.factorial(a + c)) * (math.factorial(b + d))) / \
            ((math.factorial(a)) * (math.factorial(b)) * 
             (math.factorial(c)) * (math.factorial(d)) * (math.factorial(n)))

        z[i] = p

    # Reshape result array
    result_array = z.reshape(shape)

    # Retain only p-values less than 0.01
    mask = result_array < 0.01
    filtered_array = np.zeros_like(result_array)
    filtered_array[mask] = result_array[mask]
    filtered_array = np.nan_to_num(filtered_array)

    # Save the result
    img = nib.Nifti1Image(filtered_array, affine=img_ds1.affine)
    nib.save(img, save_path)


perform_fisher_test('prob_dist_results/RHUH_DATASET/probdist_RHUH_whole_tumor.nii', 'prob_dist_results/BRAIN-TUMOR-PROGRESSION_DATASET/probdist_BTP_whole_tumor.nii', 39, 20)
