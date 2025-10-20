"""
Módulo para guardar tareas eliminadas

Este módulo proporciona funciones para almacenar tareas eliminadas
con marca de tiempo para auditoría y recuperación histórica.
"""

from datetime import datetime
from typing import Any
import logging

from utils import leer_eliminadas_json, escribir_datos_eliminadas

logger = logging.getLogger(__name__)


# Función para guardar tarea eliminada
def guardar_eliminada(tarea_a_eliminar: dict[str, Any]) -> None:
    """
    Guarda una tarea eliminada en el archivo de historial con marca de tiempo.

    Args:
        tarea (dict[str, Any]): La tarea eliminada a guardar.

    Raises:
        Exception: Si ocurre un error durante la escritura del archivo.
    """
    logger.info("Guardando tarea eliminada con ID: %s", tarea_a_eliminar["id"])

    # Agregar timestamp de cuando se eliminó
    tarea_eliminada: dict[str, Any] = tarea_a_eliminar.copy()
    tarea_eliminada["fecha_eliminacion"] = datetime.now().isoformat()

    try:
        data = leer_eliminadas_json()

        # Insertar la tarea en la posición correcta para mantener el orden por ID
        id_tarea = tarea_eliminada["id"]
        for i, tarea in enumerate(data):
            if tarea["id"] > id_tarea:
                posicion = i
                break
        else:
            posicion = len(data)
        data.insert(posicion, tarea_eliminada)

        escribir_datos_eliminadas(data)
        logger.info("Tarea eliminada guardada exitosamente")
    except Exception as e:
        logger.error("Error al guardar tarea eliminada: %s", e)
        raise
