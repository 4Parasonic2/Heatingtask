from os.path import join
import sys
import math

import numpy as np
from numba import cuda

def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask

def jacobi_helper(u, interior_mask, max_iter, threads_per_block, blocks_per_grid):
    u_curr_np = u.copy()
    u_next_np = np.empty_like(u_curr_np)

    # Send initial data to GPU (explicit is often clearer)
    u_curr_gpu = cuda.to_device(u_curr_np)
    u_next_gpu = cuda.to_device(u_next_np)
    mask_gpu = cuda.to_device(interior_mask)

    for iter_count in range(max_iter):
        jacobi_kernel[blocks_per_grid, threads_per_block](
            u_curr_gpu, mask_gpu, u_next_gpu
        )
        u_curr_gpu, u_next_gpu = u_next_gpu, u_curr_gpu

    final_u = u_curr_gpu.copy_to_host()
    return final_u


@cuda.jit
def jacobi_kernel(u, interior_mask, output):
    i, j = cuda.grid(2)
    i_cond = i > 0 and i < (u.shape[0] - 1) 
    j_cond = j > 0 and j < (u.shape[1] - 1)
    is_interior = interior_mask[i,j] == True 
    if i_cond and j_cond and is_interior:
        output[i, j] = 0.25 * (u[i-1, j] + u[i+1, j] + u[i, j+1] + u[i, j-1])

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
    # Load data
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        building_ids = f.read().splitlines()

    if len(sys.argv) < 2:
        N = 1
    else:
        N = int(sys.argv[1])
    building_ids = building_ids[:N]

    # Load floor plans
    all_u0 = np.empty((N, 514, 514))
    all_interior_mask = np.empty((N, 512, 512), dtype='bool')
    for i, bid in enumerate(building_ids):
        u0, interior_mask = load_data(LOAD_DIR, bid)
        all_u0[i] = u0
        all_interior_mask[i] = interior_mask


    threads_per_block = (16, 16)
    blocks_per_grid_x = math.ceil(all_u0[0].shape[0] / threads_per_block[0])
    blocks_per_grid_y = math.ceil(all_u0[0].shape[1] / threads_per_block[1])
    blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

    dummy_u0 = np.zeros((514,514))
    dummy_u = np.zeros((514,514))

    all_u = np.empty_like(all_u0)
    jacobi_kernel[blocks_per_grid, threads_per_block](dummy_u0,all_interior_mask[0],dummy_u)
    MAX_ITER = 20000

    for i, (u0, interior_mask) in enumerate(zip(all_u0, all_interior_mask)):
        final_u = jacobi_helper(u0, interior_mask, MAX_ITER, threads_per_block, blocks_per_grid)
        all_u[i] = final_u

    # Print summary statistics in CSV format
    stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    print('building_id, ' + ', '.join(stat_keys))  # CSV header
    for bid, u, interior_mask in zip(building_ids, all_u, all_interior_mask):
        stats = summary_stats(u, interior_mask)
        print(f"{bid},", ", ".join(str(stats[k]) for k in stat_keys))
