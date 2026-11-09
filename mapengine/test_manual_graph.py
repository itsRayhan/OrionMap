
from time import perf_counter

from manual_graph import create_manual_graph
from algorithms import bfs, dfs, dijkstra, astar


graph = create_manual_graph()

start = 0   # A
goal = 11   # L

algorithms = {
    "BFS": bfs,
    "DFS": dfs,
    "Dijkstra": dijkstra,
    "A*": astar
}


for name, algorithm in algorithms.items():

    start_time = perf_counter()

    result = algorithm(graph, start, goal)

    execution_time = perf_counter() - start_time

    if name in ("Dijkstra", "A*"):
        path, distance = result
    else:
        path = result

        distance = sum(
            graph.es[graph.get_eid(u, v)]["length"]
            for u, v in zip(path, path[1:])
        ) if path else 0

    if path:
        node_names = [graph.vs[node]["name"] for node in path]

        print(f"\nAlgorithm: {name}")
        print("Path:", " -> ".join(node_names))
        print(f"Distance: {distance / 1000:.3f} km")
        print(f"Execution Time: {execution_time:.8f} seconds")

    else:
        print(f"\n{name}: No path found")
