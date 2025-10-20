"""
Módulo para leer tareas eliminadas desde archivos JSON

Este módulo proporciona funciones para cargar tareas eliminadas
desde archivos JSON con manejo robusto de errores.

Funciones principales:
- leer_eliminadas_json(): Carga datos desde el archivo JSON de tareas eliminadas

Características:
- Manejo automático de archivos inexistentes
- Recuperación de errores de decodificación JSON
- Logging detallado de operaciones
- Retorno de lista vacía en caso de error
"""

import os
from typing import Any
import json
import logging
from constants import DELETED_JSON

logger = logging.getLogger(__name__)


# Función para leer tareas eliminadas
def leer_eliminadas_json() -> list[dict[str, Any]]:
    """
    Lee las tareas eliminadas desde el archivo JSON de historial.

    Esta función carga todas las tareas eliminadas desde el archivo de auditoría.
    Incluye información de timestamps de eliminación para cada tarea.
    Maneja automáticamente casos donde el archivo no existe o contiene JSON malformado.

    Returns:
        list[dict[str, Any]]: Lista de diccionarios representando las tareas eliminadas
                            con sus timestamps. Retorna lista vacía si el archivo no existe
                            o hay error de formato.

    Notas:
        - Archivo objetivo: tareas_eliminadas.json en directorio data/
        - Cada tarea incluye campo 'fecha_eliminacion' con timestamp ISO
        - Retorna lista vacía en lugar de lanzar excepciones
        - Logging automático de operaciones y errores

    Ejemplo:
        >>> eliminadas = leer_eliminadas_json()
        >>> for tarea in eliminadas:
        ...     print(f"Tarea {tarea['id']} eliminada en {tarea['fecha_eliminacion']}")
    """
    logger.debug("Leyendo archivo JSON de eliminadas: %s", DELETED_JSON)
    if not os.path.exists(DELETED_JSON):
        logger.warning("Archivo %s no existe, retornando lista vacía", DELETED_JSON)
        return []
    try:
        with open(DELETED_JSON, "r", encoding="utf-8") as file:
            data = json.load(file)
            logger.debug("Tareas eliminadas leídas: %s elementos", len(data))
            return data
    except json.JSONDecodeError as e:
        logger.error("Error al decodificar JSON en {DELETED_JSON}: %s", e)
        return []
