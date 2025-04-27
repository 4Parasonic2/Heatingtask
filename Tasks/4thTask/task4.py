from os.path import join
import sys
import line_profiler

import numpy as np


def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask

@line_profiler.profile
def jacobi(u, interior_mask, max_iter, atol=1e-6):
    u = np.copy(u)

    for i in range(max_iter):
        # Compute average of left, right, up and down neighbors, see eq. (1)
        u_new = 0.25 * (u[1:-1, :-2] + u[1:-1, 2:] + u[:-2, 1:-1] + u[2:, 1:-1])
        u_new_interior = u_new[interior_mask]
        delta = np.abs(u[1:-1, 1:-1][interior_mask] - u_new_interior).max()
        u[1:-1, 1:-1][interior_mask] = u_new_interior

        if delta < atol:
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


# Line #      Hits         Time  Per Hit   % Time  Line Contents
# ==============================================================
#     15                                           @line_profiler.profile
#     16                                           def jacobi(u, interior_mask, max_iter, atol=1e-6):
#     17         1        153.0    153.0      0.0      u = np.copy(u)                                                           <---- Copy into temp array
#     18
#     19      3602        767.0      0.2      0.0      for i in range(max_iter):
#     20                                                   # Compute average of left, right, up and down neighbors, see eq. (1)
#     21      3602    1757806.0    488.0     61.7          u_new = 0.25 * (u[1:-1, :-2] + u[1:-1, 2:] + u[:-2, 1:-1] + u[2:, 1:-1]) <--- Update values in copied array
#     22      3602     316576.0     87.9     11.1          u_new_interior = u_new[interior_mask]                               <--- get interior values with the mask
#     23      3602     455680.0    126.5     16.0          delta = np.abs(u[1:-1, 1:-1][interior_mask] - u_new_interior).max() <--- get the biggest change in values
#     24      3602     319196.0     88.6     11.2          u[1:-1, 1:-1][interior_mask] = u_new_interior                       <----- Update array
#     25
#     26      3602        978.0      0.3      0.0          if delta < atol:                                                  <----- If there is no change in the values, stop
#     27         1          1.0      1.0      0.0              break
#     28         1          0.0      0.0      0.0      return u
