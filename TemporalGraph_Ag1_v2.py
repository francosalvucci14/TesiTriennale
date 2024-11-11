import math

class TemporalGraph:
    def __init__(self):
        self.edge_stream = []
        self.reverse_edge_stream = []  # Nuovo stream per gli archi inversi
    
    def add_edge(self, u, v, times, lambda_):
        """
        Aggiunge un arco al grafo temporale in entrambe le direzioni.
        
        Args:
            u, v: nodi di origine e destinazione
            times: lista dei tempi in cui l'arco è attivo
            lambda_: tempo di attraversamento
        """
        # Aggiunge l'arco originale
        for t in times:
            self.edge_stream.append((u, v, t, lambda_, t + lambda_))
            # Aggiunge l'arco inverso con gli stessi tempi
            self.reverse_edge_stream.append((v, u, t, lambda_, t + lambda_))
    
    def get_all_nodes(self):
        """
        Restituisce tutti i nodi presenti nel grafo temporale.

        Returns:
        set: Insieme dei nodi
        """
        nodes = set()
        for u, v, _, _, _ in self.edge_stream:
            nodes.add(u)
            nodes.add(v)
        return nodes
    
    def earliest_arrival_time(self, source, t_alpha, t_omega, reverse=False):
        """
        Calcola il tempo di arrivo più veloce da un nodo sorgente a tutti gli altri.
        
        Args:
            source: nodo sorgente
            t_alpha: tempo iniziale
            t_omega: tempo finale
            reverse: se True, usa gli archi inversi
        """
        # Inizializza il tempo di arrivo
        t = {v: math.inf for v in self.get_all_nodes()}
        t[source] = t_alpha
        
        # Sceglie quale stream di archi usare
        edges = self.reverse_edge_stream if reverse else self.edge_stream
        
        # Ordina gli archi per tempo
        edges = sorted(edges, key=lambda x: x[2])
        
        # Scorri tutti gli archi
        for u, v, t_start, lambda_, t_end in edges:
            if t_start >= t_alpha and t_start <= t_omega:
                if t_start >= t[u]:  # Se possiamo raggiungere u in tempo
                    arrival_time = t_start + lambda_
                    if arrival_time <= t_omega and arrival_time < t[v]:
                        t[v] = arrival_time
        
        return t
    def earliest_arrival_time_rev(self, source, t_alpha, t_omega):
        """
        Calcola il tempo di arrivo più veloce da un nodo sorgente a tutti gli altri,
        permettendo anche percorsi dalle foglie alla radice.
        """
        # Inizializza il tempo di arrivo
        t = {v: math.inf for v in self.get_all_nodes()}
        t[source] = t_alpha

        # Ordina gli archi per tempo
        edges = sorted(self.edge_stream, key=lambda x: x[2])

        # Scorri tutti gli archi
        for u, v, t_start, lambda_, t_end in edges:
            if t_start >= t_alpha and t_start <= t_omega:
                # Controlla sia la direzione normale (u->v) che inversa (v->u)
                if t_start >= t[u]:  # direzione normale
                    arrival_time = t_start + lambda_
                    if arrival_time <= t_omega and arrival_time <= t[v]:
                        t[v] = arrival_time
                if t_start >= t[v]:  # direzione inversa (dalle foglie alla radice)
                    arrival_time = t_start + lambda_
                    if arrival_time <= t_omega and arrival_time <= t[u]:
                        t[u] = arrival_time

        return t
    def earliest_arrival_time_2(self, source, t_alpha, t_omega):
        """
        Calcola il tempo di arrivo più veloce da un nodo sorgente a tutti gli altri.
        Permette il movimento in entrambe le direzioni su ogni arco.
        """
        # Inizializza il tempo di arrivo
        t = {v: math.inf for v in self.get_all_nodes()}
        t[source] = t_alpha
        
        # Usa gli archi originali ma considera entrambe le direzioni
        edges = sorted(self.edge_stream, key=lambda x: x[2])
        
        # Flag per controllare se ci sono stati cambiamenti
        changed = True
        while changed:
            changed = False
            for u, v, t_start, lambda_, t_end in edges:
                if t_start >= t_alpha and t_start <= t_omega:
                    # Direzione u->v
                    if t_start >= t[u] and t[u] != math.inf:
                        arrival_time = t_start + lambda_
                        if arrival_time <= t_omega and arrival_time < t[v]:
                            t[v] = arrival_time
                            changed = True
                    
                    # Direzione v->u
                    if t_start >= t[v] and t[v] != math.inf:
                        arrival_time = t_start + lambda_
                        if arrival_time <= t_omega and arrival_time < t[u]:
                            t[u] = arrival_time
                            changed = True
        
        return t
# Crea il grafo
tg = TemporalGraph()

# Aggiungi gli archi (vengono automaticamente aggiunti in entrambe le direzioni)
tg.add_edge('A', 'B', [1, 2], 0)
tg.add_edge('A', 'C', [1, 3], 0)
tg.add_edge('B', 'D', [2], 0)
tg.add_edge('C', 'E', [2], 0)

# Per trovare i tempi dal nodo 0 verso tutti gli altri (come prima)
forward_times = tg.earliest_arrival_time_2('A', 0, 5)

# Per trovare i tempi dal nodo 4 verso tutti gli altri
backward_times = tg.earliest_arrival_time_2('E', 0, 5)

 # Stampiamo i risultati
print("Tempo di arrivo più veloce da A:")
for node, time in forward_times.items():
    print(f"Nodo {node}: {time}")

 # Stampiamo i risultati
print("Tempo di arrivo più veloce da E:")
for node, time in backward_times.items():
    print(f"Nodo {node}: {time}")
