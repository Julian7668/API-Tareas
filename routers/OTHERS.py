"""
Router para operaciones generales

Este módulo contiene rutas generales que no pertenecen a operaciones CRUD específicas.
Incluye la ruta raíz para servir la aplicación frontend y otras utilidades.

Funciones principales:
- get_aplicacion(): Sirve la interfaz web principal

Características:
- Servidor de archivos estáticos integrado
- Punto de entrada principal para la aplicación web
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
    Sirve la aplicación frontend principal (index.html).

    Esta ruta es el punto de entrada principal para la interfaz web de usuario.
    Sirve el archivo HTML que contiene la aplicación de gestión de tareas.

    Returns:
        FileResponse: El archivo HTML de la aplicación frontend con tipo MIME correcto.

    Notas:
        - Ruta raíz de la aplicación web
        - Sirve contenido estático desde el directorio /static
        - La aplicación incluye interfaz para gestionar tareas vía API
    """
    logger.info("Solicitud para servir la aplicación")
    static_path = os.path.join(os.path.dirname(__file__), "../static/index.html")
    return FileResponse(static_path)
