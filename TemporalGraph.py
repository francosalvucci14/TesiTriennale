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
        t_end = t + traversal_time  # Calcoliamo il tempo di fine dell'arco
        self.edge_stream.append((u, v, t, traversal_time, t_end))

    def get_edges_at_time(self, t):
        """
        Restituisce tutti gli archi attivi in un dato timestamp.
        Un arco è attivo se il tempo corrente t è compreso tra il tempo di inizio e il tempo di fine.

        Args:
        t (int): Il timestamp desiderato

        Returns:
        list: Lista degli archi attivi al tempo t
        """
        return [
            (u, v)
            for u, v, t_start, _, t_end in self.edge_stream
            if t_start <= t <= t_end
        ]

    def get_all_edges(self):
        """
        Restituisce tutti gli archi del grafo temporale.

        Returns:
        list: Lista di tutte le tuple (u, v, t, lambda, t_end)
        """
        return self.edge_stream


# Esempio di utilizzo
if __name__ == "__main__":
    tg = TemporalGraph()

    # Aggiungiamo alcuni archi con vari timestamp e tempi di traversata (lambda)
    tg.add_edge(
        1, 2, 1, 1
    )  # Arco tra 1 e 2 al tempo 1 con tempo di traversata 3 (t_end = 4)
    tg.add_edge(
        2, 3, 2, 1
    )  # Arco tra 2 e 3 al tempo 2 con tempo di traversata 2 (t_end = 4)
    tg.add_edge(
        3, 4, 3, 1
    )  # Arco tra 3 e 4 al tempo 3 con tempo di traversata 1 (t_end = 4)
    tg.add_edge(
        1, 3, 2, 1
    )  # Arco tra 1 e 3 al tempo 2 con tempo di traversata 4 (t_end = 6)

    # Recuperiamo tutti gli archi
    print("Tutti gli archi nel grafo temporale:")
    print(tg.get_all_edges())

    # Recuperiamo gli archi attivi al tempo 3
    print("\nArchi attivi al tempo 3:")
    print(tg.get_edges_at_time(3))

    # Recuperiamo gli archi attivi al tempo 5
    print("\nArchi attivi al tempo 5:")
    print(tg.get_edges_at_time(5))
