"""
Config de pytest: agrega src/ al path para poder importar los modulos
sin instalar el paquete.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
