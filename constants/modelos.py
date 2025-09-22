from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


# Modelo de datos para las tareas
class Tarea(BaseModel):
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
