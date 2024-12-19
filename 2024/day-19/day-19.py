# Day 19 Linen Layout
from collections import Counter

def parse_input(file_path):
    with open(file_path, 'r') as f:
        lines = f.read().strip().split('\n')

    # Towel patterns
    towel_patterns = lines[0].split(', ')

    # Desired designs
    blank_line_index = lines.index('')
    desired_designs = lines[blank_line_index + 1:]

    return towel_patterns, desired_designs

def can_construct_design(design, patterns):
    """Check if design can be constructed using given patterns."""
    def can_construct(remaining, memo):
        if remaining in memo:
            return memo[remaining]
        if remaining == "":
            return True
        for pattern in patterns:
            if remaining.startswith(pattern):
                if can_construct(remaining[len(pattern):], memo):
                    memo[remaining] = True
                    return True
        memo[remaining] = False
        return False

    return can_construct(design, {})

def count_possible_designs(file_path):
    towel_patterns, desired_designs = parse_input(file_path)

    # Count number of possible designs
    possible_count = 0
    for design in desired_designs:
        if can_construct_design(design, towel_patterns):
            possible_count += 1

    return possible_count

def count_arrangements(design, patterns):
    """Count number of ways design can be constructed."""
    def count_ways(remaining, memo):
        if remaining in memo:
            return memo[remaining]
        if remaining == "":
            return 1
        total_ways = 0
        for pattern in patterns:
            if remaining.startswith(pattern):
                total_ways += count_ways(remaining[len(pattern):], memo)
        memo[remaining] = total_ways
        return total_ways

    return count_ways(design, {})

def total_arrangements(file_path):
    towel_patterns, desired_designs = parse_input(file_path)

    total_ways = 0
    for design in desired_designs:
        total_ways += count_arrangements(design, towel_patterns)

    return total_ways

if __name__ == "__main__":
    input_file = "input.txt"  # Replace input file/path

    # Part 1: Count possible designs
    possible_designs = count_possible_designs(input_file)
    print(f"Number of possible designs: {possible_designs}")

    # Part 2: Total number of arrangements
    total_ways = total_arrangements(input_file)
    print(f"Total number of arrangements: {total_ways}")

