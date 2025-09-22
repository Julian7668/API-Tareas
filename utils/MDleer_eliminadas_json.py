import os
from typing import Any
import json
import logging
from constants import DELETED_JSON

logger = logging.getLogger(__name__)


# Función para leer tareas eliminadas
def leer_eliminadas_json() -> list[dict[str, Any]]:
    logger.debug("Leyendo archivo JSON de eliminadas: %s", DELETED_JSON)
    if not os.path.exists(DELETED_JSON):
        logger.warning("Archivo %s no existe, retornando lista vacía", DELETED_JSON)
        return []
    try:
        with open(DELETED_JSON, "r", encoding="utf-8") as file:
            data = json.load(file)
            logger.debug("Tareas eliminadas leídas: %s elementos", len(data))
            return data
    except json.JSONDecodeError as e:
        logger.error("Error al decodificar JSON en {DELETED_JSON}: %s", e)
        return []
