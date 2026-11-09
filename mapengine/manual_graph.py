
import igraph as ig
import math


def calculate_distance(lat1, lon1, lat2, lon2):

    radius = 6371000

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    return 2 * radius * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )


def create_manual_graph():

    graph = ig.Graph(directed=True)

    # 12 manually defined nodes
    nodes = [
        ("A", 23.7808, 90.2792),
        ("B", 23.7815, 90.2850),
        ("C", 23.7820, 90.2910),
        ("D", 23.7750, 90.2800),
        ("E", 23.7755, 90.2860),
        ("F", 23.7760, 90.2920),
        ("G", 23.7690, 90.2810),
        ("H", 23.7695, 90.2870),
        ("I", 23.7700, 90.2930),
        ("J", 23.7630, 90.2820),
        ("K", 23.7635, 90.2880),
        ("L", 23.7640, 90.2940),
    ]

    graph.add_vertices(len(nodes))

    graph.vs["name"] = [node[0] for node in nodes]
    graph.vs["lat"] = [node[1] for node in nodes]
    graph.vs["lon"] = [node[2] for node in nodes]

    # Manually defined road connections
    roads = [
        (0, 1), (1, 2),
        (0, 3), (1, 4), (2, 5),
        (3, 4), (4, 5),
        (3, 6), (4, 7), (5, 8),
        (6, 7), (7, 8),
        (6, 9), (7, 10), (8, 11),
        (9, 10), (10, 11),
        (1, 3), (4, 6), (5, 7)
    ]

    # Add roads in both directions
    directed_roads = roads + [
        (target, source)
        for source, target in roads
    ]

    graph.add_edges(directed_roads)

    # Calculate distance for every road
    lengths = []

    for edge in graph.es:

        source = graph.vs[edge.source]
        target = graph.vs[edge.target]

        distance = calculate_distance(
            source["lat"],
            source["lon"],
            target["lat"],
            target["lon"]
        )

        lengths.append(distance)

    graph.es["length"] = lengths

    return graph
