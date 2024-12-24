import re
import networkx as nx


def read_input(file_path):
    """
    Reads the input file and parses initial wire values and gate definitions.
    """
    with open(file_path, "r") as f:
        lines = f.read().strip().split("\n")

    wire_values = {}
    gates = []

    # Regex patterns for validation
    wire_value_pattern = re.compile(r"^([a-zA-Z0-9_]+):\s*([01])$")
    gate_pattern = re.compile(r"^([a-zA-Z0-9_]+)\s+(AND|OR|XOR)\s+([a-zA-Z0-9_]+)\s+->\s+([a-zA-Z0-9_]+)$")

    for line in lines:
        line = line.strip()

        # Skip blank lines or comments
        if not line or line.startswith("#"):
            continue

        # Match wire value lines
        wire_value_match = wire_value_pattern.match(line)
        if wire_value_match:
            wire, value = wire_value_match.groups()
            wire_values[wire] = bool(int(value))
            continue

        # Match gate definition lines
        gate_match = gate_pattern.match(line)
        if gate_match:
            gates.append(line.strip())
            continue

        # If the line doesn't match any pattern, raise an error
        raise ValueError(f"Invalid input line: {line}")

    return wire_values, gates


def build_dependency_graph(gates):
    """
    Builds a directed acyclic graph (DAG) from the gate definitions.
    """
    G = nx.DiGraph()
    gate_operations = {}
    gate_pattern = re.compile(r"^([a-zA-Z0-9_]+)\s+(AND|OR|XOR)\s+([a-zA-Z0-9_]+)\s+->\s+([a-zA-Z0-9_]+)$")

    for gate in gates:
        match = gate_pattern.match(gate)
        if match:
            input1, operation, input2, output = match.groups()
            G.add_edge(input1, output)
            G.add_edge(input2, output)
            gate_operations[output] = (operation, input1, input2)
        else:
            raise ValueError(f"Invalid gate format: {gate}")

    return G, gate_operations


def resolve_value(wire, wire_values, gate_operations):
    """
    Resolves the value of a wire using boolean logic.
    """
    if wire in wire_values:
        return wire_values[wire]

    if wire not in gate_operations:
        raise KeyError(f"Wire '{wire}' is not defined in gate operations or initial values.")

    operation, input1, input2 = gate_operations[wire]
    val1 = resolve_value(input1, wire_values, gate_operations)
    val2 = resolve_value(input2, wire_values, gate_operations)

    if operation == "AND":
        result = val1 and val2
    elif operation == "OR":
        result = val1 or val2
    elif operation == "XOR":
        result = val1 ^ val2
    else:
        raise ValueError(f"Unknown operation: {operation}")

    wire_values[wire] = result
    return result


def compute_binary_output(z_wires, wire_values):
    """
    Uses full-adder logic to compute the binary and decimal output from z wires.
    """
    z_wires_sorted = sorted(z_wires)  # Ensure z wires are sorted correctly
    binary_output = "".join(str(int(wire_values[wire])) for wire in z_wires_sorted)
    return binary_output, int(binary_output, 2)


def simulate_gates(file_path):
    """
    Simulates the gate system and computes the output.
    """
    wire_values, gates = read_input(file_path)
    G, gate_operations = build_dependency_graph(gates)

    if not nx.is_directed_acyclic_graph(G):
        raise ValueError("The dependency graph contains cycles.")

    # Resolve all wires in topological order
    for wire in nx.topological_sort(G):
        if wire not in wire_values:
            resolve_value(wire, wire_values, gate_operations)

    # Extract z wires and compute final output
    z_wires = [wire for wire in wire_values if wire.startswith("z")]
    if not z_wires:
        raise ValueError("No wires starting with 'z' found in the input.")

    binary_output, decimal_output = compute_binary_output(z_wires, wire_values)
    return binary_output, decimal_output


if __name__ == "__main__":
    input_file = "input.txt"  # Replace with your input file name
    try:
        binary_result, decimal_result = simulate_gates(input_file)
        print(f"Binary Output: {binary_result}")
        print(f"Decimal Output: {decimal_result}")
    except ValueError as e:
        print(f"Invalid input: {e}")
    except KeyError as e:
        print(f"Simulation failed: {e}")

