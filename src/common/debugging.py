from src.common.io.path_operations import extract_subject_id_from_file_path


def check_sub_with_missing_files(filelist1, filelist2):
    for idx, (file1, file2) in enumerate(zip(filelist1, filelist2)):
        file1_sub, _, _ = extract_subject_id_from_file_path(file1)
        file2_sub, _, _ = extract_subject_id_from_file_path(file2)

        if file1_sub != file2_sub:
            if file1_sub != None:
                return file1_sub
            elif file2_sub != None:
                return file2_sub
            else:
                idx_message = f"Index of subject list: {idx}"
                return idx_message
