import os
from src.constants import DATA_PATH, REGISTRATION_FOLDER

QIN_NAME = "QIN"

QIN_FOLDER_PATH = os.path.join(DATA_PATH, QIN_NAME)
T1_PATH_PATTERN = os.path.join(QIN_FOLDER_PATH, "*", "*", "anat", "masked_t1.nii.gz")
SEG_PATH_PATTERN = os.path.join(QIN_FOLDER_PATH, "*", "*", "anat", "*tumor_mask.nii.gz")

QIN_REGISTRATION_FOLDER = os.path.join(REGISTRATION_FOLDER, QIN_NAME)
