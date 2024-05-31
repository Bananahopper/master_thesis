import os

from src.constants.dataset_constants.ucsf_pdgm_v3 import (
    UCSF_CAPTK_FOLDER_PATH,
    UCSF_EDEMA,
    UCSF_FOLDER_PATH,
)
from src.constants.dataset_constants.brats import (
    BRATS_CAPTK_FOLDER_PATH,
    BRATS_EDEMA,
    BRATS_FOLDER_PATH,
    BRATS_SSA_CAPTK_FOLDER_PATH,
    BRATS_SSA_FOLDER_PATH,
)
from src.constants.dataset_constants.btp import BTP_EDEMA, BTP_FOLDER_PATH
from src.constants.dataset_constants.burdenko import (
    BURDENKO_CAPTK_FOLDER_PATH,
    BURDENKO_EDEMA,
    BURDENKO_FOLDER_PATH,
)
from src.constants.dataset_constants.lgg_1p19qdeletion import (
    LGG_1P19QDELETION_FOLDER_PATH,
    LGG_1P19QDELETION_FOLDER_PATH_CAPTK,
    LGG_EDEMA,
)
from src.constants.dataset_constants.qin import (
    QIN_CAPTK_FOLDER_PATH,
    QIN_EDEMA,
    QIN_FOLDER_PATH,
)
from src.constants.dataset_constants.rhuh import (
    RHUH_EDEMA,
    RHUH_FOLDER_PATH,
    RHUH_FOLDER_PATH_CAPTK,
)


def get_edema_value(path: str):

    if path.startswith(BRATS_FOLDER_PATH) or path.startswith(BRATS_CAPTK_FOLDER_PATH):
        edema = BRATS_EDEMA

    elif path.startswith(BRATS_SSA_FOLDER_PATH) or path.startswith(
        BRATS_SSA_CAPTK_FOLDER_PATH
    ):
        edema = BRATS_EDEMA

    elif path.startswith(QIN_FOLDER_PATH) or path.startswith(QIN_CAPTK_FOLDER_PATH):
        edema = QIN_EDEMA

    elif path.startswith(RHUH_FOLDER_PATH) or path.startswith(RHUH_FOLDER_PATH_CAPTK):
        edema = RHUH_EDEMA
    elif path.startswith(BURDENKO_FOLDER_PATH) or path.startswith(
        BURDENKO_CAPTK_FOLDER_PATH
    ):
        edema = BURDENKO_EDEMA
    elif path.startswith(BTP_FOLDER_PATH):
        edema = BTP_EDEMA
    elif path.startswith(LGG_1P19QDELETION_FOLDER_PATH) or path.startswith(
        LGG_1P19QDELETION_FOLDER_PATH_CAPTK
    ):
        edema = LGG_EDEMA

    elif path.startswith(UCSF_FOLDER_PATH) or path.startswith(UCSF_CAPTK_FOLDER_PATH):
        edema = UCSF_EDEMA

    return edema
