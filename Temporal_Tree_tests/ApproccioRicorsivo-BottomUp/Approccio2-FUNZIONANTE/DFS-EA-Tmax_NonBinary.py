class NodeNonBinary:
    def __init__(self, value, weight=[], parent=None):
        self.value = value
        self.weight = weight
        self.children = []  # Lista dei figli
        self.parent = parent


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
    
def binary_search_leq(arr, target):
    if len(arr) == 1:  # Caso in cui l'array ha un solo elemento
        return arr[0] if arr[0] <= target else -1  # Restituisce l'elemento se è ≤ target
    
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

def dfs_EA_tmax_spazioN_NonBinary(root):
    # Caso base: nodo nullo
    if root is None:
        return {}

    # Caso base: foglia
    if not root.children:
        print(f"EA e tempo max visita per il sottoalbero radicato nel nodo {root.value} (foglia): {root.weight[0], root.weight[-1]}")
        return {root.value: (root.weight[0], root.weight[-1])}

    # Variabili per raccogliere i valori EA e Tmax per ogni sottoalbero
    sottoalberi = {}

    # Calcolo ricorsivo per ogni figlio
    ea_vals = []
    t_max_vals = []

    for child in root.children:
        sottoalberi.update(dfs_EA_tmax_spazioN_NonBinary(child))
        ea, t_max = sottoalberi[child.value]
        ea_vals.append(ea)
        t_max_vals.append(t_max)

    #Controllo di consistenza tra i figli
    # for i in range(len(ea_vals)):
    #     for j in range(i + 1, len(ea_vals)):
    #         if ea_vals[i] > t_max_vals[j] and ea_vals[j] > t_max_vals[i]:
    #             return {root.value: (float("inf"), float("inf"))}

    min_tmax = min(t_max_vals)
    pos_min = t_max_vals.index(min_tmax)
    #first_ea = ea_vals[pos_min]
    for i in range(len(ea_vals)):
        if ea_vals.index(ea_vals[i]) == pos_min:
            continue
        elif ea_vals[i] > min_tmax:
            return {root.value: (float("inf"), float("inf"))}

    # Calcolo EA e Tmax per il nodo corrente
    EA = max(ea_vals)
    t_max_visita = min(t_max_vals)
    
    k = binary_search(root.weight, EA)
    nextTimeMax = binary_search_leq(root.weight, t_max_visita)  # Binary search per trovare il predecessore
    if nextTimeMax == -1 and root.value != "A":
        return {root.value: (float("inf"), float("inf"))}
    print(f"Valore di nextTimeMax: {nextTimeMax} per il nodo {root.value}")
    print(f"Valore di k: {k} per il nodo {root.value}")
    print(f"EA e tempo max visita per il sottoalbero radicato nel nodo {root.value} (nodo interno): {k, nextTimeMax}")
    minTime = min(t_max_visita, nextTimeMax)

    # Aggiornamento del nodo corrente nei risultati
    sottoalberi[root.value] = (k, minTime)

    return sottoalberi

def algoritmo3_NonBinary(root):
    print("\nQuesto è per alberi non binari\n")
    
    # Esegui DFS-EA-Tmax una sola volta
    risultati = dfs_EA_tmax_spazioN_NonBinary(root)

    # Ottieni i risultati per i figli della radice
    figli = root.children
    if not figli:
        return False

    ea_vals = []
    t_max_vals = []
    if risultati[root.value][0] == float("inf") or risultati[root.value][1] == float("inf"):
        return False
    for child in figli:
        ea, t_max = risultati[child.value]
        ea_vals.append(ea)
        t_max_vals.append(t_max)

    print("------------------------------------------------")
    for i, child in enumerate(figli):
        print(f"EA e tempo max visita del figlio {child.value}: {ea_vals[i], t_max_vals[i]}")
    # Controllo finale per la radice con binsearch
    #primo_ea = ea_vals[0]
    check = False
    #min_tmax = t_max_vals[0]
    min_tmax = min(t_max_vals)
    for i in range(len(ea_vals)):
        if ea_vals[i] <= min_tmax:
            check = True
        else:
            return False
    if check == True:
        return True
    

def print_tree(root, level=0):
    if root is not None:
        print("  " * level + f"Node {root.value}, Weight: {root.weight}")
        for child in root.children:
            print_tree(child, level + 1)

# root = NodeNonBinary("A")
# node_b = NodeNonBinary("B", weight=[1,5,7], parent=root)
# node_c = NodeNonBinary("C", weight=[2,5,8], parent=root)
# node_d = NodeNonBinary("D", weight=[2,5,10], parent=root)
# node_e = NodeNonBinary("E", weight=[1,5,6], parent=node_b)
# node_f = NodeNonBinary("F", weight=[2,7,9], parent=node_c)
# node_g = NodeNonBinary("G", weight=[2,8], parent=node_c)
# node_h = NodeNonBinary("H", weight=[1,11], parent=node_d)
# node_i = NodeNonBinary("I", weight=[1,15], parent=node_d)
# node_j = NodeNonBinary("J", weight=[1,17], parent=node_d)

# root.children = [node_b, node_c,node_d]
# node_b.children = [node_e]
# node_c.children = [node_f, node_g]
# node_d.children = [node_h, node_i, node_j]

root = NodeNonBinary("A")
node_b = NodeNonBinary("B", weight=[2,6], parent=root)
node_c = NodeNonBinary("C", weight=[2,11], parent=root)
node_d = NodeNonBinary("D", weight=[2,5], parent=root)
node_e = NodeNonBinary("E", weight=[2,4,5], parent=node_b)
node_f = NodeNonBinary("F", weight=[1,3], parent=node_b)
node_g = NodeNonBinary("G", weight=[1,11], parent=node_c)
node_h = NodeNonBinary("H", weight=[1,11], parent=node_d)
node_i = NodeNonBinary("I", weight=[1,15], parent=node_d)
node_j = NodeNonBinary("J", weight=[1,22], parent=node_d)

root.children = [node_b, node_c,node_d]
node_b.children = [node_e, node_f]
node_c.children = [node_g]
node_d.children = [node_h, node_i, node_j]

# root = NodeNonBinary("A")
# node_b = NodeNonBinary("B", weight=[1,3], parent=root)
# node_c = NodeNonBinary("C", weight=[2,4], parent=root)
# node_d = NodeNonBinary("D", weight=[3,7], parent=root)

# root.children = [node_b, node_c, node_d]


print_tree(root)
print(f"\nAlbero non binario temporalmente connesso? : {algoritmo3_NonBinary(root)}")