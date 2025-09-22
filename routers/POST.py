import logging
from fastapi import APIRouter

from constants import Tarea
from utils import leer_json, obtener_proximo_id, escribir_datos

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
    """Crea una nueva tarea"""
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

    return nueva_tarea
