import matplotlib.pyplot as plt

# Data: cores and corresponding execution times in seconds
execution_times = {
    1: 21 * 60 + 28.293,  # 21m28.293s
    2: 13 * 60 + 28.744,  # 13m28.744s
    # Add more cores and times as you test further
    # Example:
    4: 8 * 60 + 40.775,  # 8m40.775s,
    8: 5 * 60 + 50.923,  # 5m50.923s,
    16:  3 * 60 + 30.871 # 3m30.871s,
    # 32: <time_in_seconds>,
}

# Calculate speedup
cores = list(execution_times.keys())
times = list(execution_times.values())
speedup = [times[0] / t for t in times]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(cores, speedup, marker='o', label='Speedup')

# Adding a red line for the theoretical maximum speedup
theoretical_max_speedup = 3.9
plt.axhline(y=theoretical_max_speedup, color='red', linestyle='--', label='Theoretical Maximum Speedup')

# Adding labels and title
plt.title('Speedup vs Number of Cores')
plt.xlabel('Number of Cores')
plt.ylabel('Speedup')
plt.xticks(cores)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

# Save the plot as a JPG file
plt.tight_layout()
plt.savefig('speedup_plot.jpg', dpi=300)

plt.show()
