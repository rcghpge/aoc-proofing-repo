import time
from collections import defaultdict
import numpy as np

def parse_schematics(input_data):
    """
    Parse schematics into lists of heights for locks and keys.
    Locks have the top row filled, keys have the bottom row filled.
    """
    schematics = input_data.strip().split("\n\n")
    locks, keys = [], []

    for schematic in schematics:
        lines = schematic.splitlines()
        # Determine if it's a lock or a key
        if lines[0] == "#####" and lines[-1] == ".....":
            # Convert lock to pin heights
            cols = [sum(1 for line in lines[1:] if line[i] == "#") for i in range(5)]
            locks.append(cols)
        elif lines[0] == "....." and lines[-1] == "#####":
            # Convert key to heights
            cols = [sum(1 for line in lines[:-1] if line[i] == "#") for i in range(5)]
            keys.append(cols)

    return np.array(locks), np.array(keys)

def count_fitting_pairs_optimized(locks, keys, max_height=5):
    """
    Use numpy broadcasting to count the number of unique lock/key pairs that fit together.
    """
    # Compute pairwise column sums for all lock/key pairs
    lock_key_sums = locks[:, None, :] + keys[None, :, :]

    # Check where column sums are <= max_height
    valid_pairs = np.all(lock_key_sums <= max_height, axis=2)

    # Count valid pairs
    return np.sum(valid_pairs)

# Read input
with open('input.txt', 'r') as f:
    input_data = f.read()

# Execution time
start_time = time.time()

# Parse schematics
locks, keys = parse_schematics(input_data)

# Count fitting pairs with optimized numpy approach
result = count_fitting_pairs_optimized(locks, keys)

end_time = time.time()
execution_time = end_time - start_time

print("Number of unique lock/key pairs that fit together:", result)
if execution_time < 1:
    print(f"Execution time: {execution_time * 1000:.2f} milliseconds")
else:
    print(f"Execution time: {execution_time:.4f} seconds")

