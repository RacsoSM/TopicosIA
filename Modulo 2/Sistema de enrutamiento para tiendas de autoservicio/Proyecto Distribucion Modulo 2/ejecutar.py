import sys

# para que python encuentre el paquete rutas dentro de src
sys.path.insert(0, "src")

from rutas.main import menu

menu()
