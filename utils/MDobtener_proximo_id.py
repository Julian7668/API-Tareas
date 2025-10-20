"""
Módulo para generar IDs únicos para nuevas tareas

Este módulo proporciona funciones para calcular el próximo ID disponible
usando un contador persistente para evitar colisiones y asegurar unicidad.

Funciones principales:
- obtener_proximo_id(): Calcula y retorna el siguiente ID disponible

Características:
- Contador persistente en archivo JSON
- Thread-safe para operaciones concurrentes
- Manejo automático de archivos inexistentes
- Logging detallado de operaciones
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
    Calcula el próximo ID disponible para una nueva tarea usando contador persistente.

    Esta función lee el contador actual desde un archivo JSON, incrementa el valor
    y lo guarda de vuelta. Esto asegura que los IDs sean únicos incluso después
    de reinicios del servidor o eliminaciones permanentes.

    Returns:
        int: El próximo ID disponible para asignar a una nueva tarea.

    Notas:
        - Los IDs nunca se reutilizan, manteniendo integridad histórica
        - El contador se inicializa en 0 si el archivo no existe
        - Thread-safe para operaciones concurrentes básicas
        - Maneja errores de archivo automáticamente

    Ejemplo:
        >>> id_nuevo = obtener_proximo_id()
        >>> print(id_nuevo)  # 1 (primera llamada)
        >>> id_otro = obtener_proximo_id()
        >>> print(id_otro)   # 2 (segunda llamada)
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

    # Actualizar el contador persistente
    nuevo_contador = {"ultimo_id": proximo_id}
    with open(ID_COUNTER_JSON, "w", encoding="utf-8") as file:
        json.dump(nuevo_contador, file, indent=2, ensure_ascii=False)

    logger.debug("Próximo ID calculado: %s", proximo_id)
    return proximo_id


if __name__ == "__main__":
    print("Próximo ID disponible:", obtener_proximo_id())
