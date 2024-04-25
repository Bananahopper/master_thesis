import os
from src.constants import DATA_PATH, REGISTRATION_FOLDER

BURDENKO_NAME = "Burdenko"

BURDENKO_FOLDER_PATH = os.path.join(DATA_PATH, BURDENKO_NAME)
T1_PATH_PATTERN = os.path.join(BURDENKO_FOLDER_PATH, "*", "T1.nii.gz")
SEG_PATH_PATTERN = os.path.join(BURDENKO_FOLDER_PATH, "*", "seg.nii.gz")
