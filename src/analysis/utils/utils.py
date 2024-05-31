import numpy as np


def pad_or_trim_to_match(
    target_array: np.array, source_array: np.array, tolerance: list
):
    """
    Pad or trim the source array to match the shape of the target array.

    Args:
        target_array (np.array): The target array to match.
        source_array (np.array): The source array to pad or trim.
        tolerance (list): The maximum amount to pad or trim from the last dimension.

    Returns:
        np.array: The source array with the same shape as the target array.
    """
    target_shape = target_array.shape

    if target_shape[2] < source_array.shape[2]:
        trim_amounts = [
            (s2 - s1) if s2 > s1 else 0
            for s1, s2 in zip(target_shape, source_array.shape)
        ]

        trim_indices = [
            (amount // 2, amount - (amount // 2)) for amount in trim_amounts
        ]

        for item in trim_indices:
            if item[0] > tolerance[0] and item[1] > tolerance[1]:
                raise ValueError(f"Trim indices are too large {trim_indices}")

        slices = tuple(
            slice(start, source_array.shape[i] - end)
            for i, (start, end) in enumerate(trim_indices)
        )

        source_array = source_array[slices]

    else:
        pad_width = [
            (0, max(0, s1 - s2))
            for s1, s2 in zip(target_array.shape, source_array.shape)
        ]
        source_array = np.pad(
            source_array, pad_width=pad_width, mode="constant", constant_values=0
        )

    return source_array


def extract_voxel_dimensions_from_nifti(nifti_file: str):
    """
    Extract the voxel dimensions from a nifti file.

    Args:
        nifti_file (str): The path to the nifti file.

    Returns:
        tuple: The voxel dimensions.
    """
    import nibabel as nib

    img = nib.load(nifti_file)
    voxel_dimensions = (img.header["pixdim"])[1:4]

    print("Voxel dimensions:")
    print("  x = {} mm".format(voxel_dimensions[0]))
    print("  y = {} mm".format(voxel_dimensions[1]))
    print("  z = {} mm".format(voxel_dimensions[2]))
