dirSalida = "salida"

archNodos = "data/datos_distribucion_tiendas.xlsx"
archDistancias = "data/matriz_distancias.xlsx"
archCostos = "data/matriz_costos_combustible.xlsx"

# unidades de demanda de una tienda segun su nivel
demandaPorNivel = {"A": 1200, "B": 1000, "C": 400}

paramsPorDefecto = {
    "tempIni": 0.5,
    "pasosPorTemp": 50,  # L(T), vecinos probados por temperatura
    "maxNiveles": 1000,
    "movimientos": 1,  # movimientos que se aplican por vecino
    "tempMin": 0.01,
    "nivelesSinMejora": 150,  # para si no mejora en estos niveles seguidos
    "arranques": 1,  # veces que se repite el recocido por cedis
}
