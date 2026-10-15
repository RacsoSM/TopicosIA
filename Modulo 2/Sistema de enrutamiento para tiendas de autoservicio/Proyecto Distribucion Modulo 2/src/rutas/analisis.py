import os

import matplotlib
matplotlib.use("Agg")  # agg solo guarda imagenes, no abre ventanas
import matplotlib.pyplot as plt
import pandas as pd


def distanciaRuta(ruta, dist):
    total = 0
    for i in range(len(ruta) - 1):
        total += dist[ruta[i]][ruta[i + 1]]
    return total


def tablaResultados(resultados, dist, dfDemanda):
    filas = []
    totalTiendas = 0
    totalDistIni = 0
    totalDistFin = 0
    totalCostoIni = 0
    totalCostoFin = 0
    totalDemanda = 0

    for cedis, r in resultados.items():
        distIni = distanciaRuta(r.rutaInicial, dist)
        distFin = distanciaRuta(r.ruta, dist)

        if r.costoInicial <= 0:
            mejoraPct = 0.0
        else:
            mejoraPct = (r.costoInicial - r.costo) / r.costoInicial * 100

        textoInicial = ""
        for k in range(len(r.rutaInicial)):
            if k > 0:
                textoInicial += "->"
            textoInicial += str(r.rutaInicial[k])
        textoOptima = ""
        for k in range(len(r.ruta)):
            if k > 0:
                textoOptima += "->"
            textoOptima += str(r.ruta[k])

        # se busca en la tabla de demanda la fila de este cedis
        demandaZona = 0
        capacidad = 0
        usoPct = 0
        estado = ""
        for k in range(len(dfDemanda)):
            if dfDemanda["CEDIS"][k] == cedis:
                demandaZona = dfDemanda["Demanda_Zona"][k]
                capacidad = dfDemanda["Capacidad"][k]
                usoPct = dfDemanda["Uso_%"][k]
                estado = dfDemanda["Estado"][k]

        fila = {
            "CEDIS": cedis,
            "Tiendas": len(r.ruta) - 2,
            "Ruta_Inicial": textoInicial,
            "Ruta_Optima": textoOptima,
            "Dist_Inicial": round(distIni, 2),
            "Dist_Final": round(distFin, 2),
            "Costo_Inicial": round(r.costoInicial, 2),
            "Costo_Final": round(r.costo, 2),
            "Mejora": round(r.costoInicial - r.costo, 2),
            "Mejora_%": round(mejoraPct, 2),
            "Demanda_Zona": demandaZona,
            "Capacidad": capacidad,
            "Uso_%": usoPct,
            "Estado": estado,
        }
        filas.append(fila)

        # el total suma los valores ya redondeados para que cuadre con la tabla
        totalTiendas += fila["Tiendas"]
        totalDistIni += fila["Dist_Inicial"]
        totalDistFin += fila["Dist_Final"]
        totalCostoIni += fila["Costo_Inicial"]
        totalCostoFin += fila["Costo_Final"]
        totalDemanda += fila["Demanda_Zona"]

    if totalCostoIni > 0:
        totalMejoraPct = round((totalCostoIni - totalCostoFin) / totalCostoIni * 100, 2)
    else:
        totalMejoraPct = 0.0

    total = {
        "CEDIS": "TOTAL",
        "Tiendas": int(totalTiendas),
        "Ruta_Inicial": "-",
        "Ruta_Optima": "-",
        "Dist_Inicial": round(totalDistIni, 2),
        "Dist_Final": round(totalDistFin, 2),
        "Costo_Inicial": round(totalCostoIni, 2),
        "Costo_Final": round(totalCostoFin, 2),
        "Mejora": round(totalCostoIni - totalCostoFin, 2),
        "Mejora_%": totalMejoraPct,
        "Demanda_Zona": int(totalDemanda),
        "Capacidad": "-",
        "Uso_%": "-",
        "Estado": "-",
    }
    filas.append(total)
    return pd.DataFrame(filas)


def guardarExcel(tabla, rutaArchivo):
    rutaArchivo = str(rutaArchivo)
    carpeta = os.path.dirname(rutaArchivo)
    if carpeta != "":
        os.makedirs(carpeta, exist_ok=True)
    tabla.to_excel(rutaArchivo, index=False)
    return rutaArchivo


def graficarTemperatura(res, rutaPng):
    plt.figure(figsize=(9, 4.5))
    plt.plot(res.histTemp)
    plt.title("Enfriamiento logaritmico")
    plt.xlabel("Nivel de temperatura")
    plt.ylabel("Temperatura")
    plt.grid(True, linestyle=":")
    plt.tight_layout()

    rutaPng = str(rutaPng)
    carpeta = os.path.dirname(rutaPng)
    if carpeta != "":
        os.makedirs(carpeta, exist_ok=True)
    plt.savefig(rutaPng, dpi=120)
    # se cierra la figura para liberar memoria
    plt.close()
    return rutaPng


def graficarCosto(res, rutaPng):
    plt.figure(figsize=(8, 4))
    plt.plot(res.histActual, marker="o", label="Costo actual")
    plt.plot(res.histMejor, linewidth=2, label="Mejor costo")
    plt.title("Evolución del Costo en Recocido Simulado")
    plt.xlabel("Iteración")
    plt.ylabel("Costo (MXN)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    rutaPng = str(rutaPng)
    carpeta = os.path.dirname(rutaPng)
    if carpeta != "":
        os.makedirs(carpeta, exist_ok=True)
    plt.savefig(rutaPng, dpi=100)
    # se cierra la figura para liberar memoria
    plt.close()
    return rutaPng
