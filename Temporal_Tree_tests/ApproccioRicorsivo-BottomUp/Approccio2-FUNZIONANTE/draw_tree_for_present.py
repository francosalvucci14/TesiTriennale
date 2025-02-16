import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def draw_tree_with_timestamps():
    G = nx.Graph()
    pos = {}
    
    # Definizione della struttura dell'albero
    nodes = ["A", "B", "C", "D", "E", "F"]
    edges = [("A", "B"), ("A", "C"), ("A", "D"), ("B", "E"), ("B", "F")]
    timestamps = {
        ("A", "B"): [1, 3, 5],
        ("A", "C"): [2, 4],
        ("A", "D"): [1, 2, 6],
        ("B", "E"): [3, 5],
        ("B", "F"): [2, 4, 6, 8]
    }
    
    # Posizionamento dei nodi
    pos["A"] = (0, 1)
    pos["B"] = (-0.5, 0.5)
    pos["C"] = (0, 0.5)
    pos["D"] = (0.5, 0.5)
    pos["E"] = (-0.6, 0)
    pos["F"] = (-0.4, 0)
    
    plt.figure(figsize=(4, 4))
    G.add_edges_from(edges)
    
    # Disegno dell'albero
    nx.draw(G, pos, with_labels=True, node_size=800, node_color="lightblue", edge_color="black", font_size=12)
    
    # Etichette degli archi con i timestamp
    edge_labels = {edge: str(timestamps[edge]) for edge in edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_color="black")
    
    # Disegno dei triangoli per i sottoalberi
    for node in ["B", "C", "D"]:
        x, y = pos[node]
        width = 0.3  # Dimensione fissa dei triangoli
        height = 0.4
        #triangle = plt.Polygon([(x - width / 2, y - height), (x + width / 2, y - height), (x, y)], color='gray', alpha=0.5)
        #plt.gca().add_patch(triangle)
    
    plt.xlim(-1, 1)
    plt.ylim(-0.2, 1.2)
    plt.axis('off')
    #plt.show()
    plt.savefig("tree_for_present.png", format="PNG")
    
# Esegui la funzione per disegnare l'albero
draw_tree_with_timestamps()