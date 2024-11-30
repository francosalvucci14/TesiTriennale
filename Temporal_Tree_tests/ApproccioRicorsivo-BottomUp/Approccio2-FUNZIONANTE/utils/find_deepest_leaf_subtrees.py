class Node:
    def __init__(self, value, weight=[]):
        self.value = value
        self.weight = weight
        self.left = None
        self.right = None


def find_deepest_leaf_with_max_weight(node, depth=0):
    if node is None:
        return -1, -1, None  # Nessuna foglia trovata
    
    # Nodo foglia
    if node.left is None and node.right is None:
        return depth, max(node.weight, default=-1), node
    
    # Ricorsione per sottoalbero sinistro
    left_depth, left_max_weight, left_node = find_deepest_leaf_with_max_weight(node.left, depth + 1)
    
    # Ricorsione per sottoalbero destro
    right_depth, right_max_weight, right_node = find_deepest_leaf_with_max_weight(node.right, depth + 1)
    
    # Determina la foglia migliore tra i due sottoalberi
    if left_depth > right_depth:
        return left_depth, left_max_weight, left_node
    elif left_depth < right_depth:
        return right_depth, right_max_weight, right_node
    else:  # Stessa profondità, confronta il peso massimo
        if left_max_weight >= right_max_weight:
            return left_depth, left_max_weight, left_node
        else:
            return right_depth, right_max_weight, right_node


# Wrapper per calcolare la foglia più profonda con peso massimo nei sottoalberi sinistro e destro
def find_deepest_leaves_in_subtrees(root):
    if root is None:
        return None, None  # Albero vuoto
    
    left_result = find_deepest_leaf_with_max_weight(root.left)
    right_result = find_deepest_leaf_with_max_weight(root.right)
    print(left_result, right_result)
    max_timestamp_sx = left_result[1]
    max_timestamp_dx = right_result[1]
    return left_result[2], right_result[2],max_timestamp_sx,max_timestamp_dx  # Ritorna i nodi delle foglie più profonde


# Creazione dell'albero
root = Node('A')
root.left = Node('B', weight=[1, 5])
root.right = Node('C', weight=[3])
root.left.left = Node('D', weight=[2])
root.left.right = Node('E', weight=[7])
root.right.left = Node('F', weight=[4])
root.right.right = Node('G', weight=[6])
root.left.left.left = Node('H', weight=[8])
root.left.left.right = Node('I', weight=[1,2,3])

# Calcolo
left_deepest, right_deepest,max_time_sx,max_time_dx = find_deepest_leaves_in_subtrees(root)

# Stampa dei risultati
print("Foglia più profonda nel sottoalbero sinistro:", left_deepest.value if left_deepest else None)
print("Timestamp massimo sinistro:", max_time_sx if left_deepest else None)
print("Foglia più profonda nel sottoalbero destro:", right_deepest.value if right_deepest else None)
print("Timestamp massimo destro:", max_time_dx if right_deepest else None)