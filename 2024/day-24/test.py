import re
from typing import Dict, List


def parse_input() -> List[List[str]]:
    # Reads and parse input
    with open("input.txt", "r") as f:
        return [part.split("\n") for part in f.read().strip().split("\n\n")]


def simulate_gates(data):
    # Logic gate simulation
    state: Dict[str, int] = {}
    for wire in data[0]:
        name, value = wire.split(": ")
        state[name] = int(value)

    loop = True
    while loop:
        should_loop_again = False
        for gate in data[1]:
            match = re.match(r"^(.*) (AND|OR|XOR) (.*) -> (.*)$", gate)
            if match:
                left, operator, right, output = match.groups()
                if left not in state or right not in state:
                    should_loop_again = True
                    continue
                if operator == "AND":
                    state[output] = state[left] & state[right]
                elif operator == "OR":
                    state[output] = state[left] | state[right]
                elif operator == "XOR":
                    state[output] = state[left] ^ state[right]
        loop = should_loop_again

    return state


def zwire_decimals() -> int:
    # Decimals calculation for binary representation of z wires
    data = parse_input()
    state = simulate_gates(data)
    bits = "".join(
        str(state[name])
        for name, _ in sorted(
            filter(lambda x: x[0].startswith("z"), state.items()),
            key=lambda x: x[0],
            reverse=True,
        )
    )
    return int(bits, 2)


def find(a, b, operator, gates):
    # Output wire based on operators
    for gate in gates:
        if gate.startswith(f"{a} {operator} {b}") or gate.startswith(f"{b} {operator} {a}"):
            return gate.split(" -> ").pop()
    return None


def wire_calculations():
    # logic gate swapping
    data = parse_input()
    swapped = []
    c0 = None

    # Iterate over range - 45 wires
    for i in range(45):
        n = str(i).zfill(2)
        m1, n1, r1, z1, c1 = None, None, None, None, None

        # Find XOR and AND gates - half-adder logic
        m1 = find(f"x{n}", f"y{n}", "XOR", data[1])
        n1 = find(f"x{n}", f"y{n}", "AND", data[1])

        if c0:
            # Binary addition - ripple carry adder
            r1 = find(c0, m1, "AND", data[1])
            if not r1:
                m1, n1 = n1, m1
                swapped.extend([m1, n1])
                r1 = find(c0, m1, "AND", data[1])

            z1 = find(c0, m1, "XOR", data[1])

            if m1 and m1.startswith("z"):
                m1, z1 = z1, m1
                swapped.extend([m1, z1])

            if n1 and n1.startswith("z"):
                n1, z1 = z1, n1
                swapped.extend([n1, z1])

            if r1 and r1.startswith("z"):
                r1, z1 = z1, r1
                swapped.extend([r1, z1])

            c1 = find(r1, n1, "OR", data[1])

        if c1 and c1.startswith("z") and c1 != "z45":
            c1, z1 = z1, c1
            swapped.extend([c1, z1])

        c0 = c1 if c0 else n1

    return ",".join(sorted(set(swapped)))  # sort and redundancy check


# Part 1:
print("Part 1: Decimal number output on wires starting with 'z' -", zwire_decimals())

# Part 2:
print("Part 2: Sort and swap wire names -", wire_calculations())

