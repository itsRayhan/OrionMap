
from graph_loader import load_graph
from nearest_node import NearestNodeFinder

# Load Bangladesh Road Graph
G = load_graph()

# Build Spatial Index
finder = NearestNodeFinder(G)

# Use actual coordinates of Node 0 for testing
latitude = G.vs[0]["lat"]
longitude = G.vs[0]["lon"]

print("\nTesting Nearest Road Node...")

node_id, distance = finder.find_nearest(
    latitude,
    longitude
)

print("Input Latitude:", latitude)
print("Input Longitude:", longitude)

print("Nearest Node ID:", node_id)
print("Nearest Node Latitude:", G.vs[node_id]["lat"])
print("Nearest Node Longitude:", G.vs[node_id]["lon"])

print("Distance:", round(distance, 3), "meters")

if node_id == 0:
    print("\nNearest Node Test Passed!")
else:
    print("\nNearest Node Test Failed!")
