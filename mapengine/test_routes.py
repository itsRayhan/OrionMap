from graph_loader import load_graph

G = load_graph()

print("\nChecking Strongly Connected Components...")

components = G.connected_components(mode="strong")

largest_component = max(components, key=len)

print("Total Components:", len(components))
print("Largest Component Nodes:", len(largest_component))
print("Node 0 in Largest Component:", 0 in largest_component)

from algorithms import haversine

start = 0
start_component = largest_component

goal = None
max_distance = 0

for node_id in start_component:
    distance = haversine(G, start, node_id)

    if 3000 <= distance <= 5000 and distance > max_distance:
        max_distance = distance
        goal = node_id

print("\nRoute Test Nodes:")
print("Start Node:", start)
print("Goal Node:", goal)
print("Straight Line Distance:", round(max_distance / 1000, 2), "KM")


import time
from algorithms import bfs, dfs, dijkstra, astar

algorithms = [
    ("BFS", bfs),
    ("DFS", dfs),
    ("Dijkstra", dijkstra),
    ("A*", astar)
]

print("\nRunning Route Performance Tests...")

for name, algorithm in algorithms:
    print(f"\nTesting {name}...")

    start_time = time.perf_counter()

    result = algorithm(G, start, goal)

    end_time = time.perf_counter()

    if name in ("Dijkstra", "A*"):
        path, distance = result
    else:
        path = result

    elapsed = end_time - start_time

    if path:
        print("Path Found: Yes")
        print("Number of Nodes:", len(path))
        print("Execution Time:", round(elapsed, 4), "seconds")

        if name in ("Dijkstra", "A*"):
            print("Distance:", round(distance / 1000, 3), "KM")
    else:
        print("Path Found: No")