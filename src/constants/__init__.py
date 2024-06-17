import os

# ============================ PATH CONSTANTS ============================
WORK_PATH = "/"
DATA_PATH = os.path.join(WORK_PATH, "datasets")
REGISTRATION_FOLDER = os.path.join(WORK_PATH, "output_registration")

WORK_PATH_CAPTK = "/scratch/users/ggaspar/CaPTk"
REGISTRATION_FOLDER_CAPTK = os.path.join(WORK_PATH_CAPTK, "output_registration")
LOG_FOLDER = os.path.join(WORK_PATH_CAPTK, "logs")

# ============================ NAME CONSTANTS ============================
AFFINE_NAME = "affine.mat"
WARP_NAME = "warp.nii.gz"
INVERSE_WARP_NAME = "inverse_warp.nii.gz"

# ============================ ATLAS CONSTANTS ============================
MNI_ATLAS_PATH = "src/constants/atlases/mni_icbm152_t1_tal_nlin_asym_09a_brain_only/mni_icbm152_t1_tal_nlin_asym_09a_brain_only.nii"
SRI_ATLAS_PATH = "src/constants/atlases/sri24_spm8/templates/T1_brain.nii"
HARVARD_CORT_ATLAS_PATH = "src/constants/atlases/HarvardOxford-cort-maxprob-thr25-2mm.nii/HarvardOxford-cort-maxprob-thr25-2mm.nii"
HARVARD_SUB_ATLAS_PATH = "src/constants/atlases/HarvardOxford-sub-maxprob-thr25-2mm.nii/HarvardOxford-sub-maxprob-thr25-2mm.nii"
CONNECTOME_MNI_ATLAS = (
    "src/constants/atlases/masked_mni_icbm152_t1_tal_nlin_asym_09c.nii"
)
CONNECTOME_BUNDCOUNT = "src/constants/atlases/wmatlas.scale1.bundcount.nii"

# ============================ CREATE FOLDERS ============================
# if not os.path.exists(LOG_FOLDER):
#     os.makedirs(LOG_FOLDER)
