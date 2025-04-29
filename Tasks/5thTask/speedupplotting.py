import matplotlib.pyplot as plt

# Data: cores and corresponding execution times in seconds / take the 2 times in the comments, avg it and insert it. this data comes from outputsforrun folder
execution_times = {
    1: (27 * 60 + 6.006 + 25 * 60 + 8.366) / 2,   # Average of 27m6.006s and 25m8.366s
    2: (17 * 60 + 4.361 + 15 * 60 + 19.926) / 2,  # Average of 17m4.361s and 15m19.926s
    3: (12 * 60 + 15.772 + 9 * 60 + 7.702) / 2,   # Average of 12m15.772s and 9m7.702s
    4: 11 * 60 + 5.585,                           # 13m13.353s 11m5.585s
    5: (13 * 60 + 3.903 + 9 * 60 + 33.896) / 2,   # Average of 13m3.903s and 9m33.896s
    6: (10 * 60 + 20.318 + 10 * 60 + 21.079) / 2, # Average of 10m20.318s and 10m21.079s
    7: (8 * 60 + 24.045 + 7 * 60 + 25.065) / 2,   # Average of 8m24.045s and 7m25.065s
    8: (6 * 60 + 33.196 + 8 * 60 + 18.169) / 2,   # Average of 6m33.196s and 8m18.169s
    9: (7 * 60 + 1.519 + 7 * 60 + 3.249) / 2,     # Average of 7m1.519s and 7m3.249s
    10: (7 * 60 + 4.154 + 6 * 60 + 56.732) / 2,   # Average of 7m4.154s and 6m56.732s
    11: (6 * 60 + 29.385 + 6 * 60 + 16.840) / 2,  # Average of 6m29.385s and 6m16.840s
    12: (4 * 60 + 30.166 + 4 * 60 + 46.779) / 2,  # Average of 4m30.166s and 4m46.779s
    13: 3 * 60 + (12.188 + 44.934) / 2,           # Average of 4m11.248s and 3m44.934s
    14: (3 * 60 + 42.865 + 3 * 60 + 31.170) / 2,  # Average of 3m42.865s and 3m31.170s
    15: (3 * 60 + 26.114 + 3 * 60 + 37.748) / 2,  # Average of 3m26.114s and 3m37.748s
    16: 3 * 60 + (26.593 + 25.428) / 2,           # Average of 3m26.593s and 3m25.428s
}

# Calculate speedup
cores = list(execution_times.keys())
times = list(execution_times.values())
speedup = [times[0] / t for t in times]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(cores, speedup, marker='o', label='Speedup')

# Adding a red line for the theoretical maximum speedup
theoretical_max_speedup = 8 
plt.axhline(y=theoretical_max_speedup, color='red', linestyle='--', label='Theoretical Maximum Speedup')

# Adding labels and title
plt.title('Dynamic scheduling parallelization speedups')
plt.xlabel('Number of Cores')
plt.ylabel('Speedup')
plt.xticks(cores)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

# Save the plot as a JPG file
plt.tight_layout()
import os

# Ensure the directory is writable
output_path = os.path.join(os.getcwd(), 'speedup_plot.jpg')
plt.savefig(output_path, dpi=300)
print(f"Plot saved to {output_path}")

plt.show()
