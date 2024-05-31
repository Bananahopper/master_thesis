import os
from src.constants.dataset_constants.brats import BRATS_REGISTRATION_FOLDER


def extract_subject_id_from_brats_path(path: str):
    """
    Extracts the subject id from the path.

    Args:
        path (str): path to the file

    Returns:
        tuple[str, str]: subject id, file name, and dataset name
    """
    path_parts = path.split(os.sep)
    return path_parts[-2], path_parts[-1], path_parts[-3]


def create_registration_folder_for_brats_subject(
    dataset_name_constant: str, subject_id: str
) -> str:
    """
    Creates the registration folder for a BRATS subject.

    Args:
        subject_id (str): subject id

    Returns:
        str: path to the registration folder
    """
    subject_folder = os.path.join(dataset_name_constant, subject_id)

    if not os.path.exists(subject_folder):
        os.makedirs(subject_folder)

    return subject_folder
