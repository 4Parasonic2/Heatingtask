from os.path import join
from matplotlib import pyplot as plt
import sys
import multiprocessing

import numpy as np

MAX_ITER = 20_000
ABS_TOL = 1e-4

def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask

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

def chunkify(buildings, interiors, num_chunks):
    chunk_size = len(buildings) // num_chunks
    building_chunks = [buildings[i:i + chunk_size] for i in range(0, len(buildings), chunk_size)]
    interior_chunks = [interiors[i:i + chunk_size] for i in range(0, len(buildings), chunk_size)]
    return building_chunks, interior_chunks  

def process_chunk(building_chunk, interior_chunk, func):
    chunk_size = len(building_chunk)
    results = np.zeros((chunk_size, 514, 514))
    for i, (u, interior) in enumerate(zip(building_chunk, interior_chunk)):
        results[i] = func(u, interior, MAX_ITER, ABS_TOL)

    return results



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

    n_proc = int(sys.argv[2])
    pool = multiprocessing.Pool(n_proc)

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
    building_chunks, interior_chunks = chunkify(all_u0, all_interior_mask, n_proc)
    
    all_u = np.zeros((N, 514, 514))
    chunk_size = int(np.ceil(N // n_proc))

    with multiprocessing.Pool(processes=n_proc) as pool:
        chunk_results = pool.starmap(process_chunk, [(b_chunk, i_chunk, jacobi) for (b_chunk, i_chunk) in zip(building_chunks, interior_chunks)])

    
    # plt.imshow(chunk_results[0][0])
    # plt.show()

    all_u = np.zeros((N, 514, 514))
    for i, chunk_result in enumerate(chunk_results):
        all_u[i*chunk_size:(i+1)*chunk_size, :, :] = chunk_result

    # Print summary statistics in CSV format
    stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    print('building_id, ' + ', '.join(stat_keys))  # CSV header
    for bid, u, interior_mask in zip(building_ids, all_u, all_interior_mask):
        stats = summary_stats(u, interior_mask)
        print(f"{bid},", ", ".join(str(stats[k]) for k in stat_keys))
