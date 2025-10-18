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
