from os.path import join
import sys

import numpy as np
from numba import jit

def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask

@jit(nopython=True)
def jacobi(u, interior_mask, max_iter, atol=1e-6):
    u = np.copy(u)
    # Get the dimensions of the interior grid
    M, N = interior_mask.shape 

    for i in range(max_iter):
        max_delta = 0.0 # Initialize max change for this iteration
        
        # Compute potential new values for the entire interior grid
        # Note: u_new has shape (M, N) matching interior_mask
        u_new = 0.25 * (u[1:-1, :-2] + u[1:-1, 2:] + u[:-2, 1:-1] + u[2:, 1:-1])

        # Iterate through each point in the interior grid
        for r in range(M):
            for c in range(N):
                # Check if the current point is part of the interior
                if interior_mask[r, c]:
                    # Calculate the new value for this point
                    new_val = u_new[r, c]
                    # Get the corresponding old value from u (offset by 1 for boundary)
                    old_val = u[r + 1, c + 1] 
                    
                    # Calculate the absolute difference
                    diff = abs(old_val - new_val)
                    
                    # Update the maximum difference found so far
                    if diff > max_delta:
                        max_delta = diff
                        
                    # Update the value in u (offset by 1 for boundary)
                    u[r + 1, c + 1] = new_val

        # Check for convergence using the maximum change across all interior points
        if max_delta < atol:
            break
            
    return u


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
    LOAD_DIR = '../data/modified_swiss_dwellings'
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

    # Run jacobi iterations for each floor plan
    MAX_ITER = 20_000
    ABS_TOL = 1e-4

    all_u = np.empty_like(all_u0)
    for i, (u0, interior_mask) in enumerate(zip(all_u0, all_interior_mask)):
        u = jacobi(u0, interior_mask, MAX_ITER, ABS_TOL)
        all_u[i] = u

    # Print summary statistics in CSV format
    stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    print('building_id, ' + ', '.join(stat_keys))  # CSV header
    for bid, u, interior_mask in zip(building_ids, all_u, all_interior_mask):
        stats = summary_stats(u, interior_mask)
        print(f"{bid},", ", ".join(str(stats[k]) for k in stat_keys))
