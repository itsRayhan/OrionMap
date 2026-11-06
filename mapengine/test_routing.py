from routing import route_between, get_engine

# Load engine and get actual graph coordinates
graph, finder = get_engine()

start_node = 0
goal_node = 72654

start_lat = graph.vs[start_node]["lat"]
start_lon = graph.vs[start_node]["lon"]

goal_lat = graph.vs[goal_node]["lat"]
goal_lon = graph.vs[goal_node]["lon"]


print("\nORIONMAP ROUTING TEST")
print("=====================")

print("Start Coordinates:", start_lat, start_lon)
print("Goal Coordinates:", goal_lat, goal_lon)


algorithms = ["bfs", "dfs", "dijkstra", "astar"]

for algorithm in algorithms:

    print(f"\nTesting {algorithm.upper()}...")

    result = route_between(
        start_lat,
        start_lon,
        goal_lat,
        goal_lon,
        algorithm
    )

    if result["success"]:

        print("Status: SUCCESS")
        print("Start Node:", result["start_node"])
        print("Goal Node:", result["goal_node"])
        print("Path Nodes:", len(result["path"]))
        print("Distance:", result["distance_km"], "KM")

        print(
            "Start Snap Distance:",
            result["start_snap_distance_meters"],
            "meters"
        )

        print(
            "Goal Snap Distance:",
            result["goal_snap_distance_meters"],
            "meters"
        )

        print(
            "Execution Time:",
            result["execution_time_seconds"],
            "seconds"
        )

    else:
        print("Status: FAILED")
        print("Message:", result["message"])
