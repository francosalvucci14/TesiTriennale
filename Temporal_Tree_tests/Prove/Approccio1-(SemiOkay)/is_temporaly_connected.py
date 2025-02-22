from bisect import bisect_left
from timeit import default_timer as timer
from datetime import timedelta

def find_leftmost_leaf(tree, current, parent=None, depth=0):
    """Trova la foglia più profonda tutta a sinistra."""
    if current not in tree or not tree[current]:  # Caso base: nodo senza vicini
        return current, depth

    for neighbor, _ in tree[current]:  # Esplora i vicini
        if neighbor != parent:  # Evita di tornare al genitore
            return find_leftmost_leaf(tree, neighbor, current, depth + 1)
    
    return current, depth

def find_rightmost_leaf(tree, current, parent=None, depth=0):
    """Trova la foglia più profonda tutta a destra."""
    if current not in tree or not tree[current]:  # Caso base: nodo senza vicini
        return current, depth

    for neighbor, _ in reversed(tree[current]):  # Esplora i vicini in ordine inverso
        if neighbor != parent:  # Evita di tornare al genitore
            return find_rightmost_leaf(tree, neighbor, current, depth + 1)
    
    return current, depth


# da qua in giù tutto apposto
def EA_query_function(tree, u, v, t_start):
    """Calcola l'Earliest Arrival (EA) da u a v."""
    current_node = u
    current_time = t_start

    while current_node != v:
        neighbors = tree.get(current_node, [])
        parent = neighbors[0][0]
        times = []

        for neighbor, timestamps in neighbors:
            if neighbor == v or neighbor == parent:
                parent = neighbor
                times = timestamps
                break

        if parent is None or not times:
            return float("inf")
        
        idx = bisect_left(times, current_time)
        if idx == len(times):
            return float("inf")
        
        current_time = times[idx]
        current_node = parent

    return current_time

def temporal_dfs(tree, current, visited, time, is_valid_edge):
    """Esegue una DFS temporale rispettando i vincoli temporali."""
    visited.add(current)
    for neighbor, times in tree.get(current, []):
        if neighbor not in visited:
            idx = bisect_left(times, time)
            if idx < len(times) and is_valid_edge(times[idx], time):
                if not temporal_dfs(tree, neighbor, visited, times[idx], is_valid_edge):
                    return False
            else:
                return False  # Nessun timestamp valido
    return True

def temporal_dfs_from_root(tree, root, time, is_valid_edge, direction="left"):
    """
    Esegue una DFS temporale a partire dalla root in una direzione specifica.
    
    Args:
        tree: struttura dati che rappresenta l'albero.
        root: nodo radice.
        time: tempo iniziale per la DFS.
        is_valid_edge: funzione che verifica la validità di un arco rispetto al tempo.
        direction: "left" per il sottoalbero sinistro, "right" per il sottoalbero destro.
    
    Returns:
        True se la DFS visita tutti i nodi del sottoalbero specificato, False altrimenti.
    """
    # Determina il sottoalbero da esplorare
    if direction == "left":
        subtree_root = tree[root][0][0]  # Primo figlio (sottoalbero sinistro)
    elif direction == "right":
        subtree_root = tree[root][1][0]  # Secondo figlio (sottoalbero destro)
    else:
        raise ValueError("La direzione deve essere 'left' o 'right'")
    
    # Inizializza i nodi visitati e avvia la DFS
    visited = set()
    return temporal_dfs(tree, subtree_root, visited, time, is_valid_edge)


def is_temporally_connected(tree, root):
    """
    Verifica se un albero è temporalmente connesso.

    Args:
        tree: dizionario che rappresenta l'albero.
        root: nodo radice dell'albero.

    Returns:
        True se l'albero è temporalmente connesso, False altrimenti.
    """
    # Step 1: Trova le foglie estreme
    left_leaf,_= find_leftmost_leaf(tree, root)
    right_leaf,_= find_rightmost_leaf(tree, root)
    print(f"Left leaf: {left_leaf}, Right leaf: {right_leaf}")

    # Step 2: Calcola gli Earliest Arrivals
    EA_sx = EA_query_function(tree, left_leaf, root, -float("inf"))
    EA_dx = EA_query_function(tree, right_leaf, root, -float("inf"))
    print(f"EA_sx: {EA_sx}, EA_dx: {EA_dx}")

    if EA_sx == float("inf") or EA_dx == float("inf"):
        return False  # Interrompi se non c'è connessione temporale

    # Step 3: Esegui DFS temporali
    # left_subtree_root = tree[root][0][0]  # Primo figlio (sottoalbero sinistro)
    # right_subtree_root = tree[root][1][0]  # Secondo figlio (sottoalbero destro)

    # visited_left = set()
    # is_valid_left = temporal_dfs(
    #     tree, left_subtree_root, visited_left, EA_sx,
    #     lambda t, current_time: t >= current_time
    # )
    
    # visited_right = set()
    # is_valid_right = temporal_dfs(
    #     tree, right_subtree_root, visited_right, EA_dx,
    #     lambda t, current_time: t >= current_time
    # )
    # Step 3: Esegui DFS temporali con i tempi corretti
    is_valid_left = temporal_dfs_from_root(
        tree, root, EA_dx, lambda t, current_time: t >= current_time, direction="left"
    )
    is_valid_right = temporal_dfs_from_root(
        tree, root, EA_sx, lambda t, current_time: t >= current_time, direction="right"
    )

    print(f"Visited left: {is_valid_left}, Visited right: {is_valid_right}")
    
    return is_valid_left and is_valid_right

tree = {
    0: [(1, [4,5]), (2, [1,2,3])],
    1: [(0, [4,5]), (3, [5,6]),(4,[4])],
    2: [(0, [1,2,3]), (5, [2,6])],
    3: [(1, [5,6])],
    4: [(1, [4]),(6,[8]),(7,[9])],
    5: [(2, [2,6])],
    6: [(4, [8])],
    7: [(4, [9])]
}

tree3 = {
    0:[(1,[2,6]),(2,[6])],
    1:[(0,[2,6]),(3,[1,2,3,4,5,6])],
    2:[(0,[6]),(4,[6])],
    3:[(1,[1,2,3,4,5,6])],
    4:[(2,[6])]
}

tree4 = {
    0:[(1,[2]),(2,[5,7])],
    1:[(0,[2]),(3,[5])],
    2:[(0,[5,7]),(4,[8,9]),(5,[8,8])],
    3:[(1,[5])],
    4:[(2,[8,9])],
    5:[(2,[8,8])]
}

tree5 = {
    0 : [(1,[1,2,7]),(2,[1,2])],
    1 : [(0,[1,2,7]),(3,[2]),(4,[6])],
    2 : [(0,[1,2]),(5,[2])],
    3 : [(1,[2])],
    4 : [(1,[6])],
    5 : [(2,[2])]
}

tree_Catena = { 
    0 : [(1,[1,2])],
    1 : [(0,[1,2]),(2,[1,3])],
    2 : [(1,[1,2]),(3,[1,2])],
    3 : [(2,[1,3]),(4,[2])],
    4 : [(3,[2])]
}

tree12 = {
    0: [(1, [3, 12]), (2, [5, 14])],                # Radice con due figli
    1: [(0, [4, 13]), (3, [6, 10]), (4, [7, 12]), (5, [9, 15])],  # Nodo 1 con padre 0 e figli 3, 4, 5
    2: [(0, [2, 11]), (6, [1, 8]), (7, [4, 13])],   # Nodo 2 con padre 0 e figli 6, 7
    3: [(1, [5, 12])],                              # Foglia, padre 1
    4: [(1, [3, 9]), (8, [7, 14])],                 # Nodo 4 con padre 1 e figlio 8
    5: [(1, [6, 11]), (9, [2, 14]), (10, [8, 15])], # Nodo 5 con padre 1 e figli 9, 10
    6: [(2, [4, 10])],                              # Foglia, padre 2
    7: [(2, [3, 9]), (11, [6, 14])],                # Nodo 7 con padre 2 e figlio 11
    8: [(4, [5, 12])],                              # Foglia, padre 4
    9: [(5, [4, 13])],                              # Foglia, padre 5
    10: [(5, [6, 11]), (12, [7, 14])],              # Nodo 10 con padre 5 e figlio 12
    11: [(7, [5, 10])],                             # Foglia, padre 7
    12: [(10, [3, 12])]                             # Foglia, padre 10
}
tree_v2 = {
    0: [(1, [2, 6]), (2, [6])],
    1: [(0, [2, 6]), (3, [1, 2, 3, 4, 5])],
    2: [(0, [6]), (4, [6])],
    3: [(1, [1, 2, 3, 4, 5]),(5,[3]),(6,[4]),(7,[1,2,7])],
    4: [(2, [6])],
    5: [(3,[3])],
    6: [(3,[4])],
    7: [(3,[1,2,7])]
}

# Ancora non va per gli alberi a catena
root = 0
start = timer()
result = is_temporally_connected(tree5, root)
end = timer()
print(f"Tempo di esecuzione: {timedelta(seconds=end-start)}")
print(f"L'albero è temporalmente connesso: {result}")