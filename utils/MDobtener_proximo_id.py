"""
Módulo para generar IDs únicos para nuevas tareas

Este módulo proporciona funciones para calcular el próximo ID disponible
basándose en tareas activas y eliminadas para evitar colisiones.
"""

from typing import Any
import logging

from utils import leer_json, leer_eliminadas_json

logger = logging.getLogger(__name__)


# Función para obtener el próximo ID
def obtener_proximo_id() -> int:
    """
    Calcula el próximo ID disponible para una nueva tarea.

    Revisa tanto las tareas activas como las eliminadas para encontrar
    el ID más alto y retorna el siguiente número disponible.

    Returns:
        int: El próximo ID disponible (comienza en 1 si no hay tareas).
    """
    logger.debug("Obteniendo próximo ID disponible")
    datos: list[dict[str, Any]] = leer_json()
    datos_eliminados: list[dict[str, Any]] = leer_eliminadas_json()

    # Combinar todos los IDs existentes
    todos_los_ids: list[int] = []

    if datos:
        todos_los_ids.extend(tarea["id"] for tarea in datos)
    if datos_eliminados:
        todos_los_ids.extend(tarea["id"] for tarea in datos_eliminados)

    proximo_id = max(todos_los_ids) + 1 if todos_los_ids else 1
    logger.debug("Próximo ID calculado: %s", proximo_id)
    return proximo_id
