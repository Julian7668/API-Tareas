"""
Módulo para escribir datos de tareas eliminadas en archivos JSON

Este módulo proporciona funciones para escribir datos estructurados
de tareas eliminadas en archivos JSON con formato legible y manejo de errores.

Funciones principales:
- escribir_datos_eliminadas(): Guarda lista de tareas eliminadas en archivo JSON

Características:
- Formato JSON legible con indentación
- Encoding UTF-8 para caracteres especiales
- Logging detallado de operaciones
- Manejo robusto de errores de escritura
"""

from typing import Any
import json
import logging
from constants import DELETED_JSON

logger = logging.getLogger(__name__)


# Función para escribir datos al archivo JSON
def escribir_datos_eliminadas(datos: list[dict[str, Any]]) -> None:
    """
    Escribe una lista de datos de tareas eliminadas en el archivo JSON de historial.

    Esta función serializa una lista de diccionarios representando tareas eliminadas
    en formato JSON con indentación legible y encoding UTF-8. Cada tarea incluye
    información de auditoría como timestamp de eliminación.

    Args:
        datos (list[dict[str, Any]]): Lista de diccionarios representando tareas eliminadas
                                    con sus timestamps a escribir en el archivo.

    Raises:
        Exception: Si ocurre un error durante la apertura o escritura del archivo.

    Notas:
        - Archivo objetivo: tareas_eliminadas.json en directorio data/
        - Formato: JSON con indentación de 2 espacios
        - Encoding: UTF-8 para caracteres especiales
        - Logging automático de operaciones y errores
        - Sobrescribe completamente el archivo existente

    Ejemplo:
        >>> eliminadas = [{"id": 1, "titulo": "Eliminada", "fecha_eliminacion": "2023-01-01T..."}]
        >>> escribir_datos_eliminadas(eliminadas)
        # Archivo tareas_eliminadas.json actualizado
    """
    logger.debug("Escribiendo {len(datos)} elementos al archivo JSON: %s", DELETED_JSON)
    try:
        with open(DELETED_JSON, "w", encoding="utf-8") as file:
            json.dump(datos, file, indent=2, ensure_ascii=False)
        logger.debug("Datos escritos exitosamente")
    except Exception as e:
        logger.error("Error al escribir datos en {DELETED_JSON}: %s", e)
        raise
