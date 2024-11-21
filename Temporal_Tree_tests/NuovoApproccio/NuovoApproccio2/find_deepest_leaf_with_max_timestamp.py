class Node:
    def __init__(self, data, left=None, right=None, weight=0):
        self.data = data
        self.left = left
        self.right = right
        self.weight = weight

def find_deepest_leaf_with_max_weight(node, depth=0, accumulated_weight=0):
    if node is None:
        return -1, -1, None  # No leaf found
    if node.left is None and node.right is None:  # Leaf node
        return depth, accumulated_weight, node
    
    left_depth, left_weight, left_node = find_deepest_leaf_with_max_weight(node.left, depth + 1, node.left.weight)
    right_depth, right_weight, right_node = find_deepest_leaf_with_max_weight(node.right, depth + 1, node.right.weight)

    if left_depth > right_depth:
        return left_depth, left_weight, left_node
    elif left_depth < right_depth:
        return right_depth, right_weight, right_node
    else:
        return max((left_depth, left_weight, left_node), (right_depth, right_weight, right_node), key=lambda x: x[1])

def find_deepest_leaf_with_max_weight_akaEAmax(node, depth=0, accumulated_weight=0):
    if node is None:
        return -1, -1, None  # No leaf found
    if node.left is None and node.right is None:  # Leaf node
        return depth, accumulated_weight, node
    
    left_depth, left_weight, left_node = find_deepest_leaf_with_max_weight_akaEAmax(node.left, depth + 1, accumulated_weight + node.left.weight)
    right_depth, right_weight, right_node = find_deepest_leaf_with_max_weight_akaEAmax(node.right, depth + 1, accumulated_weight + node.right.weight)

    if left_depth > right_depth:
        return left_depth, left_weight, left_node
    elif left_depth < right_depth:
        return right_depth, right_weight, right_node
    else:
        return max((left_depth, left_weight, left_node), (right_depth, right_weight, right_node), key=lambda x: x[1])


# Esempio di utilizzo
# Creazione di un albero binario di esempio
root = Node(1)
root.left = Node(2, weight=5)
root.right = Node(3, weight=3)
root.left.left = Node(4, weight=2)
root.left.right = Node(5, weight=7)

# Trova la foglia più profonda con peso massimo
depth, max_weight,node = find_deepest_leaf_with_max_weight(root)

_,ea,node = find_deepest_leaf_with_max_weight_akaEAmax(root)

if depth != -1:
    print("Profondità della foglia:", depth)
    print("Peso massimo della foglia:", max_weight)
    print("Foglia più profonda:", node.data)
else:
    print("L'albero è vuoto.")

print(f"EAmax: {ea}, node: {node.data}")