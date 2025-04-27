import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the file
file_path = '2ndtask_24678923.out'
data = pd.read_csv(file_path).iloc[:-1]

# Display the first few rows of the data
print(data.head())
print("Columns in the dataset:", data.columns)
# Rename columns to remove leading/trailing spaces
data.columns = data.columns.str.strip()

# Plot mean temperature with error bars representing standard deviation
plt.figure(figsize=(10, 6))
plt.errorbar(data['building_id'], data['mean_temp'], yerr=data['std_temp'], fmt='o', ecolor='red', capsize=5, label='Mean Temp ± Std Dev')
plt.xlabel('Building ID')
plt.ylabel('Mean Temperature (°C)')
plt.title('Mean Temperature with Standard Deviation by Building')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

# Save the plot as a PNG file
output_file = 'mean_temp_with_std_dev.png'
plt.savefig(output_file, dpi=300)

plt.show()


# Plot percentage above 18 degrees and below 15 degrees as bar plots
plt.figure(figsize=(12, 8))

# Create a grouped bar plot
bar_width = 0.35
index = range(len(data['building_id']))

plt.bar(index, data['pct_above_18'], bar_width, label='Percentage Above 18°C', color='blue')
plt.bar([i + bar_width for i in index], data['pct_below_15'], bar_width, label='Percentage Below 15°C', color='orange')
# Add labels and title
plt.xlabel('Building ID')
plt.ylabel('Percentage')
plt.title('Temperature Percentages by Building')
plt.xticks([i + bar_width / 2 for i in index], data['building_id'], rotation=45)
plt.legend()

# Add values on top of the bars
for i, v in enumerate(data['pct_above_18']):
    plt.text(i, v + 1, f"{v:.1f}%", ha='center', color='blue', fontsize=9)
for i, v in enumerate(data['pct_below_15']):
    plt.text(i + bar_width, v + 1, f"{v:.1f}%", ha='center', color='orange', fontsize=9)

# Adjust layout and save the plot
plt.tight_layout()
output_file_bar = 'temperature_percentages_by_building.png'
plt.savefig(output_file_bar, dpi=300)

plt.show()


# Plot mean temperature for each building
# plt.bar(data['building_id'], data['mean_temp'], color='skyblue') 
# plt.xlabel('Building ID')
# plt.ylabel('Mean Temperature')
# plt.title('Mean Temperature by Building')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

# # Plot percentage above 18 degrees and below 15 degrees
# plt.figure(figsize=(10, 6))
# plt.plot(data['building_id'], data['pct_above_18'], label='Percentage Above 18°C', marker='o')
# plt.plot(data['building_id'], data['pct_below_15'], label='Percentage Below 15°C', marker='x')
# plt.xlabel('Building ID')
# plt.ylabel('Percentage')
# plt.title('Temperature Percentages by Building')
# plt.legend()
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()
