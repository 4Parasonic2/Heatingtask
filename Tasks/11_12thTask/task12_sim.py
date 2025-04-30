from os.path import join
import sys
import math
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numba import cuda

def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask

@cuda.jit
def jacobi_kernel(u, interior_mask, output):
    i, j = cuda.grid(2)
    
    if (1 <= i < u.shape[0]-1) and (1 <= j < u.shape[1]-1):
        if interior_mask[i-1, j-1]:
            output[i, j] = 0.25 * (u[i-1, j] + u[i+1, j] + u[i, j-1] + u[i, j+1])

@cuda.jit
def reimpose_walls(u, domain):
    i, j = cuda.grid(2)
    if (1 <= i < u.shape[0]-1) and (1 <= j < u.shape[1]-1):
        if domain[i-1, j-1] == 25:
            u[i, j] = 25.0
        elif domain[i-1, j-1] == 5:
            u[i, j] = 5.0


def summary_stats(u, interior_mask):
    u_interior = u[1:-1, 1:-1][interior_mask]
    mean_temp = u_interior.mean()
    std_temp = u_interior.std()
    pct_above_18 = np.sum(u_interior > 18) / u_interior.size * 100
    pct_below_15 = np.sum(u_interior < 15) / u_interior.size * 100
    return {
        'mean_temp': mean_temp,
        'std_temp': std_temp,
        'pct_above_18': pct_above_18,
        'pct_below_15': pct_below_15,
    }

if __name__ == '__main__':
    # === CONFIGURATION ===
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    RESULTS_DIR = 'results'
    os.makedirs(RESULTS_DIR, exist_ok=True)
    SAVE_CSV = join(RESULTS_DIR, 'results_summary.csv')
    SAVE_HISTOGRAM = join(RESULTS_DIR, 'mean_temperature_histogram.png')

    # === Load all building IDs ===
    with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        building_ids = f.read().splitlines()

    if len(sys.argv) < 2:
        N = len(building_ids)  # default: process all
    else:
        N = int(sys.argv[1])

    building_ids = building_ids[:N]

    # === Load floor plans ===
    all_u0 = np.empty((N, 514, 514))
    all_interior_mask = np.empty((N, 512, 512), dtype=bool)

    for i, bid in enumerate(building_ids):
        u0, interior_mask = load_data(LOAD_DIR, bid)
        all_u0[i] = u0
        all_interior_mask[i] = interior_mask

    threads_per_block = (16, 16)
    blocks_per_grid_x = math.ceil(all_u0[0].shape[0] / threads_per_block[0])
    blocks_per_grid_y = math.ceil(all_u0[0].shape[1] / threads_per_block[1])
    blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

    dummy_u0 = np.zeros((514, 514))
    dummy_u = np.zeros((514, 514))

    all_u = np.empty_like(all_u0)
    jacobi_kernel[blocks_per_grid, threads_per_block](dummy_u0, all_interior_mask[0], dummy_u)

    MAX_ITER = 20000

    for i, (u0, interior_mask) in enumerate(zip(all_u0, all_interior_mask)):
        u_curr_np = u0.copy()
        u_next_np = np.zeros_like(u_curr_np)  # <<< FIXED HERE
        mask_np = interior_mask


        # === NEW: Upload domain to GPU ===
        domain_np = np.ascontiguousarray(u0[1:-1, 1:-1])
        # extract the domain without padding
        domain_gpu = cuda.to_device(domain_np)

        u_curr_gpu = cuda.to_device(u_curr_np)
        u_next_gpu = cuda.to_device(u_next_np)
        mask_gpu = cuda.to_device(mask_np)

        for iter_count in range(MAX_ITER):
            jacobi_kernel[blocks_per_grid, threads_per_block](u_curr_gpu, mask_gpu, u_next_gpu)
            # Reimpose wall boundary conditions on u_next_gpu
            reimpose_walls[blocks_per_grid, threads_per_block](u_next_gpu, domain_gpu)
            u_curr_gpu, u_next_gpu = u_next_gpu, u_curr_gpu

        final_u = u_curr_gpu.copy_to_host()
        all_u[i] = final_u

        np.save(join(RESULTS_DIR, f"{building_ids[i]}_result.npy"), final_u)


    # === Summarize and Save CSV ===
    stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    rows = []

    print('building_id, ' + ', '.join(stat_keys))  # CSV header
    for bid, u, interior_mask in zip(building_ids, all_u, all_interior_mask):
        stats = summary_stats(u, interior_mask)
        print(f"{bid},", ", ".join(str(stats[k]) for k in stat_keys))
        row = {"building_id": bid}
        row.update(stats)
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(SAVE_CSV, index=False)
    print(f"Results saved to {SAVE_CSV}")

    # === Plot histogram of mean temperatures ===
    plt.hist(df["mean_temp"], bins=30, edgecolor='k')
    plt.xlabel("Mean Temperature (°C)")
    plt.ylabel("Number of Buildings")
    plt.title("Distribution of Mean Temperatures")
    plt.savefig(SAVE_HISTOGRAM)
    plt.close()
    print(f"Histogram saved to {SAVE_HISTOGRAM}")
