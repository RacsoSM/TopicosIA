import os

import folium

colorNivel = {"A": "blue", "B": "green", "C": "gray"}
coloresRuta = ["red", "purple", "orange", "darkblue", "darkgreen",
               "cadetblue", "pink", "black", "brown", "magenta"]


def construirMapa(nodos, cedis, resultados, rutaHtml):
    centro = [nodos["Latitud_WGS84"].mean(), nodos["Longitud_WGS84"].mean()]
    # openstreetmap bloquea (403) las paginas abiertas desde un archivo local, por eso se usa esri
    mapaBase = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}"
    mapa = folium.Map(location=centro, zoom_start=12, tiles=mapaBase, attr="Esri")

    for i in range(len(nodos)):
        punto = [nodos["Latitud_WGS84"][i], nodos["Longitud_WGS84"][i]]
        if i in cedis:
            icono = folium.Icon(color="red", icon="home")
            texto = f"CEDIS {i}"
        else:
            nivel = nodos["Nivel_Tienda"][i]
            icono = folium.Icon(color=colorNivel.get(nivel, "black"))
            texto = f"Tienda {i} (nivel {nivel})"
        folium.Marker(punto, popup=texto, icon=icono).add_to(mapa)

    # sin resultados solo se dibujan los puntos
    if resultados is not None:
        k = 0
        for cedisRuta, r in resultados.items():
            puntos = []
            for n in r.ruta:
                puntos.append([nodos["Latitud_WGS84"][n], nodos["Longitud_WGS84"][n]])
            folium.PolyLine(puntos, color=coloresRuta[k], weight=3,
                            tooltip=f"Ruta CEDIS {cedisRuta}").add_to(mapa)
            k += 1

    carpeta = os.path.dirname(rutaHtml)
    if carpeta != "":
        os.makedirs(carpeta, exist_ok=True)
    mapa.save(rutaHtml)
    return rutaHtml
