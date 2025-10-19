"""
Router principal para operaciones GET

Este módulo coordina todas las rutas GET de la aplicación,
organizadas por contexto (tareas activas y tareas eliminadas).
"""

from fastapi import APIRouter

from .tareas import registrar_rutas_tareas
from .eliminadas import registrar_rutas_eliminadas

router = APIRouter()

# Registrar todas las rutas en el router principal
registrar_rutas_tareas(router)
registrar_rutas_eliminadas(router)
