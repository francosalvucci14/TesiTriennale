from math import inf
from collections import defaultdict
from bisect import bisect_left
from timeit import default_timer as timer
from datetime import timedelta

# Esempio di albero fornito
tree = {
    0: [(1, [2, 6]), (2, [6])],
    1: [(0, [2, 6]), (3, [1, 2, 3, 4, 5])],
    2: [(0, [6]), (4, [6])],
    3: [(1, [1, 2, 3, 4, 5])],
    4: [(2, [6])]
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

tree4 = {
    0:[(1,[2]),(2,[5,7])],
    1:[(0,[2]),(3,[5])],
    2:[(0,[5,7]),(4,[8,9]),(5,[8,8])],
    3:[(1,[5])],
    4:[(2,[8,9])],
    5:[(2,[8,8])]
}

tree5 = {
    0 : [(1,[1,2]),(2,[1,2])],
    1 : [(0,[1,2]),(3,[2]),(4,[3])],
    2 : [(0,[1,2]),(5,[2])],
    3 : [(1,[2])],
    4 : [(1,[3])],
    5 : [(2,[2])]
}

def preprocess(tree):
    """Step 1: Trova la foglia più profonda per ogni sottoalbero della radice."""
    def dfs(node, parent, depth):
        """DFS per calcolare la profondità massima e le foglie con timestamp minimo."""
        nonlocal max_depth, candidate_leaf
        if len(tree[node]) == 1 and tree[node][0][0] == parent:  # Nodo foglia
            if depth > max_depth:
                max_depth = depth
                candidate_leaf = (node, min(tree[node][0][1]))
            elif depth == max_depth:
                candidate_leaf = min(candidate_leaf, (node, min(tree[node][0][1])), key=lambda x: x[1])
            return

        for neighbor, timestamps in tree[node]:
            if neighbor != parent:
                dfs(neighbor, node, depth + 1)
        

    root = 0
    leaves = {}
    for child, timestamps in tree[root]:  # Ogni sottoalbero
        max_depth = -1
        candidate_leaf = None
        dfs(child, root, 1)
        leaves[child] = candidate_leaf  # Salva la foglia con timestamp minimo

    return leaves

### QUESTA FUNZIONE VA BENE PER ALBERI BINARI
def calculate_max_value(tree, leaf, root):
    """Step 2: Calcola il valore massimo del timestamp nel percorso bottom-up."""
    max_timestamp = inf
    node = leaf

    while node != root:
        for parent, timestamps in tree[node]:
            if parent != node:
                current_max = max(timestamps)
                max_timestamp = min(max_timestamp, current_max)
                node = parent
                break
    return max_timestamp

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

def compare_earliest_arrival_and_max_values(tree):
    """Step 3: Confronta i valori calcolati per decidere se restituire True o False."""
    leaves = preprocess(tree)
    root = 0
    print("Foglie:", leaves) #leaves[0] = nodo, leaves[1] = timestamp minimo

    ea_from_sx = EA_query_function(tree,leaves[1][0],root,0) #calculate_max_value(tree, leaves[1][0], root)  # EA da sinistra
    ea_from_dx = EA_query_function(tree,leaves[2][0],root,0) #calculate_max_value(tree, leaves[2][0], root)  # EA da destra

    print("EA da sinistra:", ea_from_sx, "EA da destra:", ea_from_dx)

    if ea_from_dx == float("inf") or ea_from_dx == float("-inf"):
        return False

    max_value_sx = calculate_max_value(tree, leaves[1][0], root)  # Max da sinistra
    max_value_dx = calculate_max_value(tree, leaves[2][0], root)  # Max da destra

    print("Max da sinistra:", max_value_sx, "Max da destra:", max_value_dx)

    return (ea_from_sx <= max_value_dx) and (ea_from_dx <= max_value_sx)

# Esegui l'algoritmo sull'albero di esempio
start = timer()
result = compare_earliest_arrival_and_max_values(tree5)
end = timer()
print(f"Tempo di esecuzione: {timedelta(seconds=end-start)}")
print(f"L'albero è temporalmente connesso: {result}")

