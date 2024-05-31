import os
from src.constants import DATA_PATH, REGISTRATION_FOLDER, WORK_PATH_CAPTK

LGG_1P19QDELETION_NAME = "LGG-1p19qDeletion"

LGG_1P19QDELETION_FOLDER_PATH = os.path.join(DATA_PATH, LGG_1P19QDELETION_NAME)
LGG_1P19QDELETION_FOLDER_PATH_CAPTK = os.path.join(
    WORK_PATH_CAPTK, "datasets", LGG_1P19QDELETION_NAME
)

LGG_1P19QDELETION_REGISTRATION_FOLDER = os.path.join(
    REGISTRATION_FOLDER, LGG_1P19QDELETION_NAME
)

# ============================ Tumor characteristics constants ============================

LGG_EDEMA = 2
