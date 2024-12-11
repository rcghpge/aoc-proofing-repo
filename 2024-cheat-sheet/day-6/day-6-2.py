import time

class T(tuple):
    """Tuple class for handling coordinates and rotations."""
    def __add__(self, other):
        if not isinstance(other, (tuple, T)):
            raise TypeError(f"Cannot add T to non-tuple object: {type(other)}")
        if len(self) != len(other):
            raise ValueError(f"Cannot add T objects of different dimensions: {len(self)} vs {len(other)}")
        return T(tuple(x + y for x, y in zip(self, other)))

    def rot(self):
        """Rotate the direction vector 90 degrees clockwise."""
        x, y = self
        return T((y, -x))

NORTH = T((-1, 0))  # Define the initial direction (up)

def sim(grid, pos, dir):
    """
    Simulates the guard's movement on the grid.
    :param grid: Dictionary representing the grid.
    :param pos: Current position of the guard.
    :param dir: Current direction of the guard.
    :return: Tuple (stuck_in_loop, visited_positions).
    """
    if not isinstance(pos, T) or not isinstance(dir, T):
        raise ValueError(f"Invalid types for pos or dir: {type(pos)}, {type(dir)}")
    
    visited = set()
    while pos in grid:
        if (pos, dir) in visited:
            return True, visited  # The guard gets stuck in a loop.
        visited.add((pos, dir))

        # Ensure addition produces a valid T object
        try:
            next_pos = pos + dir
        except Exception as e:
            raise ValueError(f"Error during position addition: {e}")

        while grid.get(next_pos, '.') == '#':
            dir = dir.rot()  # Rotate direction if an obstacle is ahead.
            try:
                next_pos = pos + dir  # Recalculate after rotation.
            except Exception as e:
                raise ValueError(f"Error during recalculation of next_pos: {e}")

        pos = next_pos  # Move forward.

    return False, visited  # The guard exits the grid.

def read_input(file_path):
    """
    Reads the input file and constructs the grid.
    :param file_path: Path to the input file.
    :return: Tuple (grid, initial_position).
    """
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()
    grid = {T((i, j)): c for i, row in enumerate(lines) for j, c in enumerate(row)}
    pos = next((p for p, c in grid.items() if c == '^'), None)
    if pos is None:
        raise ValueError("Guard starting position ('^') not found in the grid.")
    return grid, pos

def main(input_file):
    try:
        # Time the execution.
        start_time = time.time()

        # Read the input file.
        read_start = time.time()
        grid, pos = read_input(input_file)
        read_end = time.time()

        # Run the simulation.
        sim_start = time.time()
        _, visited = sim(grid, pos, NORTH)
        visited_positions = {p for p, _ in visited}
        sim_end = time.time()

        print(f"Number of distinct positions visited: {len(visited_positions)}")

        # Test possible obstructions.
        obstruction_start = time.time()
        ans = 0
        for vpos in visited_positions:
            if grid[vpos] == '#':  # Skip existing obstacles.
                continue
            grid[vpos] = '#'  # Temporarily place an obstruction.
            try:
                works, _ = sim(grid, pos, NORTH)
            except Exception as e:
                raise ValueError(f"Error during obstruction simulation: {e}")
            ans += works
            grid[vpos] = '.'  # Remove the obstruction.
        obstruction_end = time.time()

        print(f"Number of positions where obstruction causes a loop: {ans}")

        # Print timing summary.
        total_time = time.time() - start_time
        print(f"Execution Time Details:")
        print(f"  Input Reading Time: {read_end - read_start:.4f} seconds")
        print(f"  Initial Simulation Time: {sim_end - sim_start:.4f} seconds")
        print(f"  Obstruction Testing Time: {obstruction_end - obstruction_start:.4f} seconds")
        print(f"  Total Execution Time: {total_time:.4f} seconds")

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    # Specify the input file path.
    input_file = "input.txt"
    main(input_file)

