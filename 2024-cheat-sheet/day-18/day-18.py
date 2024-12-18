from collections import deque

def read_input(file_path):
    """Reads input data from a file."""
    with open(file_path, 'r') as f:
        return [tuple(map(int, line.strip().split(','))) for line in f]

def simulate_falling_bytes(grid_size, byte_positions, num_bytes):
    """Simulates falling bytes and returns the grid after the specified number of bytes."""
    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

    for i, (x, y) in enumerate(byte_positions):
        if i >= num_bytes:
            break
        if 0 <= x < grid_size and 0 <= y < grid_size:  # Skip out-of-bound coordinates
            grid[y][x] = 1  # Mark the position as corrupted

    return grid

def is_valid(x, y, grid):
    """Checks if a position is within bounds and not corrupted."""
    return 0 <= x < len(grid) and 0 <= y < len(grid) and grid[y][x] == 0

def find_shortest_path(grid):
    """Finds the shortest path from top-left to bottom-right using BFS."""
    start, end = (0, 0), (len(grid) - 1, len(grid) - 1)
    queue = deque([(start, 0)])  # (position, steps)
    visited = set()
    visited.add(start)

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        (x, y), steps = queue.popleft()

        if (x, y) == end:
            return steps

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if is_valid(nx, ny, grid) and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), steps + 1))

    return -1  # Return -1 if there's no valid path

def find_blocking_byte(byte_positions, grid_size):
    """Finds the first byte that blocks the path to the exit."""
    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

    for i, (x, y) in enumerate(byte_positions):
        if 0 <= x < grid_size and 0 <= y < grid_size:  # Skip out-of-bound coordinates
            grid[y][x] = 1  # Mark the position as corrupted
            if find_shortest_path(grid) == -1:
                return x, y

    return None  # If no byte blocks the path

def main():
    file_path = "input.txt"
    num_bytes = 1024

    byte_positions = read_input(file_path)
    # Dynamically determine grid size
    max_x = max(x for x, y in byte_positions)
    max_y = max(y for x, y in byte_positions)
    grid_size = max(max_x, max_y) + 1  # Ensure grid size covers all positions

    # Part 1: Minimum steps to exit after first 1024 bytes
    grid = simulate_falling_bytes(grid_size, byte_positions, num_bytes)
    shortest_path_steps = find_shortest_path(grid)
    print(f"Minimum number of steps to reach the exit: {shortest_path_steps}")

    # Part 2: Find the first byte that blocks the path
    blocking_byte = find_blocking_byte(byte_positions, grid_size)
    if blocking_byte:
        print(f"First byte that blocks the path: {blocking_byte[0]},{blocking_byte[1]}")
    else:
        print("No byte blocks the path.")

if __name__ == "__main__":
    main()

