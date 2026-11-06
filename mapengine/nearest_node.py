
import numpy as np
from scipy.spatial import cKDTree


class NearestNodeFinder:

    EARTH_RADIUS = 6371000

    def __init__(self, graph):
        print("Building Road Node Spatial Index...")

        self.graph = graph

        latitudes = np.asarray(graph.vs["lat"], dtype=float)
        longitudes = np.asarray(graph.vs["lon"], dtype=float)

        valid = np.isfinite(latitudes) & np.isfinite(longitudes)

        self.node_ids = np.flatnonzero(valid)

        lat_rad = np.radians(latitudes[valid])
        lon_rad = np.radians(longitudes[valid])

        # Convert geographic coordinates into 3D sphere coordinates
        x = np.cos(lat_rad) * np.cos(lon_rad)
        y = np.cos(lat_rad) * np.sin(lon_rad)
        z = np.sin(lat_rad)

        coordinates = np.column_stack((x, y, z))

        self.tree = cKDTree(coordinates)

        print("Spatial Index Created Successfully!")
        print("Indexed Nodes:", len(self.node_ids))

    def find_nearest(self, latitude, longitude):

        if not -90 <= latitude <= 90:
            raise ValueError("Invalid latitude!")

        if not -180 <= longitude <= 180:
            raise ValueError("Invalid longitude!")

        lat_rad = np.radians(latitude)
        lon_rad = np.radians(longitude)

        x = np.cos(lat_rad) * np.cos(lon_rad)
        y = np.cos(lat_rad) * np.sin(lon_rad)
        z = np.sin(lat_rad)

        point = [x, y, z]

        chord_distance, index = self.tree.query(point)

        node_id = int(self.node_ids[index])

        # Convert chord distance to great-circle distance
        angle = 2 * np.arcsin(
            min(1.0, chord_distance / 2)
        )

        distance = self.EARTH_RADIUS * angle

        return node_id, float(distance)
