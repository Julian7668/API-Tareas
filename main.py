import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routers import GET, POST, PUT, PATCH, DELETE, OTHERS

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/app.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Crear la aplicación FastAPI
logger.info("Creando aplicación FastAPI")
app = FastAPI(
    title="API de Tareas", description="API para gestionar tareas", version="1.0.0"
)

# Configurar CORS
logger.info("Configurando CORS")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REGISTRAR TODOS LOS ROUTERS
logger.info("Registrando routers")
app.include_router(GET.router, prefix="/tareas", tags=["📖 Obtener"])
app.include_router(POST.router, prefix="/tareas", tags=["➕ Crear"])
app.include_router(PUT.router, prefix="/tareas", tags=["📝 Actualizar"])
app.include_router(PATCH.router, prefix="/tareas", tags=["⚡ Parcial"])
app.include_router(DELETE.router, prefix="/tareas", tags=["🗑️ Eliminar"])
app.include_router(OTHERS.router, tags=["🌟 General"])

# Static files
logger.info("Montando archivos estáticos")
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

if __name__ == "__main__":
    import uvicorn

    logger.info("Iniciando servidor Uvicorn en 127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
