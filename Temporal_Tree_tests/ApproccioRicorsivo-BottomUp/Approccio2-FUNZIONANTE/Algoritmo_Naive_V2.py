import networkx as nx

def exists_temporal_path_for_nodes(path, tree):
    """
    Data una lista di nodi (path) e il grafo (tree),
    verifica se esiste un cammino temporale valido, cioè se è possibile
    scegliere, per ogni nodo del percorso, un timestamp tale che la sequenza
    dei timestamp sia strettamente crescente.
    
    Se un nodo non ha timestamp (weight è None), lo consideriamo come [0].
    """
    last_time = -float('inf')
    for node in path:
        # Ottieni la lista dei timestamp associata al nodo;
        # se il nodo non ha timestamp, usiamo [0] come default.
        timestamps = tree.nodes[node].get("weight")
        if timestamps is None:
            timestamps = [0]
        # Cerca il più piccolo timestamp che sia maggiore di last_time
        found = False
        for t in timestamps:
            if t >= last_time:
                last_time = t
                found = True
                break
        if not found:
            return False
    return True

def naive_temporal_connectivity(tree):
    """
    Algoritmo naive per verificare la temporal connectivity.
    
    Per ogni coppia ordinata di nodi (u, v) nel grafo:
      - Se esiste un cammino da u a v (usando nx.has_path), si recupera il percorso
        (dato che in un albero esiste un solo semplice cammino).
      - Si verifica se lungo questo percorso esiste una sequenza di timestamp
        strettamente crescente.
        
    Restituisce True se per ogni coppia (u, v) esiste un cammino temporale valido,
    False altrimenti.
    """
    nodes = list(tree.nodes())
    for u in nodes:
        for v in nodes:
            if u == v:
                continue
            # Se non esiste un cammino diretto da u a v, la connettività temporale non è soddisfatta
            if not nx.has_path(tree, u, v):
                return False
            # Recupera il percorso (in un albero il percorso è unico)
            path = nx.shortest_path(tree, u, v)
            if not exists_temporal_path_for_nodes(path, tree):
                return False
    return True

def create_example_tree():
    tree = nx.Graph()
    tree.add_edge(1, 2, weight=[2, 6])
    tree.add_edge(1, 3, weight=[6])
    tree.add_edge(1, 6, weight=[1, 6])
    tree.add_edge(2, 4, weight=[1, 2, 3, 4, 5,6])
    tree.add_edge(3, 5, weight=[6])
    return tree

tree = create_example_tree()
print(naive_temporal_connectivity(tree))  # Output: True
