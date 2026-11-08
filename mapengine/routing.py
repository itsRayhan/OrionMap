
from functools import lru_cache
from time import perf_counter
import math

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


def _node_coordinate(graph, node):
    """Return a node coordinate in [longitude, latitude] format."""

    lon = float(graph.vs[node]["lon"])
    lat = float(graph.vs[node]["lat"])

    if not math.isfinite(lon) or not math.isfinite(lat):
        raise ValueError(f"Invalid coordinates for node: {node}")

    return [lon, lat]


def _find_route_edge(graph, current, neighbor):
    """
    Find the directed edge connecting two consecutive route nodes.

    If parallel edges exist, choose the edge with the shortest length.
    """

    edge_ids = graph.incident(current, mode="out")

    candidates = []

    for edge_id in edge_ids:
        edge = graph.es[edge_id]

        if edge.source != current or edge.target != neighbor:
            continue

        try:
            length = float(edge["length"])
        except (TypeError, ValueError):
            continue

        if math.isfinite(length) and length >= 0:
            candidates.append((length, edge_id))

    if not candidates:
        raise ValueError(
            f"Directed road edge not found: {current} -> {neighbor}"
        )

    return min(candidates, key=lambda item: item[0])[1]


def _get_edge_geometry(graph, edge_id, current, neighbor):
    """
    Get the actual OSM road geometry.

    Geometry coordinates are returned in the correct travel direction.
    Falls back to node coordinates if geometry is unavailable.
    """

    edge = graph.es[edge_id]
    geometry = edge["geometry"]

    fallback = [
        _node_coordinate(graph, current),
        _node_coordinate(graph, neighbor),
    ]

    if geometry is None or not hasattr(geometry, "coords"):
        return fallback

    try:
        coordinates = [
            [float(lon), float(lat)]
            for lon, lat in geometry.coords
        ]
    except (TypeError, ValueError, AttributeError):
        return fallback

    if len(coordinates) < 2:
        return fallback

    if not all(
        math.isfinite(value)
        for coordinate in coordinates
        for value in coordinate
    ):
        return fallback

    start = _node_coordinate(graph, current)
    end = _node_coordinate(graph, neighbor)

    def squared_distance(a, b):
        return (
            (a[0] - b[0]) ** 2
            + (a[1] - b[1]) ** 2
        )

    forward_error = (
        squared_distance(coordinates[0], start)
        + squared_distance(coordinates[-1], end)
    )

    reverse_error = (
        squared_distance(coordinates[-1], start)
        + squared_distance(coordinates[0], end)
    )

    if reverse_error < forward_error:
        coordinates.reverse()

    return coordinates


def _remove_duplicate_coordinates(coordinates):
    """Remove consecutive duplicate coordinates."""

    cleaned = []

    for coordinate in coordinates:
        if not cleaned:
            cleaned.append(coordinate)
            continue

        previous = cleaned[-1]

        if (
            abs(previous[0] - coordinate[0]) > 1e-12
            or abs(previous[1] - coordinate[1]) > 1e-12
        ):
            cleaned.append(coordinate)

    return cleaned


def build_route_geometry(graph, path):
    """
    Build the complete road-following route geometry.

    Uses actual OSM edge geometries instead of straight lines
    between graph nodes.
    """

    if not path:
        return [], []

    all_coordinates = []
    route_edge_ids = []

    if len(path) == 1:
        return [_node_coordinate(graph, path[0])], []

    for current, neighbor in zip(path, path[1:]):

        edge_id = _find_route_edge(
            graph,
            current,
            neighbor
        )

        route_edge_ids.append(edge_id)

        edge_coordinates = _get_edge_geometry(
            graph,
            edge_id,
            current,
            neighbor
        )

        if all_coordinates:
            edge_coordinates = edge_coordinates[1:]

        all_coordinates.extend(edge_coordinates)

    return (
        _remove_duplicate_coordinates(all_coordinates),
        route_edge_ids
    )


def calculate_path_distance(graph, path):
    """Calculate route distance using the selected directed edges."""

    total_distance = 0.0

    if not path:
        return total_distance

    for current, neighbor in zip(path, path[1:]):

        edge_id = _find_route_edge(
            graph,
            current,
            neighbor
        )

        total_distance += float(graph.es[edge_id]["length"])

    return total_distance


def route_between(
    start_lat,
    start_lon,
    goal_lat,
    goal_lon,
    algorithm="astar"
):
    """Calculate a road route between two geographic locations."""

    if not isinstance(algorithm, str):
        raise ValueError("Algorithm must be a string.")

    algorithm = algorithm.lower().strip()

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
        path, algorithm_distance = result
    else:
        path = result
        algorithm_distance = None

    if not path:
        return {
            "success": False,
            "message": "No road route found.",
            "algorithm": algorithm,
            "start_node": start_node,
            "goal_node": goal_node,
        }

    # Build actual road geometry and identify used edges.
    coordinates, route_edge_ids = build_route_geometry(
        graph,
        path
    )

    # Calculate distance from the selected route edges.
    distance = calculate_path_distance(graph, path)

    return {
        "success": True,
        "algorithm": algorithm,

        "start_node": start_node,
        "goal_node": goal_node,

        "path": path,
        "coordinates": coordinates,

        "distance_meters": round(distance, 2),
        "distance_km": round(distance / 1000, 3),

        "node_count": len(path),
        "edge_count": len(route_edge_ids),
        "geometry_point_count": len(coordinates),

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
