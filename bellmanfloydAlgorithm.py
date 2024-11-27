def bellman_ford_algorithm(graph: dict[str, list[tuple[str, float]]], source: str) -> tuple[dict[str, float], dict[str, str]]:
    """
    Bellman-Ford algorithm to compute shortest paths from a single source.
    Handles negative weights and detects negative weight cycles.

    Args:
        graph (dict): A dictionary where each key is a vertex, and its value is a list of tuples
                      representing edges as (neighbor, weight).
        source (str): The starting vertex.

    Returns:
        tuple:
            - A dictionary of shortest distances from the source to each vertex.
            - A dictionary mapping each vertex to its predecessor in the shortest path.

    Raises:
        ValueError: If the graph contains a negative weight cycle.
    """
    # Initialize distances and predecessors
    distances: dict[str, float] = {vertex: float('inf') for vertex in graph}
    predecessors: dict[str, str | None] = {vertex: None for vertex in graph}
    distances[source] = 0

    # Extract all edges from the graph
    edges = [(start, end, weight) for start in graph for end, weight in graph[start]]

    # Relax edges |V| - 1 times
    for _ in range(len(graph) - 1):
        for start, end, weight in edges:
            if distances[start] + weight < distances[end]:
                distances[end] = distances[start] + weight
                predecessors[end] = start

    # Check for negative weight cycles
    for start, end, weight in edges:
        if distances[start] + weight < distances[end]:
            raise ValueError("The graph contains a negative weight cycle.")

    return distances, predecessors


def reconstruct_path(predecessors: dict[str, str | None], target: str) -> list[str]:
    """
    Reconstructs the shortest path to the target using the predecessors dictionary.

    Args:
        predecessors (dict): A dictionary mapping each vertex to its predecessor.
        target (str): The target vertex.

    Returns:
        list: The reconstructed path as a list of vertices.
    """
    path = []
    current = target
    while current is not None:
        path.insert(0, current)
        current = predecessors[current]
    return path


def display_results(distances: dict[str, float], predecessors: dict[str, str | None], source: str) -> None:
    """
    Displays the shortest distances and paths from the source vertex.

    Args:
        distances (dict): Dictionary of shortest distances from the source.
        predecessors (dict): Dictionary of predecessors for reconstructing paths.
        source (str): The source vertex.
    """
    print(f"Minimum distances from source '{source}':")
    for vertex, distance in distances.items():
        distance_str = f"{distance}" if distance < float('inf') else "∞"
        print(f"{vertex}: {distance_str}")

    print("\nShortest paths from source:")
    for vertex in distances:
        if distances[vertex] < float('inf'):
            path = reconstruct_path(predecessors, vertex)
            print(f"Path to {vertex}: {' -> '.join(path)}")
        else:
            print(f"Path to {vertex}: No path")


# Example usage with a sample graph
if __name__ == "__main__":
    graph = {
        'A': [('B', 3), ('C', 5)],
        'B': [('C', 2), ('D', 6)],
        'C': [('B', 1), ('D', 4), ('E', 6)],
        'D': [('E', 2)],
        'E': [('A', 3), ('D', 7)],
    }

    try:
        source = 'A'
        distances, predecessors = bellman_ford_algorithm(graph, source)
        display_results(distances, predecessors, source)
    except ValueError as error:
        print(error)
