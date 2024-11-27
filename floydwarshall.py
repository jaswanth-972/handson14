from typing import List, Dict, Tuple, Optional


def floyd_warshall_algorithm(graph: Dict[str, List[Tuple[str, int]]]) -> Tuple[List[List[float]], List[List[Optional[str]]], List[str]]:
    """
    Floyd-Warshall algorithm to compute shortest paths between all pairs of vertices.
    
    Args:
        graph: A dictionary where each key is a vertex, and its value is a list of tuples
               representing edges as (neighbor, weight).

    Returns:
        A tuple containing:
            - distances: 2D list representing shortest distances between each pair of vertices.
            - next_vertex: 2D list for path reconstruction; next_vertex[i][j] is the next vertex on the path from i to j.
            - vertices: List of vertices corresponding to indices in the matrices.
    """
    if not graph:
        raise ValueError("The input graph is empty.")

    # Extract all vertices and map them to indices
    vertices = list(graph.keys())
    vertex_indices = {vertex: idx for idx, vertex in enumerate(vertices)}
    num_vertices = len(vertices)

    # Initialize distance and path matrices
    distances = [[float('inf')] * num_vertices for _ in range(num_vertices)]
    next_vertex = [[None] * num_vertices for _ in range(num_vertices)]

    # Set distance from each vertex to itself as zero
    for i in range(num_vertices):
        distances[i][i] = 0

    # Populate initial distances and paths based on edges in the graph
    for origin, edges in graph.items():
        for destination, weight in edges:
            i, j = vertex_indices[origin], vertex_indices[destination]
            distances[i][j] = weight
            next_vertex[i][j] = destination

    # Perform Floyd-Warshall updates
    for k in range(num_vertices):  # Intermediate vertex
        for i in range(num_vertices):  # Source vertex
            for j in range(num_vertices):  # Destination vertex
                if distances[i][k] + distances[k][j] < distances[i][j]:
                    distances[i][j] = distances[i][k] + distances[k][j]
                    next_vertex[i][j] = next_vertex[i][k]

    # Check for negative weight cycles
    for i in range(num_vertices):
        if distances[i][i] < 0:
            raise ValueError("The graph contains a negative weight cycle.")

    return distances, next_vertex, vertices


def display_matrix(matrix: List[List[float]], vertices: List[str], title: str = "Matrix") -> None:
    """
    Displays a 2D matrix in a human-readable format.
    
    Args:
        matrix: 2D list of values (distances or paths).
        vertices: List of vertex labels.
        title: Title for the matrix display.
    """
    print(f"\n{title}:")
    print("    ", "  ".join(f"{v:<5}" for v in vertices))
    for i, row in enumerate(matrix):
        print(f"{vertices[i]:<4} ", "  ".join(f"{val if val != float('inf') else '∞':<5}" for val in row))


def reconstruct_path(next_vertex: List[List[Optional[str]]], vertices: List[str], start: str, end: str) -> List[str]:
    """
    Reconstructs the shortest path from start to end using the next_vertex matrix.
    
    Args:
        next_vertex: 2D list where next_vertex[i][j] gives the next vertex to visit.
        vertices: List of vertex labels.
        start: Start vertex.
        end: End vertex.

    Returns:
        A list of vertices representing the shortest path, or an empty list if no path exists.
    """
    vertex_indices = {vertex: idx for idx, vertex in enumerate(vertices)}
    i, j = vertex_indices[start], vertex_indices[end]

    if next_vertex[i][j] is None:
        return []  # No path exists

    path = [start]
    while start != end:
        start = next_vertex[i][j]
        path.append(start)
        i = vertex_indices[start]

    return path


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
        # Execute the Floyd-Warshall algorithm
        distances, next_vertex, vertices = floyd_warshall_algorithm(graph)

        # Display the shortest path distance matrix
        display_matrix(distances, vertices, title="Shortest Path Distance Matrix")

        # Reconstruct and display paths between specific pairs
        print("\nShortest paths between vertices:")
        for start in vertices:
            for end in vertices:
                if start != end:
                    path = reconstruct_path(next_vertex, vertices, start, end)
                    path_str = " -> ".join(path) if path else "No path"
                    print(f"Path from {start} to {end}: {path_str}")
    except ValueError as e:
        print(e)
