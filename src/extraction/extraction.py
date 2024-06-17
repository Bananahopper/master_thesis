from src.common.io.path_operations import (
    extract_file_name_from_path,
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
        image_pattern: str,
        mask_pattern: str,
    ):

        self.image_path = image_pattern
        self.mask_path = mask_pattern

    def run(self):
        image_files = get_file_list_from_pattern(self.image_path)
        mask_files = get_file_list_from_pattern(self.mask_path)

        logging.info(
            f"Beginning extarction for image_pattern: {self.image_path} and mask_pattern: {self.mask_path}"
        )

        if len(image_files) != len(mask_files):
            logging.error("Number of T1 files and mask files must be the same.")

        for image_file, mask_file in zip(image_files, mask_files):
            self.extract_brain_from_image(image_file, mask_file)

        logging.info("Extraction complete.")

    def extract_brain_from_image(self, image_file: str, mask_file: str):
        image_img = nib.load(image_file)
        mask_img = nib.load(mask_file)
        image_data = image_img.get_fdata()
        mask_data = mask_img.get_fdata()
        brain_data = image_data * mask_data

        # Get Save_path

        save_path = extract_save_dir_from_path(image_file)

        filename = extract_file_name_from_path(image_file)

        # Save Brain Image
        brain_img = nib.Nifti1Image(brain_data, image_img.affine, image_img.header)
        nib.save(brain_img, f"/{save_path}/masked_{filename}")
