import os
from src.constants.dataset_constants.rhuh import RHUH_REGISTRATION_FOLDER


def extract_subject_id_from_rhuh_path(path: str):
    """
    Extracts the subject id from the path.

    Args:
        path (str): path to the file

    Returns:
        tuple[str, str]: subject id and file name
    """
    path_parts = path.split(os.sep)
    return path_parts[-3], path_parts[-1]


def create_registration_folder_for_rhuh_subject(subject_id: str):
    """
    Creates the registration folder for a RHUH subject.

    Args:
        subject_id (str): subject id

    Returns:
        str: path to the registration folder
    """

    subject_folder = os.path.join(RHUH_REGISTRATION_FOLDER, subject_id)

    if not os.path.exists(subject_folder):
        os.makedirs(subject_folder)

    return subject_folder
