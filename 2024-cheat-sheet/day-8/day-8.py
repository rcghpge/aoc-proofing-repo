from collections import defaultdict
from pathlib import Path
from itertools import product

# Duplicate test values in input
fn = Path(__file__).parent / "input.txt"
lines = fn.read_text().strip().split("\n")

freq_lut = defaultdict(list)
for ri, line in enumerate(lines):
    for ci, freq in enumerate(line):
        if freq != ".":
            freq_lut[freq].append((ri, ci))

antinodes = defaultdict(list)
for freq, coords in freq_lut.items():
    # coordinates pairs
    for coord_pair in product(coords, coords):
        if coord_pair[0] == coord_pair[1]:
            continue

        # calculate row,col delta
        dr = coord_pair[1][0] - coord_pair[0][0]
        dc = coord_pair[1][1] - coord_pair[0][1]
        # add to second
        an1 = (coord_pair[1][0] + dr, coord_pair[1][1] + dc)
        # subtract from first
        an0 = (coord_pair[0][0] - dr, coord_pair[0][1] - dc)
        # check valid
        if an1[0] >= 0 and an1[0] < len(lines) and an1[1] >= 0 and an1[1] < len(lines[0]):
            antinodes[an1].append(freq)
        if an0[0] >= 0 and an0[0] < len(lines) and an0[1] >= 0 and an0[1] < len(lines[0]):
            antinodes[an0].append(freq)

print(f"Part 1: {len(antinodes.keys())}")

# Part 2
def march(start, m, delta_c, antinodes2):
    antinodes2.add(start)
    dc = delta_c
    while True:
        r = start[0] + m * dc  # float
        c = start[1] + dc  # int
        if r < 0 or r >= len(lines) or c < 0 or c >= len(lines[0]):
            break
        # check r close to integer
        if abs(r - int(r)) < 1e-6:
            antinodes2.add((int(r), c))

        dc += delta_c


antinodes2 = set()
for freq, coords in freq_lut.items():
    # coordinates pairs
    for coord_pair in product(coords, coords):
        if coord_pair[0] == coord_pair[1]:
            continue

        # calculate row,col delta
        dr = coord_pair[1][0] - coord_pair[0][0]
        dc = coord_pair[1][1] - coord_pair[0][1]

        # gradient
        m = dr / dc

        # march "up" along gradient
        march(coord_pair[0], m, 1, antinodes2)
        # march "down"
        march(coord_pair[0], m, -1, antinodes2)

print(f"Part 2: {len(antinodes2)}")
