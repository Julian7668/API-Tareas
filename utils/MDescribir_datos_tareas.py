"""
Módulo para escribir datos en archivos JSON

Este módulo proporciona funciones para escribir datos estructurados
en archivos JSON con formato legible y manejo de errores.

Funciones principales:
- escribir_datos_tareas(): Guarda lista de tareas en archivo JSON

Características:
- Formato JSON legible con indentación
- Encoding UTF-8 para caracteres especiales
- Logging detallado de operaciones
- Manejo robusto de errores de escritura
"""

from typing import Any
import json
import logging
from constants import DATA_JSON

logger = logging.getLogger(__name__)


# Función para escribir datos al archivo JSON
def escribir_datos_tareas(datos: list[dict[str, Any]]) -> None:
    """
    Escribe una lista de datos de tareas en el archivo JSON principal.

    Esta función serializa una lista de diccionarios representando tareas
    en formato JSON con indentación legible y encoding UTF-8 para soporte
    completo de caracteres especiales.

    Args:
        datos (list[dict[str, Any]]): Lista de diccionarios representando tareas
                                    a escribir en el archivo.

    Raises:
        Exception: Si ocurre un error durante la apertura o escritura del archivo.

    Notas:
        - Archivo objetivo: tareas.json en directorio data/
        - Formato: JSON con indentación de 2 espacios
        - Encoding: UTF-8 para caracteres especiales
        - Logging automático de operaciones y errores
        - Sobrescribe completamente el archivo existente

    Ejemplo:
        >>> tareas = [{"id": 1, "titulo": "Tarea 1", "descripcion": "...", "completada": False}]
        >>> escribir_datos_tareas(tareas)
        # Archivo tareas.json actualizado
    """
    logger.debug("Escribiendo {len(datos)} elementos al archivo JSON: %s", DATA_JSON)
    try:
        with open(DATA_JSON, "w", encoding="utf-8") as file:
            json.dump(datos, file, indent=2, ensure_ascii=False)
        logger.debug("Datos escritos exitosamente")
    except Exception as e:
        logger.error("Error al escribir datos en {DATA_JSON}: %s", e)
        raise
