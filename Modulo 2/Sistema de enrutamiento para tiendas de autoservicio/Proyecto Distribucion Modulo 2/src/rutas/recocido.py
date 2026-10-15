import math
import random


class Resultado:
    def __init__(self, ruta, costo, rutaInicial, costoInicial,
                 histTemp=None, histMejor=None, histActual=None):
        self.ruta = ruta
        self.costo = costo
        self.rutaInicial = rutaInicial
        self.costoInicial = costoInicial
        if histTemp is None:
            histTemp = []
        if histMejor is None:
            histMejor = []
        if histActual is None:
            histActual = []
        self.histTemp = histTemp
        self.histMejor = histMejor
        self.histActual = histActual


def costoRuta(ruta, costos):
    # funcion objetivo: costo de combustible de recorrer la ruta en orden
    total = 0
    for i in range(len(ruta) - 1):
        total += costos[ruta[i]][ruta[i + 1]]
    return total


def armarRutaInicial(cedis, tiendas, aleatoria=True):
    orden = list(tiendas)
    if aleatoria:
        random.shuffle(orden)
    ruta = []
    ruta.append(cedis)
    ruta.extend(orden)
    ruta.append(cedis)
    return ruta


def moverSwap(vecino, i, j):
    # intercambia las tiendas de las posiciones i y j
    temporal = vecino[i]
    vecino[i] = vecino[j]
    vecino[j] = temporal
    return vecino


def moverInsercion(vecino, i, j):
    # saca la tienda de la posicion i y la reinserta en la posicion j
    tienda = vecino.pop(i)
    vecino.insert(j, tienda)
    return vecino


def mover2opt(vecino, i, j):
    # invierte el tramo entre i y j (quita cruces de la ruta)
    a = i
    b = j
    if i > j:
        a = j
        b = i
    while a < b:
        temporal = vecino[a]
        vecino[a] = vecino[b]
        vecino[b] = temporal
        a = a + 1
        b = b - 1
    return vecino


def generarVecino(ruta, movimientos=1):
    vecino = list(ruta)
    # con menos de 2 tiendas no hay nada que mover
    if len(ruta) - 2 < 2:
        return vecino
    for a in range(movimientos):
        # en cada movimiento se elige al azar un tipo; los extremos (cedis) no se tocan
        tipo = random.choice(["swap", "insercion", "2opt"])
        i, j = random.sample(range(1, len(ruta) - 1), 2)
        if tipo == "swap":
            vecino = moverSwap(vecino, i, j)
        elif tipo == "insercion":
            vecino = moverInsercion(vecino, i, j)
        else:
            vecino = mover2opt(vecino, i, j)
    return vecino


def recocidoSimulado(ruta, costos, params):
    actual = list(ruta)
    costoActual = costoRuta(actual, costos)
    mejor = list(actual)
    costoMejor = costoActual
    res = Resultado(list(actual), costoActual, list(actual), costoActual)

    t = params["tempIni"]
    niveles = 0
    sinMejora = 0
    # casi nunca se llega a tempMin: termina por maxNiveles o por niveles sin mejora
    while t > params["tempMin"] and niveles < params["maxNiveles"] and sinMejora < params["nivelesSinMejora"]:
        res.histTemp.append(t)
        res.histActual.append(costoActual)
        res.histMejor.append(costoMejor)
        mejoro = False

        for a in range(params["pasosPorTemp"]):
            candidato = generarVecino(actual, params["movimientos"])
            costoCand = costoRuta(candidato, costos)
            delta = costoCand - costoActual
            # si empeora, se acepta con probabilidad de boltzmann
            if delta < 0 or random.random() < math.exp(-delta / t):
                actual = candidato
                costoActual = costoCand
            if costoActual < costoMejor:
                mejor = list(actual)
                costoMejor = costoActual
                mejoro = True

        if mejoro:
            sinMejora = 0
        else:
            sinMejora = sinMejora + 1
        niveles = niveles + 1
        # enfriamiento logaritmico: t = t0 * ln(2) / ln(k + 2)
        t = params["tempIni"] * math.log(2) / math.log(niveles + 2)

    res.ruta = mejor
    res.costo = costoMejor
    return res


def optimizarZonas(costos, zonas, params, semilla=None):
    # con semilla entera el resultado es reproducible
    if semilla is not None:
        random.seed(semilla)
    resultados = {}
    for cedis, tiendas in zonas.items():
        # se conserva el mejor arranque; la tabla muestra el inicio de ese arranque
        mejorRes = None
        for a in range(params["arranques"]):
            inicial = armarRutaInicial(cedis, tiendas)
            res = recocidoSimulado(inicial, costos, params)
            if mejorRes is None or res.costo < mejorRes.costo:
                mejorRes = res
        resultados[cedis] = mejorRes
    return resultados
