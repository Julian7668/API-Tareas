"""
Modelos de datos Pydantic

Este módulo define los modelos de datos utilizados en la API de tareas,
incluyendo validaciones, esquemas y documentación automática para OpenAPI.

Modelos principales:
- Tarea: Modelo completo para tareas con validaciones estrictas
- TareaUpdate: Modelo para actualizaciones parciales de tareas

Características:
- Validación automática de tipos y formatos
- Documentación OpenAPI integrada
- Ejemplos de uso incluidos
- Configuración de serialización JSON
"""

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


# Modelo de datos para las tareas
class Tarea(BaseModel):
    """
    Modelo que representa una tarea completa en el sistema de gestión de tareas.

    Esta clase define la estructura de datos para tareas, incluyendo validaciones
    estrictas de tipos y formatos. Se utiliza tanto para entrada como salida de la API.

    Attributes:
        id (Optional[int]): ID único de la tarea. Opcional para creación (se asigna automáticamente).
                           Debe ser >= 1 cuando se proporciona.
        titulo (str): Título descriptivo de la tarea. Longitud: 1-100 caracteres.
                     Campo obligatorio con validación de longitud.
        descripcion (str): Descripción detallada de la tarea. Longitud: 1-500 caracteres.
                          Campo obligatorio con validación de longitud.
        completada (bool): Estado de completitud de la tarea. Por defecto False.
                          Indica si la tarea ha sido marcada como completada.

    Examples:
        >>> tarea = Tarea(titulo="Aprender Python", descripcion="Estudiar sintaxis básica")
        >>> tarea.id  # None (se asigna automáticamente)
        >>> tarea.completada  # False (valor por defecto)

        >>> tarea_completa = Tarea(id=1, titulo="Tarea", descripcion="Desc", completada=True)
    """
    id: Optional[int] = Field(default=None, description="ID único de la tarea", ge=1)
    titulo: str = Field(
        ...,
        description="Título de la tarea",
        min_length=1,
        max_length=100,
        examples=["Aprender FastAPI"],
    )
    descripcion: str = Field(
        ...,
        description="Descripción detallada de la tarea",
        min_length=1,
        max_length=500,
        examples=["Estudiar los conceptos básicos de FastAPI y crear mi primera API"],
    )
    completada: bool = Field(
        default=False, description="Estado de completitud de la tarea", examples=[False]
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "titulo": "Aprender FastAPI",
                "descripcion": "Estudiar los conceptos básicos de FastAPI y crear mi primera API",
                "completada": False,
            }
        }
    )


class TareaUpdate(BaseModel):
    """
    Modelo para actualizaciones parciales de tareas usando el método PATCH.

    Esta clase permite actualizaciones selectivas donde solo los campos proporcionados
    en la solicitud serán modificados. Los campos no incluidos mantienen sus valores actuales.
    Es ideal para operaciones como marcar una tarea como completada sin cambiar otros campos.

    Attributes:
        titulo (Optional[str]): Nuevo título para la tarea. Si se proporciona, debe tener
                               1-100 caracteres. Si es None, el título no se modifica.
        descripcion (Optional[str]): Nueva descripción para la tarea. Si se proporciona,
                                    debe tener 1-500 caracteres. Si es None, la descripción
                                    no se modifica.
        completada (Optional[bool]): Nuevo estado de completitud. Si se proporciona,
                                    actualiza el estado. Si es None, el estado no cambia.

    Examples:
        >>> # Marcar tarea como completada
        >>> update = TareaUpdate(completada=True)

        >>> # Cambiar solo el título
        >>> update = TareaUpdate(titulo="Nuevo título")

        >>> # Actualizar título y descripción
        >>> update = TareaUpdate(titulo="Título", descripcion="Descripción")

        >>> # No cambiar nada (todos None)
        >>> update = TareaUpdate()
    """
    titulo: Optional[str] = Field(
        None, description="Nuevo título de la tarea", min_length=1, max_length=100
    )
    descripcion: Optional[str] = Field(
        None, description="Nueva descripción de la tarea", min_length=1, max_length=500
    )
    completada: Optional[bool] = Field(None, description="Nuevo estado de completitud")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"titulo": "Título actualizado", "completada": True}
        }
    )
