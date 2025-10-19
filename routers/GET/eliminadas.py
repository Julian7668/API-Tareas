"""
Rutas GET para tareas eliminadas
"""

import logging
from fastapi import APIRouter, Path, HTTPException
from constants import Tarea
from utils import leer_eliminadas_json

logger = logging.getLogger(__name__)


def registrar_rutas_eliminadas(router: APIRouter) -> None:
    """
    Registra las rutas relacionadas con tareas eliminadas en el router proporcionado.

    Args:
        router: El router de FastAPI donde se registrarán las rutas.
    """

    @router.get(
        "/eliminadas",
        summary="Obtener tareas eliminadas",
        description="Retorna una lista con todas las tareas eliminadas del sistema.",
    )
    def obtener_tareas_eliminadas():
        logger.info("Solicitud para obtener todas las tareas eliminadas")
        tareas_eliminadas = leer_eliminadas_json()
        logger.info("Tareas eliminadas cargadas: %s items", len(tareas_eliminadas))
        return tareas_eliminadas

    @router.get(
        "/eliminadas/{tarea_id}",
        response_model=Tarea,
        summary="Obtener tarea eliminada por ID",
        description="Retorna los detalles de una tarea eliminada específica identificada por su ID único.",
    )
    def obtener_tarea_eliminada(
        tarea_id: int = Path(
            ..., description="ID único de la tarea eliminada a buscar", ge=1
        )
    ):
        logger.info("Solicitud para obtener tarea eliminada con ID: %s", tarea_id)
        datos = leer_eliminadas_json()

        for tarea in datos:
            if tarea["id"] == tarea_id:
                logger.info("Tarea eliminada %s encontrada", tarea_id)
                return tarea

        logger.warning("Tarea eliminada %s no encontrada", tarea_id)
        raise HTTPException(status_code=404, detail="Tarea eliminada no encontrada")
