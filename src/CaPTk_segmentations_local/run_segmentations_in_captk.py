import glob
import os
import subprocess

tool_dir = r"C:\CaPTk_Full\1.9.0\bin\BraTSPipeline.exe"
data_dir = r"C:\Users\gaspa\Desktop\segmentation_test"
dir_number = glob.glob("BRAIN-TUMO-PROGRESSION_DATASET\Brain-Tumor-Progression\sub-*")

files_t1 = glob.glob(r"BRAIN-TUMO-PROGRESSION_DATASET\Brain-Tumor-Progression\sub-0*\ses-*\anat\*_acq-T1post_ce-*.nii.gz")
files_t2 = glob.glob(r"BRAIN-TUMO-PROGRESSION_DATASET\Brain-Tumor-Progression\sub-0*\ses-*\anat\*T2w.nii.gz")
files_t1ce = glob.glob(r"BRAIN-TUMO-PROGRESSION_DATASET\Brain-Tumor-Progression\sub-0*\ses-*\anat\*_acq-T1prereg_run-*.nii.gz")
files_flair = glob.glob(r"BRAIN-TUMO-PROGRESSION_DATASET\Brain-Tumor-Progression\sub-0*\ses-*\anat\*_FLAIR.nii.gz")

print(dir_number)

for i, dir in enumerate(dir_number):
    # Set the path to the input image
    input_image_t1 = os.path.join(data_dir, f"{files_t1[i]}")
    input_image_t2 = os.path.join(data_dir, f"{files_t2[i]}")
    input_image_t1ce = os.path.join(data_dir, f"{files_t1ce[i]}")
    input_image_flair = os.path.join(data_dir, f"{files_flair[i]}")

    output_segmentation = os.path.join(data_dir, dir, f"BraTSPipeline_sub{i}")

    command_to_run = f"{tool_dir} -t1 {input_image_t1} -t1c {input_image_t1ce} -t2 {input_image_t2} -fl {input_image_flair} -o {output_segmentation}"

    process = subprocess.Popen(["powershell.exe", command_to_run])
    process.wait()