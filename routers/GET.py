"""
Router para operaciones GET

Este módulo contiene las rutas para obtener tareas del sistema.
Permite obtener todas las tareas o una tarea específica por ID.
"""

import logging
from fastapi import HTTPException, APIRouter, Path

from constants import Tarea
from utils import leer_json, leer_eliminadas_json

router = APIRouter()
logger = logging.getLogger(__name__)


# GET - Obtener todas las tareas
@router.get(
    "/tareas",
    response_model=list[Tarea],
    summary="Obtener todas las tareas",
    description="Retorna una lista con todas las tareas activas almacenadas en el sistema. "
    "Las tareas se devuelven en el orden en que están almacenadas.",
)
def obtener_tareas():
    """
    Obtiene todas las tareas activas almacenadas en el sistema.

    Returns:
        list[Tarea]: Lista de todas las tareas activas.
    """
    logger.info("Solicitud para obtener todas las tareas")
    tareas = leer_json()
    logger.info("Tareas cargadas: %s items", len(tareas))
    return tareas


# GET - Obtener una tarea específica por ID
@router.get(
    "/tareas/{tarea_id}",
    response_model=Tarea,
    summary="Obtener tarea por ID",
    description="Retorna los detalles de una tarea específica identificada por su ID único. "
    "Si la tarea ha sido eliminada, retorna un error 410 con la fecha de eliminación. "
    "Si nunca existió, retorna un error 404.",
    responses={
        200: {
            "description": "Tarea encontrada exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "titulo": "Aprender FastAPI",
                        "descripcion": "Estudiar los conceptos básicos",
                        "completada": False,
                    }
                }
            },
        },
        404: {
            "description": "Tarea no encontrada",
            "content": {
                "application/json": {"example": {"detail": "Tarea no encontrada"}}
            },
        },
        410: {
            "description": "Tarea eliminada",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "La tarea con ID 1 fue eliminada el 2023-01-01"
                    }
                }
            },
        },
    },
)
def obtener_tarea(
    tarea_id: int = Path(..., description="ID único de la tarea a buscar", ge=1)
):
    """
    Obtiene una tarea específica por su ID.

    Args:
        tarea_id (int): ID único de la tarea a buscar (debe ser >= 1).

    Returns:
        Tarea: Los detalles de la tarea encontrada.

    Raises:
        HTTPException: 404 si la tarea no existe, 410 si fue eliminada.
    """
    logger.info("Solicitud para obtener tarea con ID: %s", tarea_id)
    datos = leer_json()

    # Buscar en tareas activas
    for tarea in datos:
        if tarea["id"] == tarea_id:
            logger.info("Tarea %s encontrada en tareas activas", tarea_id)
            return tarea

    logger.info("Tarea %s no encontrada en activas, buscando en eliminadas", tarea_id)
    # Si no está en activas, buscar en eliminadas
    eliminadas = leer_eliminadas_json()
    for tarea in eliminadas:
        if tarea["id"] == tarea_id:
            logger.warning(
                "Tarea %s encontrada en eliminadas, devolviendo 410", tarea_id
            )
            raise HTTPException(
                status_code=410,  # 410 = Gone (recurso eliminado)
                detail=f"La tarea con ID {tarea_id} fue eliminada el {tarea['fecha_eliminacion'][:10]}",
            )

    # Si no está en ningún lado, nunca existió
    logger.warning("Tarea %s no encontrada en ningún archivo", tarea_id)
    raise HTTPException(status_code=404, detail="Tarea no encontrada")


# GET - Obtener todas las tareas eliminadas
@router.get(
    "/eliminadas-json",
    summary="Obtener tareas eliminadas",
    description="Retorna una lista con todas las tareas eliminadas del sistema, "
    "incluyendo la fecha de eliminación.",
)
def obtener_tareas_eliminadas():
    """
    Obtiene todas las tareas eliminadas del sistema.

    Returns:
        list[dict]: Lista de tareas eliminadas con fecha de eliminación.
    """
    logger.info("Solicitud para obtener todas las tareas eliminadas")
    tareas_eliminadas = leer_eliminadas_json()
    logger.info("Tareas eliminadas cargadas: %s items", len(tareas_eliminadas))
    return tareas_eliminadas
