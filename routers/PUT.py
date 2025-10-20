"""
Router para operaciones PUT

Este módulo contiene las rutas para actualizar completamente tareas existentes.
Reemplaza todos los campos de la tarea con los nuevos valores proporcionados.

Funciones principales:
- actualizar_tarea_completa(): Reemplaza completamente una tarea existente

Características:
- Actualización completa: todos los campos deben ser proporcionados
- Mantiene el ID original de la tarea
- Validación completa de los nuevos datos
"""

import logging
from fastapi import HTTPException, APIRouter

from constants import Tarea
from utils import leer_json, escribir_datos_tareas

router = APIRouter()
logger = logging.getLogger(__name__)


# PUT - Actualizar una tarea completa
@router.put(
    "/{tarea_id}",
    response_model=Tarea,
    summary="Actualizar tarea completa",
    description="Reemplaza completamente una tarea existente con nuevos datos. "
    "Todos los campos deben ser proporcionados.",
)
def actualizar_tarea_completa(tarea_id: int, tarea: Tarea):
    """
    Actualiza completamente una tarea existente reemplazando todos sus campos.

    Esta función realiza una actualización completa (full update) donde todos
    los campos de la tarea deben ser proporcionados. El ID original se mantiene
    pero todos los demás campos (titulo, descripcion, completada) se reemplazan.

    Args:
        tarea_id (int): ID único de la tarea a actualizar.
        tarea (Tarea): Los nuevos datos completos para la tarea. Todos los campos
                        deben estar presentes y válidos.

    Returns:
        Tarea: La tarea completamente actualizada con el ID original.

    Raises:
        HTTPException: Si la tarea con el ID especificado no existe (404).

    Notas:
        - Si solo necesitas actualizar campos específicos, usa PATCH en su lugar
        - Todos los campos son requeridos en la solicitud
        - La validación Pydantic se aplica a los nuevos datos
    """
    logger.info("Solicitud para actualizar tarea completa con ID: %s", tarea_id)
    datos = leer_json()

    for i, tarea_existente in enumerate(datos):
        if tarea_existente["id"] == tarea_id:
            # Preparar actualización manteniendo el ID original
            tarea_actualizada = tarea.model_dump()
            tarea_actualizada["id"] = tarea_id
            datos[i] = tarea_actualizada
            escribir_datos_tareas(datos)
            logger.info("Tarea %s actualizada completamente", tarea_id)
            return tarea_actualizada

    logger.warning("Tarea %s no encontrada para actualización completa", tarea_id)
    raise HTTPException(status_code=404, detail="Tarea no encontrada")
