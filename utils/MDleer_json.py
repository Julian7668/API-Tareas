"""
Módulo para leer datos desde archivos JSON

Este módulo proporciona funciones para cargar datos desde archivos JSON
con manejo robusto de errores y archivos inexistentes.
"""

import os
import json
import logging
from typing import Any
from constants import DATA_JSON

logger = logging.getLogger(__name__)


# Función para leer datos del archivo JSON
def leer_json() -> list[dict[str, Any]]:
    """
    Lee los datos desde el archivo JSON principal.

    Returns:
        list[dict[str, Any]]: Lista de datos leídos. Retorna lista vacía si el archivo no existe o hay error.
    """
    logger.debug("Leyendo archivo JSON: %s", DATA_JSON)
    if not os.path.exists(DATA_JSON):
        logger.warning("Archivo %s no existe, retornando lista vacía", DATA_JSON)
        return []
    try:
        with open(DATA_JSON, "r", encoding="utf-8") as file:
            data = json.load(file)
            logger.debug("Datos leídos: %s elementos", len(data))
            return data
    except json.JSONDecodeError as e:
        logger.error("Error al decodificar JSON en {DATA_JSON}: %s", e)
        return []
