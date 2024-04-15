import os

# ============================ PATH CONSTANTS ============================
WORK_PATH = "/scratch/users/ggaspar/CaPTk"
DATA_PATH = os.path.join(WORK_PATH, "datasets")
REGISTRATION_FOLDER = os.path.join(WORK_PATH, "output_registration")

# ============================ NAME CONSTANTS ============================
AFFINE_NAME = "affine.mat"
WARP_NAME = "warp.nii.gz"
INVERSE_WARP_NAME = "inverse_warp.nii.gz"

if not os.path.exists(REGISTRATION_FOLDER):
    os.makedirs(REGISTRATION_FOLDER)
