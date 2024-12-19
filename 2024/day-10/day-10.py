# Function to parse the input file into a grid of integers
def parse_input(file_name):
    return [list(map(int, line.strip())) for line in open(file_name)]

# Function to find the neighbors (up, down, left, right) of a given cell in the grid
def find_neighbors(x, y, grid):
    return [(nx, ny) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)] if 0 <= (nx := x + dx) < len(grid) and 0 <= (ny := y + dy) < len(grid[0])]

# Depth-First Search (DFS) to find all targets (height 9) reachable from a trailhead (height 0)
def dfs(grid, x, y, height, visited, targets):
    # Base case: stop if already visited or height does not match
    if (x, y) in visited or grid[x][y] != height: return
    visited.add((x, y))  # Mark cell as visited
    if grid[x][y] == 9: targets.add((x, y))  # Add target if height is 9
    # Recursively explore valid neighbors
    for nx, ny in find_neighbors(x, y, grid):
        dfs(grid, nx, ny, height + 1, visited, targets)

# DFS to count distinct paths to height 9 from a trailhead
# Each path is valid if it increments height by exactly 1 at each step
def dfs_paths(grid, x, y, height, visited):
    # Base case: stop if visited or height does not match
    if (x, y) in visited or grid[x][y] != height: return 0
    visited.add((x, y))  # Mark cell as visited
    if grid[x][y] == 9:  # If current cell is height 9, count as one path
        visited.remove((x, y))
        return 1
    # Recursively count paths from valid neighbors
    paths = sum(dfs_paths(grid, nx, ny, height + 1, visited) for nx, ny in find_neighbors(x, y, grid))
    visited.remove((x, y))  # Backtrack to allow other paths
    return paths

# Main computation function to handle Part 1 and Part 2
# Part 1: Count distinct height-9 targets reachable from all trailheads (height 0)
# Part 2: Count distinct paths to height 9 from all trailheads

def compute(grid, part):
    result = 0
    for x in range(len(grid)):  # Iterate through rows
        for y in range(len(grid[0])):  # Iterate through columns
            if grid[x][y] == 0:  # Only process trailheads (height 0)
                if part == 1:
                    visited, targets = set(), set()
                    dfs(grid, x, y, 0, visited, targets)  # Find reachable targets
                    result += len(targets)  # Count targets
                else:
                    result += dfs_paths(grid, x, y, 0, set())  # Count the paths
    return result

# Parse the input file and compute results for both parts
print(f"Part 1: {compute(parse_input('input.txt'), 1)}")  # Output result for Part 1
print(f"Part 2: {compute(parse_input('input.txt'), 2)}")  # Output result for Part 2
