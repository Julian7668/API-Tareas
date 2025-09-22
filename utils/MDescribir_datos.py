from typing import Any
import json
import logging
from constants import DATA_JSON

logger = logging.getLogger(__name__)


# Función para escribir datos al archivo JSON
def escribir_datos(datos: list[dict[str, Any]]) -> None:
    logger.debug("Escribiendo {len(datos)} elementos al archivo JSON: %s", DATA_JSON)
    try:
        with open(DATA_JSON, "w", encoding="utf-8") as file:
            json.dump(datos, file, indent=2, ensure_ascii=False)
        logger.debug("Datos escritos exitosamente")
    except Exception as e:
        logger.error("Error al escribir datos en {DATA_JSON}: %s", e)
        raise
