import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation, PillowWriter
from utils.utils_function import *

def dfs_EA_tmax_with_steps(tree, root, steps, pos):
    if root is None:
        return {}

    children = list(tree.successors(root))
    weight = tree.nodes[root]["weight"]

    # Caso base: foglia
    if not children:
        ea, t_max = weight[0], weight[-1]
        steps.append({
            "highlight": {"nodes": [root]},
            "message": f"Foglia {root}: EA={ea}, Tmax={t_max}",
            "results": {root: (ea, t_max)},
        })
        return {root: (ea, t_max)}

    sottoalberi = {}
    ea_tmax = []

    # Calcolo ricorsivo per ogni figlio
    for child in children:
        sottoalberi.update(dfs_EA_tmax_with_steps(tree, child, steps, pos))
        ea, t_max = sottoalberi[child]
        ea_tmax.append((ea, t_max))

    # Step 1: Ordina per Tmax
    ea_tmax.sort(key=lambda x: x[1])
    if len(ea_tmax) > 1:
        if not (ea_tmax[0][0] <= ea_tmax[1][1]):
            steps.append({
                "highlight": {"nodes": [root] + children},
                "message": f"Errore al nodo {root}: EA={ea_tmax[0][0]} > Tmax={ea_tmax[1][1]}",
                "results": {root: (float("inf"), float("inf"))},
            })
            return {root: (float("inf"), float("inf"))}
        # Step 2 e 3: Controlli di consistenza
        for i in range(1,len(ea_tmax)):
            if ea_tmax[i][0] > ea_tmax[0][1]:
                steps.append({
                    "highlight": {"nodes": [root] + children},
                    "message": f"Errore al nodo {root}: EA={ea_tmax[i][0]} > Tmax={ea_tmax[0][1]}",
                    "results": {root: (float("inf"), float("inf"))},
                })
                return {root: (float("inf"), float("inf"))}

    # Calcola EA e Tmax per il nodo corrente
    EA = max(ea_tmax, key=lambda x: x[0])[0]
    t_max_visita = min(ea_tmax, key=lambda x: x[1])[1]

    k = binary_search(weight, EA) if weight else 0
    nextTimeMax = binary_search_leq(weight, t_max_visita) if weight else 0

    if (k == -1 or nextTimeMax == -1) and root != "A":
        steps.append({
            "highlight": {"nodes": [root] + children},
            "message": f"Errore al nodo {root}: valori non validi.",
            "results": {root: (float("inf"), float("inf"))},
        })
        return {root: (float("inf"), float("inf"))}

    steps.append({
        "highlight": {"nodes": [root] + children},
        "message": f"Nodo {root}: EA={k}, Tmax={nextTimeMax}",
        "results": {root: (k, nextTimeMax)},
    })

    sottoalberi[root] = (k, nextTimeMax)
    return sottoalberi

# Creazione dell'albero
def create_tree_for_test():
    tree = nx.DiGraph()
    tree.add_node("A", weight=None)
    tree.add_node("B", weight=[2,6])
    tree.add_node("C", weight=[6])
    tree.add_node("D", weight=[1,2,3,4,5,6])
    tree.add_node("E", weight=[6])
    tree.add_node("F", weight=[1,6])
    tree.add_node("G", weight=[1,6])
    tree.add_node("H", weight=[1,6])
    tree.add_node("I", weight=[1,6])
    tree.add_edges_from([("A", "B"), ("A", "C"),("A","F"), ("B", "D"),("B","G"),("B","H"),("B","I"),("C","E")])
    return tree

def draw_tree_step(tree, pos, step):
    nx.draw(tree, pos, with_labels=True, node_color="lightgrey", node_size=2000)
    
    leaves = [node for node in tree.nodes if len(list(tree.successors(node))) == 0]
    #print(leaves)
    # Disegna EA e Tmax
    for node, (ea, t_max) in step["results"].items():
        if node == "A" : 
            if ea == float("inf") or t_max == float("inf"):
                x, y = pos[node]
                #plt.text(x+2, y + 0.5, f"EA_sx={ea}", color="red", fontsize=10, ha="right")
                #plt.text(x+2, y + 0.5, f"Tmax_sx={t_max}", color="blue", fontsize=10, ha="left")
                plt.text(x, y + 5.0, f"L'albero NON è temporalmente connesso", color="red", fontsize=10, ha="center")
            else:
                x, y = pos[node]
                plt.text(x, y + 5.0, f"L'albero è temporalmente connesso", color="red", fontsize=10, ha="center")  
        else:
            if node in leaves: 
                x, y = pos[node]
                plt.text(x, y - 0.1, f"EA={ea}", color="red", fontsize=10, ha="right")
                plt.text(x, y - 0.1, f"Tmax={t_max}", color="blue", fontsize=10, ha="left")
            else:
                x, y = pos[node]
                plt.text(x, y + 5.5, f"EA={ea}", color="red", fontsize=10, ha="right")
                plt.text(x, y + 5.5, f"Tmax={t_max}", color="blue", fontsize=10, ha="left")

    # Evidenzia nodi
    nx.draw_networkx_nodes(tree, pos, nodelist=step["highlight"]["nodes"], node_color="orange")
    nx.draw_networkx_edge_labels(tree, pos, edge_labels={(u, v): f"{tree.nodes[v]['weight']}" for u, v in tree.edges()})
    # Mostra il messaggio
    plt.title(step["message"])

# def draw_tree_standard(tree):
#     # Usa il layout Graphviz per posizionare i nodi
#     pos = nx.nx_agraph.graphviz_layout(tree, prog="dot")

#     # Disegna l'albero
#     plt.figure(figsize=(10, 8))
#     nx.draw(tree, pos, with_labels=True, node_color="lightgrey", node_size=2000, edge_color="black", font_size=12, font_weight="bold")
    
#     # Aggiungi il titolo
#     plt.title("Albero con Radice in Alto", fontsize=14)
#     plt.show()

if __name__ == "__main__":
    #tree = create_tree_for_test()
    tree = generate_random_temporal_tree(30, 6, (1, 10))
    #draw_tree_standard(tree)
    pos = nx.nx_agraph.graphviz_layout(tree, prog="dot")
    steps = []

    # Esegui DFS con registrazione dei passi
    risultati = dfs_EA_tmax_with_steps(tree, "A", steps, pos)

    # Salva animazione
    fig = plt.figure(figsize=(20, 18))
    ani = FuncAnimation(fig, lambda i: draw_tree_step(tree, pos, steps[i]), frames=len(steps), repeat=False)
    ani.save("dfs_temporal_tree.gif", writer=PillowWriter(fps=1))

    # Mostra l'animazione
    plt.show()
