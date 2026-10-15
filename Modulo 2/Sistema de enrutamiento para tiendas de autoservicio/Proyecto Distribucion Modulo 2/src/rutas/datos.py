import pandas as pd

from rutas.config import archCostos, archDistancias, archNodos


def cargarDatos():
    nodos = pd.read_excel(archNodos)
    dist = pd.read_excel(archDistancias).values
    dist = dist.astype(float)
    costos = pd.read_excel(archCostos).values
    costos = costos.astype(float)

    n = len(nodos)
    if dist.shape != (n, n) or costos.shape != (n, n):
        raise ValueError(f"Las matrices deben ser {n}x{n}: dist {dist.shape}, costos {costos.shape}")

    for i in range(n):
        for j in range(n):
            if i == j:
                dist[i][j] = 0.0
                costos[i][j] = 0.0

    cedis = []
    tiendas = []
    for i in range(n):
        if nodos["Tipo"][i] == "Centro de Distribución":
            cedis.append(i)
        elif nodos["Tipo"][i] == "Tienda":
            tiendas.append(i)
    return nodos, dist, costos, cedis, tiendas
