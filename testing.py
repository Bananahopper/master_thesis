import numpy as np

# Example arrays with different shapes
original_seg_data = np.random.rand(5, 8, 10)
original_seg_data2 = np.random.rand(5, 8, 10)
original_seg_data = original_seg_data + original_seg_data2

original_seg_data = original_seg_data / np.sum(original_seg_data)
print(np.sum(original_seg_data))
