import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def draw_tree_with_triangles(root, children, ea_values, ld_values, edge_labels):
    G = nx.Graph()
    pos = {}
    
    # Posizione della radice
    pos[root] = (0, 1)
    G.add_node(root)
    
    num_children = len(children)
    x_positions = np.linspace(-0.5, 0.5, num_children)  # Riduzione della lunghezza degli archi
    
    plt.figure(figsize=(3, 2))
    
    edge_label_dict = {}
    
    for i, child in enumerate(children):
        pos[child] = (x_positions[i], 0.2)
        G.add_edge(root, child)
        edge_label_dict[(root, child)] = f'$L_{{{child}}}$'  # Etichetta in LaTeX
    
    nx.draw(G, pos, with_labels=True, node_size=800, node_color="lightblue", edge_color="black", font_size=12)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_label_dict, font_size=12, font_color="black")
    
    # Disegno dei triangoli per i sottoalberi
    for i, child in enumerate(children):
        x, y = pos[child]
        width = 0.2#np.random.uniform(0.1, 0.4)  # Aumento delle dimensioni dei triangoli
        height = 0.2#np.random.uniform(0.4, 0.6)
        triangle = plt.Polygon([(x - width/2, y - height), (x + width/2, y - height), (x, y)], color='gray', alpha=0.5)
        plt.gca().add_patch(triangle)
        
        # Aggiunta dei valori EA e LD
        #plt.text(x, y - 0.1, f'EA: {ea_values[i]}', color='red', fontsize=10, ha='center', fontweight='bold')
        #plt.text(x, y - 0.2, f'LD: {ld_values[i]}', color='blue', fontsize=10, ha='center', fontweight='bold')
    
    plt.xlim(-0.7, 0.7)
    plt.ylim(-0.2, 1.2)
    plt.axis('off')
    plt.show()
    #plt.savefig("tree_with_triangles.png", dpi=300)

# Esempio di utilizzo
draw_tree_with_triangles("v", ["u1", "u2", "u3", "u4"], [10, 20, 30, 40], [5, 15, 25, 35], ["L1", "L2", "L3", "L4"])

