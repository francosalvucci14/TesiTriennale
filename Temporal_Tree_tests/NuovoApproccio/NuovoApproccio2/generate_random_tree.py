import random
from test_algoritmo2 import algoritmo

class Node:
    def __init__(self, value, weight=[]):
        self.value = value
        self.weight = weight
        self.left = None
        self.right = None

def generate_random_tree(values, weight_range=(1, 10), max_weights=3):
    """
    Genera un albero binario casuale.
    
    :param values: Lista dei valori da usare per i nodi.
    :param weight_range: Tuple (min_weight, max_weight) per i pesi.
    :param max_weights: Numero massimo di pesi per arco.
    :return: Radice dell'albero binario generato.
    """
    if not values:
        return None

    # Crea il nodo radice
    root = Node(values[0], generate_random_weights(weight_range, max_weights))

    # Usa una coda per costruire l'albero
    queue = [root]
    index = 1

    while index < len(values):
        current = queue.pop(0)

        # Crea il figlio sinistro se ci sono valori disponibili
        if index < len(values):
            left_node = Node(values[index], generate_random_weights(weight_range, max_weights))
            current.left = left_node
            queue.append(left_node)
            index += 1

        # Crea il figlio destro se ci sono valori disponibili
        if index < len(values):
            right_node = Node(values[index], generate_random_weights(weight_range, max_weights))
            current.right = right_node
            queue.append(right_node)
            index += 1

    return root

def generate_random_weights(weight_range, max_weights):
    """
    Genera una lista ordinata di pesi casuali.
    
    :param weight_range: Tuple (min_weight, max_weight) per i pesi.
    :param max_weights: Numero massimo di pesi.
    :return: Lista ordinata di pesi casuali.
    """
    num_weights = random.randint(1, max_weights)  # Numero casuale di pesi
    weights = [int(random.uniform(*weight_range)) for _ in range(num_weights)]
    return sorted(weights)

def print_tree(node, level=0):
    """
    Stampa l'albero in modo leggibile.
    """
    if node is not None:
        print_tree(node.right, level + 1)
        print("   " * level + f"({node.value}, weights={node.weight})")
        print_tree(node.left, level + 1)

# Lista dei valori per i nodi
values = [10, 20, 30, 40, 50]

# Genera un albero binario casuale
random_tree = generate_random_tree(values, weight_range=(2,15), max_weights=4)

# Stampa l'albero
print("Albero generato:")
print_tree(random_tree)
print(algoritmo(random_tree))