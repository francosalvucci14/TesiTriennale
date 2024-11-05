from collections import defaultdict

def is_temporally_connected(graph):
    dp = defaultdict(set)

    def dfs(node):
        if node not in graph:
            return True

        for neighbor, weights in graph[node].items():
            for weight in weights:
                if dfs(neighbor):
                    dp[node].add(True)
                    return True
        # Aggiungiamo questa riga per assicurarci che il nodo corrente sia sempre raggiungibile
        dp[node].add(True)
        return False

    root = list(graph.keys())[0]
    dfs(root)

    # Stampa la tabella DP per debugging
    print(dp)

    return all(dp[node] for node in graph)

# Esempio di utilizzo
tree_temporally_connected = {
    "A": {"B": [1, 2, 3], "C": [2, 4]},
    "B": {"D": [3, 5], "E": [4, 6]},
    "C": {"F": [5, 7]},
    "D": {},
    "E": {},
    "F": {},
}

result = is_temporally_connected(tree_temporally_connected)
print(result)