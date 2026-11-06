from graph_loader import load_graph
from algorithms import bfs, dfs, dijkstra, astar, haversine


G = load_graph()

start = 0

first_neighbors = set(G.neighbors(start, mode="out"))

goal = None

for middle in first_neighbors:

    for candidate in G.neighbors(middle, mode="out"):

        if candidate != start and candidate not in first_neighbors:
            goal = candidate
            break

    if goal is not None:
        break


if goal is None:
    print("Could not find a suitable test destination!")

else:
    print("\nTesting BFS...")

    print("Start Node:", start)
    print("Goal Node:", goal)

    path = bfs(G, start, goal)

    if path:
        print("BFS Path:", path)
        print("Number of nodes:", len(path))
        print("Number of edges:", len(path) - 1)

    else:
        print("No path found!")
        
print("\nTesting DFS...")

dfs_path = dfs(G, start, goal)

if dfs_path:
    print("DFS Path:", dfs_path)
    print("Number of nodes:", len(dfs_path))
    print("Number of edges:", len(dfs_path) - 1)
else:
    print("No path found!")
    
print("\nTesting Dijkstra...")

dijkstra_path, distance = dijkstra(G, start, goal)

if dijkstra_path:
    print("Dijkstra Path:", dijkstra_path)
    print("Number of nodes:", len(dijkstra_path))
    print("Total Distance:", round(distance, 2), "meters")
    print("Distance in KM:", round(distance / 1000, 3), "km")

else:
    print("No path found!")
    
    
    
    
print("\nTesting A*...")

astar_path, astar_distance = astar(G, start, goal)

if astar_path:
    print("A* Path:", astar_path)
    print("Number of nodes:", len(astar_path))
    print("Total Distance:", round(astar_distance, 2), "meters")
    print("Distance in KM:", round(astar_distance / 1000, 3), "km")
else:
    print("No path found!")
    
print("\nChecking Real Node Coordinates...")

for node_id in [0, 1, 2]:
    print(
        f"Node {node_id}:",
        "Latitude:", G.vs[node_id]["lat"],
        "Longitude:", G.vs[node_id]["lon"]
    )
    
print("\nFinding Distant Nodes...")

start = 0
start_lat = G.vs[start]["lat"]
start_lon = G.vs[start]["lon"]

farthest_node = None
max_distance = 0

for node in G.vs:
    lat = node["lat"]
    lon = node["lon"]

    distance = haversine(G, start, node.index)

    if distance > max_distance:
        max_distance = distance
        farthest_node = node.index

print("Start Node:", start)
print("Destination Node:", farthest_node)
print("Straight Line Distance:", round(max_distance / 1000, 2), "KM")