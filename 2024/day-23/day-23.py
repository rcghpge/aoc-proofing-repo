import networkx as nx
import re

def parse_graph(filename):
    """
    Parse the input file to create a graph using NetworkX.
    Each line in the file represents an edge between two nodes.
    """
    graph = nx.Graph()
    with open(filename, 'r') as file:
        for line in file:
            match = re.match(r"(\w+)-(\w+)", line.strip())
            if match:
                a, b = match.groups()
                graph.add_edge(a, b)
    return graph

def find_triangles(graph):
    """
    Find all triangles in the graph.
    A triangle is a set of three nodes where each node is connected to the other two.
    """
    triangles = set()
    for node in graph:
        neighbors = set(graph.neighbors(node))
        for neighbor in neighbors:
            common_neighbors = neighbors.intersection(graph.neighbors(neighbor))
            for common in common_neighbors:
                triangle = tuple(sorted([node, neighbor, common]))
                triangles.add(triangle)
    return list(triangles)

def filter_triangles_by_prefix(triangles, prefix):
    """
    Filters triangles to include only those where at least one node starts with the given prefix.
    """
    return [triangle for triangle in triangles if any(node.startswith(prefix) for node in triangle)]

def print_filtered_triangles_sample(filtered_triangles):
    """
    Prints a concise sample of the filtered triangles and their count.
    """
    print("Sample of Filtered Triangles (at least one node starts with 't', up to 3):")
    for triangle in filtered_triangles[:3]:  # Show only the first 3 filtered triangles
        print(triangle)

    print(f"\nNumber of triangles containing at least one 't': {len(filtered_triangles)}")

def find_largest_clique(graph):
    """
    Finds the largest clique in the graph.
    Returns the sorted list of nodes in the largest clique.
    """
    cliques = list(nx.find_cliques(graph))  # Find all maximal cliques
    largest_clique = max(cliques, key=len)  # Find the largest clique
    return sorted(largest_clique)          # Return sorted nodes in the clique

def generate_password(clique):
    """
    Generate the password by joining the sorted clique nodes with commas.
    """
    return ",".join(clique)

def print_part2_results(largest_clique, password):
    """
    Prints the results for Part 2: largest clique and the password.
    """
    print("\nPart 2 Results:")
    print(f"Largest Clique: {largest_clique}")
    print(f"The password to get into the LAN party is: {password}")

if __name__ == "__main__":
    input_file = "input.txt"  # Replace with your input file path

    # Parse the input and create the graph
    graph = parse_graph(input_file)

    # Part 1: Find triangles and filter by prefix 't'
    triangles = find_triangles(graph)
    filtered_triangles = filter_triangles_by_prefix(triangles, 't')
    print_filtered_triangles_sample(filtered_triangles)

    # Part 2: Find the largest clique and generate the password
    largest_clique = find_largest_clique(graph)
    password = generate_password(largest_clique)
    print_part2_results(largest_clique, password)

