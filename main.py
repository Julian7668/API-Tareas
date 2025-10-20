"""
API de Tareas

Esta es la aplicación principal de FastAPI para gestionar tareas.
Incluye configuración de logging, CORS, routers y archivos estáticos.

Módulos principales:
- routers: Contiene todos los endpoints organizados por método HTTP
- constants: Define modelos de datos y rutas de archivos
- utils: Funciones auxiliares para manejo de datos JSON

Ejecución:
    python main.py

La API estará disponible en http://127.0.0.1:8000
Documentación automática en http://127.0.0.1:8000/docs
"""

import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routers import GET, POST, PUT, PATCH, DELETE, OTHERS

# Crear directorio de logs si no existe
log_dir: str = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(log_dir, exist_ok=True)

# Configurar logging
# Se configura logging a nivel INFO con formato detallado
# Los logs se guardan en archivo y se muestran en consola
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "app.log")),
        logging.StreamHandler(),
    ],
)
logger: logging.Logger = logging.getLogger(__name__)

# Crear la aplicación FastAPI
# Se inicializa la aplicación con metadatos para documentación automática
logger.info("Creando aplicación FastAPI")
app: FastAPI = FastAPI(
    title="API de Tareas",
    description="API RESTful para gestión completa de tareas con operaciones CRUD, validación de datos y auditoría.",
    version="1.0.0",
    docs_url="/docs",  # URL para Swagger UI
    redoc_url="/redoc",  # URL para ReDoc
)

# Configurar CORS
# Permite solicitudes desde cualquier origen para desarrollo
# En producción, especificar orígenes permitidos
logger.info("Configurando CORS")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes (configurar en producción)
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los headers
)

# REGISTRAR TODOS LOS ROUTERS
# Cada router maneja un conjunto específico de operaciones HTTP
logger.info("Registrando routers")
app.include_router(GET.router, tags=["📖 Obtener"])
app.include_router(POST.router, tags=["➕ Crear"])
app.include_router(PUT.router, prefix="/tareas", tags=["📝 Actualizar"])
app.include_router(PATCH.router, prefix="/tareas", tags=["⚡ Parcial"])
app.include_router(DELETE.router, tags=["🗑️ Eliminar"])
app.include_router(OTHERS.router, tags=["🌟 General"])

# Static files
# Montar directorio de archivos estáticos para servir frontend
logger.info("Montando archivos estáticos")
static_dir: str = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

if __name__ == "__main__":
    import uvicorn

    # Punto de entrada principal para ejecutar la aplicación
    # Se ejecuta solo cuando el script se llama directamente
    logger.info("Iniciando servidor Uvicorn en 127.0.0.1:8000")
    uvicorn.run(
        app,
        host="127.0.0.1",  # Escuchar en localhost
        port=8000,         # Puerto estándar para desarrollo
        reload=False       # Deshabilitar recarga automática en producción
    )
