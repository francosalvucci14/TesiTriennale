# Fase 1 : Prepcrocessing
## Verifico se partendo da root, posso visitare tutti i nodi dell'albero
## (se non è possibile, l'albero non è temporalmente connesso). 
## Per farlo basta fare una visita DFS che controlla se ogni nodo rispetta la condizione di crescita incrementale dei timestamp.

# Fase 2 : Calcolo foglia con peso massimo nei sottoalberi sinistro e destro
## Per trovare la foglia con peso massimo nei sottoalberi sinistro e destro,
## posso utilizzare la funzione find_leaf_max_timestamp definita in precedenza.
## Questa funzione calcola la foglia con peso massimo in un albero binario.

# Fase 3 : Calcolo dell'EAmax partendo dalla fgolia più profonda fino alla radice (e se fosse EA min? quindi quello che parte dalla foglia più profonda, con peso minimo)
## se non esiste EAmin allora non esiste EAmax, ma se non esiste EAmax non è detto che non eisste EAmin
## Questa fase è simmetrica, ovvero vale per entrambi i sottoalberi, quindi ci concentreremo solo su un sottoalbero
## A questo punto, applico l'algoritmo per calcolare l'EA, usando la struttura dati del professore, ovvero quella che impiega tempo O(logMlogL)
## Se la funzione ritortna -inf, sia da un lato che dall'altro, allora ritorno subito False (l'albero non è temporalmente connesso)

# Fase 4 : Verifica finale
## Se l'EAmax calcolato è minore o uguale al timestamp massimo del sottoalbero sinistro e destro,
## ovvero il timestamp che mi permette di visitare tutto il sottoalbero, allora l'albero è temporalmente connesso.
## Altrimenti, l'albero non è temporalmente connesso.

## Oppure faccio cosi, parto dall'EAmax da sx, e lo uso come input per la visita DFS temporale da root, ovvero uso EAmax ad sx come t_start per la visita.
## Faccio la stessa cosa da EAmax da dx, se uno dei due ritorna false allora ritorno False e affermo che l'albero non è temporalmente connesso.
## Altrimenti, se entrambi ritornano True, allora l'albero è temporalmente connesso.
from bisect import bisect_left

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

def find_leaf_with_max_weight(node):
    if node is None:
        return -1, None  # Nessuna foglia trovata
    
    # Nodo foglia
    if node.left is None and node.right is None:
        return max(node.weight, default=-1), node
    
    # Ricorsione per sottoalbero sinistro
    left_max_weight, left_node = find_leaf_with_max_weight(node.left)
    
    # Ricorsione per sottoalbero destro
    right_max_weight, right_node = find_leaf_with_max_weight(node.right)
    
    # Determina la foglia con il massimo peso
    if left_max_weight >= right_max_weight:
        return left_max_weight, left_node
    else:
        return right_max_weight, right_node


# Wrapper per calcolare le foglie con il timestamp massimo nei sottoalberi sinistro e destro
def find_leaves_with_max_weights_in_subtrees(root):
    if root is None:
        return None, None, -1, -1  # Albero vuoto
    
    # Trova la foglia con il massimo timestamp nel sottoalbero sinistro
    max_weight_sx, left_leaf = find_leaf_with_max_weight(root.left)

    # Trova la foglia con il massimo timestamp nel sottoalbero destro
    max_weight_dx, right_leaf = find_leaf_with_max_weight(root.right)
    
    return left_leaf, right_leaf, max_weight_sx, max_weight_dx

def algoritmo(root,tree=None):
    # Step1
    left_leaf, right_leaf, max_t_sx, max_t_dx = find_leaves_with_max_weights_in_subtrees(root)
    print("Foglia con peso massimo nel sottoalbero sinistro:", left_leaf.value, "Timestamp:", max_t_sx)
    print("Foglia con peso massimo nel sottoalbero destro:", right_leaf.value, "Timestamp:", max_t_dx)
    tree = build_temporal_tree(root)
    print_temporal_tree(tree)
    # Step2
    result = calculate_maximum_earliest_arrivals(tree, left_leaf, right_leaf, root, (max_t_sx, max_t_dx), EA_max_query_function)
    if not result:
        return False
    else:
        return "Bisogna partire con step 3"
    # Step3
    ## Calcolo tempi max per visitare un intero sottoalbero
    
    # Step4 
    ## Verifica finale

    # Ster 5 return check
    """
    """

# Albero di esempio
# root = Node('A')
# root.left = Node('B', weight=[1, 9])
# root.right = Node('C', weight=[3])
# root.left.left = Node('D', weight=[2])
# root.left.right = Node('E', weight=[7])
# root.right.left = Node('F', weight=[4])
# root.right.right = Node('G', weight=[6])
# root.left.left.left = Node('H', weight=[3])
# root.left.left.right = Node('I', weight=[1, 2, 3])

# Struttura temporale dell'albero
# temporal_tree = {
#     'H': [('D', [8])],
#     'I': [('D', [1, 2, 3])],
#     'D': [('B', [2])],
#     'E': [('B', [7])],
#     'F': [('C', [4])],
#     'G': [('C', [6])],
#     'B': [('A', [1, 5])],
#     'C': [('A', [3])],
# }

root = Node('A')
root.left = Node('B', weight=[2])
root.right=Node('C', weight=[3,5])
root.left.left=Node('D', weight=[1])
root.left.right=Node('E', weight=[1,5,9])
root.left.left.left=Node('I', weight=[2,4])
root.right.left=Node('F', weight=[7])
root.right.right=Node('G', weight=[6])
root.right.left.left=Node('H', weight=[8,9,11])

# Calcolo
#left_leaf, right_leaf, max_t_sx, max_t_dx = find_leaves_with_max_weights_in_subtrees(root)


#print_temporal_tree(tree)
#result = calculate_maximum_earliest_arrivals(tree, left_leaf, right_leaf, root, (max_t_sx, max_t_dx), EA_max_query_function)

# Output
#print("Risultato massimo EA:", result)
print("L'albero è temporalmente connesso?", algoritmo(root))