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


def generate_random_temporal_tree(N=10, max_timestamps=1, timestamp_range=(1, 1)):
    """
    Genera un albero temporale casuale con N nodi e al più K timestamp per ogni nodo.

    Args:
        N (int): Numero di nodi dell'albero (N >= 1).
        max_timestamps (int): Numero massimo di timestamp per nodo (1 <= max_timestamps <= 15).
        timestamp_range (tuple): Intervallo dei valori possibili per i timestamp (min, max).

    Returns:
        nx.DiGraph: Albero temporale con timestamp sui nodi.
    """
    if N < 1:
        raise ValueError("Il numero di nodi deve essere almeno 1.")
    #if not (1 <= max_timestamps <= 5000):
        #raise ValueError("Il numero massimo di timestamp deve essere tra 1 e 5000.")

    # Crea un grafo diretto
    tree = nx.DiGraph()

    # Genera i nomi dei nodi (A, B, C, ...)
    #nodes = [chr(65 + i) for i in range(N)]  # A, B, C, ... fino a N nodi
    #nodes = ["A"] + [f"N{i+1}" for i in range(1, N)]
    nodes = list(range(1, N + 1))

    # Aggiungi i nodi all'albero
    for node in nodes:
        if node == nodes[0]:
            tree.add_node(node, weight=None)  # La radice non ha timestamp
        else:
            num_timestamps = random.randint(1, max_timestamps)
            timestamps = sorted(random.sample(range(timestamp_range[0], timestamp_range[1] + 1), num_timestamps))
            tree.add_node(node, weight=timestamps)

    # Collega i nodi al parent generando un albero
    for node in nodes[1:]:
        # Scegli un parent casuale tra i nodi già aggiunti (garantisce un albero valido)
        parent = random.choice(nodes[:nodes.index(node)])

        # Aggiungi l'arco (i timestamp sono già sui nodi)
        tree.add_edge(parent, node)

    return tree

def genera_albero_temporale(N, M,timestamp_range):
    """
    Genera un albero temporale casuale con N nodi e un totale di M timestamp distribuiti sui nodi.

    Args:
        N (int): Numero di nodi dell'albero (N >= 1).
        timestamp_range (tuple): Intervallo dei valori possibili per i timestamp (min, max).
        M (int): Numero totale di timestamp da distribuire sui nodi.

    Returns:
        nx.DiGraph: Albero temporale con timestamp sui nodi.
    """
    if N < 1:
        raise ValueError("Il numero di nodi deve essere almeno 1.")
    if M < N - 1:
        raise ValueError("Il numero totale di timestamp deve essere almeno pari al numero di archi (N-1).")

    # Crea un grafo diretto
    tree = nx.DiGraph()

    # Genera i nomi dei nodi (A, N1, N2, ...)
    nodes = ["A"] + [f"N{i}" for i in range(1, N)]

    # Aggiungi i nodi all'albero
    for node in nodes:
        if node == "A":
            tree.add_node(node, weight=None)  # La radice "A" non ha timestamp (weight)
        else:
            tree.add_node(node)

    # Collega i nodi al parent generando un albero
    edges = []
    for node in nodes[1:]:
        # Scegli un parent casuale tra i nodi già aggiunti (garantisce un albero valido)
        parent = random.choice(nodes[:nodes.index(node)])
        edges.append((parent, node))
        tree.add_edge(parent, node)

    # Distribuisci i timestamp sui nodi (esclusa la radice)
    remaining_timestamps = M
    available_timestamps = list(range(timestamp_range[0], timestamp_range[1] + 1))

    if len(available_timestamps) < M:
        raise ValueError("Intervallo dei timestamp troppo piccolo per distribuirli tutti.")

    random.shuffle(available_timestamps)

    for node in nodes[1:]:
        if len(nodes) - 1 == 1:  # Ultimo nodo
            timestamps = available_timestamps[:remaining_timestamps]
        else:
            max_possible = remaining_timestamps // (len(nodes) - 1)
            num_timestamps = random.randint(1, max_possible)
            timestamps = available_timestamps[:num_timestamps]

        tree.nodes[node]['weight'] = sorted(timestamps)

        # Rimuovi i timestamp utilizzati
        available_timestamps = available_timestamps[num_timestamps:]
        remaining_timestamps -= num_timestamps

    return tree

def print_temporal_tree(tree):
    """
    Stampa l'albero temporale in una struttura leggibile.

    Args:
        tree (nx.DiGraph): Albero temporale generato.
    """
    def print_subtree(node, depth=0):
        indent = "    " * depth
        if depth == 0:
            print(f"- Radice {node}")
        else:
            parent = list(tree.predecessors(node))[0]  # Ottieni il genitore
            timestamps = tree.nodes[node]['weight']
            print(f"{indent}- Nodo Interno (figlio di {parent}) {node} . lista timestamp: {timestamps}")

        for child in tree.successors(node):
            print_subtree(child, depth + 1)

    root = [n for n, d in tree.in_degree() if d == 0][0]  # Trova la radice (nodo con in-degree 0)
    print_subtree(root)

def create_tree_with_networkx():
    # Crea un grafo diretto
    tree = nx.DiGraph()

    # # # Aggiungi i nodi e i pesi degli archi entranti
    
    tree.add_node("A", weight=None)  # Radice senza arco entrante
    tree.add_node("B", weight=[3,4,5])
    tree.add_node("C", weight=[2,4])
    tree.add_node("D", weight=[1, 2, 3, 4, 5, 6])
    tree.add_node("E", weight=[2,3,4,5,6])
    tree.add_node("F", weight=[2,3])
    tree.add_node("G", weight=[1,2,3,4,5,6])
    tree.add_node("H", weight=[2,6])
    tree.add_node("I", weight=[1,3])
    tree.add_node("J", weight=[1,3])

    # Aggiungi gli archi (parent -> child)
    tree.add_edges_from([
        ("A", "B"),
        ("A", "E"),
        ("A", "F"),
        ("B", "C"),
        ("B", "D"),
        ("C", "G"),
        ("C", "H"),
        ("D", "J"),
        ("F", "I")
    ])
    return tree