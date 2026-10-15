def zonificar(cedis, tiendas, dist):
    zonas = {}
    for c in cedis:
        zonas[c] = []

    # cada tienda va al cedis con menor distancia (si hay empate gana el primero)
    for t in tiendas:
        cercano = cedis[0]
        menorDist = dist[t][cercano]
        for c in cedis:
            if dist[t][c] < menorDist:
                cercano = c
                menorDist = dist[t][c]
        zonas[cercano].append(t)
    return zonas
