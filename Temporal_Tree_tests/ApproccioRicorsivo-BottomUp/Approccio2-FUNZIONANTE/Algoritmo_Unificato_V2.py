import networkx as nx
from utils.utils_function import *
from timeit import default_timer as timer
from datetime import timedelta


def visit_dfs(tree, node, EA_max, LD_max):
    """
    Visita DFS unificata che, per ogni nodo v:
      - Se v è foglia, imposta EA_max[v] = min(L_v) e LD_max[v] = max(L_v)
      - Altrimenti, visita ricorsivamente i figli, raccoglie le coppie (EA_max, LD_max)
        e controlla la consistenza degli intervalli secondo lo pseudocodice.
      - Infine, calcola EA = max_{u in child(v)} EA_max[u] e LD = min_{u in child(v)} LD_max[u],
        e determina NextEA e NextLD in L_v (lista dei pesi associati a v) tramite funzioni di
        ricerca (binary_search e binary_search_leq).

    Se per qualche ragione il calcolo fallisce (NextEA o NextLD == -1), imposta EA_max[v] e
    LD_max[v] a infinito e ritorna False, altrimenti ritorna True.

    Parametri:
      - tree: grafo orientato rappresentante l'albero.
      - node: nodo corrente.
      - EA_max: dizionario per memorizzare i valori EA_max per ciascun nodo.
      - LD_max: dizionario per memorizzare i valori LD_max per ciascun nodo.

    Ritorna:
      - True se la connettività temporale risulta consistente lungo il ramo, False altrimenti.
    """
    # L_v: vettore dei pesi associato al nodo corrente
    weights = tree.nodes[node].get("weight", [])
    children = list(tree.successors(node))

    # Caso base: foglia
    if not children:
        EA_max[node] = min(weights)
        LD_max[node] = max(weights)
        return True

    # Inizializza il vettore D_v per raccogliere le coppie dai figli
    D_v = []
    for child in children:
        if not visit_dfs(tree, child, EA_max, LD_max):
            return False
        # Se uno dei figli ha valori infiniti, la connettività non è rispettata
        if EA_max[child] == float("inf") or LD_max[child] == float("inf"):
            return False
        D_v.append((EA_max[child], LD_max[child]))

    # Se sono presenti almeno due figli, eseguo il controllo di consistenza
    if len(D_v) > 1:
        # Trovo i due minimi rispetto a EA_max:
        # (min1, ld1) è la coppia con EA_min più piccolo e (min2, ld2) la seconda
        sorted_intervals = sorted(D_v, key=lambda x: x[0])
        minEA, ld1 = sorted_intervals[0]
        secondEA, ld2 = sorted_intervals[1]
        # Per ogni figlio, effettuo il controllo:
        for child in children:
            if EA_max[child] == minEA:
                # Se il figlio con EA_min ha un EA_max maggiore di ld2, la condizione non è soddisfatta
                if EA_max[child] > ld2:
                    return False
            else:
                # Gli altri devono rispettare EA_max[u] <= ld1
                if EA_max[child] > ld1:
                    return False
    # Se c'è un solo figlio non serve ulteriore controllo

    if node == 1:
        return True

    # Calcolo EA e LD aggregati dai figli
    EA = max(EA_max[child] for child in children)
    LD = min(LD_max[child] for child in children)

    # Calcola NextEA e NextLD usando la lista dei pesi L_v e le funzioni di ricerca
    # Si assume che 'binary_search' trovi il successore di EA in weights,
    # e 'binary_search_leq' trovi il predecessore (o il più vicino minore uguale) di LD.
    NextEA = binary_search(weights, EA) if weights else -1
    NextLD = binary_search_leq(weights, LD) if weights else -1

    if (NextEA == -1 or NextLD == -1) and node != 1:
        EA_max[node] = float("inf")
        LD_max[node] = float("inf")
        return False
    elif NextEA != -1 and NextLD != -1:
        EA_max[node] = NextEA
        LD_max[node] = NextLD
        return True


def algoritmo_unificato(T):
    """
    Algoritmo unificato per la verifica della connettività temporale di un albero.

    T: grafo orientato rappresentante l'albero.
    """
    n = T.number_of_nodes()
    EA_max = [0] * (n + 1)
    LD_max = [0] * (n + 1)
    if visit_dfs(T, 1, EA_max, LD_max):
        return "L'albero è temporalmente connesso"
    else:
        return "L'albero non è temporalmente connesso"


def create_tree_for_test():
    tree = nx.DiGraph()
    tree.add_node(1, weight=None)
    tree.add_node(2, weight=[1, 3])
    tree.add_node(3, weight=[2])
    tree.add_node(4, weight=[2, 6])
    tree.add_edges_from([(1, 2), (1, 3), (1, 4)])

    return tree


def create_test_2():
    tree = nx.DiGraph()
    tree.add_node(1, weight=None)
    tree.add_node(2, weight=[1, 3, 5])
    tree.add_node(3, weight=[2, 4])
    tree.add_node(4, weight=[1, 2, 6])
    tree.add_node(5, weight=[3, 5])
    tree.add_node(6, weight=[2, 4, 6, 8])

    tree.add_edges_from([(1, 2), (1, 3), (1, 4), (2, 5), (2, 6)])
    return tree


def tree_test():
    tree = nx.DiGraph()
    tree.add_node(1, weight=None)
    tree.add_node(2, weight=[1, 3, 5])
    tree.add_node(3, weight=[3, 5])
    tree.add_node(4, weight=[2, 4, 6, 8])
    tree.add_node(5, weight=[2, 4])
    tree.add_node(6, weight=[1, 3])
    tree.add_node(7, weight=[2, 6])
    tree.add_node(8, weight=[1, 4, 7])
    tree.add_node(9, weight=[1, 2, 6])

    tree.add_edges_from(
        [(1, 2), (1, 5), (1, 8), (2, 3), (2, 4), (5, 6), (7, 8), (7, 9)]
    )
    return tree


tree = tree_test()
start = timer()
print(algoritmo_unificato(tree))
end = timer()
print("Tempo di esecuzione:", timedelta(seconds=end - start))
