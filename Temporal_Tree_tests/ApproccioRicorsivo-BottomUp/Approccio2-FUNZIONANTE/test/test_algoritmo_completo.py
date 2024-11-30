from bisect import bisect_left
from timeit import default_timer as timer
from datetime import timedelta

# Esempio di albero
class Node:
    def __init__(self, value, weight=[]):
        self.value = value
        self.weight = weight
        self.left = None
        self.right = None

def build_temporal_tree(node, parent=None, tree=None):
    """
    Costruisce un albero temporale a partire da un albero binario.

    Args:
        node: Nodo corrente dell'albero binario.
        parent: Nodo genitore del nodo corrente.
        tree: Dizionario che rappresenta l'albero temporale.

    Returns:
        Il dizionario rappresentante l'albero temporale.
    """
    if tree is None:
        tree = {}

    if node is None:
        return tree

    # Aggiungi la connessione dal nodo corrente al genitore
    if parent is not None:
        if node.value not in tree:
            tree[node.value] = []
        tree[node.value].append((parent.value, node.weight))

    # Visita i figli
    build_temporal_tree(node.left, node, tree)
    build_temporal_tree(node.right, node, tree)

    return tree



def print_temporal_tree(tree):
    """
    Stampa l'albero temporale in modo leggibile.

    Args:
        tree: Dizionario che rappresenta l'albero temporale.
    """
    for node, edges in tree.items():
        print(f"{node}: {edges}")

def EA_max_query_function(tree, u, v, t_start):
    """
    Calcola il tempo di arrivo massimo (EA massimo) dal nodo u al nodo v con partenza non prima di t_start.
    
    Args:
        tree: struttura dati che rappresenta l'albero temporale.
        u: nodo di partenza.
        v: nodo di destinazione (radice).
        t_start: tempo minimo di partenza.
    
    Returns:
        Il tempo di arrivo massimo a v o float("-inf") se nessun percorso è possibile.
    """
    current_node = u
    current_time = t_start
    
    while current_node != v:
        # Recupera l'arco (current_node -> parent) e i relativi timestamp
        neighbors = tree.get(current_node, [])
        parent = None
        times = []

        for neighbor, timestamps in neighbors:
            if neighbor == v or neighbor == neighbors[0][0]:  # Identifica il nodo genitore
                parent = neighbor
                times = timestamps
                break

        if not parent or not times:
            return float("-inf")  # Non c'è percorso verso la radice
        
        # Trova il primo timestamp >= current_time
        idx = bisect_left(times, current_time)
        if idx == len(times):
            return float("-inf")  # Nessun timestamp valido trovato
        
        # Prendi il timestamp massimo disponibile >= t_start
        max_valid_time = max(times[idx:])
        
        # Aggiorna il tempo corrente e il nodo corrente
        current_time = max_valid_time
        current_node = parent

    return current_time


def calculate_maximum_earliest_arrivals(tree, left_leaf, right_leaf, root, max_timestamps, EA_query_function):
    """
    Calcola il massimo Earliest Arrival (EA massimo) per i percorsi dalle foglie sinistra e destra alla radice.
    
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
        "Max_EA_sx": EA_sx,
        "Max_EA_dx": EA_dx
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


def find_node_with_max_weight(node):
    """
    Trova il nodo con il timestamp massimo in un albero binario.

    Args:
        node: Nodo corrente.

    Returns:
        Una tupla (timestamp massimo, nodo corrispondente).
    """
    if node is None:
        return float("-inf"), None

    # Massimo timestamp del nodo corrente
    max_timestamp = max(node.weight, default=float("-inf"))

    # Ricorsione sui figli
    left_max, left_node = find_node_with_max_weight(node.left)
    right_max, right_node = find_node_with_max_weight(node.right)

    # Determina il massimo tra nodo corrente e figli
    if max_timestamp >= left_max and max_timestamp >= right_max:
        return max_timestamp, node
    elif left_max >= right_max:
        return left_max, left_node
    else:
        return right_max, right_node

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

    # Fase 2: Trova i nodi con il timestamp massimo nei sottoalberi
    max_left, left_node = find_node_with_max_weight(root.left)
    max_right, right_node = find_node_with_max_weight(root.right)

    print("\n--------FASE 2--------")
    print(f"\nNodo massimo sottoalbero sinistro: {left_node.value if left_node else None}, Timestamp: {max_left}")
    print(f"Nodo massimo sottoalbero destro: {right_node.value if right_node else None}, Timestamp: {max_right}")

    print("\n--------FASE 3--------")
    # Fase 3: Calcolo dell'EA massimo partendo dai nodi trovati in Fase 2
    tree = build_temporal_tree(root)
    print("\nStruttura dell'albero temporale:")
    print_temporal_tree(tree)

    # Forse da sistemare questo?? 
    # Forse bisogna fare in modo che se EA max non esiste, prende quello subito dopo?
    EA_sx = EA_max_query_function(tree, left_node.value, root.value, max_left) if left_node else float("-inf")
    EA_dx = EA_max_query_function(tree, right_node.value, root.value, max_right) if right_node else float("-inf")

    print(f"EA massimo dal nodo sinistro: {EA_sx}")
    print(f"EA massimo dal nodo destro: {EA_dx}")

    # if EA_sx == float("-inf") or EA_dx == float("-inf"):
    #     print("\nCheck Fase 3 NO")
    #     return "L'albero non è temporalmente connesso (EA non valido)."
    # else:
    #     print("\nCheck Fase 3 OK")

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


# Albero di esempio
# root = Node('A')
# root.left = Node('B', weight=[2])
# root.right = Node('C', weight=[3, 5])
# root.left.left = Node('D', weight=[1])
# root.left.right = Node('E', weight=[1, 5, 9])
# root.left.left.left = Node('I', weight=[2, 4])
# root.right.left = Node('F', weight=[7])
# root.right.right = Node('G', weight=[6])
# root.right.left.left = Node('H', weight=[8, 9, 11])

# root = Node('A')
# root.left = Node('B', weight=[2,6])
# root.right = Node('C', weight=[6])
# root.left.left = Node('D', weight=[1,2,3,4,5,6])
# root.left.left.left = Node('F', weight=[3])
# root.left.left.right = Node('G', weight=[1,2,7])
# root.right.right = Node('E', weight=[6])

# root = Node('A')
# root.left = Node('B', weight=[4,5])
# root.right = Node('C', weight=[1,2,3])
# root.left.left = Node('D', weight=[5,6])
# root.left.right = Node('E', weight=[4])
# root.left.right.left = Node('G', weight=[8])
# root.left.right.right = Node('H', weight=[9])
# root.right.left = Node('F', weight=[2,6])

# root = Node('A')
# root.left = Node('B', weight=[2])
# root.right = Node('C', weight=[5,7])
# root.left.left = Node('D', weight=[5])
# root.right.right = Node('E', weight=[8,9])
# root.right.left = Node('F', weight=[8])
# root.left.left.left = Node('G', weight=[1,3])
# root.left.left.right = Node('H', weight=[6])
# root.right.right.left = Node('I', weight=[2,4])

# Esempi vari
# Esempio 1
# root = Node('A')
# root.left = Node('B', weight=[1, 4])
# root.right = Node('C', weight=[2, 6])
# root.left.left = Node('D', weight=[1, 2])
# root.left.right = Node('E', weight=[3])
# root.right.left = Node('F', weight=[5])
# root.right.right = Node('G', weight=[6, 7])

# Esempio 2
root=Node('A')
root.left = Node('B', weight=[1,3])
root.right = Node('C', weight=[2,5])
root.left.left = Node('D', weight=[2,7])

# Esempio 3
# root = Node('A')
# root.left = Node('B', weight=[1, 6])
# root.left.left = Node('D', weight=[2, 6])
# root.left.right = Node('C', weight=[3])
# root.left.left.left = Node('F', weight=[1,4,6])
# root.left.left.right = Node('E', weight=[2,3])
# root.left.left.left.left = Node('H', weight=[1,2,3,4])
# root.left.left.left.right = Node('G', weight=[5])
# root.right = Node('I', weight=[1])

# Esempio 4
# root = Node('A')
# root.left = Node('B', weight=[1, 3,4])
# root.right = Node('C', weight=[4])
# root.left.left = Node('D', weight=[2,4])
# root.right.right = Node('E', weight=[2,5,6])

# Calcolo
start = timer()
print(algoritmo(root))
end = timer()
print(f"\nTempo di esecuzione: {timedelta(seconds=end-start)}")