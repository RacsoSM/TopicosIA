from rutas.analisis import graficarCosto
from rutas.analisis import graficarTemperatura
from rutas.analisis import guardarExcel
from rutas.analisis import tablaResultados
from rutas.config import dirSalida, paramsPorDefecto
from rutas.datos import cargarDatos
from rutas.demanda import verificarDemanda
from rutas.recocido import optimizarZonas
from rutas.zonas import zonificar

opciones = """
=============================================
  ENRUTAMIENTO DE TIENDAS - Recocido Simulado
  Culiacan, Sinaloa
=============================================
  1. Ejecutar todo (cargar, zonificar, demanda, optimizar)
  2. Cambiar parametros (opcional)
  3. Ver resultados (y guardar Excel)
  4. Graficar un CEDIS
  5. Salir
============================================="""


def pedir(texto, tipo=str, recomendado=None):
    # con valor recomendado, enter lo acepta
    if recomendado is not None:
        sufijo = f" [Enter = {recomendado}]"
    else:
        sufijo = ""
    while True:
        crudo = input(f"  {texto}{sufijo}: ").strip()
        if crudo == "" and recomendado is not None:
            return recomendado
        try:
            return tipo(crudo)
        except ValueError:
            print("  Valor no valido, intenta de nuevo.")


def pedirParametros(paramsActuales):
    nuevos = {}
    nuevos["tempIni"] = pedir("Temperatura inicial", float, paramsActuales["tempIni"])
    nuevos["pasosPorTemp"] = pedir("L(T), pasos por temperatura", int, paramsActuales["pasosPorTemp"])
    nuevos["maxNiveles"] = pedir("Maximo de niveles de temperatura", int, paramsActuales["maxNiveles"])
    nuevos["movimientos"] = pedir("Inserciones por vecino", int, paramsActuales["movimientos"])
    nuevos["tempMin"] = pedir("Temperatura minima", float, paramsActuales["tempMin"])
    nuevos["nivelesSinMejora"] = pedir("Niveles sin mejora", int, paramsActuales["nivelesSinMejora"])
    nuevos["arranques"] = pedir("Numero de arranques (1 = una sola corrida)", int, paramsActuales["arranques"])
    return nuevos


def mostrarParametros(params):
    texto = ""
    for clave in params:
        if texto != "":
            texto += ", "
        texto += f"{clave}={params[clave]}"
    print(f"  Parametros: {texto}")


def ejecutarTodo(params):
    # siempre se recalcula todo desde cero, para no usar datos viejos
    nodos, dist, costos, cedis, tiendas = cargarDatos()
    print(f"  Datos cargados: {len(nodos)} nodos, {len(cedis)} CEDIS, {len(tiendas)} tiendas")
    zonas = zonificar(cedis, tiendas, dist)
    dfDemanda = verificarDemanda(nodos, zonas)
    print(dfDemanda.to_string(index=False))
    mostrarParametros(params)
    resultados = optimizarZonas(costos, zonas, params)
    print("  Optimizacion terminada.")
    return dist, dfDemanda, resultados


def menu():
    # todo empieza vacio; la opcion 1 llena lo que necesitan las demas
    dist = dfDemanda = resultados = None
    params = paramsPorDefecto.copy()

    while True:
        print(opciones)
        op = input("  Opcion: ").strip()

        if op == "1":
            dist, dfDemanda, resultados = ejecutarTodo(params)
        elif op == "2":
            params = pedirParametros(params)
            mostrarParametros(params)
        elif op in ("3", "4") and resultados is None:
            print("  Primero ejecuta todo (1).")
        elif op == "3":
            tabla = tablaResultados(resultados, dist, dfDemanda)
            print(tabla.drop(columns=["Ruta_Inicial", "Ruta_Optima"]).to_string(index=False))
            archivo = dirSalida + "/Resultados.xlsx"
            print(f"  Excel: {guardarExcel(tabla, archivo)}")
        elif op == "4":
            elegido = pedir("CEDIS", int)
            if elegido not in resultados:
                print("  CEDIS no valido.")
                continue
            archivoTemp = dirSalida + f"/temp_cedis{elegido}.png"
            archivoCosto = dirSalida + f"/costo_cedis{elegido}.png"
            print(f"  {graficarTemperatura(resultados[elegido], archivoTemp)}")
            print(f"  {graficarCosto(resultados[elegido], archivoCosto)}")
        elif op == "5":
            print("  Hasta luego.")
            break
        else:
            print("  Opcion no valida.")


if __name__ == "__main__":
    menu()
