"""
Módulo para leer datos desde archivos JSON

Este módulo proporciona funciones para cargar datos desde archivos JSON
con manejo robusto de errores y archivos inexistentes.

Funciones principales:
- leer_json(): Carga datos desde el archivo JSON principal de tareas

Características:
- Manejo automático de archivos inexistentes
- Recuperación de errores de decodificación JSON
- Logging detallado de operaciones
- Retorno de lista vacía en caso de error
"""

import os
import json
import logging
from typing import Any
from constants import DATA_JSON

logger: logging.Logger = logging.getLogger(__name__)


# Función para leer datos del archivo JSON
def leer_json() -> list[dict[str, Any]]:
    """
    Lee los datos desde el archivo JSON principal de tareas activas.

    Esta función carga todas las tareas activas desde el archivo de datos principal.
    Maneja automáticamente casos donde el archivo no existe (retornando lista vacía)
    o contiene JSON malformado.

    Returns:
        list[dict[str, Any]]: Lista de diccionarios representando las tareas activas.
                            Retorna lista vacía si el archivo no existe o hay error de formato.

    Notas:
        - Archivo objetivo: tareas.json en directorio data/
        - Retorna lista vacía en lugar de lanzar excepciones
        - Logging automático de operaciones y errores
        - Encoding UTF-8 para soporte de caracteres especiales

    Ejemplo:
        >>> tareas = leer_json()
        >>> print(len(tareas))  # Número de tareas activas
    """
    logger.debug("Leyendo archivo JSON: %s", DATA_JSON)
    if not os.path.exists(DATA_JSON):
        logger.warning("Archivo %s no existe, retornando lista vacía", DATA_JSON)
        return []
    try:
        with open(DATA_JSON, "r", encoding="utf-8") as file:
            data: list[dict[str, Any]] = json.load(file)
            logger.debug("Datos leídos: %s elementos", len(data))
            return data
    except json.JSONDecodeError as e:
        logger.error("Error al decodificar JSON en {DATA_JSON}: %s", e)
        return []
