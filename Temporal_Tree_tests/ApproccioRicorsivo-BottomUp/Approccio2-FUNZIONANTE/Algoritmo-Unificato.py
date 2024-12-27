import networkx as nx
from utils.utils_function import *
from timeit import default_timer as timer
from datetime import timedelta

def create_tree_with_networkx():
    # Crea un grafo diretto
    tree = nx.DiGraph()

    # # # Aggiungi i nodi e i pesi degli archi entranti
    
    tree.add_node("A", weight=None)  # Radice senza arco entrante
    tree.add_node("B", weight=[2, 6])
    tree.add_node("C", weight=[6])
    tree.add_node("D", weight=[1, 2, 3, 4, 5, 6])
    tree.add_node("E", weight=[6])
    tree.add_node("F", weight=[1, 6])

    # Aggiungi gli archi (parent -> child)
    tree.add_edges_from([
        ("A", "B"),
        ("A", "C"),
        ("A", "F"),
        ("B", "D"),
        ("C", "E")
    ])

    return tree

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

    #print(f"Valore di nextTimeMax: {nextTimeMax} per il nodo {root}")
    #print(f"Valore di k: {k} per il nodo {root}")
    #print(
    #    f"EA e tempo max visita per il sottoalbero radicato nel nodo {root} (nodo interno): {k, nextTimeMax}"
    #)

    #minTime = min(t_max_visita, nextTimeMax)

    # Aggiorna i risultati
    sottoalberi[root] = (k, nextTimeMax)
    return sottoalberi


def algoritmo3_networkx(tree):
    # Esegui DFS-EA-Tmax
    root = "A"
    risultati = dfs_EA_tmax_networkx(tree, root)

    # Ottieni i risultati per i figli della radice
    figli = list(tree.successors(root))
    if not figli:
        return False

    ea_tmax = []
    if risultati[root][0] == float("inf") or risultati[root][1] == float("inf"):
        return False

    for child in figli:
        ea, t_max = risultati[child]
        ea_tmax.append((ea, t_max))

    print("------------------------------------------------")
    for i, child in enumerate(figli):
        print(
            f"EA e tempo max visita del figlio {child}: {ea_tmax[i][0], ea_tmax[i][1]}"
        )

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
        return True
    
    return True

def calculate_average_time():
    tempo_totale = timedelta()
    for _ in range(400):
        tree = create_random_tree(8, (1, 15))
        check, elapsed_time = algoritmo3_networkx(tree)
        tempo_totale += elapsed_time
        print(check)

    print("Tempo medio di esecuzione:", tempo_totale / 400)
    print("Tempo totale di esecuzione:", tempo_totale)

if __name__ == "__main__":
    #calculate_average_time()
    start = timer()
    tree = create_tree_with_networkx()

    #print("Albero creato con NetworkX:")
    #print_tree_networkx(tree, "A")
    print(f"\nAlbero temporalmente connesso? : {algoritmo3_networkx(tree)}")
    end = timer()
    print("Tempo di esecuzione:", timedelta(seconds=end - start))



