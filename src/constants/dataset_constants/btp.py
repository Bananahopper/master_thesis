import os
from src.analysis import WORK_PATH_CAPTK
from src.constants import DATA_PATH, REGISTRATION_FOLDER, REGISTRATION_FOLDER_CAPTK

BTP_NAME = "BTP"

BTP_FOLDER_PATH = os.path.join(DATA_PATH, BTP_NAME)
BTP_CAPTK_FOLDER_PATH = os.path.join(WORK_PATH_CAPTK, "datasets", BTP_NAME)

BTP_REGISTRATION_FOLDER = os.path.join(REGISTRATION_FOLDER, BTP_NAME)

BTP_CAPTK_REGISTRATION_FOLDER = os.path.join(REGISTRATION_FOLDER_CAPTK, BTP_NAME)

# ============================ Tumor characteristics constants ============================

BTP_EDEMA = 2
