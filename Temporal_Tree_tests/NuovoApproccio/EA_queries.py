from bisect import bisect_left

def EA_query_function(tree, u, v, t_start):
    """
    Calcola il tempo di arrivo più precoce (EA) dal nodo u al nodo v con partenza non prima di t_start.
    
    Args:
        tree: struttura dati che rappresenta l'albero temporale.
        u: nodo di partenza.
        v: nodo di destinazione (radice).
        t_start: tempo minimo di partenza.
    
    Returns:
        Il tempo di arrivo più precoce a v o float("inf") se nessun percorso è possibile.
    """
    current_node = u
    current_time = t_start
    
    while current_node != v:
        # Recupera l'arco (current_node -> parent) e i relativi timestamp
        neighbors = tree.get(current_node, [])
        parent = None
        times = []

        for neighbor, timestamps in neighbors:
            if neighbor == v or neighbor == "parent":  # Identifica il nodo genitore
                parent = neighbor
                times = timestamps
                break

        if not parent or not times:
            return float("inf")  # Non c'è percorso verso la radice
        
        # Trova il primo timestamp >= current_time
        idx = bisect_left(times, current_time)
        if idx == len(times):
            return float("inf")  # Nessun timestamp valido trovato
        
        # Aggiorna il tempo corrente e il nodo corrente
        current_time = times[idx]
        current_node = parent

    return current_time

def calculate_earliest_arrivals(tree, left_leaf, right_leaf, root, EA_query_function):
    """
    Calcola gli Earliest Arrival (EA) per i percorsi dalle foglie sinistra e destra alla radice.
    
    Args:
        tree: struttura dati che rappresenta l'albero temporale.
        left_leaf: nodo foglia più profondo tutto a sinistra.
        right_leaf: nodo foglia più profondo tutto a destra.
        root: nodo radice dell'albero.
        EA_query_function: funzione che implementa la query EA dalla struttura del paper.
    
    Returns:
        - Un dizionario contenente EA_sx e EA_dx se validi, oppure False se almeno uno è infinito.
    """
    # Calcola EA per il percorso dalla foglia sinistra alla radice
    EA_sx = EA_query_function(tree, left_leaf, root, -float("inf"))
    
    # Calcola EA per il percorso dalla foglia destra alla radice
    EA_dx = EA_query_function(tree, right_leaf, root, -float("inf"))
    
    # Controlla se uno dei risultati è infinito
    if EA_sx == float("inf") or EA_dx == float("inf"):
        return False  # Non c'è percorso temporalmente connesso
    
    # Salva le informazioni nella radice
    root_info = {
        "EA_sx": EA_sx,
        "EA_dx": EA_dx
    }
    return root_info
