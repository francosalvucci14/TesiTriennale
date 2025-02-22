import math


class TemporalGraph:
    def __init__(self):
        # Lista degli archi nel formato (u, v, t, lambda, t_end)
        self.edge_stream = []

    def add_edge(self, u, v, t, traversal_time):
        """
        Aggiunge un arco al grafo temporale con il tempo di inizio, tempo di traversata e tempo di fine.

        Args:
        u (int): Nodo sorgente
        v (int): Nodo destinazione
        t (int): Timestamp dell'inizio dell'arco
        traversal_time (int): Tempo di traversata dell'arco (lambda)
        """
        if type(t) == list:
            for time in t:
                t_end = time + traversal_time
            t = min(t)  # Calcoliamo il tempo di fine dell'arco
        else:
            t_end = t + traversal_time
        self.edge_stream.append((u, v, t, traversal_time, t_end))

    def earliest_arrival_time(self, source, t_alpha, t_omega):
        """
        Calcola il tempo di arrivo più veloce da un nodo sorgente `source` a tutti gli altri nodi.

        Args:
        source (int): Nodo sorgente
        t_alpha (int): Inizio dell'intervallo temporale
        t_omega (int): Fine dell'intervallo temporale

        Returns:
        dict: Mappa del tempo di arrivo più veloce per ogni nodo
        """
        # Inizializza il tempo di arrivo
        t = {v: math.inf for v in self.get_all_nodes()}
        t[source] = t_alpha  # Il tempo di arrivo alla sorgente è t_alpha

        # Scorri tutti gli archi nell'edge stream
        for u, v, t_start, lambda_, t_end in self.edge_stream:
            if t_start >= t_alpha and t_start <= t_omega:
                if t_start >= t[u]:  # Se possiamo raggiungere u in tempo
                    arrival_time = t_start + lambda_
                    if arrival_time <= t_omega and arrival_time < t[v]:
                        t[v] = (
                            arrival_time  # Aggiorniamo il tempo di arrivo se è più veloce
                        )

        return t

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

    def reverse_earliest_arrival_time(self, target, t_alpha, t_omega):
        """
        Calcola il tempo di arrivo più veloce da tutti i nodi verso un nodo target,
        lavorando all'indietro nel grafo temporale.

        Args:
            target (int): Nodo target/destinazione
            t_alpha (int): Inizio dell'intervallo temporale
            t_omega (int): Fine dell'intervallo temporale

        Returns:
            dict: Mappa del tempo di arrivo più veloce per ogni nodo verso il target
        """
        # Inizializza il tempo di arrivo
        t = {v: math.inf for v in self.get_all_nodes()}
        t[target] = t_omega  # Il tempo di arrivo al target è t_omega

        # Creiamo una lista di archi inversa per processarli dal più recente al meno recente
        reverse_edges = []
        for u, v, t_start, lambda_, t_end in self.edge_stream:
            reverse_edges.append((v, u, t_start, lambda_, t_end))
        
        # Ordiniamo gli archi per tempo decrescente
        reverse_edges.sort(key=lambda x: x[2], reverse=True)

        # Scorri tutti gli archi all'indietro
        for v, u, t_start, lambda_, t_end in reverse_edges:
            if t_start >= t_alpha and t_start <= t_omega:
                arrival_time = t_start  # Tempo di arrivo all'arco
                
                # Se possiamo raggiungere il nodo v (che ora è la nostra sorgente per questo arco)
                if arrival_time <= t[v]:
                    # Calcoliamo il tempo di partenza necessario da u
                    departure_time = arrival_time - lambda_
                    
                    # Se questo tempo di partenza è valido e migliore di quello attuale
                    if departure_time >= t_alpha and departure_time < t[u]:
                        t[u] = departure_time

        return t

# Esempio di utilizzo
if __name__ == "__main__":
    tg = TemporalGraph()

    # # Aggiungiamo alcuni archi con vari timestamp e tempi di traversata (lambda)
    # tg.add_edge(
    #     1, 2, 1, 0
    # )  # Arco tra 1 e 2 al tempo 1 con tempo di traversata 3 (t_end = 4)
    # tg.add_edge(
    #     2, 3, 2, 0
    # )  # Arco tra 2 e 3 al tempo 2 con tempo di traversata 2 (t_end = 4)
    # tg.add_edge(
    #     3, 4, 3, 0
    # )  # Arco tra 3 e 4 al tempo 3 con tempo di traversata 1 (t_end = 4)
    # tg.add_edge(
    #     1, 3, 2, 0
    # )  # Arco tra 1 e 3 al tempo 2 con tempo di traversata 4 (t_end = 6)

    tg.add_edge(0,1,[1,2],0)
    tg.add_edge(0,2,[1,3],0)
    tg.add_edge(1,3,[2],0)
    tg.add_edge(2,4,[2],0)
    # Calcoliamo il tempo di arrivo più veloce da 1 all'interno dell'intervallo [1, 10]
    earliest_arrival = tg.reverse_earliest_arrival_time(4, 2, 0)

    # Stampiamo i risultati
    print("Tempo di arrivo più veloce da 4:")
    for node, time in earliest_arrival.items():
        print(f"Nodo {node}: {time}")

