from os.path import join
import os
import sys
import math

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
    RESULTS_DIR = 'results_task12_arrayed'
    os.makedirs(RESULTS_DIR, exist_ok=True)

    BLOCK_SIZE = 100  # number of buildings per job

    # === Load all building IDs ===
    with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        all_building_ids = f.read().splitlines()

    # === Read job array index from environment
    job_idx = int(os.getenv('LSB_JOBINDEX', '1'))  # defaults to 1 if not set

    start_idx = (job_idx - 1) * BLOCK_SIZE
    end_idx = start_idx + BLOCK_SIZE

    building_ids = all_building_ids[start_idx:end_idx]

    if not building_ids:
        print("No buildings assigned to this job.")
        sys.exit(0)

    print(f"Processing buildings from index {start_idx} to {end_idx} (total: {len(building_ids)})")

    # === Load floor plans ===
    all_u0 = np.empty((len(building_ids), 514, 514))
    all_interior_mask = np.empty((len(building_ids), 512, 512), dtype=bool)

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
    jacobi_kernel[blocks_per_grid, threads_per_block](dummy_u0, all_interior_mask[0], dummy_u)

    MAX_ITER = 20000

    # === Process buildings ===
    results = []

    for u0, interior_mask, bid in zip(all_u0, all_interior_mask, building_ids):
        u_curr_np = u0.copy()
        u_next_np = np.zeros_like(u_curr_np)

        domain_np = np.ascontiguousarray(u0[1:-1, 1:-1])
        domain_gpu = cuda.to_device(domain_np)

        u_curr_gpu = cuda.to_device(u_curr_np)
        u_next_gpu = cuda.to_device(u_next_np)
        mask_gpu = cuda.to_device(interior_mask)

        for _ in range(MAX_ITER):
            jacobi_kernel[blocks_per_grid, threads_per_block](u_curr_gpu, mask_gpu, u_next_gpu)
            reimpose_walls[blocks_per_grid, threads_per_block](u_next_gpu, domain_gpu)
            u_curr_gpu, u_next_gpu = u_next_gpu, u_curr_gpu

        final_u = u_curr_gpu.copy_to_host()

        # Save result
        np.save(join(RESULTS_DIR, f"{bid}_result.npy"), final_u)

        # Collect summary statistics
        stats = summary_stats(final_u, interior_mask)
        row = {"building_id": bid}
        row.update(stats)
        results.append(row)

    # === Save partial CSV
    df = pd.DataFrame(results)
    df.to_csv(join(RESULTS_DIR, f"results_summary_job{job_idx}.csv"), index=False)

    print(f"Finished processing {len(building_ids)} buildings.")
