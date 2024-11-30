class Node:
    def __init__(self, value, weight=[]):
        self.value = value
        self.weight = weight
        self.left = None
        self.right = None

def binary_search(arr, target):
    if len(arr) == 1:  # Caso in cui l'array ha un solo elemento
        return arr[0] if arr[0] >= target else -1  # Restituisce l'indice se il valore è >= target
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

def dfs_EA_tmax(root):
    if root is None:
        return float("-inf"),float("inf")
    if root.left == None and root.right == None:
        print(f"EA e tempo max visita per il sottoalbero radicato nel nodo {root.value} (foglia) : {root.weight[0],root.weight[-1]}")
        return root.weight[0],root.weight[-1] #min(root.weight), max(root.weight)

    # Per ogni figlio del nodo corrente, faccio partire scansione ricorsiva per alberi non binari
    min_sx,max_sx = dfs_EA_tmax(root.left)
    min_dx,max_dx = dfs_EA_tmax(root.right)
    
    if not (min_sx<=max_dx or min_dx<=max_sx):
        return float("inf"),float("inf")
    
    EA = max(min_sx,min_dx)
    t_max_visita = min(max_sx,max_dx)
    print(f"EA e tempo max visita per il sottoalbero radicato nel nodo {root.value} (nodo interno) : {EA,t_max_visita}")
    k = binary_search(root.weight,EA)
    if k == -1:
        return float("inf"),float("inf")
    return k,min(t_max_visita,root.weight[-1])

def algoritmo(root):
    
    # Tutti figli root, poi dfs per ongi figlio per alberi non binari
    ea_sx,t_max_sx = dfs_EA_tmax(root.left)
    ea_dx,t_max_dx = dfs_EA_tmax(root.right)
    print("------------------------------------------------")
    print(f"EA e tempo max visita sx della radice {root.value} : {ea_sx,t_max_sx}")
    print(f"EA e tempo max visita dx della radice {root.value} : {ea_dx,t_max_dx}")
    
    if ea_sx == float("inf") or ea_dx == float("inf"):
        return False
    
    # Ogni controllo del caso per alberi non binari
    if ea_sx <= t_max_dx and ea_dx <= t_max_sx:
        return True
    else:
        return False

# Esempio 1
# root = Node('A')
# root.left = Node('B', weight=[3])
# root.right = Node('C', weight=[1,4])
# root.left.left = Node('D', weight=[1,3])
# root.left.right = Node('E', weight=[2,5])

# Esempio 2
# root = Node('A')
# root.left = Node('B', weight=[2,6])
# root.right = Node('C', weight=[6])
# root.left.left = Node('D', weight=[1,2,3,4,5])
# root.right.right = Node('E', weight=[6])

# Esempio 3
# root = Node('A')
# root.left = Node('B', weight=[3])
# root.right = Node('C', weight=[2, 5])
# root.right.right = Node('D', weight=[1,2,3,4,5,6,7])

# Esempio 4
# root = Node('A')
# root.left = Node('B', weight=[2])
# root.right = Node('C', weight=[5,7])
# root.left.left = Node('D', weight=[5])
# root.right.left = Node('E', weight=[8,9])
# root.right.right = Node('F', weight=[1,2])

# Esempio 5
# root = Node('A')
# root.left = Node('B', weight=[1, 3,4])
# root.right = Node('C', weight=[4])
# root.left.left = Node('D', weight=[2,4])
# root.right.right = Node('E', weight=[2,5,6])

# Esempio 6
# root = Node('A')
# root.left = Node('B', weight=[1, 3])
# root.right = Node('C', weight=[2, 6])
# root.left.left = Node('D', weight=[3,5])
# root.left.right = Node('E', weight=[4,6])

# Esempio 7
# root = Node('A')
# root.left = Node('B', weight=[1,3])
# root.left.left = Node('D', weight=[1,2])
# root.left.right = Node('E', weight=[2,4])

# Esempio 8
root = Node('A')
root.left = Node('B', weight=[1,4])
root.left.left = Node('C', weight=[2,4])
root.left.left.left = Node('D', weight=[1,3])
root.left.left.left.left = Node('E', weight=[3,4])

print(f"Albero temporalmente connesso? : {algoritmo(root)}")