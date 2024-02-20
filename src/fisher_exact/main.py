import numpy as np
import nibabel as nib
import math
import datetime
import os
from multiprocessing import Pool

fileRHUH = nib.load('prob_dist_results/RHUH_DATASET/probdist_RHUH_whole_tumor.nii')
imgRHUH = fileRHUH.get_fdata()
fileBTP = nib.load('prob_dist_results/BRAIN-TUMOR-PROGRESSION_DATASET/probdist_BTP_whole_tumor.nii')
imgBTP = fileBTP.get_fdata()


x = imgRHUH.flatten()

def fisher_fast(x):
    result_array = np.zeros_like(imgRHUH, dtype=float)

    shape = result_array.shape

    y = imgBTP.flatten()
    z = result_array.flatten()

    for i, value in enumerate(x):
        a = int(value)
        b = int(y[i])
        c = 39 - a
        d = 20 - b
        n = 59
         
        p = ((math.factorial(a + b)) * (math.factorial(c + d)) * (math.factorial(a + c)) * (math.factorial(b + d))) / ((math.factorial(a)) * (math.factorial(b)) * (math.factorial(c)) * (math.factorial(d)) * (math.factorial(n)))

        z[i] = p

    result_array = z.reshape(shape)
    
    return result_array

start_time = datetime.datetime.now()

if __name__ == '__main__':
    # Create a pool to use all cpus
    pool = Pool(processes=os.cpu_count())
    pool.map(fisher_fast, range(len(x)))
    # Close the process pool
    pool.close()

# Store current time after execution
end_time = datetime.datetime.now()
 
# Print multi threading execution time
print('Time taken: ', end_time-start_time)