import os
import subprocess

brats_deep = os.listdir("/scratch/users/ggaspar/Deep/BRATS/images/")
brats_captk = os.listdir("/scratch/users/ggaspar/CaPTk/datasets/Brats2021_wTumor/")
brats_deep.sort()
brats_captk.sort()

print(brats_deep[0])
print(brats_captk[0])

print(len(brats_deep), len(brats_captk))

if len(brats_deep) == len(brats_captk):
    for idx, (brats_deep, brats_captk) in enumerate(zip(brats_deep, brats_captk)):
        print(f"running command {idx}")
        deep = os.path.join("/scratch/users/ggaspar/Deep/BRATS/images/", brats_deep)
        captk = os.path.join(
            "/scratch/users/ggaspar/CaPTk/datasets/Brats2021_wTumor/", brats_captk
        )
        command = f"mv {deep} {captk}/"
        print(command)
        subprocess.run(command, shell=True)
