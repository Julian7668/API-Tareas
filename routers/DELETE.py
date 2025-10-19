"""
Router para operaciones DELETE

Este módulo contiene las rutas para eliminar tareas del sistema.
Las tareas eliminadas se mueven a un historial para auditoría.
"""

import logging
from typing import Any
from fastapi import APIRouter, HTTPException

# import sys
# import os

# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils import (
    leer_json,
    guardar_eliminada,
    escribir_datos_tareas,
    leer_eliminadas_json,
    escribir_datos_eliminadas,
)

router = APIRouter()
logger = logging.getLogger(__name__)


# DELETE - Eliminar una tarea
@router.delete(
    "/tareas/{tarea_id}",
    summary="Eliminar tarea",
    description="Elimina una tarea del sistema. La tarea se mueve a un historial de eliminadas "
    "con marca de tiempo para auditoría.",
)
def eliminar_tarea(tarea_id: int) -> dict[str, Any]:
    """
    Elimina una tarea específica del sistema.

    Args:
        tarea_id (int): ID de la tarea a eliminar.

    Returns:
        dict[str, Any]: Diccionario con mensaje de confirmación y datos de la tarea eliminada.

    Raises:
        HTTPException: Si la tarea no se encuentra (404).
    """
    logger.info("Solicitud para eliminar tarea con ID: %s", tarea_id)
    datos = leer_json()

    for i, tarea in enumerate(datos):
        if tarea["id"] == tarea_id:
            tarea_eliminada = datos.pop(i)

            # Guardar en historial de eliminadas
            guardar_eliminada(tarea_eliminada)

            # Actualizar archivo principal
            escribir_datos_tareas(datos)

            logger.info("Tarea %s eliminada exitosamente", tarea_id)
            return {"mensaje": "Tarea eliminada exitosamente", "tarea": tarea_eliminada}

    logger.warning("Tarea %s no encontrada para eliminación", tarea_id)
    raise HTTPException(status_code=404, detail="Tarea no encontrada")


@router.delete(
    "/eliminadas/{tarea_id}!",
    summary="Eliminar tarea permanentemente del historial",
    description="Elimina una tarea del historial de eliminadas de forma PERMANENTE. "
    "Esta acción NO se puede deshacer. El ID quedará libre pero no se reutilizará "
    "para mantener la integridad histórica del sistema.",
)
def eliminar_tarea_completamente(tarea_id: int) -> dict[str, Any]:
    """
    Elimina permanentemente una tarea del historial de eliminadas.

    Esta función es para limpiar completamente el sistema de tareas que
    ya no necesitas en ningún registro. El ID se perderá pero no se reutilizará
    automáticamente, manteniendo la secuencia incremental intacta.

    Args:
        tarea_id (int): ID de la tarea a eliminar permanentemente.

    Returns:
        dict[str, Any]: Mensaje de confirmación con datos de la tarea eliminada.

    Raises:
        HTTPException: Si la tarea no se encuentra en el historial (404).
    """
    logger.warning(
        "Solicitud de ELIMINACIÓN PERMANENTE para tarea con ID: %s", tarea_id
    )

    # Leer el historial de eliminadas
    datos_eliminadas = leer_eliminadas_json()

    # Buscar y eliminar la tarea
    for i, tarea in enumerate(datos_eliminadas):
        if tarea["id"] == tarea_id:
            tarea_eliminada = datos_eliminadas.pop(i)

            # Guardar el archivo actualizado de eliminadas
            try:
                escribir_datos_eliminadas(datos_eliminadas)

                logger.warning(
                    "Tarea %s ELIMINADA PERMANENTEMENTE del historial", tarea_id
                )
                return {
                    "mensaje": "Tarea eliminada permanentemente del sistema",
                    "advertencia": "Esta acción no se puede deshacer",
                    "tarea": tarea_eliminada,
                }
            except Exception as e:
                logger.error("Error al guardar cambios: %s", e)
                raise

    logger.warning(
        "Tarea %s no encontrada en historial para eliminación permanente", tarea_id
    )
    raise HTTPException(
        status_code=404, detail="Tarea no encontrada en el historial de eliminadas"
    )
