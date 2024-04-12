import os

# ============================ PATH CONSTANTS ============================
DATA_PATH = os.path.join(os.getcwd(), "datasets")
REGISTRATION_FOLDER = os.path.join(os.getcwd(), "output_registration")

# ============================ NAME CONSTANTS ============================
AFFINE_NAME = "affine.mat"
WARP_NAME = "warp.nii.gz"
INVERSE_WARP_NAME = "inverse_warp.nii.gz"

if not os.path.exists(REGISTRATION_FOLDER):
    os.makedirs(REGISTRATION_FOLDER)
