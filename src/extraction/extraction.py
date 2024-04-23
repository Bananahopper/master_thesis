from common.io.path_operations import (
    extract_save_dir_from_path,
    get_file_list_from_pattern,
)
import nibabel as nib
import logging


class Extractor:
    """
    Extracts the brain from a T1 image using a mask.
    """

    def __init__(
        self,
        t1_pattern: str,
        mask_pattern: str,
    ):

        self.t1_path = t1_pattern
        self.mask_path = mask_pattern

    def run(self):
        t1_files = get_file_list_from_pattern(self.t1_path)
        mask_files = get_file_list_from_pattern(self.mask_path)

        logging.info(
            f"Beginning extarction for t1_pattern: {self.t1_path} and mask_pattern: {self.mask_path}"
        )

        if len(t1_files) != len(mask_files):
            logging.error("Number of T1 files and mask files must be the same.")

        for t1_file, mask_file in zip(t1_files, mask_files):
            self.extract_brain_from_t1(t1_file, mask_file)

        logging.info("Extraction complete.")

    def extract_brain_from_t1(self, t1_file: str, mask_file: str):
        t1_img = nib.load(t1_file)
        mask_img = nib.load(mask_file)
        t1_data = t1_img.get_fdata()
        mask_data = mask_img.get_fdata()
        brain_data = t1_data * mask_data

        # Get Save_path

        save_path = extract_save_dir_from_path(t1_file)

        # Save Brain Image
        brain_img = nib.Nifti1Image(brain_data, t1_img.affine, t1_img.header)
        nib.save(brain_img, f"/{save_path}/masked_t1.nii.gz")
