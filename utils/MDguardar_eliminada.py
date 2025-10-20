"""
Módulo para guardar tareas eliminadas

Este módulo proporciona funciones para almacenar tareas eliminadas
con marca de tiempo para auditoría y recuperación histórica.

Funciones principales:
- guardar_eliminada(): Almacena una tarea en el historial de eliminadas

Características:
- Timestamp automático de eliminación
- Mantenimiento del orden por ID
- Logging detallado de operaciones
- Integración con sistema de archivos JSON
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

    Esta función toma una tarea eliminada, le agrega un timestamp de eliminación
    y la almacena en el archivo de historial manteniendo el orden por ID.
    Esto permite auditoría completa y recuperación histórica de eliminaciones.

    Args:
        tarea_a_eliminar (dict[str, Any]): La tarea que fue eliminada, con todos sus campos originales.

    Raises:
        Exception: Si ocurre un error durante la lectura/escritura de archivos.

    Notas:
        - Agrega automáticamente campo 'fecha_eliminacion' con timestamp ISO 8601
        - Mantiene orden ascendente por ID en el archivo de historial
        - Logging automático de operaciones exitosas y errores
        - Parte integral del sistema de auditoría de eliminaciones

    Ejemplo:
        >>> tarea = {"id": 1, "titulo": "Tarea eliminada", "descripcion": "...", "completada": False}
        >>> guardar_eliminada(tarea)
        # La tarea se guarda con fecha_eliminacion agregada
    """
    logger.info("Guardando tarea eliminada con ID: %s", tarea_a_eliminar["id"])

    # Agregar timestamp de eliminación para auditoría
    tarea_eliminada: dict[str, Any] = tarea_a_eliminar.copy()
    tarea_eliminada["fecha_eliminacion"] = datetime.now().isoformat()

    try:
        data = leer_eliminadas_json()

        # Insertar en posición correcta para mantener orden por ID
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
