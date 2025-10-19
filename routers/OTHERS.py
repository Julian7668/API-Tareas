"""
Router para operaciones generales

Este módulo contiene rutas generales que no pertenecen a operaciones CRUD específicas.
Incluye la ruta raíz para servir la aplicación frontend.
"""

import os
import logging
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/")
def get_aplicacion():
    """
    Sirve la aplicación frontend (index.html).

    Returns:
        FileResponse: El archivo HTML de la aplicación frontend.
    """
    logger.info("Solicitud para servir la aplicación")
    static_path = os.path.join(os.path.dirname(__file__), "../static/index.html")
    return FileResponse(static_path)


@router.get("/eliminadas")
def get_eliminadas():
    """
    Sirve la página de tareas eliminadas.

    Returns:
        FileResponse: El archivo HTML de tareas eliminadas.
    """
    logger.info("Solicitud para servir página de eliminadas")
    static_path = os.path.join(os.path.dirname(__file__), "../static/eliminadas.html")
    return FileResponse(static_path)
