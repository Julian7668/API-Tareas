from .MDleer_json import leer_json
from .MDescribir_datos_tareas import escribir_datos_tareas
from .MDescribir_datos_eliminadas import escribir_datos_eliminadas
from .MDleer_eliminadas_json import leer_eliminadas_json
from .MDguardar_eliminada import guardar_eliminada
from .MDobtener_proximo_id import obtener_proximo_id

__all__ = [
    "escribir_datos_tareas",
    "escribir_datos_eliminadas",
    "guardar_eliminada",
    "leer_eliminadas_json",
    "leer_json",
    "obtener_proximo_id",
]
