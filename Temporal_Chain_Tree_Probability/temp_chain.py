import random
from collections import deque

def genera_etichette_casuali(albero, k):
    """Assegna etichette casuali agli archi dell'albero.

    Args:
        albero (dict): L'albero da etichettare.
        k: Il valore massimo per le etichette.
    """
    for nodo, figli in albero.items():
        for i, figlio in enumerate(figli):
            albero[nodo][i] = (figlio, random.randint(1, k))

def verifica_connettivita_temporale(albero):
    visitati = set()
    coda = deque([(0, float('-inf'))])

    while coda:
        nodo_corrente, tempo_precedente = coda.popleft()
        if nodo_corrente in visitati:
            continue
        visitati.add(nodo_corrente)

        try:
            for figlio, tempo in albero[nodo_corrente]:
                if tempo >= tempo_precedente:
                    coda.append((figlio, tempo))
        except KeyError as e:
            print(f"Errore: chiave non trovata {e}")

    return len(visitati) == len(albero)

def calcola_probabilita_connettivita(albero, k, num_esperimenti):
    successi = 0
    for _ in range(num_esperimenti):
        genera_etichette_casuali(albero, k)
        if verifica_connettivita_temporale(albero):
            successi += 1
    return successi / num_esperimenti

# Esempio di utilizzo:
albero = {0: [(1, 0)], 1: [(2, 0)], 2: []}  # Albero iniziale
k = 10  # Valore massimo delle etichette
num_esperimenti = 1000
probabilita = calcola_probabilita_connettivita(albero, k, num_esperimenti)
print(probabilita)