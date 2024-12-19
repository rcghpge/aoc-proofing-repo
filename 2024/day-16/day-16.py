import heapq
from collections import deque

def parse_input(filename):
    with open(filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f]
    return lines

def solve_maze(maze_lines):
    # Directions: 0=East, 1=South, 2=West, 3=North
    directions = [
        (0, 1),   # East
        (1, 0),   # South
        (0, -1),  # West
        (-1, 0)   # North
    ]

    rows = len(maze_lines)
    cols = len(maze_lines[0])

    start, end = None, None
    for r in range(rows):
        for c in range(cols):
            if maze_lines[r][c] == 'S':
                start = (r, c)
            elif maze_lines[r][c] == 'E':
                end = (r, c)
    if not start or not end:
        raise ValueError("Could not find 'S' or 'E' in the maze.")

    INF = float('inf')
    dist = [[[INF]*4 for _ in range(cols)] for __ in range(rows)]
    start_dir = 0
    dist[start[0]][start[1]][start_dir] = 0

    pq = [(0, start[0], start[1], start_dir)]
    heapq.heapify(pq)
    visited = set()

    while pq:
        cost, r, c, d = heapq.heappop(pq)

        if (r, c) == end:
            return cost

        if (r, c, d) in visited:
            continue
        visited.add((r, c, d))

        current_dist = dist[r][c][d]
        if cost > current_dist:
            continue

        # Move forward
        dr, dc = directions[d]
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze_lines[nr][nc] != '#':
            new_cost = cost + 1
            if new_cost < dist[nr][nc][d]:
                dist[nr][nc][d] = new_cost
                heapq.heappush(pq, (new_cost, nr, nc, d))

        # Turn left
        left_dir = (d - 1) % 4
        new_cost = cost + 1000
        if new_cost < dist[r][c][left_dir]:
            dist[r][c][left_dir] = new_cost
            heapq.heappush(pq, (new_cost, r, c, left_dir))

        # Turn right
        right_dir = (d + 1) % 4
        new_cost = cost + 1000
        if new_cost < dist[r][c][right_dir]:
            dist[r][c][right_dir] = new_cost
            heapq.heappush(pq, (new_cost, r, c, right_dir))

    return None  # No path found

def solve_part2(maze_lines):
    rows = len(maze_lines)
    cols = len(maze_lines[0])
    directions = [
        (0, 1),   # East
        (1, 0),   # South
        (0, -1),  # West
        (-1, 0)   # North
    ]

    start, end = None, None
    for r in range(rows):
        for c in range(cols):
            if maze_lines[r][c] == 'S':
                start = (r, c)
            elif maze_lines[r][c] == 'E':
                end = (r, c)
    if not start or not end:
        raise ValueError("Could not find 'S' or 'E' in the maze.")

    INF = float('inf')
    dist = [[[INF]*4 for _ in range(cols)] for __ in range(rows)]
    start_dir = 0
    dist[start[0]][start[1]][start_dir] = 0

    pq = [(0, start[0], start[1], start_dir)]
    heapq.heapify(pq)
    visited = set()

    while pq:
        cost, r, c, d = heapq.heappop(pq)

        if (r, c, d) in visited:
            continue
        visited.add((r, c, d))

        current_dist = dist[r][c][d]
        if cost > current_dist:
            continue

        # Move forward
        dr, dc = directions[d]
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze_lines[nr][nc] != '#':
            new_cost = cost + 1
            if new_cost < dist[nr][nc][d]:
                dist[nr][nc][d] = new_cost
                heapq.heappush(pq, (new_cost, nr, nc, d))

        # Turn left
        left_dir = (d - 1) % 4
        new_cost = cost + 1000
        if new_cost < dist[r][c][left_dir]:
            dist[r][c][left_dir] = new_cost
            heapq.heappush(pq, (new_cost, r, c, left_dir))

        # Turn right
        right_dir = (d + 1) % 4
        new_cost = cost + 1000
        if new_cost < dist[r][c][right_dir]:
            dist[r][c][right_dir] = new_cost
            heapq.heappush(pq, (new_cost, r, c, right_dir))

    min_cost_end = min(dist[end[0]][end[1]][d] for d in range(4))
    if min_cost_end == INF:
        return 0

    on_best_path = [[False]*cols for _ in range(rows)]
    queue = deque((end[0], end[1], d) for d in range(4) if dist[end[0]][end[1]][d] == min_cost_end)
    visited_rev = set(queue)

    while queue:
        r, c, d = queue.popleft()
        on_best_path[r][c] = True

        cost_here = dist[r][c][d]

        dr, dc = directions[d]
        r_prev, c_prev = r - dr, c - dc
        if 0 <= r_prev < rows and 0 <= c_prev < cols:
            if maze_lines[r_prev][c_prev] != '#' and dist[r_prev][c_prev][d] == cost_here - 1:
                if (r_prev, c_prev, d) not in visited_rev:
                    visited_rev.add((r_prev, c_prev, d))
                    queue.append((r_prev, c_prev, d))

        for d_pre in [(d - 1) % 4, (d + 1) % 4]:
            if dist[r][c][d_pre] == cost_here - 1000:
                if (r, c, d_pre) not in visited_rev:
                    visited_rev.add((r, c, d_pre))
                    queue.append((r, c, d_pre))

    return sum(on_best_path[r][c] for r in range(rows) for c in range(cols))

def main():
    maze_lines = parse_input("input.txt")
    part1_result = solve_maze(maze_lines)
    print("Lowest possible score (Part 1):", part1_result)

    part2_result = solve_part2(maze_lines)
    print("Number of tiles on at least one best path (Part 2):", part2_result)

if __name__ == "__main__":
    main()
