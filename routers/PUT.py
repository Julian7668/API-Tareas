import logging
from fastapi import HTTPException, APIRouter

from constants import Tarea
from utils import leer_json, escribir_datos

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
    """Actualiza completamente una tarea existente"""
    logger.info("Solicitud para actualizar tarea completa con ID: %s", tarea_id)
    datos = leer_json()

    for i, tarea_existente in enumerate(datos):
        if tarea_existente["id"] == tarea_id:
            # Mantener el ID original
            tarea_actualizada = tarea.model_dump()
            tarea_actualizada["id"] = tarea_id
            datos[i] = tarea_actualizada
            escribir_datos(datos)
            logger.info("Tarea %s actualizada completamente", tarea_id)
            return tarea_actualizada

    logger.warning("Tarea %s no encontrada para actualización completa", tarea_id)
    raise HTTPException(status_code=404, detail="Tarea no encontrada")
