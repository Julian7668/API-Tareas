"""
Rutas GET para tareas eliminadas

Este módulo define las rutas para consultar tareas eliminadas en el sistema.
Proporciona endpoints para obtener todas las tareas eliminadas o una específica por ID.

Funciones principales:
- obtener_tareas_eliminadas(): Lista todas las tareas eliminadas con timestamps
- obtener_tarea_eliminada(): Obtiene una tarea eliminada específica por su ID
"""

import logging
from typing import Any
from fastapi import APIRouter, Path, HTTPException
from constants import Tarea
from utils import leer_eliminadas_json

logger: logging.Logger = logging.getLogger(__name__)


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
    def obtener_tareas_eliminadas() -> list[dict[str, Any]]:
        """
        Obtiene todas las tareas eliminadas del sistema con información de auditoría.

        Returns:
            list[dict]: Lista de todas las tareas eliminadas incluyendo fecha de eliminación.

        Ejemplo de respuesta:
            [
                {
                    "id": 1,
                    "titulo": "Tarea eliminada",
                    "descripcion": "Esta tarea fue eliminada",
                    "completada": false,
                    "fecha_eliminacion": "2023-01-01T12:00:00"
                }
            ]
        """
        logger.info("Solicitud para obtener todas las tareas eliminadas")
        tareas_eliminadas: list[dict[str, Any]] = leer_eliminadas_json()
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
    ) -> dict[str, Any]:
        """
        Obtiene una tarea eliminada específica por su ID único.

        Args:
            tarea_id (int): ID único de la tarea eliminada a buscar. Debe ser mayor o igual a 1.

        Returns:
            dict: Los detalles completos de la tarea eliminada incluyendo fecha de eliminación.

        Raises:
            HTTPException: Si la tarea eliminada con el ID especificado no existe (404).

        Ejemplo de respuesta:
            {
                "id": 1,
                "titulo": "Tarea eliminada",
                "descripcion": "Esta tarea fue eliminada",
                "completada": false,
                "fecha_eliminacion": "2023-01-01T12:00:00"
            }
        """
        logger.info("Solicitud para obtener tarea eliminada con ID: %s", tarea_id)
        datos: list[dict[str, Any]] = leer_eliminadas_json()

        for tarea in datos:
            if tarea["id"] == tarea_id:
                logger.info("Tarea eliminada %s encontrada", tarea_id)
                return tarea

        logger.warning("Tarea eliminada %s no encontrada", tarea_id)
        raise HTTPException(status_code=404, detail="Tarea eliminada no encontrada")
