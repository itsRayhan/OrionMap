
from functools import lru_cache
from time import perf_counter
try:
    from .graph_loader import load_graph
    from .nearest_node import NearestNodeFinder
    from .algorithms import bfs, dfs, dijkstra, astar
except ImportError:
    from graph_loader import load_graph
    from nearest_node import NearestNodeFinder
    from algorithms import bfs, dfs, dijkstra, astar


ALGORITHMS = {
    "bfs": bfs,
    "dfs": dfs,
    "dijkstra": dijkstra,
    "astar": astar,
}


@lru_cache(maxsize=1)
def get_engine():
    print("Initializing OrionMap Routing Engine...")

    graph = load_graph()
    nearest_finder = NearestNodeFinder(graph)

    print("OrionMap Routing Engine Ready!")

    return graph, nearest_finder


def calculate_path_distance(graph, path):
    total_distance = 0

    for current, neighbor in zip(path, path[1:]):
        edge_ids = graph.incident(current, mode="out")

        matching_edges = [
            graph.es[edge_id]["length"]
            for edge_id in edge_ids
            if graph.es[edge_id].target == neighbor
        ]

        if not matching_edges:
            raise ValueError(
                f"Road edge not found: {current} -> {neighbor}"
            )

        total_distance += min(matching_edges)

    return total_distance


def route_between(
    start_lat,
    start_lon,
    goal_lat,
    goal_lon,
    algorithm="astar"
):
    algorithm = algorithm.lower()

    if algorithm not in ALGORITHMS:
        raise ValueError(
            "Supported algorithms: bfs, dfs, dijkstra, astar"
        )

    graph, nearest_finder = get_engine()

    start_node, start_snap_distance = (
        nearest_finder.find_nearest(start_lat, start_lon)
    )

    goal_node, goal_snap_distance = (
        nearest_finder.find_nearest(goal_lat, goal_lon)
    )

    start_time = perf_counter()

    result = ALGORITHMS[algorithm](
        graph,
        start_node,
        goal_node
    )

    execution_time = perf_counter() - start_time

    if algorithm in ("dijkstra", "astar"):
        path, distance = result
    else:
        path = result

        distance = (
            calculate_path_distance(graph, path)
            if path else float("inf")
        )

    if not path:
        return {
            "success": False,
            "message": "No road route found.",
            "algorithm": algorithm,
            "start_node": start_node,
            "goal_node": goal_node,
        }

    coordinates = [
        [
            graph.vs[node]["lon"],
            graph.vs[node]["lat"]
        ]
        for node in path
    ]

    return {
        "success": True,
        "algorithm": algorithm,
        "start_node": start_node,
        "goal_node": goal_node,
        "path": path,
        "coordinates": coordinates,
        "distance_meters": round(distance, 2),
        "distance_km": round(distance / 1000, 3),
        "start_snap_distance_meters": round(
            start_snap_distance, 2
        ),
        "goal_snap_distance_meters": round(
            goal_snap_distance, 2
            
            
        ),
        "execution_time_seconds": round(
            execution_time, 6
        ),
    }
