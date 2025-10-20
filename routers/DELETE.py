"""
Router para operaciones DELETE

Este módulo contiene las rutas para eliminar tareas del sistema.
Las tareas eliminadas se mueven a un historial para auditoría y posible restauración.

Funciones principales:
- eliminar_tarea(): Elimina una tarea moviéndola al historial
- eliminar_tarea_completamente(): Elimina permanentemente del historial

Características:
- Auditoría completa con timestamps de eliminación
- Historial persistente de tareas eliminadas
- Eliminación permanente opcional
- Logging detallado de todas las operaciones
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

router: APIRouter = APIRouter()
logger: logging.Logger = logging.getLogger(__name__)


# DELETE - Eliminar una tarea
@router.delete(
    "/tareas/{tarea_id}",
    summary="Eliminar tarea",
    description="Elimina una tarea del sistema. La tarea se mueve a un historial de eliminadas "
    "con marca de tiempo para auditoría.",
)
def eliminar_tarea(tarea_id: int) -> dict[str, Any]:
    """
    Elimina una tarea específica del sistema moviéndola al historial de eliminadas.

    Esta función no elimina permanentemente la tarea, sino que la mueve a un
    historial de auditoría con marca de tiempo. La tarea puede ser restaurada
    posteriormente si es necesario.

    Args:
        tarea_id (int): ID único de la tarea a eliminar.

    Returns:
        dict[str, Any]: Diccionario con mensaje de confirmación y los datos
                        completos de la tarea eliminada.

    Raises:
        HTTPException: Si la tarea con el ID especificado no existe (404).

    Notas:
        - La tarea permanece accesible en el endpoint /eliminadas
        - Se registra timestamp de eliminación para auditoría
        - La tarea puede ser restaurada usando POST /eliminadas/{id}
    """
    logger.info("Solicitud para eliminar tarea con ID: %s", tarea_id)
    datos: list[dict[str, Any]] = leer_json()

    for i, tarea in enumerate(datos):
        if tarea["id"] == tarea_id:
            tarea_eliminada: dict[str, Any] = datos.pop(i)

            # Mover al historial de eliminadas con timestamp
            guardar_eliminada(tarea_eliminada)

            # Actualizar archivo de tareas activas
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

    Esta función realiza una eliminación irreversible del sistema. Una vez ejecutada,
    la tarea se pierde completamente y no puede ser recuperada. El ID queda liberado
    pero no se reutiliza automáticamente para mantener la integridad histórica.

    Args:
        tarea_id (int): ID único de la tarea a eliminar permanentemente del historial.

    Returns:
        dict[str, Any]: Diccionario con mensaje de confirmación, advertencia sobre
                       la irreversibilidad de la acción y datos de la tarea eliminada.

    Raises:
        HTTPException: Si la tarea no se encuentra en el historial de eliminadas (404).

    Advertencias:
        - Esta acción NO se puede deshacer
        - La tarea se pierde permanentemente del sistema
        - Solo debe usarse para limpieza definitiva de datos
    """
    logger.warning(
        "Solicitud de ELIMINACIÓN PERMANENTE para tarea con ID: %s", tarea_id
    )

    # Leer el historial completo de eliminadas
    datos_eliminadas: list[dict[str, Any]] = leer_eliminadas_json()

    # Buscar y eliminar la tarea específica
    for i, tarea in enumerate(datos_eliminadas):
        if tarea["id"] == tarea_id:
            tarea_eliminada: dict[str, Any] = datos_eliminadas.pop(i)

            # Persistir el historial actualizado
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
