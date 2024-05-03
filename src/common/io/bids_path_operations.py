import os
from src.constants.dataset_constants.qin import QIN_REGISTRATION_FOLDER


def extract_subject_id_from_bids_path(path: str):
    """
    Extracts the subject id from the path.

    Args:
        path (str): path to the file

    Returns:
        tuple[str, str]: subject id, file name, and dataset name
    """
    path_parts = path.split(os.sep)
    return path_parts[-4], path_parts[-1], path_parts[-5]


def create_registration_folder_for_bids_subject(
    dataset_name_constant: str, subject_id: str
):
    """
    Creates the registration folder for a QIN subject.

    Args:
        subject_id (str): subject id

    Returns:
        str: path to the registration folder
    """

    subject_folder = os.path.join(dataset_name_constant, subject_id)

    if not os.path.exists(subject_folder):
        os.makedirs(subject_folder)

    return subject_folder


def extract_subject_id_from_bids_path_exception(path: str):
    """
    Extracts the subject id from the path.

    Args:
        path (str): path to the file

    Returns:
        tuple[str, str]: subject id, file name, and dataset name
    """
    path_parts = path.split(os.sep)
    return path_parts[-2], path_parts[-1], path_parts[-3]
