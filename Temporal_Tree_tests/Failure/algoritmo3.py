import networkx as nx

def is_temporalmente_connesso(G):
    G_time_expanded = nx.DiGraph()

    for u, v, data in G.edges(data=True):
        min_label, max_label = data['label']
        G_time_expanded.add_edge(u, v, weight=min_label)
        G_time_expanded.add_edge(v, u, weight=max_label)

    try:
        nx.topological_sort(G_time_expanded)
        return True
    except nx.NetworkXUnfeasible:
        return False

# Esempio di utilizzo con etichette singole
G = nx.Graph()
G.add_edge('A', 'B', label=[1,2])
G.add_edge('A', 'C', label=[1,3])
G.add_edge('B', 'D', label=[2,2])
G.add_edge('C', 'E', label=[2,2])

print(is_temporalmente_connesso(G))  # Output: True (se l'albero è effettivamente connesso)