"""
Router para operaciones DELETE

Este módulo contiene las rutas para eliminar tareas del sistema.
Las tareas eliminadas se mueven a un historial para auditoría.
"""

import logging
from typing import Any
from fastapi import APIRouter, HTTPException

from utils import leer_json, guardar_eliminada, escribir_datos

router = APIRouter()
logger = logging.getLogger(__name__)


# DELETE - Eliminar una tarea
@router.delete(
    "/{tarea_id}",
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
            escribir_datos(datos)

            logger.info("Tarea %s eliminada exitosamente", tarea_id)
            return {"mensaje": "Tarea eliminada exitosamente", "tarea": tarea_eliminada}

    logger.warning("Tarea %s no encontrada para eliminación", tarea_id)
    raise HTTPException(status_code=404, detail="Tarea no encontrada")
