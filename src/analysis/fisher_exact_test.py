import multiprocessing as mp
import numpy as np
import nibabel as nib
from scipy.stats import fisher_exact

class FisherExactTest:
    def __init__(self, dataset1_path: str, dataset2_path: str, size1: int, size2: int, num_processes: int = mp.cpu_count()):
        self.dataset1_path = dataset1_path
        self.dataset2_path = dataset2_path
        self.size1 = size1
        self.size2 = size2
        self.num_processes = num_processes

    @staticmethod
    def fisher_test_worker(args):
        a, b, c, d = args
        return fisher_exact([[a, b], [c, d]])[1]

    def perform_fisher_test(self, save_path: str):
        """
        Perform Fisher's exact test between two datasets using multiprocessing.
        Args:
            save_path (str): Path to save the result.
        """
        # Load datasets
        file_ds1 = nib.load(self.dataset1_path)
        img_ds1 = file_ds1.get_fdata()
        file_ds2 = nib.load(self.dataset2_path)
        img_ds2 = file_ds2.get_fdata()
        # Flatten datasets
        x = img_ds1.flatten().astype(int)
        y = img_ds2.flatten().astype(int)
        a = x
        b = y
        c = self.size1 - a
        d = self.size2 - b
        # Create a pool of worker processes
        pool = mp.Pool(processes=self.num_processes)
        # Distribute the workload among the worker processes
        args = [(a[i], b[i], c[i], d[i]) for i in range(len(a))]
        p = pool.map(self.fisher_test_worker, args)
        # Close the pool and wait for the worker processes to finish
        pool.close()
        pool.join()
        # Convert the result to a NumPy array
        p = np.array(p)
        # Retain only p-values less than 0.05
        mask = p < 0.05
        p[~mask] = 0.0
        # Reshape result array to match the original image shape
        p = p.reshape(img_ds1.shape)
        # Save the result
        img = nib.Nifti1Image(p, affine=file_ds1.affine)
        nib.save(img, save_path)


