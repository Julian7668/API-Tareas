# ❓ Preguntas Frecuentes (FAQ) - API de Tareas

Respuestas a las preguntas más comunes sobre la API de Tareas.

## 📋 Índice

- [General](#general)
- [Instalación y Configuración](#instalación-y-configuración)
- [Uso de la API](#uso-de-la-api)
- [Desarrollo](#desarrollo)
- [Solución de Problemas](#solución-de-problemas)

## 🤔 General

### ¿Qué es esta API?

La API de Tareas es una aplicación RESTful construida con FastAPI que permite gestionar tareas de manera completa. Incluye operaciones CRUD, validación de datos, auditoría, logging y una interfaz web integrada.

### ¿Qué tecnologías usa?

- **Backend**: FastAPI (Python)
- **Validación**: Pydantic
- **Documentación**: OpenAPI/Swagger automática
- **Persistencia**: Archivos JSON
- **Frontend**: HTML/CSS/JavaScript vanilla
- **Testing**: pytest

### ¿Es gratuita?

Sí, completamente gratuita y open source bajo licencia MIT.

## ⚙️ Instalación y Configuración

### ¿Cómo instalo la API?

```bash
cd API
pip install -r requirements.txt
python main.py
```

### ¿Qué versiones de Python soporta?

Python 3.8 o superior. Recomendamos Python 3.9+ para mejor rendimiento.

### ¿Puedo usar un entorno virtual?

¡Absolutamente recomendado!

```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### ¿Dónde se guardan los datos?

Los datos se guardan automáticamente en archivos JSON en el directorio `data/`:
- `tareas.json`: Tareas activas
- `tareas_eliminadas.json`: Historial de eliminadas
- `contador_id.json`: Contador de IDs

## 🚀 Uso de la API

### ¿Cómo creo mi primera tarea?

```bash
curl -X POST "http://127.0.0.1:8000/tareas" \
     -H "Content-Type: application/json" \
     -d '{
       "titulo": "Mi primera tarea",
       "descripcion": "Aprendiendo a usar la API",
       "completada": false
     }'
```

### ¿Cuál es la diferencia entre PUT y PATCH?

- **PUT**: Actualización completa. Debes enviar TODOS los campos.
- **PATCH**: Actualización parcial. Solo envías los campos que quieres cambiar.

### ¿Qué pasa cuando elimino una tarea?

La tarea se mueve a un historial de "eliminadas" con timestamp. No se pierde permanentemente y puede ser restaurada.

### ¿Cómo elimino una tarea permanentemente?

```bash
# ⚠️ PELIGRO: Esto es irreversible
curl -X DELETE "http://127.0.0.1:8000/eliminadas/1%21"
```

### ¿Puedo acceder desde otros dominios?

Por defecto, CORS está configurado para permitir cualquier origen (`*`). Para producción, configura orígenes específicos en `main.py`.

## 💻 Desarrollo

### ¿Cómo agrego un nuevo endpoint?

1. Crea un nuevo archivo en `routers/`
2. Define tus rutas usando `@router.get`, `@router.post`, etc.
3. Registra el router en `main.py`

Ejemplo:
```python
# routers/nuevo.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/saludo")
def saludar():
    return {"mensaje": "¡Hola!"}

# main.py
from routers.nuevo import router as nuevo_router
app.include_router(nuevo_router, tags=["🆕 Nuevo"])
```

### ¿Cómo valido datos personalizados?

Usa Pydantic con validadores personalizados:

```python
from pydantic import BaseModel, validator

class TareaPersonalizada(BaseModel):
    titulo: str
    prioridad: str

    @validator('prioridad')
    def validar_prioridad(cls, v):
        if v not in ['baja', 'media', 'alta']:
            raise ValueError('Prioridad debe ser baja, media o alta')
        return v
```

### ¿Cómo agrego logging personalizado?

```python
import logging

logger = logging.getLogger(__name__)

def mi_funcion():
    logger.info("Iniciando operación")
    # ... código ...
    logger.debug("Operación completada")
```

### ¿Cómo escribo pruebas?

```python
# tests/test_mi_funcion.py
def test_mi_funcion():
    # Arrange
    entrada = "test"

    # Act
    resultado = mi_funcion(entrada)

    # Assert
    assert resultado == "esperado"
```

## 🔧 Solución de Problemas

### La API no inicia

**Posibles causas:**
- Puerto 8000 ocupado
- Dependencias faltantes
- Error de sintaxis

**Soluciones:**
```bash
# Verificar puerto
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall

# Verificar sintaxis
python -m py_compile main.py
```

### Error "Module not found"

```bash
# Instalar dependencias faltantes
pip install fastapi uvicorn pydantic

# Verificar instalación
python -c "import fastapi, uvicorn, pydantic"
```

### Los datos no se guardan

**Verificar permisos:**
```bash
# Linux/Mac
ls -la data/
chmod 755 data/

# Windows - verificar que no esté abierto en otro programa
```

### Error de validación

Los errores de validación incluyen detalles específicos:

```json
{
  "detail": [
    {
      "loc": ["body", "titulo"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.const"
    }
  ]
}
```

Esto significa que el campo `titulo` está vacío.

### La documentación no carga

- Verifica que la API esté ejecutándose
- Accede a `http://127.0.0.1:8000/docs`
- Si no funciona, verifica que FastAPI esté instalado correctamente

### Problemas de rendimiento

Para producción:
```bash
# Usar múltiples workers
uvicorn main:app --workers 4

# Usar servidor ASGI optimizado
pip install uvicorn[standard]
uvicorn main:app --loop uvloop --http httptools
```

## 🔒 Seguridad

### ¿Es seguro usar esta API?

Para desarrollo local sí. Para producción:

- Configura CORS específicamente
- Usa HTTPS
- Implementa autenticación si es necesario
- Valida todas las entradas
- Monitorea logs

### ¿Cómo configuro CORS para producción?

```python
# En main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tu-dominio.com"],  # Lista específica
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)
```

## 📊 Monitoreo y Logs

### ¿Dónde están los logs?

Los logs se guardan en `logs/app.log` con formato:
```
2023-01-01 12:00:00,000 - main - INFO - Mensaje de log
```

### ¿Cómo cambio el nivel de logging?

```python
# En main.py
logging.basicConfig(
    level=logging.DEBUG,  # Cambiar a INFO, WARNING, ERROR
    # ... resto de configuración
)
```

## 🚀 Despliegue

### ¿Puedo usar Docker?

¡Sí! Ejemplo de Dockerfile:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### ¿Qué servicios en la nube recomiendan?

- **Heroku**: Fácil para principiantes
- **Railway**: Despliegue automático desde Git
- **Render**: Gratuito con límites generosos
- **Fly.io**: Buen rendimiento para APIs
- **AWS/GCP/Azure**: Para escalado empresarial

## 🤝 Contribución

### ¿Cómo reporto un bug?

1. Verifica que no esté reportado ya
2. Crea un issue con:
   - Descripción clara
   - Pasos para reproducir
   - Versión de Python/SO
   - Logs relevantes

### ¿Cómo contribuyo código?

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/nueva-funcion`)
3. Haz tus cambios
4. Ejecuta pruebas (`pytest`)
5. Crea un Pull Request

## 📚 Recursos Adicionales

- [Documentación FastAPI](https://fastapi.tiangolo.com/)
- [Tutorial Pydantic](https://pydantic-docs.helpmanual.io/)
- [Guía OpenAPI](https://swagger.io/docs/specification/about/)
- [Tutoriales de esta API](TUTORIALES.md)

---

¿No encuentras respuesta a tu pregunta? Abre un [issue](https://github.com/tu-repo/api-tareas/issues) en el repositorio.