# Estructura de Tests

Este directorio contiene la suite de tests para la API de tareas, organizada en módulos específicos para mejor mantenibilidad.

## Estructura

```
tests/
├── conftest.py              # Configuración y fixtures globales
├── README.md               # Esta documentación
├── tests_routers/          # Tests organizados por router HTTP
│   ├── testGET.py          # Tests para operaciones GET
│   ├── testPOST.py         # Tests para operaciones POST
│   ├── testPUT.py          # Tests para operaciones PUT
│   ├── testPATCH.py        # Tests para operaciones PATCH
│   ├── testDELETE.py       # Tests para operaciones DELETE
│   └── testOTHERS.py       # Tests para rutas misceláneas
└── tests_utils/             # Tests organizados por función utility
    ├── TESTleer_json.py      # Tests para leer_json()
    ├── TESTobtener_proximo_id.py  # Tests para obtener_proximo_id()
    ├── TESTguardar_eliminada.py   # Tests para guardar_eliminada()
    ├── TESTleer_eliminadas_json.py # Tests para leer_eliminadas_json()
    └── TESTescribir_datos.py      # Tests para escribir_datos()
```

## Características

### Módulos Individuales

Cada módulo contiene funciones de test independientes con nombres descriptivos en snake_case.

### Fixtures Reutilizables

Los fixtures definidos en `conftest.py` están disponibles para todos los módulos:

- `client`: Cliente de test para la API FastAPI
- `sample_tasks`: Datos de tareas de ejemplo
- `sample_deleted_tasks`: Datos de tareas eliminadas de ejemplo
- `temp_data_dir`: Directorio temporal para archivos de test
- `mock_data_files`: Archivos JSON mock para testing

### Ejecución de Tests

```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests de un módulo específico
pytest tests/test_routers/testGET.py
pytest tests/test_utils/TESTleer_json.py

# Ejecutar tests de una carpeta completa
pytest tests/test_routers/
pytest tests/test_utils/

# Ejecutar un test específico
pytest tests/test_routers/testGET.py::test_obtener_tareas
```

## Ventajas de esta estructura

1. **Organización clara**: Tests agrupados por funcionalidad
2. **Mantenimiento fácil**: Cada módulo es independiente
3. **Ejecución granular**: Puedes ejecutar tests específicos
4. **Reutilización**: Los fixtures son compartidos entre módulos
5. **Escalabilidad**: Fácil agregar nuevos módulos de test
6. **Simplicidad**: Sin código innecesario (if **name**, **init**.py)

## Agregar nuevos tests

Para agregar un nuevo módulo de test:

1. Crear el archivo en la carpeta correspondiente
2. Definir funciones de test con nombres descriptivos
3. Usar los fixtures disponibles de `conftest.py`
4. **NO agregar** `if __name__ == "__main__"` (pytest lo maneja automáticamente)
