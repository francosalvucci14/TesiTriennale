from bisect import bisect_left

class Node:
    def __init__(self, value, weight=[]):
        self.value = value
        self.weight = weight
        self.left = None
        self.right = None

def build_temporal_tree(node, parent=None, tree=None):
    if tree is None:
        tree = {}

    if node is None:
        return tree

    if parent is not None:
        if node.value not in tree:
            tree[node.value] = []
        tree[node.value].append((parent.value, node.weight))

    build_temporal_tree(node.left, node, tree)
    build_temporal_tree(node.right, node, tree)

    return tree

def print_temporal_tree(tree):
    for node, edges in tree.items():
        print(f"{node}: {edges}")

def EA_min_query_function(tree, u, v, t_start):
    current_node = u
    current_time = t_start
    
    while current_node != v:
        neighbors = tree.get(current_node, [])
        parent = None
        times = []

        for neighbor, timestamps in neighbors:
            if neighbor == v or neighbor == neighbors[0][0]:
                parent = neighbor
                times = timestamps
                break

        if not parent or not times:
            return float("-inf")
        
        idx = bisect_left(times, current_time)
        if idx == len(times):
            return float("-inf")
        
        max_valid_time = min(times[idx:])
        current_time = max_valid_time
        current_node = parent

    return current_time

def find_node_with_max_weight(node, depth=0):
    """
    Trova la foglia più profonda con il timestamp minimo alla sua profondità.
    
    Args:
        node: Nodo corrente.
        depth: Profondità corrente del nodo.

    Returns:
        Una tupla (timestamp minimo, nodo corrispondente, profondità).
    """
    if node is None:
        return float("inf"), None, -1  # Nessun nodo

    # Se è una foglia, restituisci il timestamp minimo
    if node.left is None and node.right is None:
        min_timestamp = min(node.weight, default=float("inf"))
        return min_timestamp, node, depth

    # Ricorsione sui figli
    left_min, left_node, left_depth = find_node_with_max_weight(node.left, depth + 1)
    right_min, right_node, right_depth = find_node_with_max_weight(node.right, depth + 1)

    # Scegli la foglia più profonda; in caso di parità, quella con il timestamp minimo
    if left_depth > right_depth:
        return left_min, left_node, left_depth
    elif right_depth > left_depth:
        return right_min, right_node, right_depth
    else:  # Stessa profondità
        if left_min <= right_min:
            return left_min, left_node, left_depth
        else:
            return right_min, right_node, right_depth

def calculate_maximum_earliest_arrivals(tree, left_leaf, right_leaf, root, max_timestamps, EA_query_function):
    """
    Calcola il minimo Earliest Arrival (EA minimo) per i percorsi dalle foglie sinistra e destra alla radice.
    
    Args:
        tree: struttura dati che rappresenta l'albero temporale.
        left_leaf: nodo foglia più profondo tutto a sinistra.
        right_leaf: nodo foglia più profondo tutto a destra.
        root: nodo radice dell'albero.
        max_timestamps: tuple con i timestamp massimi per le foglie sinistra e destra.
        EA_query_function: funzione che implementa la query EA dalla struttura del paper.
    
    Returns:
        - Un dizionario contenente EA_sx e EA_dx se validi, oppure False se almeno uno è infinito.
    """
    # Timestamp massimo per le foglie
    max_t_sx, max_t_dx = max_timestamps

    # Calcola EA per il percorso dalla foglia sinistra alla radice
    EA_sx = EA_query_function(tree, left_leaf.value, root.value, max_t_sx)
    
    # Calcola EA per il percorso dalla foglia destra alla radice
    EA_dx = EA_query_function(tree, right_leaf.value, root.value, max_t_dx)
    
    # Controlla se uno dei risultati è infinito
    if EA_sx == float("-inf") or EA_dx == float("-inf"):
        return False  # Non c'è percorso temporalmente connesso
    
    # Salva le informazioni nella radice
    root_info = {
        "Min_EA_sx": EA_sx,
        "Min_EA_dx": EA_dx
    }
    return root_info

def verify_temporal_connectivity(node, current_time=float("-inf")):
    """
    Verifica se l'albero è temporalmente connesso usando una visita DFS.

    Args:
        node: Nodo corrente dell'albero.
        current_time: Timestamp corrente minimo per rispettare la connettività temporale.

    Returns:
        True se l'albero è temporalmente connesso, False altrimenti.
    """
    if node is None:
        return True  # Nodo vuoto è sempre connesso

    # Controlla se esiste un timestamp valido
    valid_timestamps = [t for t in node.weight if t >= current_time]
    if not valid_timestamps:
        return False  # Non esiste un percorso temporale valido

    # Procedi verso i figli con il timestamp minimo richiesto
    next_time = min(valid_timestamps)
    left_connected = verify_temporal_connectivity(node.left, next_time)
    right_connected = verify_temporal_connectivity(node.right, next_time)

    return left_connected and right_connected

def calculate_max_timestamp_bottom_up(node):
    """
    Calcola il timestamp massimo per visitare un intero sottoalbero usando un approccio bottom-up.

    Args:
        node: Nodo corrente.

    Returns:
        Il timestamp massimo utilizzabile per il sottoalbero.
    """
    if node is None:
        return float("inf")  # Nodo vuoto non impone restrizioni

    # Calcola ricorsivamente i timestamp massimi per i figli
    left_max = calculate_max_timestamp_bottom_up(node.left)
    right_max = calculate_max_timestamp_bottom_up(node.right)

    # Calcola il massimo utilizzabile per il nodo corrente
    node_max = max(node.weight, default=float("-inf"))

    return min(left_max, right_max, node_max)

def algoritmo(root):
    print("--------FASE 1--------")
    # Fase 1: Verifica della connettività temporale
    if not verify_temporal_connectivity(root.left):
        return "L'albero non è temporalmente connesso."
    
    print("\nCheck Fase 1 OK")

    # Fase 2: Trova le foglie più profonde con timestamp minimo nei sottoalberi
    min_left, left_node, _ = find_node_with_max_weight(root.left)
    min_right, right_node, _ = find_node_with_max_weight(root.right)

    print("\n--------FASE 2--------")
    print(f"\nFoglia più profonda sottoalbero sinistro: {left_node.value if left_node else None}, Timestamp: {min_left}")
    print(f"Foglia più profonda sottoalbero destro: {right_node.value if right_node else None}, Timestamp: {min_right}")

    print("\n--------FASE 3--------")
    # Fase 3: Calcolo dell'EA minimo partendo dalle foglie trovate in Fase 2
    tree = build_temporal_tree(root)
    print("\nStruttura dell'albero temporale:")
    print_temporal_tree(tree)

    EA_sx = EA_min_query_function(tree, left_node.value, root.value, min_left) if left_node else float("-inf")
    EA_dx = EA_min_query_function(tree, right_node.value, root.value, min_right) if right_node else float("-inf")

    print(f"EA minimo dal nodo sinistro: {EA_sx}")
    print(f"EA minimo dal nodo destro: {EA_dx}")

    print("\n--------FASE 4--------")
    # Fase 4: Calcolo dei timestamp massimi per entrambi i sottoalberi
    t_max_sx = calculate_max_timestamp_bottom_up(root.left)
    t_max_dx = calculate_max_timestamp_bottom_up(root.right)

    print(f"\nTimestamp massimo sottoalbero sinistro: {t_max_sx}")
    print(f"Timestamp massimo sottoalbero destro: {t_max_dx}")

    # Check finale
    if EA_sx <= t_max_dx and EA_dx <= t_max_sx:
        print("\nCheck Fase 4 OK")
        return "\nL'albero è temporalmente connesso."
    else:
        print("\nCheck Fase 4 NO")
        return "\nL'albero non è temporalmente connesso."

# root = Node('A')
# root.left = Node('B', weight=[1, 3, 5, 7])
# root.right = Node('C', weight=[2, 5, 6])
# root.left.left = Node('D', weight=[2, 3])
# root.right.right = Node('E', weight=[5, 6, 7])

# root = Node('A')
# root.left = Node('B', weight=[1, 3,4])
# root.right = Node('C', weight=[4])
# root.left.left = Node('D', weight=[2,4])
# root.right.right = Node('E', weight=[2,5,6])

root = Node('A')
root.left = Node('B', weight=[2,6])
root.right = Node('C', weight=[6])
root.left.left = Node('D', weight=[1,2,3,4,5])
root.right.right = Node('E', weight=[6])

print(algoritmo(root))