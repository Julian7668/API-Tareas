# API de Tareas

Una API RESTful para gestión de tareas construida con FastAPI. Incluye operaciones CRUD completas, validación de datos, logging, auditoría de eliminaciones y documentación automática.

## Características

- ✅ **Operaciones CRUD completas**: Crear, leer, actualizar y eliminar tareas
- ✅ **Validación de datos**: Modelos Pydantic con validaciones estrictas
- ✅ **Documentación automática**: OpenAPI/Swagger integrada
- ✅ **Logging completo**: Registro de todas las operaciones
- ✅ **Auditoría**: Historial de tareas eliminadas con timestamps
- ✅ **CORS habilitado**: Para integración con frontends
- ✅ **Pruebas unitarias**: Cobertura completa con pytest
- ✅ **Frontend básico**: Interfaz web incluida

## Instalación

### Prerrequisitos

- Python 3.8+
- pip

### Instalación de dependencias

```bash
cd API
pip install -r requirements.txt
```

## Uso

### Ejecutar la API

```bash
python main.py
```

La API estará disponible en: http://127.0.0.1:8000

### Documentación

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **Frontend**: http://127.0.0.1:8000/app

## Endpoints

### Tareas

| Método | Endpoint       | Descripción                   |
| ------ | -------------- | ----------------------------- |
| GET    | `/tareas`      | Obtener todas las tareas      |
| GET    | `/tareas/{id}` | Obtener tarea específica      |
| POST   | `/tareas`      | Crear nueva tarea             |
| PUT    | `/tareas/{id}` | Actualizar tarea completa     |
| PATCH  | `/tareas/{id}` | Actualizar tarea parcialmente |
| DELETE | `/tareas/{id}` | Eliminar tarea                |

### Información

| Método | Endpoint | Descripción           |
| ------ | -------- | --------------------- |
| GET    | `/`      | Información de la API |
| GET    | `/app`   | Servir frontend       |

## Modelo de Datos

### Tarea

```json
{
  "id": 1,
  "titulo": "Aprender FastAPI",
  "descripcion": "Estudiar los conceptos básicos de FastAPI",
  "completada": false
}
```

### Validaciones

- **titulo**: 1-100 caracteres, obligatorio
- **descripcion**: 1-500 caracteres, obligatorio
- **completada**: booleano, por defecto `false`

## Ejemplos de Uso

### Crear tarea

```bash
curl -X POST "http://127.0.0.1:8000/tareas" \
     -H "Content-Type: application/json" \
     -d '{
       "titulo": "Mi nueva tarea",
       "descripcion": "Descripción detallada",
       "completada": false
     }'
```

### Obtener todas las tareas

```bash
curl -X GET "http://127.0.0.1:8000/tareas"
```

### Actualizar tarea parcialmente

```bash
curl -X PATCH "http://127.0.0.1:8000/tareas/1" \
     -H "Content-Type: application/json" \
     -d '{"completada": true}'
```

## Pruebas

### Ejecutar pruebas

```bash
pytest
```

### Ejecutar con cobertura

```bash
pytest --cov=. --cov-report=html
```

## Estructura del Proyecto

```
API/
├── main.py                 # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias del proyecto
├── README.md              # Esta documentación
├── constants/
│   ├── __init__.py
│   ├── constants.py       # Constantes del proyecto
│   └── modelos.py         # Modelos Pydantic
├── routers/
│   ├── __init__.py
│   ├── GET.py            # Endpoints GET
│   ├── POST.py           # Endpoints POST
│   ├── PUT.py            # Endpoints PUT
│   ├── PATCH.py          # Endpoints PATCH
│   ├── DELETE.py         # Endpoints DELETE
│   └── OTHERS.py         # Endpoints misceláneos
├── utils/
│   ├── __init__.py
│   ├── MDleer_json.py    # Utilidades para leer JSON
│   ├── MDobtener_proximo_id.py  # Gestión de IDs
│   ├── MDguardar_eliminada.py   # Auditoría de eliminaciones
│   └── MDescribir_datos.py      # Escritura de datos
├── data/
│   ├── .gitkeep
│   ├── tareas.json       # Datos de tareas activas
│   └── tareas_eliminadas.json  # Historial de eliminadas
├── logs/
│   ├── .gitkeep
│   └── app.log           # Logs de la aplicación
├── static/
│   ├── index.html        # Frontend básico
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── app.js
└── tests/
    ├── conftest.py       # Configuración de pruebas
    ├── test_utils.py     # Pruebas de utilidades
    └── test_routers.py   # Pruebas de endpoints
```

## Logs

Los logs se almacenan en `API/logs/app.log` con el siguiente formato:

```
2023-01-01 12:00:00,000 - main - INFO - Mensaje de log
```

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Soporte

Para soporte o preguntas, por favor abre un issue en el repositorio.
