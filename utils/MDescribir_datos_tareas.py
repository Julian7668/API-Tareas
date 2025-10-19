"""
Módulo para escribir datos en archivos JSON

Este módulo proporciona funciones para escribir datos estructurados
en archivos JSON con formato legible y manejo de errores.
"""

from typing import Any
import json
import logging
from constants import DATA_JSON

logger = logging.getLogger(__name__)


# Función para escribir datos al archivo JSON
def escribir_datos_tareas(datos: list[dict[str, Any]]) -> None:
    """
    Escribe una lista de datos en el archivo JSON especificado.

    Args:
        datos (list[dict[str, Any]]): Lista de diccionarios a escribir en el archivo.

    Raises:
        Exception: Si ocurre un error durante la escritura del archivo.
    """
    logger.debug("Escribiendo {len(datos)} elementos al archivo JSON: %s", DATA_JSON)
    try:
        with open(DATA_JSON, "w", encoding="utf-8") as file:
            json.dump(datos, file, indent=2, ensure_ascii=False)
        logger.debug("Datos escritos exitosamente")
    except Exception as e:
        logger.error("Error al escribir datos en {DATA_JSON}: %s", e)
        raise
