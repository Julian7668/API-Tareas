from typing import Any
import logging

from utils import leer_json, leer_eliminadas_json

logger = logging.getLogger(__name__)


# Función para obtener el próximo ID
def obtener_proximo_id() -> int:
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
