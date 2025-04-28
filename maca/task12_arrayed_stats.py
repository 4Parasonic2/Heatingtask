import pandas as pd
import matplotlib.pyplot as plt

# === LOAD FINAL FILES ===
results_file = "results_task12_arrayed/results_summary_full.csv"
timing_file = "results_task12_arrayed/execution_times_per_job.csv"

results_df = pd.read_csv(results_file)
timing_df = pd.read_csv(timing_file)

# === TASK 12 QUESTIONS ===

# a) Distribution of mean temperatures
plt.figure(figsize=(8,6))
plt.hist(results_df["mean_temp"], bins=30, edgecolor='k')
plt.xlabel("Mean Temperature (°C)")
plt.ylabel("Number of Buildings")
plt.title("Distribution of Mean Temperatures")
plt.grid(True)
plt.savefig("results_task12_arrayed/mean_temperature_histogram_task12.png")
plt.close()

# b) Average mean temperature
avg_mean_temp = results_df["mean_temp"].mean()
print(f"Average mean temperature: {avg_mean_temp:.2f} °C")

# c) Average temperature standard deviation
avg_std_temp = results_df["std_temp"].mean()
print(f"Average standard deviation of temperatures: {avg_std_temp:.2f} °C")

# d) Buildings with at least 50% of area above 18°C
buildings_above_18 = (results_df["pct_above_18"] >= 50).sum()
print(f"Number of buildings with >=50% of area above 18°C: {buildings_above_18}")

# e) Buildings with at least 50% of area below 15°C
buildings_below_15 = (results_df["pct_below_15"] >= 50).sum()
print(f"Number of buildings with >=50% of area below 15°C: {buildings_below_15}")

# === EXTRA PLOTS / INSIGHTS ===

# Histogram of standard deviations
plt.figure(figsize=(8,6))
plt.hist(results_df["std_temp"], bins=30, edgecolor='k')
plt.xlabel("Temperature Standard Deviation (°C)")
plt.ylabel("Number of Buildings")
plt.title("Distribution of Temperature Standard Deviations")
plt.grid(True)
plt.savefig("results_task12_arrayed/temperature_std_histogram_task12.png")
plt.close()

# Scatter plot: mean temperature vs. standard deviation
plt.figure(figsize=(8,6))
plt.scatter(results_df["mean_temp"], results_df["std_temp"], alpha=0.7)
plt.xlabel("Mean Temperature (°C)")
plt.ylabel("Temperature Standard Deviation (°C)")
plt.title("Mean Temperature vs. Temperature Std Dev")
plt.grid(True)
plt.savefig("results_task12_arrayed/mean_vs_std_scatter_task12.png")
plt.close()

# Execution times statistics
avg_exec_time = timing_df["total_seconds"].mean()
total_exec_time = timing_df["total_seconds"].sum()

print(f"Average execution time per job: {avg_exec_time:.2f} seconds ({avg_exec_time/60:.2f} minutes)")
print(f"Total execution time across all jobs: {total_exec_time:.2f} seconds ({total_exec_time/3600:.2f} hours)")

# Execution times histogram
plt.figure(figsize=(8,6))
plt.hist(timing_df["total_seconds"], bins=30, edgecolor='k')
plt.xlabel("Execution Time per Job (seconds)")
plt.ylabel("Number of Jobs")
plt.title("Distribution of Execution Times per Job")
plt.grid(True)
plt.savefig("results_task12_arrayed/job_execution_time_histogram_task12.png")
plt.close()

# === NEW: DETAILED DISTRIBUTIONS ===

# Distribution of percentage of area above 18°C
plt.figure(figsize=(8,6))
plt.hist(results_df["pct_above_18"], bins=30, edgecolor='k', color='green')
plt.xlabel("Percentage of Area > 18°C")
plt.ylabel("Number of Buildings")
plt.title("Distribution of Areas Above 18°C")
plt.grid(True)
plt.savefig("results_task12_arrayed/area_above_18_distribution_task12.png")
plt.close()

# Distribution of percentage of area below 15°C
plt.figure(figsize=(8,6))
plt.hist(results_df["pct_below_15"], bins=30, edgecolor='k', color='blue')
plt.xlabel("Percentage of Area < 15°C")
plt.ylabel("Number of Buildings")
plt.title("Distribution of Areas Below 15°C")
plt.grid(True)
plt.savefig("results_task12_arrayed/area_below_15_distribution_task12.png")
plt.close()

# Scatter plot: pct_above_18 vs pct_below_15
plt.figure(figsize=(8,6))
plt.scatter(results_df["pct_above_18"], results_df["pct_below_15"], alpha=0.7, color='purple')
plt.xlabel("Percentage of Area > 18°C")
plt.ylabel("Percentage of Area < 15°C")
plt.title("Area Above 18°C vs Area Below 15°C")
plt.grid(True)
plt.savefig("results_task12_arrayed/area_above_vs_below_scatter_task12.png")
plt.close()

print("\nAll extended analysis completed. Extra plots saved to 'results_task12_arrayed/' folder.")
