# Presentazione Tesi
- Introduzione
- Algoritmo
- Risultati
- Conclusione
---
## Second slide

BLA BLA BLA BLA BLA lorem 
> [!IMPORTANT]
> duce

---

```python [2|3-10|12-35]
def visita-DFS(tree, root):
    # Caso base: nodo nullo
    if root is None:
        return {}

    # Ottieni i figli del nodo corrente
    children = list(tree.successors(root))
    weight = tree.nodes[root]["weight"]

    # Caso base: foglia
    if not children:
        return {root: (weight[0], weight[-1])}

    # Variabili per raccogliere i valori EA e Tmax per ogni sottoalbero
    sottoalberi = {}
    ea_tmax = []

    # Calcolo ricorsivo per ogni figlio
    for child in children:
        sottoalberi.update(visita-DFS(tree, child))
        ea, t_max = sottoalberi[child]
        ea_tmax.append((ea, t_max))

    # Step 1: Ordina per Tmax
    ea_tmax.sort(key=lambda x: x[1])

    # Step 2 e 3: Controlli di consistenza
    if len(ea_tmax) > 1:
        if not (ea_tmax[0][0] <= ea_tmax[1][1]):
            return {root: (float("inf"), float("inf"))}

        for i in range(1, len(ea_tmax)):
            if ea_tmax[i][0] > ea_tmax[0][1]:
                return {root: (float("inf"), float("inf"))}

    # Calcola EA e Tmax per il nodo corrente
    EA = max(ea_tmax, key=lambda x: x[0])[0]
    t_max_visita = min(ea_tmax, key=lambda x: x[1])[1]
    if not weight:
        k, nextTimeMax = 0, 0
        sottoalberi[root] = (k, nextTimeMax)
        return sottoalberi
    k = binary_search(weight, EA)
    nextTimeMax = binary_search_leq(weight, t_max_visita)

    if nextTimeMax == -1 and root != "A":
        return {root: (float("inf"), float("inf"))}

    # Aggiorna i risultati
    sottoalberi[root] = (k, nextTimeMax)
    return sottoalberi
```
---
## Ciao
