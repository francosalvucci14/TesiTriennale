def find_leftmost_leaf_with_earliest_timestamp(tree, current, parent=None, depth=0, earliest_timestamp=float('inf'), visited=None):
    if visited is None:
        visited = set()
    
    if current not in tree or not tree[current] or current in visited:
        return current, depth, earliest_timestamp
    
    visited.add(current)

    for neighbor, timestamps in tree[current]:
        if neighbor != parent:
            leaf, new_depth, new_earliest_timestamp = find_leftmost_leaf_with_earliest_timestamp(tree, neighbor, current, depth + 1, min(earliest_timestamp, timestamps[0]), visited)
            if new_depth > depth or (new_depth == depth and new_earliest_timestamp < earliest_timestamp):
                earliest_timestamp = new_earliest_timestamp
                current = leaf
                depth = new_depth

    return current, depth, earliest_timestamp

def find_rightmost_leaf_with_earliest_timestamp(tree, current, parent=None, depth=0, earliest_timestamp=float('inf'), visited=None):
    if visited is None:
        visited = set()
    
    if current not in tree or not tree[current] or current in visited:
        return current, depth, earliest_timestamp
    
    visited.add(current)

    for neighbor, timestamps in reversed(tree[current]):
        if neighbor != parent:
            leaf, new_depth, new_earliest_timestamp = find_rightmost_leaf_with_earliest_timestamp(tree, neighbor, current, depth + 1, min(earliest_timestamp, timestamps[0]), visited)
            if new_depth > depth or (new_depth == depth and new_earliest_timestamp < earliest_timestamp):
                earliest_timestamp = new_earliest_timestamp
                current = leaf
                depth = new_depth

    return current, depth, earliest_timestamp
# Example usage
tree_v2 = {
    0: [(1, [2, 6]), (2, [6])],
    1: [(0, [2, 6]), (3, [1, 2, 3, 4, 5])],
    2: [(0, [6]), (4, [6])],
    3: [(1, [1, 2, 3, 4, 5]), (5, [3]), (6, [4]), (7, [1, 2, 7])],
    4: [(2, [6])],
    5: [(3, [3])],
    6: [(3, [4])],
    7: [(3, [1, 2, 7])]
}

print(find_leftmost_leaf_with_earliest_timestamp(tree_v2, 0)) 
print(find_rightmost_leaf_with_earliest_timestamp(tree_v2, 0))