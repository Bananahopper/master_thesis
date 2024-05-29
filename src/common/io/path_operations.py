import glob
import os
from src.constants.dataset_constants.btp import BTP_REGISTRATION_FOLDER
from src.constants.dataset_constants.btp import BTP_FOLDER_PATH
from src.constants.dataset_constants.burdenko import (
    BURDENKO_CAPTK_FOLDER_PATH,
    BURDENKO_FOLDER_PATH,
    BURDENKO_REGISTRATION_FOLDER,
)
from src.constants.dataset_constants.rhuh import (
    RHUH_FOLDER_PATH,
    RHUH_FOLDER_PATH_CAPTK,
)
from src.common.io.rhuh_path_operations import (
    create_registration_folder_for_rhuh_subject,
    extract_subject_id_from_rhuh_path,
)
from src.common.io.bids_path_operations import (
    extract_subject_id_from_bids_path,
    create_registration_folder_for_bids_subject,
    extract_subject_id_from_bids_path_exception,
)
from src.constants.dataset_constants.qin import (
    QIN_CAPTK_FOLDER_PATH,
    QIN_FOLDER_PATH,
    QIN_REGISTRATION_FOLDER,
)
from src.constants.dataset_constants.lgg_1p19qdeletion import (
    LGG_1P19QDELETION_FOLDER_PATH,
    LGG_1P19QDELETION_FOLDER_PATH_CAPTK,
    LGG_1P19QDELETION_REGISTRATION_FOLDER,
)
from src.common.io.brats_path_operation import (
    create_registration_folder_for_brats_subject,
    extract_subject_id_from_brats_path,
)
from src.constants.dataset_constants.brats import (
    BRATS_CAPTK_FOLDER_PATH,
    BRATS_FOLDER_PATH,
)


def get_file_list_from_pattern(pattern: str):
    """
    Get a list of files from a pattern.
    """
    path = glob.glob(pattern)
    path.sort()
    return path


def extract_subject_id_from_file_path(path: str):
    """
    Extracts the subject id from the path.

    Args:
        path (str): path to the file

    Returns:
        tuple[str, str]: subject id and file name
    """
    if path.startswith(BRATS_FOLDER_PATH) or path.startswith(BRATS_CAPTK_FOLDER_PATH):
        return extract_subject_id_from_brats_path(path)
    elif path.startswith(QIN_FOLDER_PATH) or path.startswith(QIN_CAPTK_FOLDER_PATH):
        return extract_subject_id_from_bids_path(path)
    elif path.startswith(RHUH_FOLDER_PATH) or path.startswith(RHUH_FOLDER_PATH_CAPTK):
        return extract_subject_id_from_rhuh_path(path)
    elif path.startswith(BURDENKO_FOLDER_PATH) or path.startswith(
        BURDENKO_CAPTK_FOLDER_PATH
    ):
        return extract_subject_id_from_bids_path_exception(path)
    elif path.startswith(BTP_FOLDER_PATH):
        return extract_subject_id_from_bids_path(path)
    elif path.startswith(LGG_1P19QDELETION_FOLDER_PATH) or path.startswith(
        LGG_1P19QDELETION_FOLDER_PATH_CAPTK
    ):
        return extract_subject_id_from_bids_path(path)


def create_registration_folder_for_subject_file_path(
    path: str,
):
    """
    Creates the registration folder for a subject.

    Args:
        path (str): path to the file

    Returns:
        tuple[str, str, str, str]: path to the subject folder, affine folder, warp folder, and inverse warp folder
    """
    subject_id, _, _ = extract_subject_id_from_file_path(path)
    if path.startswith(BRATS_FOLDER_PATH):
        subject_folder = create_registration_folder_for_brats_subject(subject_id)
    elif path.startswith(QIN_FOLDER_PATH):
        subject_folder = create_registration_folder_for_bids_subject(
            QIN_REGISTRATION_FOLDER, subject_id
        )
    elif path.startswith(RHUH_FOLDER_PATH):
        subject_folder = create_registration_folder_for_rhuh_subject(subject_id)
    elif path.startswith(BURDENKO_FOLDER_PATH):
        subject_folder = create_registration_folder_for_bids_subject(
            BURDENKO_REGISTRATION_FOLDER, subject_id
        )
    elif path.startswith(BTP_FOLDER_PATH):
        subject_folder = create_registration_folder_for_bids_subject(
            BTP_REGISTRATION_FOLDER, subject_id
        )
    elif path.startswith(LGG_1P19QDELETION_FOLDER_PATH):
        subject_folder = create_registration_folder_for_bids_subject(
            LGG_1P19QDELETION_REGISTRATION_FOLDER, subject_id
        )

    affine_folder = os.path.join(subject_folder, "affine")
    if not os.path.exists(affine_folder):
        os.makedirs(affine_folder)

    warp_folder = os.path.join(subject_folder, "warp")
    if not os.path.exists(warp_folder):
        os.makedirs(warp_folder)

    inverse_warp_folder = os.path.join(subject_folder, "inverse_warp")
    if not os.path.exists(inverse_warp_folder):
        os.makedirs(inverse_warp_folder)

    return subject_folder, affine_folder, warp_folder, inverse_warp_folder


def create_registration_folder_for_subject_file_path_multiple_images(
    path: str,
    modality: str,
):
    """
    Creates a seperate registration folder for the registration of all available modalities, and a subject folder.

    Args:
        path (str): path to the file
        modality (str): modality of the file

    Returns:
        tuple[str, str, str, str]: path to the modality folder, affine folder, warp folder, and inverse warp folder
    """
    subject_id, _ = extract_subject_id_from_file_path(path)
    if path.startswith(BRATS_FOLDER_PATH):
        subject_folder = create_registration_folder_for_brats_subject(subject_id)
    elif path.startswith(QIN_FOLDER_PATH):
        subject_folder = create_registration_folder_for_bids_subject(
            QIN_REGISTRATION_FOLDER, subject_id
        )
    elif path.startswith(RHUH_FOLDER_PATH):
        subject_folder = create_registration_folder_for_rhuh_subject(subject_id)
    elif path.startswith(BURDENKO_FOLDER_PATH):
        subject_folder = create_registration_folder_for_bids_subject(
            BURDENKO_REGISTRATION_FOLDER, subject_id
        )

    multiple_images_folder = os.path.join(subject_folder, "multiple_images")
    if not os.path.exists(multiple_images_folder):
        os.makedirs(multiple_images_folder)

    modality_folder = os.path.join(multiple_images_folder, modality)
    if not os.path.exists(modality_folder):
        os.makedirs(modality_folder)

    affine_folder = os.path.join(modality_folder, "affine")
    if not os.path.exists(affine_folder):
        os.makedirs(affine_folder)

    warp_folder = os.path.join(modality_folder, "warp")
    if not os.path.exists(warp_folder):
        os.makedirs(warp_folder)

    inverse_warp_folder = os.path.join(modality_folder, "inverse_warp")
    if not os.path.exists(inverse_warp_folder):
        os.makedirs(inverse_warp_folder)

    return modality_folder, affine_folder, warp_folder, inverse_warp_folder


def extract_srf_from_prob_dist_path(path: str):
    """
    Extracts the subject id from the path.

    Returns:
        tuple[str, str, str]: patient id, registration modality, and file name
    """
    path_split = path.split(os.sep)
    dataset_name = path_split[-4]
    subject_id = path_split[-3]
    registration_modality = path_split[-2]
    file_name = path_split[-1]

    return dataset_name, subject_id, registration_modality, file_name


def extract_save_dir_from_path(path: str):
    """
    Extracts the save directory from the path.

    Args:
        path (str): path to the file

    Returns:
        str: save directory
    """
    path_split = path.split(os.sep)
    save_dir = os.path.join(*path_split[:-4])

    return save_dir


def extract_file_name_from_path(path: str):
    """
    Extracts the file name from the path.

    Args:
        path (str): path to the file

    Returns:
        str: file name
    """
    path_split = path.split(os.sep)
    return path_split[-1]


def extract_fsd_from_output_analysis_path(path: str):
    """
    Extracts the subject id, file name, and dataset name from the output_analysis path.

    Args:
        path (str): path to the file

    Returns:
        tuple[str, str, str]: subject id, file name, and dataset name
    """

    path_parts = path.split(os.sep)
    return path_parts[-2], path_parts[-1], path_parts[-4]
