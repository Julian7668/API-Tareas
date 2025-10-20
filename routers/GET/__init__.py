"""
Router principal para operaciones GET

Este módulo coordina todas las rutas GET de la aplicación,
organizadas por contexto (tareas activas y tareas eliminadas).

Rutas disponibles:
- GET /tareas: Lista todas las tareas activas
- GET /tareas/{id}: Obtiene una tarea específica
- GET /eliminadas: Lista todas las tareas eliminadas
- GET /eliminadas/{id}: Obtiene una tarea eliminada específica

El módulo importa y registra las funciones de los submódulos
tareas.py y eliminadas.py para mantener la organización del código.
"""

from fastapi import APIRouter

from .tareas import registrar_rutas_tareas
from .eliminadas import registrar_rutas_eliminadas

router: APIRouter = APIRouter()

# Registrar todas las rutas en el router principal
# Se organizan las rutas por contexto para mejor mantenibilidad
registrar_rutas_tareas(router)
registrar_rutas_eliminadas(router)
