import networkx as nx
from utils.utils_function import *
from timeit import default_timer as timer
import time
from datetime import timedelta
import Algoritmo_Naive as naive
import Algoritmo_Naive_V2 as naive_v2
import Algoritmo_Unificato as unificato
import ALgoritmo_Unificato_V2 as unificato_v2
import matplotlib.pyplot as plt
import numpy as np

def test1():

    for i in range(1,12):
        print("\nTempi con N = ",10*i," nodi e L = ",25*i," timestamp")
        tree = generate_random_temporal_tree(10*i, 25*i, (1, 1500))
        tree2 = tree.to_undirected()
        #print(type(tree))
        #print_temporal_tree(tree)
        start = timer()
        print(f"\nAlbero temporalmente connesso? Algoritmo 1 : {unificato_v2.algoritmo_unificato(tree)}")
        #unificato.algoritmo3_networkx(tree)
        end = timer()
        print("Tempo di esecuzione:", timedelta(seconds=end - start))
        start2 = timer()
        print(f"\nAlbero temporalmente connesso? Algoritmo Naive : {naive_v2.is_temporally_connected(tree2)}")
        #naive.is_temporally_connected_v2(tree)
        end2 = timer()
        print("Tempo di esecuzione algoritmo naive:", timedelta(seconds=end2 - start2))
        originale = timedelta(seconds=end2 - start2)
        nuovo = timedelta(seconds=end - start)
        print("Miglioramento del : ",100*((originale-nuovo)/originale),"%")

def test_1mil(trials=10):
    tree = generate_random_temporal_tree(1000000, 3, (1, 15))
    start = timer()
    unificato.algoritmo3_networkx(tree)
    end = timer()
    print("Tempo di esecuzione:", timedelta(seconds=end - start))

def test3(trials=100):
    """
    Confronta i tempi medi di esecuzione di due algoritmi su un numero specificato di prove.

    Args:
        trials (int): Numero di prove.

    """
    total_time_algo3 = timedelta()
    total_time_is_connected = timedelta()
    
    for i in range(trials):
        tree = generate_random_temporal_tree(500, 120, (25, 350))
        tree2 = tree.to_undirected()
        #print_temporal_tree(tree)
        print(f"Trial {i + 1}/{trials}")
        # Misura il tempo di esecuzione di algoritmo3_networkx
        start = timer()
        risposta1 = unificato_v2.algoritmo_unificato(tree)
        end= timer()
        total_time_algo3 += timedelta(seconds=end - start)

        # Misura il tempo di esecuzione di is_temporally_connected_v2
        start2 = timer()
        risposta2 = naive_v2.naive_temporal_connectivity(tree2)
        end2= timer()
        total_time_is_connected += timedelta(seconds=end2 - start2)
    #avg_time_algo3 = total_time_algo3 / trials
    #avg_time_is_connected = total_time_is_connected / trials
    avg_time_algo3 = timedelta(seconds=total_time_algo3.total_seconds() / trials)
    avg_time_is_connected = timedelta(seconds=total_time_is_connected.total_seconds() / trials)
    
    print("Risultati : ")
    print(f"Algoritmo 1: Tempo medio di esecuzione su {trials} prove: {avg_time_algo3}")
    print(f"Algoritmo Naive: Tempo medio di esecuzione su {trials} prove: {avg_time_is_connected}")

    #Algoritmo 1: Tempo medio di esecuzione su 100 prove: 0:00:00.001651
    #Algoritmo Naive: Tempo medio di esecuzione su 100 prove: 0:00:27.620086

def test3_plot(trials=100, node_sizes=[10,50,100,200,500,1000]):
    """
    Confronta i tempi medi di esecuzione di due algoritmi su un numero specificato di prove
    per varie dimensioni del problema (numero di nodi) e produce un grafico.

    Args:
        trials (int): Numero di prove per ogni dimensione del problema.
        node_sizes (list of int): Lista del numero di nodi da testare.
    """
    avg_times_algo3 = []
    avg_times_naive = []

    for num_nodes in node_sizes:
        total_time_algo3 = timedelta()
        total_time_is_connected = timedelta()

        print("\nNumero di nodi: ", num_nodes)

        for _ in range(trials):
            timestamp_range = (1, num_nodes*2+100)  # Intervallo casuale di timestamp
            tree = generate_random_temporal_tree(num_nodes, num_nodes**2, timestamp_range)
            #tree = genera_albero_temporale(num_nodes, num_nodes*10, timestamp_range)

            print("Trials : {}/{}".format(_+1,trials))
            tree2 = tree.to_undirected()

            # Misura il tempo di esecuzione di algoritmo3_networkx
            start = timer()
            risposta1 = unificato_v2.algoritmo_unificato(tree)
            end = timer()
            total_time_algo3 += timedelta(seconds=end - start)

            # Misura il tempo di esecuzione di is_temporally_connected
            start2 = timer()
            risposta2 = naive_v2.naive_temporal_connectivity(tree2)
            end2 = timer()
            total_time_is_connected += timedelta(seconds=end2 - start2)

        # Calcola i tempi medi
        avg_time_algo3 = total_time_algo3.total_seconds() / trials
        avg_time_is_connected = total_time_is_connected.total_seconds() / trials

        avg_times_algo3.append(avg_time_algo3)
        avg_times_naive.append(avg_time_is_connected)

    # Plot dei risultati
    x = np.arange(len(node_sizes))

    plt.figure(figsize=(10, 6))
    plt.plot(x, avg_times_algo3,marker='o',linewidth=3.5, color='red', label='Algoritmo Unificato')
    plt.plot(x, avg_times_naive,marker='o',linewidth=3.5, color='blue', label='Algoritmo Naive')
    #plt.yscale('log')
    plt.xticks(ticks=x, labels=[f"{n} nodi" for n in node_sizes])
    plt.xlabel("Numero di nodi")
    plt.ylabel("Tempo medio di esecuzione (secondi)")
    plt.title("Confronto dei tempi medi di esecuzione")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    #plt.show()
    plt.savefig("Test_n^2_2000n.png")


def test2(intervals):
    for i in range(5):
        tree = generate_random_temporal_tree(5,random.randint(1,5),random.choice(intervals))
        tree2 = tree.to_undirected()
        print_temporal_tree(tree)
        print(f"Algoritmo 1 : {unificato.algoritmo3_networkx(tree)}")
        print(f"Algoritmo Naive : {naive.is_temporally_connected(tree2)}")
        print("-----------------")

def test4():
    num_true=0
    for i in range(15000):
        #N = random.randint(10,150)
        #L = random.randint(5,80)
        tree = generate_random_temporal_tree(50,20,(1,200))
        #print("Albero generato : N={}, L={}".format(N,L))
        print(f"Test {i+1}/15000")
        if unificato.algoritmo3_networkx(tree):
            num_true+=1
    print("Numero di alberi temporaneamente connessi : ",num_true)
    print("Percentuale di alberi temporaneamente connessi : ",(num_true/15000)*100,"%")



if __name__ == "__main__":
    # tree = create_tree_with_networkx()
    # print(algoritmo(tree))
    #calculate_average_time()
    #test1()
    #test3()
    #test_1mil()
    test3_plot()
    #test2([(1, 15), (3, 9), (5, 40), (2, 18)])
    #test4()