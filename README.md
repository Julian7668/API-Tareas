# API de Tareas

Una API RESTful completa para gestión de tareas construida con FastAPI. Ofrece operaciones CRUD completas, validación de datos, logging exhaustivo, auditoría de eliminaciones con timestamps, documentación automática OpenAPI/Swagger, y una interfaz web integrada.

## 🚀 Características Principales

- ✅ **Operaciones CRUD completas**: Crear, leer, actualizar y eliminar tareas
- ✅ **Validación de datos**: Modelos Pydantic con validaciones estrictas y mensajes de error detallados
- ✅ **Documentación automática**: OpenAPI/Swagger y ReDoc integrados
- ✅ **Logging completo**: Registro estructurado de todas las operaciones con niveles configurables
- ✅ **Auditoría completa**: Historial de tareas eliminadas con timestamps ISO 8601
- ✅ **CORS habilitado**: Configuración flexible para integración con frontends
- ✅ **Pruebas unitarias**: Suite completa con pytest y reportes de cobertura
- ✅ **Frontend integrado**: Interfaz web responsiva incluida
- ✅ **Gestión de IDs**: Sistema automático de asignación de IDs únicos persistentes
- ✅ **Recuperación de datos**: Funcionalidad de restauración de tareas eliminadas
- ✅ **Eliminación permanente**: Opción de limpieza definitiva del historial

## 📦 Instalación y Configuración

### Prerrequisitos del Sistema

- **Python**: Versión 3.8 o superior
- **pip**: Gestor de paquetes de Python (incluido con Python 3.4+)
- **Sistema Operativo**: Windows, macOS, o Linux

### Instalación de Dependencias

1. **Clonar o descargar el proyecto**:
   ```bash
   cd API  # Navegar al directorio del proyecto
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verificar instalación**:
   ```bash
   python -c "import fastapi, uvicorn, pydantic; print('✅ Todas las dependencias instaladas correctamente')"
   ```

### Configuración del Entorno

La aplicación crea automáticamente los directorios y archivos necesarios:
- `data/`: Directorio para archivos JSON de datos
- `logs/`: Directorio para archivos de log
- `static/`: Archivos estáticos del frontend

**Nota**: No se requiere configuración adicional. La aplicación es autocontenida.

## 🚀 Uso y Ejecución

### Iniciar la API

```bash
python main.py
```

**Comandos alternativos**:
```bash
# Usando uvicorn directamente
uvicorn main:app --host 127.0.0.1 --port 8000 --reload

# Con variables de entorno
UVICORN_HOST=127.0.0.1 UVICORN_PORT=8000 uvicorn main:app
```

### Acceder a la Aplicación

Una vez iniciada, la API estará disponible en:

- **API Base**: http://127.0.0.1:8000
- **Documentación Swagger UI**: http://127.0.0.1:8000/docs
- **Documentación ReDoc**: http://127.0.0.1:8000/redoc
- **Frontend Web**: http://127.0.0.1:8000 (redirige automáticamente)

### Verificación de Funcionamiento

```bash
# Verificar que la API responde
curl http://127.0.0.1:8000/

# Obtener todas las tareas (inicialmente vacío)
curl http://127.0.0.1:8000/tareas
```

## 📋 Referencia de la API

### Endpoints de Tareas

| Método | Endpoint              | Descripción                          | Estado |
|--------|----------------------|--------------------------------------|--------|
| GET    | `/tareas`            | Obtener todas las tareas activas     | ✅     |
| GET    | `/tareas/{id}`       | Obtener tarea específica por ID      | ✅     |
| POST   | `/tareas`            | Crear nueva tarea                    | ✅     |
| PUT    | `/tareas/{id}`       | Actualizar tarea completa            | ✅     |
| PATCH  | `/tareas/{id}`       | Actualizar tarea parcialmente        | ✅     |
| DELETE | `/tareas/{id}`       | Eliminar tarea (mover a historial)   | ✅     |

### Endpoints de Historial y Utilidades

| Método | Endpoint              | Descripción                          | Estado |
|--------|----------------------|--------------------------------------|--------|
| GET    | `/eliminadas`        | Obtener todas las tareas eliminadas  | ✅     |
| GET    | `/eliminadas/{id}`   | Obtener tarea eliminada específica   | ✅     |
| POST   | `/eliminadas/{id}`   | Restaurar tarea eliminada            | ✅     |
| DELETE | `/eliminadas/{id}!`  | Eliminar permanentemente del historial| ✅    |
| GET    | `/`                  | Información de la API y frontend    | ✅     |

### Códigos de Estado HTTP

- **200 OK**: Operación exitosa
- **201 Created**: Recurso creado exitosamente
- **204 No Content**: Operación exitosa sin contenido de respuesta
- **400 Bad Request**: Datos de entrada inválidos
- **404 Not Found**: Recurso no encontrado
- **422 Unprocessable Entity**: Validación de datos fallida
- **500 Internal Server Error**: Error interno del servidor

## 📊 Modelo de Datos

### Estructura de Tarea

```json
{
  "id": 1,
  "titulo": "Aprender FastAPI",
  "descripcion": "Estudiar los conceptos básicos de FastAPI y crear mi primera API",
  "completada": false
}
```

### Campos y Validaciones

| Campo       | Tipo    | Requerido | Validación                  | Descripción |
|-------------|---------|-----------|-----------------------------|-------------|
| `id`        | integer | ❌        | ≥ 1 (auto-asignado)        | Identificador único |
| `titulo`    | string  | ✅        | 1-100 caracteres           | Título descriptivo |
| `descripcion`| string | ✅        | 1-500 caracteres           | Descripción detallada |
| `completada`| boolean | ❌        | true/false (default: false)| Estado de completitud |

### Modelo de Actualización Parcial (PATCH)

```json
{
  "titulo": "Nuevo título opcional",
  "descripcion": "Nueva descripción opcional",
  "completada": true
}
```

**Nota**: En actualizaciones parciales, todos los campos son opcionales. Solo los campos proporcionados serán modificados.

### Tarea Eliminada (con Auditoría)

```json
{
  "id": 1,
  "titulo": "Tarea eliminada",
  "descripcion": "Esta tarea fue eliminada",
  "completada": false,
  "fecha_eliminacion": "2023-01-01T12:00:00.000000"
}
```

**Campo adicional**: `fecha_eliminacion` (timestamp ISO 8601) se agrega automáticamente al eliminar una tarea.

## 💡 Ejemplos de Uso

### Gestión Completa de Tareas

#### 1. Crear una Nueva Tarea

```bash
curl -X POST "http://127.0.0.1:8000/tareas" \
     -H "Content-Type: application/json" \
     -d '{
       "titulo": "Aprender FastAPI",
       "descripcion": "Estudiar los conceptos básicos de FastAPI y crear mi primera API RESTful",
       "completada": false
     }'
```

**Respuesta esperada**:
```json
{
  "id": 1,
  "titulo": "Aprender FastAPI",
  "descripcion": "Estudiar los conceptos básicos de FastAPI y crear mi primera API RESTful",
  "completada": false
}
```

#### 2. Obtener Todas las Tareas

```bash
curl -X GET "http://127.0.0.1:8000/tareas"
```

#### 3. Obtener una Tarea Específica

```bash
curl -X GET "http://127.0.0.1:8000/tareas/1"
```

#### 4. Actualizar Tarea Completamente (PUT)

```bash
curl -X PUT "http://127.0.0.1:8000/tareas/1" \
     -H "Content-Type: application/json" \
     -d '{
       "titulo": "Aprender FastAPI Avanzado",
       "descripcion": "Dominar conceptos avanzados de FastAPI incluyendo autenticación y bases de datos",
       "completada": false
     }'
```

#### 5. Actualizar Tarea Parcialmente (PATCH)

```bash
# Marcar como completada
curl -X PATCH "http://127.0.0.1:8000/tareas/1" \
     -H "Content-Type: application/json" \
     -d '{"completada": true}'

# Cambiar solo el título
curl -X PATCH "http://127.0.0.1:8000/tareas/1" \
     -H "Content-Type: application/json" \
     -d '{"titulo": "Nuevo título"}'
```

#### 6. Eliminar una Tarea

```bash
curl -X DELETE "http://127.0.0.1:8000/tareas/1"
```

**Nota**: La tarea se mueve al historial, no se elimina permanentemente.

#### 7. Ver Historial de Eliminadas

```bash
curl -X GET "http://127.0.0.1:8000/eliminadas"
```

#### 8. Restaurar una Tarea Eliminada

```bash
curl -X POST "http://127.0.0.1:8000/eliminadas/1"
```

#### 9. Eliminar Permanentemente (del historial)

```bash
curl -X DELETE "http://127.0.0.1:8000/eliminadas/1%21"
```

**⚠️ Advertencia**: Esta acción es irreversible.

### Ejemplos con Python (usando requests)

```python
import requests

# Crear tarea
response = requests.post("http://127.0.0.1:8000/tareas", json={
    "titulo": "Mi tarea",
    "descripcion": "Descripción detallada"
})
tarea = response.json()
print(f"Tarea creada con ID: {tarea['id']}")

# Obtener todas las tareas
tareas = requests.get("http://127.0.0.1:8000/tareas").json()
print(f"Total de tareas: {len(tareas)}")

# Marcar como completada
requests.patch(f"http://127.0.0.1:8000/tareas/{tarea['id']}", json={"completada": True})
```

## 🧪 Pruebas y Calidad

### Ejecutar Suite de Pruebas

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar con salida detallada
pytest -v

# Ejecutar pruebas específicas
pytest tests/test_routers.py
pytest tests/test_utils.py
```

### Reportes de Cobertura

```bash
# Generar reporte HTML de cobertura
pytest --cov=. --cov-report=html

# Ver reporte en navegador
# El reporte se genera en htmlcov/index.html

# Cobertura en terminal
pytest --cov=. --cov-report=term-missing
```

### Configuración de Pruebas

Las pruebas están configuradas en `tests/conftest.py` con:
- Fixtures para datos de prueba
- Configuración de logging para pruebas
- Inicialización de archivos de datos temporales

### Estructura de Pruebas

```
tests/
├── conftest.py       # Configuración y fixtures
├── test_utils.py     # Pruebas de utilidades
└── test_routers.py   # Pruebas de endpoints
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

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Este proyecto sigue el modelo de desarrollo abierto.

### Proceso de Contribución

1. **Fork el repositorio** en GitHub
2. **Clona tu fork** localmente:
   ```bash
   git clone https://github.com/tu-usuario/api-tareas.git
   cd api-tareas
   ```

3. **Crea una rama** para tu contribución:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   # o
   git checkout -b fix/error-en-endpoint
   ```

4. **Desarrolla** siguiendo las mejores prácticas:
   - Agrega docstrings a nuevas funciones
   - Incluye pruebas para nueva funcionalidad
   - Actualiza documentación si es necesario
   - Sigue el estilo de código existente

5. **Ejecuta las pruebas**:
   ```bash
   pytest --cov=. --cov-report=term-missing
   ```

6. **Commit tus cambios**:
   ```bash
   git add .
   git commit -m "feat: agrega nueva funcionalidad X"
   ```

7. **Push y crea Pull Request**:
   ```bash
   git push origin feature/nueva-funcionalidad
   ```

### Guías de Estilo

- **Python**: PEP 8 con verificación mediante flake8
- **Commits**: [Conventional Commits](https://conventionalcommits.org/)
- **Docstrings**: Formato Google/Numpy
- **Pruebas**: Cobertura mínima del 80%

### Tipos de Contribuciones

- 🐛 **Bug fixes**: Corrección de errores
- ✨ **Features**: Nueva funcionalidad
- 📚 **Documentation**: Mejoras en documentación
- 🧪 **Tests**: Agregar o mejorar pruebas
- 🔧 **Maintenance**: Mejoras de código, refactorización

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**. Ver el archivo [`LICENSE`](LICENSE) para más detalles.

```
MIT License

Copyright (c) 2023 API de Tareas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

## 🆘 Soporte y Comunidad

### Reportar Problemas

Para reportar bugs o solicitar nuevas características:

1. Verifica que el issue no existe ya
2. Usa las plantillas de issue disponibles
3. Proporciona información detallada:
   - Versión de Python
   - Sistema operativo
   - Pasos para reproducir
   - Comportamiento esperado vs actual

### Preguntas y Discusiones

- 📧 **Email**: Para consultas privadas
- 💬 **Issues**: Para preguntas técnicas públicas
- 📖 **Documentación**: Wiki del repositorio

### Código de Conducta

Este proyecto sigue un código de conducta para mantener un ambiente respetuoso e inclusivo. Al participar, aceptas:

- Ser respetuoso con todos los colaboradores
- Mantener un lenguaje profesional
- Aceptar constructivamente críticas y sugerencias
- Enfocarte en resolver problemas técnicos

---

**⭐ Si encuentras útil este proyecto, considera darle una estrella en GitHub.**
