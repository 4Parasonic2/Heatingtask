import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

# Load the data
domain_data_1 = np.load('testdata/23_domain.npy')
interior_data_1 = np.load('testdata/23_interior.npy')
domain_data_2 = np.load('testdata/69_domain.npy')
interior_data_2 = np.load('testdata/69_interior.npy')
domain_data_3 = np.load('testdata/630_domain.npy')
interior_data_3 = np.load('testdata/630_interior.npy')
domain_data_4 = np.load('testdata/2755_domain.npy')
interior_data_4 = np.load('testdata/2755_interior.npy')

# Save the raw data of 23_domain.npy and 23_interior.npy into text files
np.savetxt('23_domain_data.txt', domain_data_1, fmt='%s')
np.savetxt('23_interior_data.txt', interior_data_1, fmt='%s')

# Plot the data
plt.figure(figsize=(24, 12))

# Plot domain data
plt.subplot(2, 4, 1)
plt.imshow(domain_data_1, cmap='viridis')
plt.title('Domain Data 23')
plt.colorbar()

plt.subplot(2, 4, 2)
plt.imshow(domain_data_2, cmap='viridis')
plt.title('Domain Data 69')
plt.colorbar()

plt.subplot(2, 4, 3)
plt.imshow(domain_data_3, cmap='viridis')
plt.title('Domain Data 630')
plt.colorbar()

plt.subplot(2, 4, 4)
plt.imshow(domain_data_4, cmap='viridis')
plt.title('Domain Data 2755')
plt.colorbar()

# Plot interior data
plt.subplot(2, 4, 5)
plt.imshow(interior_data_1, cmap='viridis')
plt.title('Interior Data 23')
plt.colorbar()

plt.subplot(2, 4, 6)
plt.imshow(interior_data_2, cmap='viridis')
plt.title('Interior Data 69')
plt.colorbar()

plt.subplot(2, 4, 7)
plt.imshow(interior_data_3, cmap='viridis')
plt.title('Interior Data 630')
plt.colorbar()

plt.subplot(2, 4, 8)
plt.imshow(interior_data_4, cmap='viridis')
plt.title('Interior Data 2755')
plt.colorbar()

plt.tight_layout()
plt.savefig('combined_plot.png')
plt.show()

