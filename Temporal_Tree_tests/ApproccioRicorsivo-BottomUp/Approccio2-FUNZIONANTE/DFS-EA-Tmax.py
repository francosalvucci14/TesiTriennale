from timeit import default_timer as timer
from datetime import timedelta

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

def dfs_EA_tmax_spazio1(root):
    
    if root is None:
        return float("-inf"),float("inf")
    if root.left == None and root.right == None:
        print(f"EA e tempo max visita per il sottoalbero radicato nel nodo {root.value} (foglia) : {root.weight[0],root.weight[-1]}")
        return root.weight[0],root.weight[-1] #min(root.weight), max(root.weight)

    min_sx,max_sx = dfs_EA_tmax_spazio1(root.left)

    min_dx,max_dx = dfs_EA_tmax_spazio1(root.right)
    
    if min_sx>max_dx or min_dx>max_sx:
        return float("inf"),float("inf")
    
    EA = max(min_sx,min_dx)
    t_max_visita = min(max_sx,max_dx)
    print(f"EA e tempo max visita per il sottoalbero radicato nel nodo {root.value} (nodo interno) : {EA,t_max_visita}")
    k = binary_search(root.weight,EA)
    nextTimeMax = binary_search_leq(root.weight,t_max_visita) #binary search per trovare il predecessore, quindi il primo tempo t <= t_max_visita
    if k == -1 or nextTimeMax == -1 or nextTimeMax < t_max_visita:
        return float("inf"),float("inf")
        #exit("Errore: EA o tempo max visita non trovati")
    minTime = min(t_max_visita,nextTimeMax)
    #valori_EA_Tmax=(EA,t_max_visita)

    return k,minTime

def dfs_EA_tmax_spazioN(root):
    # Caso base: nodo nullo
    if root is None:
        return {}

    sottoalberi = {}
    # Caso base: foglia
    if root.left is None and root.right is None:
        print(f"EA e tempo max visita per il sottoalbero radicato nel nodo {root.value} (foglia): {root.weight[0], root.weight[-1]}")
        #return {root.value: (root.weight[0], root.weight[-1])}
        sottoalberi[root.value] = (root.weight[0], root.weight[-1])
        return sottoalberi
    # Variabili per raccogliere i valori EA e Tmax per ogni sottoalbero
    

    # Calcolo ricorsivo per il sottoalbero sinistro
    if root.left is not None:
        sottoalberi.update(dfs_EA_tmax_spazioN(root.left))

    # Calcolo ricorsivo per il sottoalbero destro
    if root.right is not None:
        sottoalberi.update(dfs_EA_tmax_spazioN(root.right))

    # Estrai i valori di EA e Tmax dai figli
    ea_sx, t_max_sx = sottoalberi[root.left.value] if root.left else (float("-inf"), float("inf"))
    ea_dx, t_max_dx = sottoalberi[root.right.value] if root.right else (float("-inf"), float("inf"))

    # Controllo di consistenza tra i sottoalberi
    if ea_sx > t_max_dx or ea_dx > t_max_sx:
        #return {root.value: (float("inf"), float("inf"))}
        sottoalberi[root.value] = (float("inf"), float("inf"))
        return sottoalberi

    # Calcolo EA e Tmax per il nodo corrente
    EA = max(ea_sx, ea_dx)
    t_max_visita = min(t_max_sx, t_max_dx)
    print(f"EA e tempo max visita per il sottoalbero radicato nel nodo {root.value} (nodo interno): {EA, t_max_visita}")
    
    k = binary_search(root.weight,EA)
    nextTimeMax = binary_search_leq(root.weight,t_max_visita) #binary search per trovare il predecessore, quindi il primo tempo t <= t_max_visita
    if root.weight == []:
        k,nextTimeMax = 0,0
        sottoalberi[root.value] = (k, nextTimeMax)
        return sottoalberi
    if k == -1 or nextTimeMax == -1 or nextTimeMax < t_max_visita:
        sottoalberi[root.value] = (float("inf"), float("inf"))
        #return {root.value: (float("inf"), float("inf"))}
        return sottoalberi
    minTime = min(t_max_visita,nextTimeMax)
    # Aggiornamento del nodo corrente nei risultati
    sottoalberi[root.value] = (k, minTime)

    return sottoalberi


def algoritmo(root):
    print("Questo è per alberi binari\n")
    
    ea_sx,t_max_sx = dfs_EA_tmax_spazio1(root.left)
    ea_dx,t_max_dx = dfs_EA_tmax_spazio1(root.right)
    #print(valori_sx,valori_dx)
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
    
def algoritmo2(root):
    print("Questo è per alberi binari\n")
    
    # Esegui DFS-EA-Tmax una sola volta
    risultati = dfs_EA_tmax_spazioN(root)

    # Ottieni i risultati per i figli della radice
    ea_sx, t_max_sx = risultati[root.left.value] if root.left else (float("-inf"), float("inf"))
    ea_dx, t_max_dx = risultati[root.right.value] if root.right else (float("-inf"), float("inf"))

    print("------------------------------------------------")
    print(f"EA e tempo max visita sx della radice {root.value}: {ea_sx, t_max_sx}")
    print(f"EA e tempo max visita dx della radice {root.value}: {ea_dx, t_max_dx}")

    # Controllo finale per la radice
    if ea_sx == float("inf") or ea_dx == float("inf"):
        return False

    if ea_sx <= t_max_dx and ea_dx <= t_max_sx:
        return True
    else:
        return False

def print_tree(root, level=0):
    if root is not None:
        print("  " * level + f"Node {root.value}, Weight: {root.weight}")
        for child in root.children:
            print_tree(child, level + 1)


# Esempio 1
# root = Node('A')
# root.left = Node('B', weight=[3])
# root.right = Node('C', weight=[1,4])
# root.left.left = Node('D', weight=[1,3])
# root.left.right = Node('E', weight=[2,5])

# Esempio 2
root = Node('A')
root.left = Node('B', weight=[2,6])
root.right = Node('C', weight=[6])
root.left.left = Node('D', weight=[1,2,3,4,5])
root.right.right = Node('E', weight=[6])

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
# root = Node('A',weight=[float("-inf")])
# root.left = Node('B', weight=[1,3])
# root.left.left = Node('D', weight=[1,2])
# root.left.right = Node('E', weight=[2,4])

# Esempio 8
# root = Node('A')
# root.left = Node('B', weight=[1,4])
# root.left.left = Node('C', weight=[2,4])
# root.left.left.left = Node('D', weight=[1,3])
# root.left.left.left.left = Node('E', weight=[3,4])

# Esempio 9
# root = Node('A')
# root.left = Node('B', weight=[2,3,5,8])
# root.right = Node('C', weight=[3,5])
# root.left.left = Node('D', weight=[1,4,5,6])
# root.left.right = Node('E', weight=[1,5,9])
# root.right.left = Node('F', weight=[1,2,5])
# root.right.right = Node('G', weight=[2,5])
# root.left.left.left = Node('H', weight=[2,4])
# root.right.left.right = Node('I', weight=[1,11])

# Esempio 10
# root = Node('A')
# root.left = Node('B', weight=[1,9])
# root.right = Node('C', weight=[8])
# root.left.left = Node('D', weight=[2])
# root.left.right = Node('E', weight=[7])
# root.right.left = Node('F', weight=[4])
# root.right.right = Node('G', weight=[6])
# root.left.left.left = Node('H', weight=[3])
# root.left.left.right = Node('I', weight=[1,2,3])

# Esempio 11
# root = Node('A',root=True)
# root.left = Node('B', weight=[1,5,7])
# root.right = Node('C', weight=[2,5,8])
# root.left.left = Node('D', weight=[2,8])
# root.left.right = Node('E', weight=[2,5,10])
# root.left.right.left = Node('F', weight=[1,5,6])
# root.left.right.right = Node('G', weight=[2,7,9])
# root.right.right = Node('H', weight=[2,3,4])
# root.right.right.left = Node('I', weight=[1,15])
# root.right.right.right = Node('J', weight=[1,11])

start = timer()
print("Versione con spazio O(1)")
print(f"Albero temporalmente connesso? : {algoritmo(root)}")
print("\nVersione con spazio O(n)")
print(f"Albero temporalmente connesso? : {algoritmo2(root)}")
end = timer()
print(timedelta(seconds=end-start))
