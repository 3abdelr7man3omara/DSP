import numpy as np

x = np.array([1, 2, 3])
upsampled_x = np.zeros(len(x) * 3)
upsampled_x[::3] = x

print(upsampled_x)

