# merge_and_extract_task12.py
import pandas as pd
import glob
import re

# === Part 1: Merge all partial results_summary_job*.csv ===

print("Merging building result CSVs...")

csv_files = sorted(glob.glob("results_task12_arrayed/results_summary_job*.csv"))

dfs = [pd.read_csv(f) for f in csv_files]
full_df = pd.concat(dfs, ignore_index=True)

full_df.to_csv("results_task12_arrayed/results_summary_full.csv", index=False)

print(f"Merged {len(csv_files)} CSVs into results_summary_full.csv.")


# === Part 2: Extract execution times from .out files ===

print("Extracting execution times from output files...")
import pandas as pd
import re
import glob
import os

timing_data = []

# Search in the correct folder
for filename in sorted(glob.glob("results_task12_arrayed/task12_*_*.err")):
    job_info = re.search(r'task12_(\d+)_(\d+)\.err', filename)
    if job_info:
        job_id = job_info.group(1)
        array_idx = int(job_info.group(2))

        with open(filename, 'r') as f:
            for line in f:
                if line.startswith('real'):
                    match = re.match(r"real\s+(\d+)m([\d\.]+)s", line.strip())
                    if match:
                        minutes = int(match.group(1))
                        seconds = float(match.group(2))
                        total_seconds = minutes * 60 + seconds
                        timing_data.append({
                            "array_index": array_idx,
                            "real_minutes": minutes,
                            "real_seconds": seconds,
                            "total_seconds": total_seconds,
                            "filename": os.path.basename(filename)
                        })
                    break

# Create DataFrame
df = pd.DataFrame(timing_data)

# Sort safely
if not df.empty:
    df = df.sort_values("array_index")
    df.to_csv("execution_times_per_job.csv", index=False)

    print(f"Extracted execution times for {len(df)} jobs into execution_times_per_job.csv.")

    # Calculate total runtime
    total_seconds = df["total_seconds"].sum()
    total_hours = total_seconds / 3600
    print(f"Total runtime across all jobs: {total_seconds:.2f} seconds ({total_hours:.2f} hours).")
else:
    print("No execution times found. Skipping timing summary.")
