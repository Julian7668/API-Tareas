"""
Constantes del proyecto

Este módulo define las rutas y constantes utilizadas en toda la aplicación,
incluyendo las ubicaciones de archivos de datos y configuración de directorios.

Constantes principales:
- DIR_DATA: Directorio donde se almacenan todos los archivos de datos
- DATA_JSON: Archivo JSON con tareas activas
- DELETED_JSON: Archivo JSON con historial de tareas eliminadas
- ID_COUNTER_JSON: Archivo JSON con contador de IDs

El módulo crea automáticamente el directorio de datos si no existe.
"""

import os

# Directorio de datos - se crea automáticamente si no existe
DIR_DATA: str = os.path.join(os.path.dirname(__file__), "../data")

# Archivos JSON donde se almacenan los datos persistentes
DATA_JSON: str = os.path.join(DIR_DATA, "tareas.json")  # Tareas activas
DELETED_JSON: str = os.path.join(DIR_DATA, "tareas_eliminadas.json")  # Historial de eliminadas
ID_COUNTER_JSON: str = os.path.join(DIR_DATA, "contador_id.json")  # Contador de IDs únicos

# Crear el directorio de datos si no existe
# Esto asegura que la aplicación pueda ejecutarse sin configuración manual
os.makedirs(DIR_DATA, exist_ok=True)
