"""
Router para operaciones PATCH

Este módulo contiene las rutas para actualizar parcialmente tareas existentes.
Permite modificar solo los campos especificados sin afectar los demás.

Funciones principales:
- actualizar_tarea_parcial(): Modifica solo campos específicos de una tarea

Características:
- Actualización parcial: solo campos proporcionados se modifican
- Campos opcionales: titulo, descripcion, completada
- Mantiene valores existentes para campos no especificados
"""

import logging
from typing import Any
from fastapi import HTTPException, APIRouter

from constants import Tarea, TareaUpdate
from utils import leer_json, escribir_datos_tareas

router: APIRouter = APIRouter()
logger: logging.Logger = logging.getLogger(__name__)


# PATCH - Actualizar parcialmente una tarea
@router.patch(
    "/{tarea_id}",
    response_model=Tarea,
    summary="Actualizar tarea parcialmente",
    description="Actualiza solo los campos especificados de una tarea existente. "
    "Los campos no proporcionados mantienen su valor actual.",
)
def actualizar_tarea_parcial(tarea_id: int, tarea_update: TareaUpdate) -> Tarea:
    """
    Actualiza parcialmente una tarea existente modificando solo los campos especificados.

    Esta función permite actualizaciones selectivas donde solo los campos proporcionados
    en la solicitud se modifican. Los campos no incluidos mantienen sus valores actuales.
    Es útil para operaciones como marcar una tarea como completada sin cambiar el título.

    Args:
        tarea_id (int): ID único de la tarea a actualizar parcialmente.
        tarea_update (TareaUpdate): Objeto con los campos a actualizar. Solo los campos
                                    no None serán modificados en la tarea existente.

    Returns:
        Tarea: La tarea actualizada con todos sus campos (modificados y no modificados).

    Raises:
        HTTPException: Si la tarea con el ID especificado no existe (404).

    Ejemplo:
        Para marcar una tarea como completada:
        PATCH /tareas/1
        {"completada": true}

        Para cambiar solo el título:
        PATCH /tareas/1
        {"titulo": "Nuevo título"}
    """
    logger.info("Solicitud para actualizar tarea parcial con ID: %s", tarea_id)
    datos: list[dict[str, Any]] = leer_json()

    for i, tarea_existente in enumerate(datos):
        if tarea_existente["id"] == tarea_id:
            # Aplicar actualizaciones solo a campos proporcionados
            if tarea_update.titulo is not None:
                datos[i]["titulo"] = tarea_update.titulo
            if tarea_update.descripcion is not None:
                datos[i]["descripcion"] = tarea_update.descripcion
            if tarea_update.completada is not None:
                datos[i]["completada"] = tarea_update.completada

            escribir_datos_tareas(datos)
            logger.info("Tarea %s actualizada parcialmente", tarea_id)
            return Tarea(**datos[i])

    logger.warning("Tarea %s no encontrada para actualización parcial", tarea_id)
    raise HTTPException(status_code=404, detail="Tarea no encontrada")
