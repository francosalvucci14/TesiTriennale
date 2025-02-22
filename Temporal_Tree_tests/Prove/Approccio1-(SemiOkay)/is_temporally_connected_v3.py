class TreeNode:
    def __init__(self, value, left=None, right=None, timestamps=[]):
        self.value = value
        self.left = left
        self.right = right
        self.timestamps = timestamps

def calculate_earliest_arrival(node):
    if not node:
        return float('inf')
    
    left_ea = calculate_earliest_arrival(node.left)
    right_ea = calculate_earliest_arrival(node.right)
    
    print(left_ea, right_ea)
    # Considera il minimo tra i timestamp uscenti dal nodo e i valori EA dei figli
    return min(node.timestamps, left_ea, right_ea)

# Creazione di un nodo
root = TreeNode('A', timestamps=[0])

# Aggiunta dei figli
root.left = TreeNode('B', timestamps=[1,2])
root.right = TreeNode('C', timestamps=[1])

# Aggiunta dei nipoti
root.left.left = TreeNode('D', timestamps=[0])
root.left.right = TreeNode('E', timestamps=[2])
# ... e così via

print(calculate_earliest_arrival(root))  # Output: 0