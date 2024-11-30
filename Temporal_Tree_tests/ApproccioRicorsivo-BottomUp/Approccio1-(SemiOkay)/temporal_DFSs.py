from bisect import bisect_left

def temporal_dfs(tree, current, visited, time, is_valid_edge):
    """
    Esegue una DFS temporale rispettando i vincoli temporali con ricerca binaria.
    
    Args:
        tree: struttura dati che rappresenta l'albero temporale.
        current: nodo attuale.
        visited: insieme dei nodi visitati.
        time: tempo corrente della DFS.
        is_valid_edge: funzione che verifica la validità di un arco rispetto al tempo.
    
    Returns:
        True se la DFS visita tutti i nodi del sottoalbero, False altrimenti.
    """
    visited.add(current)
    
    for neighbor, times in tree.get(current, []):
        if neighbor not in visited:
            # Trova il primo timestamp valido >= tempo corrente
            idx = bisect_left(times, time)
            if idx < len(times) and is_valid_edge(times[idx], time):
                if not temporal_dfs(tree, neighbor, visited, times[idx], is_valid_edge):
                    return False
            else:
                return False  # Nessun timestamp valido, esci immediatamente

    return True

def validate_temporal_subtrees(tree, root, EA_sx, EA_dx):
    """
    Valida i sottoalberi tramite DFS temporale con vincoli temporali.
    
    Args:
        tree: struttura dati che rappresenta l'albero temporale.
        root: nodo radice.
        EA_sx: Earliest Arrival dal sottoalbero sinistro.
        EA_dx: Earliest Arrival dal sottoalbero destro.
    
    Returns:
        True se entrambi i sottoalberi sono validi, False altrimenti.
    """
    left_subtree_root = tree[root][0][0]  # Primo figlio (sottoalbero sinistro)
    right_subtree_root = tree[root][1][0]  # Secondo figlio (sottoalbero destro)
    
    # DFS sul sottoalbero sinistro
    visited_left = set()
    is_valid_left = temporal_dfs(
        tree, left_subtree_root, visited_left, EA_sx,
        lambda t, current_time: t >= current_time
    )
    
    # DFS sul sottoalbero destro
    visited_right = set()
    is_valid_right = temporal_dfs(
        tree, right_subtree_root, visited_right, EA_dx,
        lambda t, current_time: t >= current_time
    )
    
    # Controlla se entrambe le DFS hanno visitato tutti i nodi
    return is_valid_left and is_valid_right
