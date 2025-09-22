import logging
from fastapi import HTTPException, APIRouter

from constants import Tarea, TareaUpdate
from utils import leer_json, escribir_datos

router = APIRouter()
logger = logging.getLogger(__name__)


# PATCH - Actualizar parcialmente una tarea
@router.patch(
    "/{tarea_id}",
    response_model=Tarea,
    summary="Actualizar tarea parcialmente",
    description="Actualiza solo los campos especificados de una tarea existente. "
    "Los campos no proporcionados mantienen su valor actual.",
)
def actualizar_tarea_parcial(tarea_id: int, tarea_update: TareaUpdate):
    """Actualiza parcialmente una tarea existente"""
    logger.info("Solicitud para actualizar tarea parcial con ID: %s", tarea_id)
    datos = leer_json()

    for i, tarea_existente in enumerate(datos):
        if tarea_existente["id"] == tarea_id:
            # Actualizar solo los campos proporcionados
            if tarea_update.titulo is not None:
                datos[i]["titulo"] = tarea_update.titulo
            if tarea_update.descripcion is not None:
                datos[i]["descripcion"] = tarea_update.descripcion
            if tarea_update.completada is not None:
                datos[i]["completada"] = tarea_update.completada

            escribir_datos(datos)
            logger.info("Tarea %s actualizada parcialmente", tarea_id)
            return datos[i]

    logger.warning("Tarea %s no encontrada para actualización parcial", tarea_id)
    raise HTTPException(status_code=404, detail="Tarea no encontrada")
