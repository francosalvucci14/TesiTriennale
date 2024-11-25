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
    
    if node.left is not None:
        left_depth, left_weight, left_node = find_deepest_leaf_with_max_weight(node.left, depth + 1, max(node.left.weight) )
    else:
        left_depth, left_weight, left_node = -1, -1, None
    if node.right is not None:
        right_depth, right_weight, right_node = find_deepest_leaf_with_max_weight(node.right, depth + 1, max(node.right.weight))
    else:
        right_depth, right_weight, right_node = -1, -1, None

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
    
    left_depth, left_weight, left_node = find_deepest_leaf_with_max_weight_akaEAmax(node.left, depth + 1, accumulated_weight + max(node.left.weight))
    right_depth, right_weight, right_node = find_deepest_leaf_with_max_weight_akaEAmax(node.right, depth + 1, accumulated_weight + max(node.right.weight))
    
    if left_depth > right_depth:
        return left_depth, left_weight, left_node
    elif left_depth < right_depth:
        return right_depth, right_weight, right_node
    else:
        return max((left_depth, left_weight, left_node), (right_depth, right_weight, right_node), key=lambda x: x[1])


# Esempio di utilizzo
# Creazione di un albero binario di esempio
root = Node('A')
root.left = Node('B', weight=[1,5])
root.right = Node('C', weight=[3])
root.left.left = Node('D', weight=[2])
root.left.right = Node('E', weight=[7])
root.right.left = Node('F', weight=[4])
root.right.right = Node('G', weight=[6])
root.left.left.left = Node('H', weight=[8])


# Trova la foglia più profonda con peso massimo
depth, max_weight,node = find_deepest_leaf_with_max_weight(root)

#_,ea,node = find_deepest_leaf_with_max_weight_akaEAmax(root)

if depth != -1:
    print("Profondità della foglia:", depth)
    print("Peso massimo della foglia:", max_weight)
    print("Foglia più profonda:", node.data)
else:
    print("L'albero è vuoto.")

#print(f"EAmax: {ea}, node: {node.data}")