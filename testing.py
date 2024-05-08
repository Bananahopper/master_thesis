import pandas as pd
import glob

"Burdenko-GBM-Progression/per_region_dist/sub-*/*_cortical.csv"
"Burdenko-GBM-Progression/per_region_dist/sub-*/*_subcortical.csv"


def test(cort_pattern, sub_pattern):
    data_cort = glob.glob(cort_pattern)
    data_sub = glob.glob(sub_pattern)

    for idx, (cort, sub) in enumerate(zip(data_cort, data_sub)):
        if cort is None or sub is None:
            print(f"No data found in {idx}")
            return

        df_cort = pd.read_csv(cort)
        df_sub = pd.read_csv(sub)

        x = sum(df_cort["Tumor in region"])
        y = sum(df_sub["Tumor in region"])
        if x == 0 or y == 0:
            print(f"No tumor found in {idx}")
            return

        print(f"Test {idx} passed")


test(
    "Burdenko-GBM-Progression/per_region_dist/sub-*/*_cortical.csv",
    "Burdenko-GBM-Progression/per_region_dist/sub-*/*_subcortical.csv",
)
