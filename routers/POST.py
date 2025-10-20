"""
Router para operaciones POST

Este módulo contiene las rutas para crear nuevas tareas en el sistema
y restaurar tareas previamente eliminadas.

Funciones principales:
- crear_tarea(): Crea una nueva tarea asignando ID automáticamente
- restaurar_tarea(): Restaura una tarea eliminada a las tareas activas

Características:
- Asignación automática de IDs únicos usando contador persistente
- Validación completa de datos usando modelos Pydantic
- Logging detallado de todas las operaciones
"""

import logging
from fastapi import APIRouter, HTTPException

from constants import Tarea
from utils import (
    leer_json,
    obtener_proximo_id,
    escribir_datos_tareas,
    leer_eliminadas_json,
)

router = APIRouter()
logger = logging.getLogger(__name__)


# POST - Crear una nueva tarea
@router.post(
    "/tareas",
    response_model=Tarea,
    summary="Crear nueva tarea",
    description="Crea una nueva tarea en el sistema. El ID se asigna automáticamente. "
    "Los campos título y descripción son obligatorios y deben cumplir con las validaciones.",
    status_code=200,
    responses={
        200: {
            "description": "Tarea creada exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "id": 3,
                        "titulo": "Nueva tarea",
                        "descripcion": "Descripción de la nueva tarea",
                        "completada": False,
                    }
                }
            },
        },
        422: {
            "description": "Datos de entrada inválidos",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "titulo"],
                                "msg": "ensure this value has at least 1 characters",
                                "type": "value_error.const",
                            }
                        ]
                    }
                }
            },
        },
    },
)
def crear_tarea(tarea: Tarea):
    """
    Crea una nueva tarea en el sistema asignando automáticamente un ID único.

    El ID se genera usando un contador persistente que asegura unicidad
    incluso después de eliminaciones. La tarea se valida completamente
    antes de ser almacenada.

    Args:
        tarea (Tarea): Los datos de la nueva tarea sin ID (se asigna automáticamente).
                      Debe incluir titulo, descripcion y opcionalmente completada.

    Returns:
        Tarea: La tarea creada completa con su ID asignado.

    Raises:
        HTTPException: Si hay errores de validación en los datos proporcionados.

    Ejemplo:
        >>> tarea = Tarea(titulo="Nueva tarea", descripcion="Descripción")
        >>> creada = crear_tarea(tarea)
        >>> print(creada.id)  # ID asignado automáticamente
    """
    logger.info("Solicitud para crear tarea: %s", tarea.titulo)
    datos = leer_json()

    # Asignar ID automáticamente usando contador persistente
    nueva_tarea = tarea.model_dump()
    nueva_tarea["id"] = obtener_proximo_id()
    logger.info("ID asignado: %s", nueva_tarea["id"])

    # Agregar la nueva tarea a los datos y persistir
    datos.append(nueva_tarea)
    escribir_datos_tareas(datos)
    logger.info("Tarea creada exitosamente con ID: %s", nueva_tarea["id"])
    logger.debug("Retornando nueva_tarea: %s", nueva_tarea)
    return nueva_tarea


# POST - Restaurar una tarea eliminada
@router.post(
    "/eliminadas/{tarea_id}",
    response_model=Tarea,
    summary="Restaurar tarea eliminada",
    description="Restaura una tarea previamente eliminada, moviéndola de vuelta a las tareas activas.",
    status_code=200,
    responses={
        200: {
            "description": "Tarea restaurada exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "titulo": "Tarea restaurada",
                        "descripcion": "Esta tarea fue restaurada",
                        "completada": False,
                    }
                }
            },
        },
        404: {
            "description": "Tarea no encontrada en eliminadas",
            "content": {
                "application/json": {
                    "example": {"detail": "Tarea no encontrada en eliminadas"}
                }
            },
        },
    },
)
def restaurar_tarea(tarea_id: int):
    """
    Restaura una tarea previamente eliminada moviéndola de vuelta a las tareas activas.

    La tarea se busca en el historial de eliminadas, se remueve la marca de tiempo
    de eliminación y se inserta en la posición correcta del archivo de tareas activas
    para mantener el orden por ID.

    Args:
        tarea_id (int): ID único de la tarea a restaurar.

    Returns:
        Tarea: La tarea restaurada sin la fecha de eliminación.

    Raises:
        HTTPException: Si la tarea no se encuentra en el historial de eliminadas (404).

    Notas:
        - La tarea restaurada mantiene su ID original
        - Se inserta en orden para preservar la secuencia por ID
        - El historial de eliminadas se actualiza automáticamente
    """
    logger.info("Solicitud para restaurar tarea con ID: %s", tarea_id)

    # Leer datos actuales de tareas activas y eliminadas
    datos = leer_json()
    eliminadas = leer_eliminadas_json()

    # Buscar y extraer la tarea del historial de eliminadas
    tarea_a_restaurar = None
    for i, tarea in enumerate(eliminadas):
        if tarea["id"] == tarea_id:
            tarea_a_restaurar = eliminadas.pop(i)
            break

    if not tarea_a_restaurar:
        logger.warning("Tarea %s no encontrada en eliminadas", tarea_id)
        raise HTTPException(status_code=404, detail="Tarea no encontrada en eliminadas")

    # Limpiar la tarea removiendo metadata de eliminación
    tarea_restaurada = {
        k: v for k, v in tarea_a_restaurar.items() if k != "fecha_eliminacion"
    }

    # Insertar en posición correcta para mantener orden por ID
    id_restaurado = tarea_restaurada["id"]
    for i, tarea in enumerate(datos):
        if tarea["id"] > id_restaurado:
            posicion = i
            break
    else:
        posicion = len(datos)
    datos.insert(posicion, tarea_restaurada)

    # Persistir cambios en ambos archivos
    escribir_datos_tareas(datos)

    # Actualizar archivo de eliminadas (sin la tarea restaurada)
    import json
    from constants import DELETED_JSON

    with open(DELETED_JSON, "w", encoding="utf-8") as file:
        json.dump(eliminadas, file, indent=2, ensure_ascii=False)

    logger.info("Tarea %s restaurada exitosamente", tarea_id)
    return tarea_restaurada
