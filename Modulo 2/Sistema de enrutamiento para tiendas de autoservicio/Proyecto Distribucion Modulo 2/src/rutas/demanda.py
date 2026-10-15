# solo verifica: no cambia rutas ni asignaciones
import pandas as pd

from rutas.config import demandaPorNivel


def verificarDemanda(nodos, zonas, demandaNivel=demandaPorNivel):
    filas = []
    for cedis, tiendas in zonas.items():
        total = 0
        for t in tiendas:
            nivel = nodos["Nivel_Tienda"][t]
            total += demandaNivel[nivel]
        capacidad = float(nodos["Capacidad_Almacenamiento"][cedis])
        uso = total / capacidad * 100
        if uso <= 100:
            estado = "OK"
        else:
            estado = "SOBRECARGADO"
        filas.append({
            "CEDIS": cedis,
            "Tiendas": len(tiendas),
            "Demanda_Zona": total,
            "Capacidad": capacidad,
            "Uso_%": round(uso, 2),
            "Estado": estado,
        })
    return pd.DataFrame(filas)
