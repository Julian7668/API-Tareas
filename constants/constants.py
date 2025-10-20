"""
Constantes del proyecto

Este módulo define las rutas y constantes utilizadas en toda la aplicación,
incluyendo las ubicaciones de archivos de datos y configuración de directorios.
"""

import os

# Archivos JSON donde guardaremos los datos
DIR_DATA = os.path.join(os.path.dirname(__file__), "../data")
DATA_JSON = os.path.join(DIR_DATA, "tareas.json")
DELETED_JSON = os.path.join(DIR_DATA, "tareas_eliminadas.json")
ID_COUNTER_JSON = os.path.join(DIR_DATA, "contador_id.json")

# Crear el directorio si no existe
os.makedirs(DIR_DATA, exist_ok=True)
