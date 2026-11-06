import math
from heapq import heappush, heappop

from collections import deque


def bfs(graph, start, goal):

    queue = deque([start])

    visited = {start}

    parent = {start: None}

    while queue:

        current = queue.popleft()

        if current == goal:

            path = []

            while current is not None:
                path.append(current)
                current = parent[current]

            return path[::-1]

        for neighbor in graph.neighbors(current, mode="out"):

            if neighbor not in visited:

                visited.add(neighbor)

                parent[neighbor] = current

                queue.append(neighbor)

    return None
def dfs(graph, start, goal):

    stack = [start]

    visited = {start}

    parent = {start: None}

    while stack:

        current = stack.pop()

        if current == goal:

            path = []

            while current is not None:
                path.append(current)
                current = parent[current]

            return path[::-1]

        neighbors = graph.neighbors(current, mode="out")

        for neighbor in reversed(neighbors):

            if neighbor not in visited:

                visited.add(neighbor)

                parent[neighbor] = current

                stack.append(neighbor)

    return None
import heapq


def dijkstra(graph, start, goal):

    priority_queue = [(0, start)]

    distances = {start: 0}

    parent = {start: None}

    visited = set()

    while priority_queue:

        current_distance, current = heapq.heappop(priority_queue)

        if current in visited:
            continue

        visited.add(current)

        if current == goal:

            path = []

            while current is not None:
                path.append(current)
                current = parent[current]

            return path[::-1], current_distance

        for edge_id in graph.incident(current, mode="out"):

            edge = graph.es[edge_id]

            neighbor = edge.target

            if neighbor in visited:
                continue

            weight = edge["length"]

            new_distance = current_distance + weight

            if new_distance < distances.get(neighbor, float("inf")):

                distances[neighbor] = new_distance

                parent[neighbor] = current

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor)
                )

    return None, float("inf")


def haversine(graph, node1, node2):
    lat1 = math.radians(graph.vs[node1]["lat"])
    lon1 = math.radians(graph.vs[node1]["lon"])

    lat2 = math.radians(graph.vs[node2]["lat"])
    lon2 = math.radians(graph.vs[node2]["lon"])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    return 6371000 * 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )


def astar(graph, start, goal):
    priority_queue = [(0, start)]

    g_score = {start: 0}
    parent = {start: None}
    visited = set()

    while priority_queue:
        _, current = heappop(priority_queue)

        if current in visited:
            continue

        visited.add(current)

        if current == goal:
            path = []

            while current is not None:
                path.append(current)
                current = parent[current]

            return path[::-1], g_score[goal]

        for edge_id in graph.incident(current, mode="out"):
            edge = graph.es[edge_id]
            neighbor = edge.target

            if neighbor in visited:
                continue

            new_distance = g_score[current] + edge["length"]

            if new_distance < g_score.get(neighbor, float("inf")):
                g_score[neighbor] = new_distance
                parent[neighbor] = current

                heuristic = haversine(graph, neighbor, goal)

                f_score = new_distance + heuristic

                heappush(
                    priority_queue,
                    (f_score, neighbor)
                )

    return None, float("inf")