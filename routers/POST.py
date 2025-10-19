"""
Router para operaciones POST

Este módulo contiene las rutas para crear nuevas tareas en el sistema.
Asigna automáticamente IDs únicos a las nuevas tareas.
"""

import logging
from fastapi import APIRouter, HTTPException

from constants import Tarea
from utils import leer_json, obtener_proximo_id, escribir_datos, leer_eliminadas_json

router = APIRouter()
logger = logging.getLogger(__name__)


# POST - Crear una nueva tarea
@router.post(
    "",
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
    Crea una nueva tarea en el sistema.

    Args:
        tarea (Tarea): Los datos de la nueva tarea (sin ID, se asigna automáticamente).

    Returns:
        Tarea: La tarea creada con su ID asignado.
    """
    logger.info("Solicitud para crear tarea: %s", tarea.titulo)
    datos = leer_json()

    # Asignar ID automáticamente
    nueva_tarea = tarea.model_dump()
    nueva_tarea["id"] = obtener_proximo_id()
    logger.info("ID asignado: %s", nueva_tarea["id"])

    # Agregar la nueva tarea a los datos
    datos.append(nueva_tarea)
    escribir_datos(datos)
    logger.info("Tarea creada exitosamente con ID: %s", nueva_tarea["id"])
    logger.debug("Retornando nueva_tarea: %s", nueva_tarea)
    return nueva_tarea


# POST - Restaurar una tarea eliminada
@router.post(
    "/restaurar/{tarea_id}",
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
    Restaura una tarea eliminada moviéndola de vuelta a las tareas activas.

    Args:
        tarea_id (int): ID de la tarea a restaurar.

    Returns:
        Tarea: La tarea restaurada.

    Raises:
        HTTPException: Si la tarea no se encuentra en las eliminadas.
    """
    logger.info("Solicitud para restaurar tarea con ID: %s", tarea_id)

    # Leer tareas activas y eliminadas
    datos = leer_json()
    eliminadas = leer_eliminadas_json()

    # Buscar la tarea en eliminadas
    tarea_a_restaurar = None
    for i, tarea in enumerate(eliminadas):
        if tarea["id"] == tarea_id:
            tarea_a_restaurar = eliminadas.pop(i)
            break

    if not tarea_a_restaurar:
        logger.warning("Tarea %s no encontrada en eliminadas", tarea_id)
        raise HTTPException(status_code=404, detail="Tarea no encontrada en eliminadas")

    # Remover la fecha de eliminación y agregar a tareas activas
    tarea_restaurada = {
        k: v for k, v in tarea_a_restaurar.items() if k != "fecha_eliminacion"
    }
    datos.append(tarea_restaurada)

    # Guardar cambios
    escribir_datos(datos)
    # Actualizar archivo de eliminadas (sin la tarea restaurada)
    import json
    from constants import DELETED_JSON

    with open(DELETED_JSON, "w", encoding="utf-8") as file:
        json.dump(eliminadas, file, indent=2, ensure_ascii=False)

    logger.info("Tarea %s restaurada exitosamente", tarea_id)
    return tarea_restaurada
