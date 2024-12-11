import time
from itertools import product
import operator

# Define the available operators
OPS = {
    '+': operator.add,
    '*': operator.mul,
    '||': lambda l, r: int(f"{l}{r}")
}

def parse_input(file_path):
    equations = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():  # Skip empty lines
                target, numbers = line.split(':')
                target = int(target.strip())
                numbers = list(map(int, numbers.strip().split()))
                equations.append((target, numbers))
    return equations

def evaluate_expression(numbers, operators):
    result = numbers[0]
    for num, op in zip(numbers[1:], operators):
        result = OPS[op](result, num)
    return result

def is_valid_equation(target, numbers):
    for ops in product(OPS.keys(), repeat=len(numbers) - 1):
        if evaluate_expression(numbers, ops) == target:
            return True
    return False

def calculate_total_calibration_result(equations):
    total_sum = 0
    for target, numbers in equations:
        if is_valid_equation(target, numbers):
            total_sum += target
    return total_sum

if __name__ == "__main__":
    input_file = "input.txt"  # Ensure this path points to your input.txt file

    # Record the start time
    start_time = time.time()

    equations = parse_input(input_file)
    result = calculate_total_calibration_result(equations)
    print(f"Total Calibration Result: {result}")

    # Record the end time
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.4f} seconds")

