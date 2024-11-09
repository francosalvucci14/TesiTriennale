class Node:
    def __init__(self, value):
        self.value = value
        self.edges = {}  # Adiacenza temporale: {nodo_destinazione: [tempi]}

def is_temporally_connected(node, parent_time=None):
    # Se il nodo ha già una condizione temporale di "risalita", la dobbiamo verificare.
    for neighbor, times in node.edges.items():
        for time in times:
            # Controllo della discesa: tempo sul arco deve essere maggiore del tempo del nodo corrente (ordinamento crescente)
            if parent_time is not None and time >= parent_time:
                return False  # Se non c'è ordinamento crescente, ritorniamo False
            # Chiamata ricorsiva per esplorare i figli (risalita)
            if not is_temporally_connected(neighbor, max(times)):
                return False  # Se uno dei sottoalberi non è connesso temporalmente, ritorniamo False
    return True  # Se tutte le condizioni sono rispettate

# Creiamo un esempio di albero e vediamo se è temporalmente connesso
nodeA = Node('A')
nodeB = Node('B')
nodeC = Node('C')
nodeD = Node('D')
nodeE = Node('E')

nodeA.edges = {nodeB: [1, 2], nodeC: [1,3]}
nodeB.edges = {nodeD: [2]}
nodeC.edges = {nodeE: [3]}
nodeD.edges = {}
nodeE.edges = {}

# Verifica se l'albero è temporalmente connesso
print(is_temporally_connected(nodeA))  # Questo restituirà True o False in base alla struttura dell'albero
