class Node:
    def __init__(self, value, weight=[],root=None):
        self.value = value
        self.weight = weight
        self.left = None
        self.right = None
        self.root = root


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

def dfs_EA_tmax(root):
    # Caso base: nodo nullo
    if root is None:
        return {}

    # Caso base: foglia
    if root.left is None and root.right is None:
        print(f"EA e tempo max visita per il sottoalbero radicato nel nodo {root.value} (foglia): {root.weight[0], root.weight[-1]}")
        return {root.value: (root.weight[0], root.weight[-1])}

    # Variabili per raccogliere i valori EA e Tmax per ogni sottoalbero
    sottoalberi = {}

    # Calcolo ricorsivo per il sottoalbero sinistro
    if root.left is not None:
        sottoalberi.update(dfs_EA_tmax(root.left))

    # Calcolo ricorsivo per il sottoalbero destro
    if root.right is not None:
        sottoalberi.update(dfs_EA_tmax(root.right))

    # Estrai i valori di EA e Tmax dai figli
    ea_sx, t_max_sx = sottoalberi[root.left.value] if root.left else (float("-inf"), float("inf"))
    ea_dx, t_max_dx = sottoalberi[root.right.value] if root.right else (float("-inf"), float("inf"))

    # Controllo di consistenza tra i sottoalberi
    if ea_sx > t_max_dx and ea_dx > t_max_sx:
        return {root.value: (float("inf"), float("inf"))}

    # Calcolo EA e Tmax per il nodo corrente
    EA = max(ea_sx, ea_dx)
    t_max_visita = min(t_max_sx, t_max_dx)
    print(f"EA e tempo max visita per il sottoalbero radicato nel nodo {root.value} (nodo interno): {EA, t_max_visita}")
    
    k = binary_search(root.weight,EA)
    nextTimeMax = binary_search_leq(root.weight,t_max_visita) #binary search per trovare il predecessore, quindi il primo tempo t <= t_max_visita
    
    minTime = min(t_max_visita,nextTimeMax)
    # Aggiornamento del nodo corrente nei risultati
    sottoalberi[root.value] = (k, minTime)

    return sottoalberi


def algoritmo(root):
    print("Questo è per alberi binari\n")
    
    # Esegui DFS-EA-Tmax una sola volta
    risultati = dfs_EA_tmax(root)

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

root = Node('A')
root.left = Node('B', weight=[2,6])
root.right = Node('C', weight=[6])
root.left.left = Node('D', weight=[1,2,3,4,5,6])
root.right.right = Node('E', weight=[6])


print(algoritmo(root))