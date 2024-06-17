import os
from src.analysis import WORK_PATH_CAPTK
from src.constants import DATA_PATH, REGISTRATION_FOLDER, REGISTRATION_FOLDER_CAPTK

BURDENKO_NAME = "Burdenko-GBM-Progression"

BURDENKO_FOLDER_PATH = os.path.join(DATA_PATH, BURDENKO_NAME)

BURDENKO_REGISTRATION_FOLDER = os.path.join(REGISTRATION_FOLDER, BURDENKO_NAME)

# ============================ BURDENKO CAPTK ============================

BURDENKO_CAPTK_FOLDER_PATH = os.path.join(WORK_PATH_CAPTK, "datasets", BURDENKO_NAME)
BURDNEKO_CAPTK_REGISTRATION_FOLDER = os.path.join(
    REGISTRATION_FOLDER_CAPTK, BURDENKO_NAME
)

# ============================ Tumor characteristics constants ============================

BURDENKO_EDEMA = 2
