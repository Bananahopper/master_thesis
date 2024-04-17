import os


def extract_subject_id_and_dataset_name(path: str):
    """
    Extracts the subject id and dataset name from the path.

    Args:
        path (str): path to the file

    Returns:
        tuple[str, str]: dataset name and subject id
    """
    split_path = path.split(os.sep)
    dataset_name = split_path[-2]
    subject_id = split_path[-1]

    return dataset_name, subject_id
