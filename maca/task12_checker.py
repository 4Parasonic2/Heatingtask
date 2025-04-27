import numpy as np
import matplotlib.pyplot as plt

# === CONFIGURATION ===
RESULTS_DIR = "results"
building_id = "10000"  # Change this to any building you want to check
result_file = f"{building_id}_result.npy"

# === LOAD RESULT ===
u = np.load(result_file)

# === PRINT STATISTICS ===
print(f"Building ID: {building_id}")
print(f"Mean temperature: {u.mean():.2f} °C")
print(f"Std deviation: {u.std():.2f} °C")
print(f"Max temperature: {u.max():.2f} °C")
print(f"Min temperature: {u.min():.2f} °C")

# === PLOT TEMPERATURE FIELD ===
plt.imshow(u, cmap="hot", origin="lower")
plt.colorbar(label="Temperature (°C)")
plt.title(f"Temperature Distribution - Building {building_id}")
plt.xlabel("x")
plt.ylabel("y")
plt.show()
