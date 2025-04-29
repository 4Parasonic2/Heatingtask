from os.path import join
import sys
import cupy as cp

def load_data(load_dir, bid):
    SIZE = 512
    u = cp.zeros((SIZE + 2, SIZE + 2), dtype=cp.float32)  # Use float32 for faster computation
    u[1:-1, 1:-1] = cp.load(join(load_dir, f"{bid}_domain.npy")).astype(cp.float32)
    interior_mask = cp.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask

def batched_jacobi(u_batch, mask_batch, max_iter, atol=1e-6):
    # Use double buffering and batch processing
    u_current = u_batch.copy()
    u_next = u_batch.copy()
    
    converged = cp.zeros(u_batch.shape[0], dtype=cp.bool_)
    delta_max = cp.zeros(u_batch.shape[0], dtype=cp.float32)
    
    for i in range(max_iter):
        if i % 100 == 0:  # Reduce convergence check frequency
            # Early exit if all converged
            if cp.all(converged):
                break
        
        # Vectorized update for all buildings
        u_next[:, 1:-1, 1:-1] = 0.25 * (
            u_current[:, 1:-1, :-2] + 
            u_current[:, 1:-1, 2:] + 
            u_current[:, :-2, 1:-1] + 
            u_current[:, 2:, 1:-1]
        )
        
        # Apply mask and compute delta
        delta = cp.abs(u_current[:, 1:-1, 1:-1] - u_next[:, 1:-1, 1:-1])
        delta_masked = cp.where(mask_batch, delta, 0)
        delta_max = cp.max(delta_masked, axis=(1,2))
        
        # Update convergence status
        converged = delta_max < atol
        
        # Swap buffers
        u_current, u_next = u_next, u_current
        
    return u_current

def summary_stats(u, interior_mask):
    u_interior = u[:, 1:-1, 1:-1][interior_mask]
    return {
        'mean_temp': u_interior.mean(),
        'std_temp': u_interior.std(),
        'pct_above_18': cp.sum(u_interior > 18) / u_interior.size * 100,
        'pct_below_15': cp.sum(u_interior < 15) / u_interior.size * 100,
    }

if __name__ == '__main__':
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    
    # Batch loading
    with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        building_ids = f.read().splitlines()
    
    N = int(sys.argv[1]) if len(sys.argv) >= 2 else 1
    building_ids = building_ids[:N]
    
    # Preallocate batch arrays
    batch_size = len(building_ids)
    all_u0 = cp.empty((batch_size, 514, 514), dtype=cp.float32)
    all_interior_mask = cp.empty((batch_size, 512, 512), dtype=bool)
    
    # Parallel data loading
    for i, bid in enumerate(building_ids):
        all_u0[i], all_interior_mask[i] = load_data(LOAD_DIR, bid)
    
    # Batched Jacobi iterations
    MAX_ITER = 20_000
    ABS_TOL = 1e-4
    
    # Process all buildings in a single batch
    final_u = batched_jacobi(all_u0, all_interior_mask, MAX_ITER, ABS_TOL)
    
    # Batch statistics computation
    print('building_id, mean_temp, std_temp, pct_above_18, pct_below_15')
    for bid, u in zip(building_ids, final_u):
        stats = summary_stats(u, all_interior_mask[i])
        print(f"{bid}, {stats['mean_temp']}, {stats['std_temp']}, "
              f"{stats['pct_above_18']}, {stats['pct_below_15']}")

