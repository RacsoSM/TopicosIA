from random import sample
import time


def mostrar_tablero(tablero, titulo):
    m = len(tablero)
    c = FO(tablero)
    print("\n%s (colisiones: %d)" % (titulo, c))
    sp = "   " if m > 9 else "  "
    encabezado = sp
    for j in range(m):
        encabezado += "%-3d" % j
    print(encabezado)
    print(sp + "-" * (m * 3))
    for i in range(m):
        fila = ("%2d|" % i) if m > 9 else (str(i) + "|")
        for j in range(m):
            if tablero[j] == i:
                fila += " ♕ "
            else:
                fila += " . "
        print(fila)
    print()
    return c


def FO(tablero):
    # tablero[columna] = fila
    # permutacion de 0 a n-1:
    # sin repetir filas ni columnas
    # solo quedan choques diagonales
    m = len(tablero)
    c = 0
    for i in range(m):
        for j in range(i + 1, m):
            if abs(tablero[i] - tablero[j]) == j - i:
                c += 1
    return c


def N(x):
    m = len(x)
    nx = []
    for i in range(m):
        for j in range(i + 1, m):
            v = x[:]
            v[i], v[j] = v[j], v[i]
            nx.append((v, (i, j)))
    return nx


def buscar(t, n, tt):
    x = t[:]  # solucion actual
    fo = FO(x)
    # mejor: x*; fm: su valor
    mejor, fm = x[:], fo
    historial, tabu = [], []

    sep = "-" * 77
    print(sep)
    print("Iter | Swap     | FO  | Tabu? | Aspiracion? | Mejor FO | Accion")
    print(sep)

    for k in range(1, n + 1):
        if fm == 0:
            break

        xp = None  # vecino seleccionado
        fv = 0
        swap = None
        movimiento_tabu, aplica_aspiracion = False, False

        # N(x): vecinos por swap
        for v, par in N(x):
            c = FO(v)
            es_tabu = False
            for mov, vida in tabu:
                if mov == par:
                    es_tabu = True
                    break

            # aspiracion: aceptar un tabu
            # si mejora la mejor solucion
            cumple_aspiracion = es_tabu and c < fm
            if es_tabu and not cumple_aspiracion:
                continue

            if xp is None or c < fv:
                xp = v
                fv = c
                swap = par
                movimiento_tabu, aplica_aspiracion = (
                    es_tabu, cumple_aspiracion
                )

        # memoria a corto plazo:
        # baja la tenencia y elimina
        # movimientos vencidos
        aux = []
        for mov, vida in tabu:
            if vida > 1:
                aux.append([mov, vida - 1])
        tabu = aux

        if xp is None:
            accion = "sin movimiento"
        else:
            x = xp
            fo = fv
            if aplica_aspiracion:
                accion = "aspiracion aplicada"
            elif fo < fm:
                accion = "mejora encontrada"
            else:
                accion = "movimiento normal"

            if fo < fm:
                mejor, fm = x[:], fo

            # nuevo tabu: tt vueltas completas
            if tt > 0:
                tabu.append([swap, tt])

        mov = "---" if swap is None else str(swap)
        ts = "Si" if movimiento_tabu else "No"
        aa = "Si" if aplica_aspiracion else "No"
        print(
            "%-4d | %-8s | %-3d | %-5s | %-11s | %-8d | %s" %
            (k, mov, fo, ts, aa, fm, accion)
        )
        historial.append({
            "iter": k, "swap": swap, "fo": fo,
            "tabu": movimiento_tabu, "aspiracion": aplica_aspiracion,
            "mejor_fo": fm, "accion": accion
        })

    print(sep)
    return mejor, fm, historial


def reporte(datos, dt, c, n):
    print("=" * 60)
    print("  REPORTE DE METRICAS")
    print("=" * 60)
    for nom, val in datos:
        print("  %s: %s" % (nom, val))
    print(
        "  Tiempo de busqueda (impresion de iteraciones incluida):",
        round(dt, 6), "segundos"
    )
    if c == 0:
        print("  >>> OPTIMO GLOBAL ALCANZADO: f(x*) = 0")
    else:
        print("  >>> Criterio de parada: %d iteraciones" % n)
        print("  >>> Mejor costo logrado: %d" % c)
    print("=" * 60)


num_reinas = 8
n = 200
tt = 3
for texto in [
    "=" * 60,
    "  PROBLEMA DE LAS %d REINAS - BUSQUEDA TABU" % num_reinas,
    "  Topicos Selectos de Inteligencia Artificial",
    "  P: colocar %d reinas sin colisiones" % num_reinas,
    "  S: permutaciones de 0 a %d" % (num_reinas - 1),
    "  FO: numero de colisiones diagonales",
    "  Memoria a Corto Plazo | Tenencia Tabu = %d" % tt,
    "=" * 60
]:
    print(texto)

ini = sample(range(num_reinas), num_reinas)
f0 = mostrar_tablero(ini, ">>> SOLUCION INICIAL")
t0 = time.perf_counter()
sol, c, historial = buscar(ini, n, tt)
dt = time.perf_counter() - t0

movs = 0
for paso in historial:
    if paso["swap"] is not None:
        movs += 1

mostrar_tablero(sol, ">>> MEJOR SOLUCION ENCONTRADA")
datos = [
    ("Solucion inicial", ini),
    ("FO inicial", f0),
    ("Mejor solucion encontrada", sol),
    ("Mejor FO", c),
    ("Iteraciones usadas", len(historial)),
    ("Movimientos realizados", movs)
]
reporte(datos, dt, c, n)
