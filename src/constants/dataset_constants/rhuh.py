import os
from src.analysis import WORK_PATH_CAPTK
from src.constants import DATA_PATH, REGISTRATION_FOLDER

RHUH_NAME = "RHUH_GBM"

RHUH_FOLDER_PATH = os.path.join(DATA_PATH, RHUH_NAME)
RHUH_FOLDER_PATH_CAPTK = os.path.join(WORK_PATH_CAPTK, "datasets", RHUH_NAME)

T1_PATH_PATTERN = os.path.join(RHUH_FOLDER_PATH, "*", "0", "*adc.nii.gz")
SEG_PATH_PATTERN = os.path.join(RHUH_FOLDER_PATH, "*", "0", "*segmentations.nii.gz")

RHUH_REGISTRATION_FOLDER = os.path.join(REGISTRATION_FOLDER, RHUH_NAME)
