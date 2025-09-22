import os
import logging
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/")
def read_root():
    logger.info("Acceso al endpoint raíz")
    return {"mensaje": "¡API de Tareas funcionando!", "documentacion": "/docs"}


@router.get("/app")
def get_frontend():
    logger.info("Solicitud para servir el frontend")
    static_path = os.path.join(os.path.dirname(__file__), "../static/index.html")
    return FileResponse(static_path)
