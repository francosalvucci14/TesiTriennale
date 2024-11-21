from collections import defaultdict, deque

def calculate_minimum_of_maximums_bottom_up(tree, root):
    """
    Calcola il minimo tra i massimi dei timestamp per ogni livello dell'albero,
    risalendo dalle foglie fino alla radice.
    
    Args:
        tree: dizionario che rappresenta l'albero con archi etichettati.
        root: nodo radice.
    
    Returns:
        Il valore minimo tra i massimi degli archi risalendo dalle foglie alla radice.
    """
    # Identifica le foglie: nodi che hanno come vicini solo il padre (nodi con indice minore)
    leaves = [
        node for node in tree
        if all(neighbor < node for neighbor, _ in tree[node])  # Nessun figlio
    ]

    # Struttura per memorizzare il minimo tra i massimi calcolati
    node_values = {}
    queue = deque(leaves)

    # Bottom-up BFS
    while queue:
        node = queue.popleft()

        if node not in tree or all(neighbor < node for neighbor, _ in tree[node]):  # Nodo foglia
            node_values[node] = float("inf")  # Le foglie non contribuiscono
        else:
            max_values = []
            for neighbor, timestamps in tree[node]:
                if neighbor > node:  # Solo i figli
                    max_values.append(max(timestamps))
            node_values[node] = min(max_values) if max_values else float("inf")

        # Se il nodo ha un genitore, aggiungilo alla coda
        for neighbor, _ in tree[node]:
            if neighbor < node:  # Identifica il genitore
                # Rimuovi il nodo corrente dai figli del genitore
                tree[neighbor] = [(n, t) for n, t in tree[neighbor] if n != node]
                if all(n < neighbor for n, _ in tree[neighbor]):  # Diventa una foglia
                    queue.append(neighbor)

    # Calcolo finale per la radice
    if root not in node_values:  # Verifica se la radice è stata elaborata
        max_values = []
        for neighbor, timestamps in tree[root]:
            if neighbor > root:
                max_values.append(max(timestamps))
        node_values[root] = min(max_values) if max_values else float("inf")

    return node_values[root]


tree12 = {
    0: [(1, [3, 12]), (2, [5, 14])],
    1: [(0, [4, 13]), (3, [6, 10]), (4, [7, 12]), (5, [9, 15])],
    2: [(0, [2, 11]), (6, [1, 8]), (7, [4, 13])],
    3: [(1, [5, 12])],
    4: [(1, [3, 9]), (8, [7, 14])],
    5: [(1, [6, 11]), (9, [2, 14]), (10, [8, 15])],
    6: [(2, [4, 10])],
    7: [(2, [3, 9]), (11, [6, 14])],
    8: [(4, [5, 12])],
    9: [(5, [4, 13])],
    10: [(5, [6, 11]), (12, [7, 14])],
    11: [(7, [5, 10])],
    12: [(10, [3, 12])]
}

tree4 = {
    0:[(1,[2]),(2,[5,7])],
    1:[(0,[2]),(3,[5])],
    2:[(0,[5,7]),(4,[8,9]),(5,[8,8])],
    3:[(1,[5])],
    4:[(2,[8,8])],
    5:[(2,[8,8])]
}

root = 0
result = calculate_minimum_of_maximums_bottom_up(tree4, root)
print(f"Il minimo tra i massimi risalendo dalle foglie alla radice è: {result}")
