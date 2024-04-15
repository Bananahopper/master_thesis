import glob
import os
from common.io.brats_path_operation import (
    create_registration_folder_for_brats_subject,
    extract_subject_id_from_brats_path,
)
from constants.dataset_constants.brats import BRATS_FOLDER_PATH


def get_file_list_from_pattern(pattern: str):
    """
    Get a list of files from a pattern.
    """
    path = glob.glob(pattern)
    path.sort()
    return path


def extract_subject_id_from_file_path(path: str) -> tuple[str, str]:
    """
    Extracts the subject id from the path.

    Args:
        path (str): path to the file

    Returns:
        tuple[str, str]: subject id and file name
    """
    if path.startswith(BRATS_FOLDER_PATH):
        return extract_subject_id_from_brats_path(path)
    else:
        raise ValueError("Path does not match any dataset.")
    # elif path.startswith(QIN_FOLDER_PATH):
    # return extract_subject_id_from_qin_path(path)


def create_registration_folder_for_subject_file_path(
    path: str,
) -> tuple[str, str, str, str]:
    """
    Creates the registration folder for a subject.

    Args:
        path (str): path to the file

    Returns:
        tuple[str, str, str, str]: path to the subject folder, affine folder, warp folder, and inverse warp folder
    """
    subject_id, _ = extract_subject_id_from_file_path(path)
    if path.startswith(BRATS_FOLDER_PATH):
        subject_folder = create_registration_folder_for_brats_subject(subject_id)

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
