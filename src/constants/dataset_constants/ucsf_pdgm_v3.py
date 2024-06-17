import os
from src.analysis import WORK_PATH_CAPTK
from src.constants import DATA_PATH, REGISTRATION_FOLDER, REGISTRATION_FOLDER_CAPTK

UCSF_PDGM_V3_NAME = "UCSF-PDGM-v3"

UCSF_FOLDER_PATH = os.path.join(DATA_PATH, UCSF_PDGM_V3_NAME)

UCSF_REGISTRATION_FOLDER = os.path.join(REGISTRATION_FOLDER, UCSF_PDGM_V3_NAME)

# ============================ BURDENKO CAPTK ============================

UCSF_CAPTK_FOLDER_PATH = os.path.join(WORK_PATH_CAPTK, "datasets", UCSF_PDGM_V3_NAME)
UCSF_CAPTK_REGISTRATION_FOLDER = os.path.join(
    REGISTRATION_FOLDER_CAPTK, UCSF_PDGM_V3_NAME
)

# ============================ Tumor characteristics constants ============================

UCSF_EDEMA = 2
