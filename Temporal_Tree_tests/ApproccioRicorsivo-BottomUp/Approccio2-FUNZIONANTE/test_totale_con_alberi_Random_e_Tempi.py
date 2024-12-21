import networkx as nx
from utils.utils_function import *
from timeit import default_timer as timer
from datetime import timedelta

def preprocess(tree, node, EA_max, LD_max):
    """
    Procedura di preprocessing per calcolare EA_max e LD_max per ogni nodo.
    
    tree: grafo orientato rappresentante l'albero
    node: nodo corrente
    EA_max: dizionario per salvare i valori di EA_max
    LD_max: dizionario per salvare i valori di LD_max
    """
    children = list(tree.successors(node))
    weights = tree.nodes[node].get("weight", [])

    # Caso base: foglia
    if not children:
        EA_max[node] = min(weights)
        LD_max[node] = max(weights)
        return EA_max[node], LD_max[node]

    # Variabili temporanee per raccogliere i valori dai figli
    ea_values = []
    ld_values = []

    for child in children:
        ea_child, ld_child = preprocess(tree, child, EA_max, LD_max)
        ea_values.append(ea_child)
        ld_values.append(ld_child)

    # Calcolo di EA e LD per il nodo corrente
    EA = max(ea_values)
    LD = min(ld_values)

    # Trova il successore e predecessore in base ai pesi
    if weights:
        NextEA = binary_search(weights, EA)
        NextLD = binary_search_leq(weights, LD)
        if NextEA == -1 or NextLD == -1:
            EA_max[node] = float('inf')
            LD_max[node] = float('inf')
        else:
            
            EA_max[node] = NextEA
            LD_max[node] = NextLD
    else:
        EA_max[node] = -1
        LD_max[node] = -1

    return EA_max[node], LD_max[node]

def check_temporal_connectivity(tree, node, EA_max, LD_max):
    """
    Procedura per controllare la connettività temporale di un albero.
    
    tree: grafo orientato rappresentante l'albero
    node: nodo corrente
    EA_max: dizionario contenente i valori di EA_max
    LD_max: dizionario contenente i valori di LD_max
    """
    children = list(tree.successors(node))

    # Caso base: foglia
    if not children:
        return True

    intervals = []

    for child in children:
        if not check_temporal_connectivity(tree, child, EA_max, LD_max):
            return False
        if not (EA_max[child] == float("inf") or LD_max[child] == float("inf")):
            intervals.append((EA_max[child], LD_max[child]))
        else:
            return False

    # Ordina gli intervalli per LD_max
    intervals.sort(key=lambda x: x[1])

    if len(intervals) > 1:
        if not (intervals[0][0] <= intervals[1][1]):
            return False
        
        # Controllo di consistenza
        for i in range(1, len(intervals)):
            if intervals[i][0] > intervals[0][1]:
                return False
    elif len(intervals) == 1:
        return True
        
    return True

def algoritmo(T):
    """
    Algoritmo per la verifica della connettività temporale di un albero.
    
    T: grafo orientato rappresentante l'albero
    """
    start = timer()
    EA_max = {}
    LD_max = {}
    preprocess(T, "A", EA_max, LD_max)

    check = check_temporal_connectivity(T, "A", EA_max, LD_max) 
    end = timer()
    print("Tempo di esecuzione:", timedelta(seconds=end-start))
    if check:
        return "L'albero è temporalmente connesso",timedelta(seconds=end-start)
    else:
        return "L'albero non è temporalmente connesso",timedelta(seconds=end-start)
    
def calculate_average_time():
    tempo_totale = timedelta()
    tempo_totale2 = timedelta()
    for _ in range(1000):
        tree = create_random_tree(8, (1, 15))
        check, elapsed_time = algoritmo(tree)
        check2, elapsed_time2 = algoritmo3_networkx(tree)
        tempo_totale += elapsed_time
        tempo_totale2 += elapsed_time2
    print("-------------------\n")
    print("Tempi per algoritmo separato:")
    print("Tempo medio di esecuzione:", tempo_totale / 400)
    print("Tempo totale di esecuzione:", tempo_totale)
    print("\nTempi per algoritmo unificato:")
    print("Tempo medio di esecuzione:", tempo_totale2 / 400)
    print("Tempo totale di esecuzione:", tempo_totale2)


def dfs_EA_tmax_networkx(tree, root):
    # Caso base: nodo nullo
    if root is None:
        return {}

    # Ottieni i figli del nodo corrente
    children = list(tree.successors(root))
    weight = tree.nodes[root]["weight"]

    # Caso base: foglia
    if not children:
        #print(
        #    f"EA e tempo max visita per il sottoalbero radicato nel nodo {root} (foglia): {weight[0], weight[-1]}"
        #)
        return {root: (weight[0], weight[-1])}

    # Variabili per raccogliere i valori EA e Tmax per ogni sottoalbero
    sottoalberi = {}
    ea_tmax = []

    # Calcolo ricorsivo per ogni figlio
    for child in children:
        sottoalberi.update(dfs_EA_tmax_networkx(tree, child))
        ea, t_max = sottoalberi[child]
        ea_tmax.append((ea, t_max))

    # Step 1: Ordina per Tmax
    ea_tmax.sort(key=lambda x: x[1])

    # Step 2 e 3: Controlli di consistenza
    if len(ea_tmax) > 1:
        if not (ea_tmax[0][0] <= ea_tmax[1][1]):
            return {root: (float("inf"), float("inf"))}

        for i in range(1, len(ea_tmax)):
            if ea_tmax[i][0] > ea_tmax[0][1]:
                return {root: (float("inf"), float("inf"))}

    # Calcola EA e Tmax per il nodo corrente
    EA = max(ea_tmax, key=lambda x: x[0])[0]
    t_max_visita = min(ea_tmax, key=lambda x: x[1])[1]
    if not weight:
        k, nextTimeMax = 0, 0
        sottoalberi[root] = (k, nextTimeMax)
        return sottoalberi
    k = binary_search(weight, EA)
    nextTimeMax = binary_search_leq(weight, t_max_visita)

    if nextTimeMax == -1 and root != "A":
        return {root: (float("inf"), float("inf"))}

    # Aggiorna i risultati
    sottoalberi[root] = (k, nextTimeMax)
    return sottoalberi


def algoritmo3_networkx(tree):
    # Trova la radice (nodo senza archi entranti)
    root = [n for n, d in tree.in_degree() if d == 0][0]

    # Esegui DFS-EA-Tmax
    start = timer()
    start1 = timer()
    start2 = timer()
    risultati = dfs_EA_tmax_networkx(tree, root)

    # Ottieni i risultati per i figli della radice
    figli = list(tree.successors(root))
    if not figli:
        return False

    ea_tmax = []
    if risultati[root][0] == float("inf") or risultati[root][1] == float("inf"):
        end1 = timer()
        print(f"\nTempo di esecuzione: {timedelta(seconds=end1 - start1)}")
        return False,timedelta(seconds=end1 - start1)

    for child in figli:
        ea, t_max = risultati[child]
        ea_tmax.append((ea, t_max))

    # Step 1: Ordina per Tmax
    ea_tmax.sort(key=lambda x: x[1])

    # Step 2 e 3: Controlli di consistenza
    if len(ea_tmax) > 1:
        if not (ea_tmax[0][0] <= ea_tmax[1][1]):
            return False

        for i in range(1, len(ea_tmax)):
            if ea_tmax[i][0] > ea_tmax[0][1]:
                return False
    elif len(ea_tmax) == 1:
        end2 = timer()
        print(f"\nTempo di esecuzione: {timedelta(seconds=end2 - start2)}")
        return True,timedelta(seconds=end2 - start2)
    end = timer()
    print(f"\nTempo di esecuzione: {timedelta(seconds=end - start)}")
    return True,timedelta(seconds=end - start)

if __name__ == "__main__":
    # tree = create_tree_with_networkx()
    # print(algoritmo(tree))
    calculate_average_time()

