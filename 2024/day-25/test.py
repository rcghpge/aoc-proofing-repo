import numpy as np
import pandas as pd
import time
from collections import defaultdict

def process_file_optimized(filename):
    # Read and process the input file
    with open(filename) as f:
        content = f.read().split("\n\n")
    
    locks = []
    keys = []
    lock_codes = []
    key_codes = []

    # Process schematics
    for schematic in content:
        schematic_lines = schematic.strip().split("\n")
        if schematic_lines[0] == "#####" and schematic_lines[-1] == ".....":
            locks.append(schematic_lines)
            # Using NumPy to count '#' in columns for locks
            array = np.array([list(line) for line in schematic_lines[1:]])
            lock_codes.append(np.sum(array == "#", axis=0).tolist())
        elif schematic_lines[0] == "....." and schematic_lines[-1] == "#####":
            keys.append(schematic_lines)
            # Using NumPy to count '#' in columns for keys
            array = np.array([list(line) for line in schematic_lines[:-1]])
            key_codes.append(np.sum(array == "#", axis=0).tolist())

    # Match locks and keys
    matches = defaultdict(list)
    match_count = 0

    lock_matrix = np.array(lock_codes)
    key_matrix = np.array(key_codes)

    # Vectorized check for compatibility
    for lock_idx, lock in enumerate(lock_matrix):
        valid_keys = key_matrix[np.all((lock + key_matrix) <= 5, axis=1)]
        for key in valid_keys:
            match_count += 1
            matches[tuple(lock)].append(key.tolist())
    
    return match_count, matches

def main():
    start_time = time.perf_counter()
    match_count, matches = process_file_optimized("input.txt")
    end_time = time.perf_counter()

    # Calculate and format execution time
    execution_time = (end_time - start_time) * 1000 if (end_time - start_time) < 1 else end_time - start_time
    time_unit = "milliseconds" if (end_time - start_time) < 1 else "seconds"

    # Output results
    print(f"Match Count: {match_count}")
    print(f"Execution Time: {execution_time:.3f} {time_unit}")

if __name__ == "__main__":
    main()

