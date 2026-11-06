from pathlib import Path
import igraph as ig


GRAPH_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "bangladesh-road-network.pkl"
)


def load_graph():

    if not GRAPH_PATH.exists():
        raise FileNotFoundError("Bangladesh Road Graph not found!")

    print("Loading saved Bangladesh Road Graph...")

    G = ig.Graph.Read_Pickle(str(GRAPH_PATH))

    print("Graph loaded successfully!")
    print("Total Nodes:", G.vcount())
    print("Total Edges:", G.ecount())
    print("Directed Graph:", G.is_directed())

    return G


if __name__ == "__main__":
    load_graph()