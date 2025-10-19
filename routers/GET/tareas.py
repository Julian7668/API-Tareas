"""
Rutas GET para tareas activas
"""

import logging
from fastapi import HTTPException, APIRouter, Path
from constants import Tarea
from utils import leer_json

logger = logging.getLogger(__name__)


def registrar_rutas_tareas(router: APIRouter) -> None:
    """
    Registra las rutas relacionadas con tareas activas en el router proporcionado.

    Args:
        router: El router de FastAPI donde se registrarán las rutas.
    """

    @router.get(
        "/tareas",
        response_model=list[Tarea],
        summary="Obtener todas las tareas",
        description="Retorna una lista con todas las tareas activas almacenadas en el sistema.",
    )
    def obtener_tareas():
        logger.info("Solicitud para obtener todas las tareas")
        tareas = leer_json()
        logger.info("Tareas cargadas: %s items", len(tareas))
        return tareas

    @router.get(
        "/tareas/{tarea_id}",
        response_model=Tarea,
        summary="Obtener tarea por ID",
        description="Retorna los detalles de una tarea específica identificada por su ID único.",
    )
    def obtener_tarea(
        tarea_id: int = Path(..., description="ID único de la tarea a buscar", ge=1)
    ):
        logger.info("Solicitud para obtener tarea con ID: %s", tarea_id)
        datos = leer_json()

        for tarea in datos:
            if tarea["id"] == tarea_id:
                logger.info("Tarea %s encontrada", tarea_id)
                return tarea

        logger.warning("Tarea %s no encontrada", tarea_id)
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
