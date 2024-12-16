from collections import deque

def parse_input(file_path):
    """Parse the input from the file."""
    with open(file_path, 'r') as file:
        return file.read().strip().splitlines()[0]

def checksum(values):
    """Calculate checksum for the given list of values."""
    return sum(int(val) * idx for idx, val in enumerate(values) if val != '.')

def initialize_values(input_data):
    """Initialize the value sequence and runs from the input data."""
    values = []
    runs = []
    run_dict = {}
    num = 0

    for i, char in enumerate(input_data):
        count = int(char)
        if i % 2 == 0:  # Value run
            values.extend([num] * count)
            runs.append((num, count))
            run_dict[num] = count
            num += 1
        else:  # Gap
            values.extend(['.'] * count)

    return values, runs, run_dict

def part1(values):
    """Solve part 1 of the problem."""
    result = []
    queue = deque(values)

    while queue:
        current = queue.popleft()
        if current == '.':
            while queue and queue[-1] == '.':
                queue.pop()
            if queue:
                result.append(queue.pop())
        else:
            result.append(current)

    return checksum(result)

def find_gaps(values):
    """Identify gaps in the sequence."""
    gaps = {}
    i = 0
    while i < len(values):
        if values[i] == '.':
            start = i
            while i < len(values) and values[i] == '.':
                i += 1
            gaps[start] = i - start
        else:
            i += 1
    return gaps

def fill_gaps_part2(values, runs, gaps):
    """Fill gaps for part 2 based on file movement rules."""
    filled_gaps = {}
    for file_id, length in reversed(runs):
        # Find all gaps large enough to fit the current file
        candidates = [(start, gap_len) for start, gap_len in gaps.items() if gap_len >= length]
        if not candidates:
            continue

        # Choose the leftmost valid gap
        start, gap_len = min(candidates, key=lambda x: x[0])
        filled_gaps[start] = (file_id, length)

        # Update gaps
        del gaps[start]
        if gap_len > length:
            gaps[start + length] = gap_len - length

    return filled_gaps

def part2(values, runs):
    """Solve part 2 of the problem."""
    gaps = find_gaps(values)
    filled_gaps = fill_gaps_part2(values, runs, gaps)

    result = []
    i = 0

    while i < len(values):
        if i in filled_gaps:
            file_id, length = filled_gaps[i]
            result.extend([str(file_id)] * length)
            i += length
        elif values[i] == '.':
            result.append('.')
            i += 1
        else:
            result.append(values[i])
            i += 1

    return checksum(result)

if __name__ == "__main__":
    input_data = parse_input("input.txt")
    values, runs, _ = initialize_values(input_data)

    print(part1(values))
    print(part2(values, runs))

