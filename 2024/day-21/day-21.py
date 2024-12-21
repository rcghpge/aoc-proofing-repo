from time import perf_counter_ns
import os
from itertools import permutations
from functools import cache
from typing import Any

input_file = os.path.join(os.path.dirname(__file__), "input.txt")


# Time profiling
def profiler(method):
    def wrapper_method(*args: Any, **kwargs: Any) -> Any:
        start = perf_counter_ns()
        result = method(*args, **kwargs)
        end = perf_counter_ns() - start
        time_len = min(9, ((len(str(end)) - 1) // 3) * 3)
        timeConv = {9: 's', 6: 'ms', 3: 'µs', 0: 'ns'}
        print(f"Answer: {result} - Elapsed time: {end / (10 ** time_len)} {timeConv[time_len]}")
        return result

    return wrapper_method


def read_data(file_path):
    with open(file_path) as file:
        return file.readlines()


# Define keypad and arrows
keypad = [list('789'), list('456'), list('123'), list(' 0A')]
arrows = [list(' ^A'), list('<v>')]

# Dictionaries for keypad and arrows
keypad_dict = {}
for i, row in enumerate(keypad):
    for j, c in enumerate(row):
        keypad_dict[c] = (i, j)

arrows_dict = {}
for i, row in enumerate(arrows):
    for j, c in enumerate(row):
        arrows_dict[c] = (i, j)


# Calculate keystrokes on arrows keypad
@cache
def quantifyStrokes(code):
    curr = arrows_dict['A']
    total = 0
    for x in code:
        coords = arrows_dict[x]
        total += abs(coords[0] - curr[0]) + abs(coords[1] - curr[1]) + 1
        curr = coords
    return total


# Recursive keystroke calculation on arrows keypad
@cache
def numPadKeystrokes(code, recurse):
    if recurse == 0:
        return quantifyStrokes(code)
    curr = arrows_dict['A']
    avoidPad = arrows_dict[' ']
    totalNum = 0
    for x in code:
        coords = arrows_dict[x]
        dy = coords[0] - curr[0]
        dx = coords[1] - curr[1]
        s = 'v' * dy if dy > 0 else '^' * (-dy)
        s += '>' * dx if dx > 0 else '<' * (-dx)
        min_keystrokes = float('inf')
        for p in permutations(s):
            n = curr
            for char in p:
                if char == 'v':
                    n = (n[0] + 1, n[1])
                elif char == '^':
                    n = (n[0] - 1, n[1])
                elif char == '>':
                    n = (n[0], n[1] + 1)
                elif char == '<':
                    n = (n[0], n[1] - 1)
                if n == avoidPad:
                    break
            if n == avoidPad:
                continue
            # Recursive call on numPadKeystrokes
            min_keystrokes = min(numPadKeystrokes(''.join(p) + 'A', recurse - 1), min_keystrokes)
        curr = coords
        totalNum += min_keystrokes
    return totalNum


# Keystroke calculation with recursive calls on keypad
@cache
def part1Keystrokes(code):
    curr = keypad_dict['A']
    avoidPad = keypad_dict[' ']
    totalNum = 0
    for x in code:
        coords = keypad_dict[x]
        dy = coords[0] - curr[0]
        dx = coords[1] - curr[1]
        s = 'v' * dy if dy > 0 else '^' * (-dy)
        s += '>' * dx if dx > 0 else '<' * (-dx)
        min_keystrokes = float('inf')
        for p in permutations(s):
            n = curr
            for char in p:
                if char == 'v':
                    n = (n[0] + 1, n[1])
                elif char == '^':
                    n = (n[0] - 1, n[1])
                elif char == '>':
                    n = (n[0], n[1] + 1)
                elif char == '<':
                    n = (n[0], n[1] - 1)
                if n == avoidPad:
                    break
            if n == avoidPad:
                continue
            min_keystrokes = min(numPadKeystrokes(''.join(p) + 'A', 1),
                                 min_keystrokes)  # first call on numPadKeystrokes
        curr = coords
        totalNum += min_keystrokes
    return totalNum


# Keystroke calculation with recursive calls (more levels)
@cache
def part2Keystrokes(codeSequence):
    curr = keypad_dict['A']
    avoidPad = keypad_dict[' ']
    totalNum = 0
    for x in codeSequence:
        coords = keypad_dict[x]
        dy = coords[0] - curr[0]
        dx = coords[1] - curr[1]
        s = 'v' * dy if dy > 0 else '^' * (-dy)
        s += '>' * dx if dx > 0 else '<' * (-dx)
        min_keystrokes = float('inf')
        for p in permutations(s):
            n = curr
            for char in p:
                if char == 'v':
                    n = (n[0] + 1, n[1])
                elif char == '^':
                    n = (n[0] - 1, n[1])
                elif char == '>':
                    n = (n[0], n[1] + 1)
                elif char == '<':
                    n = (n[0], n[1] - 1)
                if n == avoidPad:
                    break
            if n == avoidPad:
                continue
            min_keystrokes = min(numPadKeystrokes(''.join(p) + 'A', 24),
                                 min_keystrokes)  # first call on numPadKeystrokes
        curr = coords
        totalNum += min_keystrokes
    return totalNum


# Part 1
@profiler
def part1(arg):
    calculate = 0
    for line in arg:
        numberVal = line.strip()[:-1]
        calculate += part1Keystrokes(line.strip()) * int(numberVal)
    return calculate


# Part 2
@profiler
def part2(arg):
    calculate = 0
    for line in arg:
        numberVal = line.strip()[:-1]
        calculate += part2Keystrokes(line.strip()) * int(numberVal)
    return calculate


if __name__ == "__main__":
    data = read_data(input_file)
    part1(data)
    part2(data)
