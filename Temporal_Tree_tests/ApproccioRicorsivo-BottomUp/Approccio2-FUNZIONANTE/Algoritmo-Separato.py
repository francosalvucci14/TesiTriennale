import networkx as nx
from utils.utils_function import *
from timeit import default_timer as timer
from datetime import timedelta


def create_tree_with_networkx():
    # Crea un grafo diretto
    tree = nx.DiGraph()

    # # Aggiungi i nodi e i pesi degli archi entranti
    # tree.add_node("A", weight=None)
    # tree.add_node("B", weight=[2,6])
    # tree.add_node("C", weight=[6])
    # tree.add_node("D", weight=[1,2,3,4,5,6])
    # tree.add_node("E", weight=[6])
    # tree.add_node("F", weight=[1,6])
    # tree.add_node("G", weight=[2,3])
    # tree.add_node("H", weight=[3,4])

    # tree.add_edges_from([
    #     ("A", "B"),
    #     ("A", "C"),
    #     ("A", "F"),
    #     ("B", "D"),
    #     ("C", "E"),
    #     ("F", "G"),
    #     ("F", "H")
    # ])
    tree.add_node("A", weight=None)
    tree.add_node("B", weight=[1,3])
    tree.add_node("C", weight=[2])
    tree.add_node("D", weight=[2,7])

    # Aggiungi gli archi (parent -> child)
    tree.add_edges_from([
        ("A", "B"),
        ("A", "C"),
        ("A", "D")
    ])

    return tree

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
    #start = timer()
    EA_max = {}
    LD_max = {}
    preprocess(T, "A", EA_max, LD_max)
    print("Valori di EA_max:", EA_max,"\n")
    print("Valori di LD_max:", LD_max,"\n")
    check = check_temporal_connectivity(T, "A", EA_max, LD_max) 
    #end = timer()
    #print("Tempo di esecuzione:", timedelta(seconds=end-start))
    if check:
        return "L'albero è temporalmente connesso"
    else:
        return "L'albero non è temporalmente connesso"
    
def calculate_average_time():
    tempo_totale = timedelta()
    for _ in range(400):
        tree = create_random_tree(8, (1, 15))
        check, elapsed_time = algoritmo(tree)
        tempo_totale += elapsed_time
        print(check)

    print("Tempo medio di esecuzione:", tempo_totale / 400)
    print("Tempo totale di esecuzione:", tempo_totale)

if __name__ == "__main__":
    tree = create_tree_with_networkx()
    print(algoritmo(tree))
    #calculate_average_time()

