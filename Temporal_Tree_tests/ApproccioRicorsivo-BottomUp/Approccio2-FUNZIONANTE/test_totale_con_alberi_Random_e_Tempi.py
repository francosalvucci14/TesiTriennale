import networkx as nx
from utils.utils_function import *
from timeit import default_timer as timer
import time
from datetime import timedelta
import Algoritmo_Naive as naive
import Algoritmo_Unificato as unificato

def test1():
    # tree = generate_random_temporal_tree()
    # tree = create_tree_with_networkx()
    # tree = generate_random_temporal_tree(500, 250, (1, 1500))
    # start = timer()
    # print(f"\nAlbero temporalmente connesso? Algoritmo 1 : {unificato.algoritmo3_networkx(tree)}")
    # end = timer()
    # print("Tempo di esecuzione:", timedelta(seconds=end - start))
    # start = timer()
    # print(f"\nAlbero temporalmente connesso? Algoritmo Naive : {naive.is_temporally_connected(tree)}")
    # end = timer()
    # print("Tempo di esecuzione algoritmo naive:", timedelta(seconds=end - start))

    for i in range(1,21):
        print("\nTempi con N = ",10*i," nodi e L = ",25*i," timestamp")
        tree = generate_random_temporal_tree(10*i, 25*i, (1, 1500))
        tree2 = tree.to_undirected()
        #print(type(tree))
        #print_temporal_tree(tree)
        start = timer()
        print(f"\nAlbero temporalmente connesso? Algoritmo 1 : {unificato.algoritmo3_networkx(tree)}")
        #unificato.algoritmo3_networkx(tree)
        end = timer()
        print("Tempo di esecuzione:", timedelta(seconds=end - start))
        start2 = timer()
        print(f"\nAlbero temporalmente connesso? Algoritmo Naive : {naive.is_temporally_connected(tree2)}")
        #naive.is_temporally_connected_v2(tree)
        end2 = timer()
        print("Tempo di esecuzione algoritmo naive:", timedelta(seconds=end2 - start2))
        originale = timedelta(seconds=end2 - start2)
        nuovo = timedelta(seconds=end - start)
        print("Miglioramento del : ",100*((originale-nuovo)/originale),"%")


def test2(trials=10000):
    """
    Confronta i tempi medi di esecuzione di due algoritmi su un numero specificato di prove.

    Args:
        trials (int): Numero di prove.

    Returns:
        dict: Tempi medi di esecuzione per i due algoritmi.
    """
    total_time_algo3 = timedelta()
    total_time_is_connected = timedelta()
    
    num_t_1,num_t_2 = 0,0
    num_f_1,num_f_2 = 0,0
    for i in range(trials):
        tree = generate_random_temporal_tree()
        tree2 = tree.to_undirected()
        #print_temporal_tree(tree)
        print("TEST : ", i)
        # Misura il tempo di esecuzione di algoritmo3_networkx
        start = timer()
        risposta1 = unificato.algoritmo3_networkx(tree)
        end= timer()
        total_time_algo3 += timedelta(seconds=end - start)

        # Misura il tempo di esecuzione di is_temporally_connected_v2
        start2 = timer()
        risposta2 = naive.is_temporally_connected(tree2)
        end2= timer()
        total_time_is_connected += timedelta(seconds=end2 - start2)
        print("Tempo di esecuzione algoritmo 1 : ",total_time_algo3)
        print("Tempo di esecuzione algoritmo 2 : ",total_time_is_connected)
    avg_time_algo3 = timedelta(seconds=total_time_algo3 / trials)
    avg_time_is_connected = timedelta(seconds=total_time_is_connected / trials)

    print(f"Algoritmo 1: Tempo medio di esecuzione su {trials} prove: {avg_time_algo3}")
    print(f"Algoritmo Naive: Tempo medio di esecuzione su {trials} prove: {avg_time_is_connected}")

    #print("------------------------------------------------")
    #print(f"Numero di alberi temporaneamente connessi con algoritmo 1: {num_t_1}")
    #print(f"Numero di alberi temporaneamente non connessi con algoritmo 1: {num_f_1}")
    #print(f"Numero di alberi temporaneamente connessi con algoritmo Naive: {num_t_2}")
    #print(f"Numero di alberi temporaneamente non connessi con algoritmo 1Naive: {num_f_2}")


def create_tree_with_networkx():
    # Crea un grafo diretto
    tree = nx.DiGraph()

    # # # Aggiungi i nodi e i pesi degli archi entranti
    
    tree.add_node("A", weight=None)  # Radice senza arco entrante
    tree.add_node("B", weight=[3,4,5])
    tree.add_node("C", weight=[2,4])
    tree.add_node("D", weight=[1, 2, 3, 4, 5, 6])
    tree.add_node("E", weight=[2,3,4,5,6])
    tree.add_node("F", weight=[2,3])
    tree.add_node("G", weight=[1,2,3,4,5,6])
    tree.add_node("H", weight=[2,6])
    tree.add_node("I", weight=[1,3])
    tree.add_node("J", weight=[1,3])

    # Aggiungi gli archi (parent -> child)
    tree.add_edges_from([
        ("A", "B"),
        ("A", "E"),
        ("A", "F"),
        ("B", "C"),
        ("B", "D"),
        ("C", "G"),
        ("C", "H"),
        ("D", "J"),
        ("F", "I")
    ])
    return tree

if __name__ == "__main__":
    # tree = create_tree_with_networkx()
    # print(algoritmo(tree))
    #calculate_average_time()
    #test1()
    #test2()
    tree = generate_random_temporal_tree(100,5,(1,50))
    print_temporal_tree(tree)
    #print(naive.is_temporally_connected_v2(create_tree_with_networkx()))