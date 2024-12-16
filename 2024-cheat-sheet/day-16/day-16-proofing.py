import heapq
from collections import deque

def parse_input(filename):
    """Parse the maze input from a file."""
    with open(filename, 'r') as f:
        return [line.rstrip('\n') for line in f]

def find_positions(maze, char):
    """Find positions of 'S' (start) and 'E' (end) in the maze."""
    for r, row in enumerate(maze):
        for c, cell in enumerate(row):
            if cell == char:
                return (r, c)
    return None

def traverse_maze(maze, start, end, return_distances=False):
    rows, cols = len(maze), len(maze[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # East, South, West, North
    inf = float('inf')
    dist = [[[inf] * 4 for _ in range(cols)] for __ in range(rows)]  # Distance for each direction
    dist[start[0]][start[1]][0] = 0  # Start facing East
    pq = [(0, start[0], start[1], 0)]  # (cost, row, col, direction)

    while pq:
        cost, r, c, d = heapq.heappop(pq)

        # Validate Part 1 traversal
        if not return_distances and (r, c) == end:
            return cost

        # Explore all moves
        for i, (dr, dc) in enumerate(directions):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != '#':
                move_cost = cost + 1 if i == d else cost + 1000
                if move_cost < dist[nr][nc][i]:
                    dist[nr][nc][i] = move_cost
                    heapq.heappush(pq, (move_cost, nr, nc, i))

    return dist if return_distances else inf

def backtrack_path(maze, dist, end):
    rows, cols = len(maze), len(maze[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # East, South, West, North
    min_cost = min(dist[end[0]][end[1]])  # minimal traversal path
    queue = deque((end[0], end[1], d) for d in range(4) if dist[end[0]][end[1]][d] == min_cost)
    best_path = set(queue)  # Track tiles to optimum  paths

    while queue:
        r, c, d = queue.popleft()

        # Backtracked path to previous tiles
        for i, (dr, dc) in enumerate(directions):
            nr, nc = r - dr, c - dc
            if 0 <= nr < rows and 0 <= nc < cols:
                move_cost = dist[nr][nc][i]
                if move_cost + 1 == dist[r][c][d]:  # Valid forward move
                    if (nr, nc, i) not in best_path:
                        best_path.add((nr, nc, i))
                        queue.append((nr, nc, i))

        # Rotations
        for rot_dir in [(d - 1) % 4, (d + 1) % 4]:
            if dist[r][c][rot_dir] + 1000 == dist[r][c][d]:  # Valid rotation
                if (r, c, rot_dir) not in best_path:
                    best_path.add((r, c, rot_dir))
                    queue.append((r, c, rot_dir))

    # Return unique tile positions
    return len(set((r, c) for r, c, _ in best_path))

def main():
    maze = parse_input("input.txt")
    start, end = find_positions(maze, 'S'), find_positions(maze, 'E')

    # Part 1: Minimum score to reach 'E'
    part1_result = traverse_maze(maze, start, end, return_distances=False)
    print("Lowest possible score (Part 1):", part1_result)

    # Part 2: Count tiles on any best path
    dist = traverse_maze(maze, start, end, return_distances=True)
    part2_result = backtrack_path(maze, dist, end)
    print("Number of tiles on at least one best path (Part 2):", part2_result)

if __name__ == "__main__":
    main()

