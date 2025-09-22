from datetime import datetime
from typing import Any
import json
import logging

from constants import DELETED_JSON
from .MDleer_eliminadas_json import leer_eliminadas_json

logger = logging.getLogger(__name__)


# Función para guardar tarea eliminada
def guardar_eliminada(tarea: dict[str, Any]) -> None:
    logger.info("Guardando tarea eliminada con ID: %s", tarea.get("id"))
    eliminadas: list[dict[str, Any]] = leer_eliminadas_json()
    # Agregar timestamp de cuando se eliminó
    tarea_eliminada: dict[str, Any] = tarea.copy()
    tarea_eliminada["fecha_eliminacion"] = datetime.now().isoformat()
    eliminadas.append(tarea_eliminada)

    try:
        with open(DELETED_JSON, "w", encoding="utf-8") as file:
            json.dump(eliminadas, file, indent=2, ensure_ascii=False)
        logger.info("Tarea eliminada guardada exitosamente")
    except Exception as e:
        logger.error("Error al guardar tarea eliminada: %s", e)
        raise
