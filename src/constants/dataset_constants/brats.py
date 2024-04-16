import os
from src.constants import DATA_PATH, REGISTRATION_FOLDER

BRATS_NAME = "Brats2021_wTumor"

BRATS_FOLDER_PATH = os.path.join(DATA_PATH, BRATS_NAME)
T1_PATH_PATTERN = os.path.join(BRATS_FOLDER_PATH, "*", "*_t1.nii.gz")
SEG_PATH_PATTERN = os.path.join(BRATS_FOLDER_PATH, "*", "*_seg.nii.gz")

BRATS_REGISTRATION_FOLDER = os.path.join(REGISTRATION_FOLDER, BRATS_NAME)
