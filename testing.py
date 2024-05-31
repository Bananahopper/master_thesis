from src.analysis.utils.utils import extract_voxel_dimensions_from_nifti

path = "src/constants/atlases/mni_icbm152_t1_tal_nlin_asym_09a_brain_only/mni_icbm152_t1_tal_nlin_asym_09a_brain_only.nii"

print(extract_voxel_dimensions_from_nifti(path))
