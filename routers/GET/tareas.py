"""
Rutas GET para tareas activas

Este módulo define las rutas para consultar tareas activas en el sistema.
Proporciona endpoints para obtener todas las tareas o una tarea específica por ID.

Funciones principales:
- obtener_tareas(): Lista todas las tareas activas
- obtener_tarea(): Obtiene una tarea específica por su ID
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
        """
        Obtiene todas las tareas activas del sistema.

        Returns:
            list[Tarea]: Lista de todas las tareas activas con sus detalles completos.

        Ejemplo de respuesta:
            [
                {
                    "id": 1,
                    "titulo": "Aprender FastAPI",
                    "descripcion": "Estudiar conceptos básicos",
                    "completada": false
                }
            ]
        """
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
        """
        Obtiene una tarea específica por su ID único.

        Args:
            tarea_id (int): ID único de la tarea a buscar. Debe ser mayor o igual a 1.

        Returns:
            Tarea: Los detalles completos de la tarea encontrada.

        Raises:
            HTTPException: Si la tarea con el ID especificado no existe (404).

        Ejemplo de respuesta:
            {
                "id": 1,
                "titulo": "Aprender FastAPI",
                "descripcion": "Estudiar conceptos básicos",
                "completada": false
            }
        """
        logger.info("Solicitud para obtener tarea con ID: %s", tarea_id)
        datos = leer_json()

        for tarea in datos:
            if tarea["id"] == tarea_id:
                logger.info("Tarea %s encontrada", tarea_id)
                return tarea

        logger.warning("Tarea %s no encontrada", tarea_id)
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
