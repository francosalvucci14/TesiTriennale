# Esempio di albero
class Node:
    def __init__(self, value, weight=[]):
        self.value = value
        self.weight = weight
        self.left = None
        self.right = None

def find_leaf_with_max_weight(node):
    if node is None:
        return -1, None  # Nessuna foglia trovata
    
    # Nodo foglia
    if node.left is None and node.right is None:
        return max(node.weight, default=-1), node
    
    # Ricorsione per sottoalbero sinistro
    left_max_weight, left_node = find_leaf_with_max_weight(node.left)
    
    # Ricorsione per sottoalbero destro
    right_max_weight, right_node = find_leaf_with_max_weight(node.right)
    
    # Determina la foglia con il massimo peso
    if left_max_weight >= right_max_weight:
        return left_max_weight, left_node
    else:
        return right_max_weight, right_node


# Wrapper per calcolare le foglie con il timestamp massimo nei sottoalberi sinistro e destro
def find_leaves_with_max_weights_in_subtrees(root):
    if root is None:
        return None, None, -1, -1  # Albero vuoto
    
    # Trova la foglia con il massimo timestamp nel sottoalbero sinistro
    max_weight_sx, left_leaf = find_leaf_with_max_weight(root.left)
    
    # Trova la foglia con il massimo timestamp nel sottoalbero destro
    max_weight_dx, right_leaf = find_leaf_with_max_weight(root.right)
    
    return left_leaf, right_leaf, max_weight_sx, max_weight_dx


root = Node('A')
root.left = Node('B', weight=[1, 9])
root.right = Node('C', weight=[3])
root.left.left = Node('D', weight=[2])
root.left.right = Node('E', weight=[7])
root.right.left = Node('F', weight=[4])
root.right.right = Node('G', weight=[6])
root.left.left.left = Node('H', weight=[3])
root.left.left.right = Node('I', weight=[1, 2, 3])

# Trova le foglie con timestamp massimo
left_leaf, right_leaf, max_weight_sx, max_weight_dx = find_leaves_with_max_weights_in_subtrees(root)

# Stampa dei risultati
print(f"Foglia con timestamp massimo nel sottoalbero sinistro: {left_leaf.value if left_leaf else None}, Timestamp: {max_weight_sx}")
print(f"Foglia con timestamp massimo nel sottoalbero destro: {right_leaf.value if right_leaf else None}, Timestamp: {max_weight_dx}")
