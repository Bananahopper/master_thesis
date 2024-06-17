import os
import nibabel as nib
import pandas as pd
import argparse


class BrainPlotter:
    def __init__(
        self,
        atlas_path_cort: str,
        atlas_path_sub: str,
        result_path_cort: str,
        result_path_sub: str,
        save_path: str,
    ):

        self.atlas_path_cort = atlas_path_cort
        self.atlas_path_sub = atlas_path_sub
        self.result_path_cort = result_path_cort
        self.result_path_sub = result_path_sub
        self.save_path = save_path
        self.cortical = True if atlas_path_cort != None else False
        self.subcortical = True if atlas_path_sub != None else False

        self.cort_labels = [
            "void",
            "frontal pole",
            "insular cortex",
            "superior frontal gyrus",
            "middle frontal gyrus",
            "inferior frontal gyrus, pars triangularis",
            "inferior frontal gyrus, pars opercularis",
            "precentral gyrus",
            "temporal pole",
            "superior temporal gyrus, anterior division",
            "superior temporal gyrus, posterior division",
            "middle temporal gyrus, anterior division",
            "middle temporal gyrus, posterior division",
            "middle temporal gyrus, temporooccipital part",
            "inferior temporal gyrus, anterior division",
            "inferior temporal gyrus, posterior division",
            "inferior temporal gyrus, temporooccipital part",
            "postcentral gyrus",
            "superior parietal lobule",
            "supramarginal gyrus, anterior division",
            "supramarginal gyrus, posterior division",
            "angular gyrus",
            "lateral occipital cortex, superior division",
            "lateral occipital cortex, inferior division",
            "intracalcarine cortex",
            "frontal medial cortex",
            "juxtapositional lobule cortex",
            "subcallosal cortex",
            "paracingulate gyrus",
            "cingulate gyrus, anterior division",
            "cingulate gyrus, posterior division",
            "precuneous cortex",
            "cuneal cortex",
            "frontal oribtal cortex",
            "parahippocampal gyrus, anterior division",
            "parahippocampal gyrus, posterior division",
            "lingual gyrus",
            "temporal fusiform cortex, anterior division",
            "temporal fusiform cortex, posterior division",
            "temporal occipital fusiform cortex",
            "occipital fusiform gyrus",
            "frontal operculum cortex",
            "central opercular cortex",
            "parietal operculum cortex",
            "planum polare",
            "heschls gyrus",
            "planum temporale",
            "supracalcarine cortex",
            "occipital pole",
        ]
        self.sub_labels = [
            "void",
            "left cerebral white matter",
            "left cerebral cortex",
            "left lateral ventrical",
            "left thalamus",
            "left caudate",
            "left putamen",
            "left pallidum",
            "brain-stem",
            "left hippocampus",
            "left amygdala",
            "left accumbens",
            "right cerebral white matter",
            "right cerebral cortex",
            "right lateral ventricle",
            "right thalamus",
            "right caudate",
            "right putamen",
            "right pallidum",
            "right hippocampus",
            "right amygdala",
            "right accumbens",
        ]

        self.affine_nib = (
            self.atlas_path_cort if self.atlas_path_cort else self.atlas_path_sub
        )
        self.affine = nib.load(self.affine_nib).affine

        self.task_1 = True if self.cortical and not self.subcortical else False
        self.task_2 = True if self.subcortical and not self.cortical else False
        self.task_3 = self.cortical and self.subcortical

    def process(self):

        if self.task_1:
            atlas_dict = self.create_atlas_dict(self.atlas_path_cort, self.cort_labels)
            atlas_dict = [atlas_dict]
            self.atlas_path = [self.atlas_path_cort]
            self.result_path = [self.result_path_cort]

        elif self.task_2:
            atlas_dict = self.create_atlas_dict(self.atlas_path_sub, self.sub_labels)
            atlas_dict = [atlas_dict]
            self.atlas_path = [self.atlas_path_sub]
            self.result_path = [self.result_path_sub]

        elif self.task_3:
            atlas_dict_1 = self.create_atlas_dict(
                self.atlas_path_cort, self.cort_labels
            )
            atlas_dict_2 = self.create_atlas_dict(self.atlas_path_sub, self.sub_labels)

            atlas_dict = [atlas_dict_1, atlas_dict_2]
            self.atlas_path = [self.atlas_path_cort, self.atlas_path_sub]
            self.result_path = [self.result_path_cort, self.result_path_sub]

        atlas_nib_result = self.replace_values_in_nib(
            self.atlas_path, atlas_dict, self.result_path
        )

        print(len(atlas_nib_result))
        self.save_nib(atlas_nib_result)

    def create_atlas_dict(self, atlas_path: str, labels) -> dict:

        atlas_data = nib.load(atlas_path).get_fdata()
        atlas_values = list(set(atlas_data.flatten()))

        atlas_dict = dict(zip(labels, atlas_values))

        return atlas_dict

    def replace_values_in_nib(
        self, atlas_path: list, atlas_dict: list, result_path: list
    ):
        """
        Replace the values in the nibabel file with the values from the result dataframe
        """
        atlas_nib_result = []

        for index, item in enumerate(zip(atlas_path, result_path)):
            print(index)
            print(item)
            atlas, result = item
            print(result)
            result_dict = pd.read_csv(result, index_col=0).to_dict()
            atlas_nib = nib.load(atlas).get_fdata()

            for key, value in atlas_dict[index].items():
                if value == 0:
                    continue
                atlas_nib[atlas_nib == value] = result_dict["Tumor in region"][key]

            atlas_nib_result.append(atlas_nib)

            for atlas_nib in atlas_nib_result:
                atlas_nib = atlas_nib * 100

        return atlas_nib_result

    def save_nib(self, atlas_nib_result: list):

        dataset_name = self.result_path[0].split("/")[-2]

        if not os.path.exists(f"{self.save_path}/{dataset_name}"):
            os.makedirs(f"{self.save_path}/{dataset_name}")

        for index, atlas_nib in enumerate(atlas_nib_result):
            atlas_nib = nib.Nifti1Image(atlas_nib, affine=self.affine)

            nib.save(atlas_nib, f"{self.save_path}/{dataset_name}/{dataset_name}_{"cortical" if index == 0 else "subcortical"}.nii")

            print(f"Saved output{index}.nii to {self.save_path}")


# RUN THE CODE

# atlas_path_cort = "Atlases/HarvardOxford-cort-maxprob-thr25-2mm.nii/HarvardOxford-cort-maxprob-thr25-2mm.nii"
# atlas_path_sub = "Atlases/HarvardOxford-sub-maxprob-thr25-2mm.nii/HarvardOxford-sub-maxprob-thr25-2mm.nii"
# result_path_cort = "per_dataset_BRATS/cortical_stats_for_BRATS.csv"
# result_path_sub = "per_dataset_BRATS/subcortical_stats_for_BRATS.csv"
# save_path = "test"

# bp = BrainPlotter(atlas_path_cort, atlas_path_sub, result_path_cort, result_path_sub, save_path)
# bp.process()


def main(atlas_path_cort, atlas_path_sub, result_path_cort, result_path_sub, save_path):
    bp = BrainPlotter(
        atlas_path_cort, atlas_path_sub, result_path_cort, result_path_sub, save_path
    )
    bp.process()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate probability distribution")
    parser.add_argument(
        "--atlas_path_cort",
        type=str,
        required=True,
        help="Path to the cortical atlas",
    )
    parser.add_argument(
        "--atlas_path_sub",
        type=str,
        required=True,
        help="Path to the subcortical atlas",
    )
    parser.add_argument(
        "--result_path_cort",
        type=str,
        required=True,
        help="Path to the cortical result",
    )
    parser.add_argument(
        "--result_path_sub",
        type=str,
        required=True,
        help="Path to the subcortical result",
    )
    parser.add_argument(
        "--save_path",
        type=str,
        required=True,
        help="Path to save the result",
    )

    args = parser.parse_args()

    main(
        args.atlas_path_cort,
        args.atlas_path_sub,
        args.result_path_cort,
        args.result_path_sub,
        args.save_path,
    )
