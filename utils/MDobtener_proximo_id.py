"""
Módulo para generar IDs únicos para nuevas tareas

Este módulo proporciona funciones para calcular el próximo ID disponible
usando un contador persistente para evitar colisiones.
"""

import json
import logging

# import sys
# import os

# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from constants import ID_COUNTER_JSON

logger = logging.getLogger(__name__)


# Función para obtener el próximo ID
def obtener_proximo_id() -> int:
    """
    Calcula el próximo ID disponible para una nueva tarea.

    Usa un contador persistente para asegurar que los IDs sean únicos
    y no se repitan incluso después de eliminaciones permanentes.

    Returns:
        int: El próximo ID disponible.
    """
    logger.debug("Obteniendo próximo ID disponible")

    try:
        with open(ID_COUNTER_JSON, "r", encoding="utf-8") as file:
            contador = json.load(file)
            ultimo_id = contador.get("ultimo_id", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        logger.warning("Archivo de contador no encontrado, inicializando en 0")
        ultimo_id = 0

    proximo_id = ultimo_id + 1

    # Actualizar el contador
    nuevo_contador = {"ultimo_id": proximo_id}
    with open(ID_COUNTER_JSON, "w", encoding="utf-8") as file:
        json.dump(nuevo_contador, file, indent=2, ensure_ascii=False)

    logger.debug("Próximo ID calculado: %s", proximo_id)
    return proximo_id


if __name__ == "__main__":
    print("Próximo ID disponible:", obtener_proximo_id())
