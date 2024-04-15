from src.registration.registrator import Registrator

# Run the registration

registrator = Registrator(
    "/scratch/users/ggaspar/CaPTk/atlases/mni_icbm152_t1_tal_nlin_asym_09a_brain_only.nii",
    "/scratch/users/ggaspar/CaPTk/atlases/HarvardOxford-cort-maxprob-thr25-2mm.nii",
    "/scratch/users/ggaspar/CaPTk/atlases/HarvardOxford-sub-maxprob-thr25-2mm.nii",
)

registrator.run(
    "/scratch/users/ggaspar/CaPTk/datasets/Brats2021_wTumor/*/*_t1.nii.gz",
    "/scratch/users/ggaspar/CaPTk/datasets/Brats2021_wTumor/*/*_seg.nii.gz",
)
