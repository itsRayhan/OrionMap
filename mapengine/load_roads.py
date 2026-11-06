from pathlib import Path
from pyrosm import OSM


DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "bangladesh-261104.osm.pbf"
)
GRAPH_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "bangladesh-road-network.pkl"
)

def load_road_graph():

    if not DATA_PATH.exists():
        print("OSM dataset not found!")
        return

    print("Loading Bangladesh road network...")

    osm = OSM(str(DATA_PATH))

    print("Building Graph...")

    G = osm.get_graph(
        network_type="driving",
        graph_type="igraph",
        retain_all=True,
        simplify=True
    )

    if G is None:
        print("Graph could not be created!")
        return
    print("Saving Bangladesh Road Graph...")

    G.write_pickle(str(GRAPH_PATH))

    print("Graph saved successfully!")
    print("Saved at:", GRAPH_PATH)

    
    print("\nBangladesh Road Graph created!")

    print("Total Nodes:", G.vcount())
    print("Total Edges:", G.ecount())
    print("Directed Graph:", G.is_directed())

    print("\nNode attributes:")
    print(G.vs.attributes())

    print("\nEdge attributes:")
    print(G.es.attributes())


if __name__ == "__main__":
    load_road_graph()