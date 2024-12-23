import random
import networkx as nx
def binary_search(arr, target):
    if len(arr) == 1:  # Caso in cui l'array ha un solo elemento
        return (
            arr[0] if arr[0] >= target else -1
        )  # Restituisce l'indice se il valore è >= target
    left, right = 0, len(arr) - 1
    result = -1  # Inizialmente, supponiamo che non ci sia un valore valido

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] >= target:
            result = mid  # Salviamo l'indice come potenziale risultato
            right = mid - 1  # Continuiamo a cercare nella metà sinistra
        else:
            left = mid + 1  # Cerchiamo nella metà destra
    if result == -1:
        return -1
    else:
        return arr[result]


def binary_search_leq(arr, target):
    if len(arr) == 1:  # Caso in cui l'array ha un solo elemento
        return (
            arr[0] if arr[0] <= target else -1
        )  # Restituisce l'elemento se è ≤ target

    left, right = 0, len(arr) - 1
    result = -1  # Inizialmente, supponiamo che non ci sia un valore valido

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] <= target:
            result = mid  # Salviamo l'indice come potenziale risultato
            left = mid + 1  # Continuiamo a cercare nella metà destra
        else:
            right = mid - 1  # Cerchiamo nella metà sinistra

    if result == -1:
        return -1  # Nessun valore trovato ≤ target
    else:
        return arr[result]
    
def print_tree_networkx(tree, root, level=0):
    """
    Stampa un albero creato con NetworkX in modo gerarchico.

    :param tree: Grafo (albero) creato con NetworkX.
    :param root: Nodo radice dell'albero.
    :param level: Livello di profondità attuale (per l'indentazione).
    """
    # Stampa il nodo corrente
    weight = tree.nodes[root].get("weight", None)
    indent = "  " * level
    print(f"{indent}Node {root}, Weight: {weight}")

    # Itera sui figli (successors) e stampa ricorsivamente
    for child in tree.successors(root):
        # Trova il peso associato all'arco entrante
        edge_weight = tree.edges[root, child].get("weight", None)
        print(f"{indent}  ↳ Edge to {child}, Weight: {edge_weight}")
        print_tree_networkx(tree, child, level + 1)


def create_random_tree(N, timestamp_range):
    """
    Crea un albero diretto casuale con N nodi e timestamp casuali ordinati.

    Parametri:
        N (int): Numero di nodi dell'albero.
        timestamp_range (tuple): Intervallo dei timestamp, ad esempio (1, 10).

    Ritorna:
        tree (nx.DiGraph): Un albero diretto casuale.
    """
    if N < 1:
        raise ValueError("Il numero di nodi deve essere almeno 1.")

    # Crea un grafo diretto
    tree = nx.DiGraph()

    # Aggiungi il nodo radice
    tree.add_node("A", weight=None)

    # Genera i restanti nodi
    nodes = [f"N{i}" for i in range(1, N)]

    # Assegna pesi (timestamp) ai nodi e costruisce l'albero
    for node in nodes:
        num_timestamps = random.randint(1, 8)  # Numero casuale di timestamp per nodo
        timestamps = sorted(random.sample(range(timestamp_range[0], timestamp_range[1] + 1), num_timestamps))
        tree.add_node(node, weight=timestamps)

    # Collegare i nodi per formare un albero
    all_nodes = ["A"] + nodes
    for node in nodes:
        parent = random.choice(all_nodes[:all_nodes.index(node)])  # Seleziona un genitore tra i nodi già aggiunti
        tree.add_edge(parent, node)

    return tree
