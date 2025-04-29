import matplotlib.pyplot as plt

# Data: cores and corresponding execution times in seconds
execution_times = {
    1: 24 * 60 + 52,  # 42m22.830s
    2: 14 * 60 + 35,  # 41m2.202s
    3: 12 * 60 + 20,  # 16m12.384s
    4: 7 * 60 + 59,   # 13m17.725s
    5: 6 * 60 + 45,   # 19m50.678s
    6: 6 * 60 + 10,   # 16m29.170s
    7: 5 * 60 + 50,   # 15m5.262s
    8: 5 * 60 + 15,   # 11m58.386s
    9: 4 * 60 + 50,   # 11m34.125s
    10: 4 * 60 + 30,  # 12m18.037s
    11: 4 * 60 + 15,  # 9m3.026s
    12: 4 * 60 + 5,   # 7m28.694s
    13: 3 * 60 + 55,  # 7m14.859s
    14: 3 * 60 + 50,  # 6m29.194s
    15: 3 * 60 + 47,  # 6m7.390s
    16: 3 * 60 + 45,  # 5m42.902s
}

# Calculate speedup
cores = list(execution_times.keys())
times = list(execution_times.values())
speedup = [times[0] / t for t in times]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(cores, speedup, marker='o', label='Speedup')

# Adding a red line for the theoretical maximum speedup
# theoretical_max_speedup = 8 
# plt.axhline(y=theoretical_max_speedup, color='red', linestyle='--', label='Theoretical Maximum Speedup')

# Adding labels and title
plt.title('Dynamic scheduling parallelization speedups')
plt.xlabel('Number of Cores')
plt.ylabel('Speedup')
plt.xticks(cores)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

# Save the plot as a JPG file
plt.tight_layout()
plt.savefig('speedup_plot_dynamic.jpg', dpi=300)

plt.show()
