import os

from src.constants.dataset_constants.ucsf_pdgm_v3 import (
    UCSF_CAPTK_FOLDER_PATH,
    UCSF_CAPTK_REGISTRATION_FOLDER,
    UCSF_EDEMA,
)
from src.constants.dataset_constants.brats import (
    BRATS_CAPTK_FOLDER_PATH,
    BRATS_CAPTK_REGISTRATION_FOLDER,
    BRATS_EDEMA,
    BRATS_SSA_CAPTK_FOLDER_PATH,
    BRATS_SSA_CAPTK_REGISTRATION_FOLDER,
)
from src.constants.dataset_constants.btp import (
    BTP_CAPTK_FOLDER_PATH,
    BTP_CAPTK_REGISTRATION_FOLDER,
    BTP_EDEMA,
)
from src.constants.dataset_constants.burdenko import (
    BURDENKO_CAPTK_FOLDER_PATH,
    BURDENKO_EDEMA,
    BURDNEKO_CAPTK_REGISTRATION_FOLDER,
)
from src.constants.dataset_constants.lgg_1p19qdeletion import (
    LGG_1P19QDELETION_CAPTK_REGISTRATION_FOLDER,
    LGG_1P19QDELETION_FOLDER_PATH_CAPTK,
    LGG_EDEMA,
)
from src.constants.dataset_constants.qin import (
    QIN_CAPTK_FOLDER_PATH,
    QIN_CAPTK_REGISTRATION_FOLDER,
    QIN_EDEMA,
)
from src.constants.dataset_constants.rhuh import (
    RHUH_CAPTK_REGISTRATION_FOLDER,
    RHUH_EDEMA,
    RHUH_FOLDER_PATH_CAPTK,
)


def get_edema_value(path: str):

    if path.startswith(BRATS_CAPTK_REGISTRATION_FOLDER) or path.startswith(
        BRATS_CAPTK_FOLDER_PATH
    ):
        edema = int(BRATS_EDEMA)

    elif path.startswith(BRATS_SSA_CAPTK_REGISTRATION_FOLDER) or path.startswith(
        BRATS_SSA_CAPTK_FOLDER_PATH
    ):
        edema = int(BRATS_EDEMA)

    elif path.startswith(QIN_CAPTK_REGISTRATION_FOLDER) or path.startswith(
        QIN_CAPTK_FOLDER_PATH
    ):
        edema = int(QIN_EDEMA)

    elif path.startswith(RHUH_CAPTK_REGISTRATION_FOLDER) or path.startswith(
        RHUH_FOLDER_PATH_CAPTK
    ):
        edema = int(RHUH_EDEMA)
    elif path.startswith(BURDNEKO_CAPTK_REGISTRATION_FOLDER) or path.startswith(
        BURDENKO_CAPTK_FOLDER_PATH
    ):
        edema = int(BURDENKO_EDEMA)
    elif path.startswith(BTP_CAPTK_REGISTRATION_FOLDER) or path.startswith(
        BTP_CAPTK_FOLDER_PATH
    ):
        edema = int(BTP_EDEMA)
    elif path.startswith(
        LGG_1P19QDELETION_CAPTK_REGISTRATION_FOLDER
    ) or path.startswith(LGG_1P19QDELETION_FOLDER_PATH_CAPTK):
        edema = int(LGG_EDEMA)

    elif path.startswith(UCSF_CAPTK_REGISTRATION_FOLDER) or path.startswith(
        UCSF_CAPTK_FOLDER_PATH
    ):
        edema = int(UCSF_EDEMA)

    return edema
