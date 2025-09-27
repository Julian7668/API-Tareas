import json
import os
import sys
import tempfile
from pathlib import Path
import pytest

from fastapi.testclient import TestClient

# Debug logging for import issue
print(f"Current working directory: {os.getcwd()}")
print(f"Python path includes: {[p for p in sys.path if 'API' in p or p == '.']}")

try:
    # Try absolute import first
    from main import app

    print("Absolute import 'from API.main import app' succeeded")
except ImportError as e:
    print(f"Absolute import failed: {e}")
    try:
        # Try relative import for when running from project root
        from main import app

        print("Relative import 'from ..API.main import app' succeeded")
    except ImportError as e2:
        print(f"Relative import failed: {e2}")
        try:
            # Add parent directory to path if needed
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)

            from main import app

            print("Fallback import with path manipulation succeeded")
        except ImportError as e3:
            print(f"Fallback import failed: {e3}")
            raise  # Re-raise to fail the import


@pytest.fixture
def client():
    """Cliente de prueba para la API"""
    return TestClient(app)


@pytest.fixture
def temp_data_dir():
    """Directorio temporal para archivos de datos de prueba"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_tasks():
    """Datos de tareas de ejemplo"""
    return [
        {
            "id": 1,
            "titulo": "Tarea 1",
            "descripcion": "Descripción 1",
            "completada": False,
        },
        {
            "id": 2,
            "titulo": "Tarea 2",
            "descripcion": "Descripción 2",
            "completada": True,
        },
    ]


@pytest.fixture
def sample_deleted_tasks():
    """Datos de tareas eliminadas de ejemplo"""
    return [
        {
            "id": 3,
            "titulo": "Tarea Eliminada",
            "descripcion": "Esta tarea fue eliminada",
            "completada": False,
            "fecha_eliminacion": "2023-01-01T00:00:00",
        }
    ]


@pytest.fixture
def mock_data_files(
    temp_data_dir, sample_tasks, sample_deleted_tasks
):  # pylint: disable=redefined-outer-name
    """Crear archivos JSON de prueba en directorio temporal"""
    # Archivo de tareas activas
    tasks_file = temp_data_dir / "tareas.json"
    with open(tasks_file, "w", encoding="utf-8") as f:
        json.dump(sample_tasks, f, indent=2, ensure_ascii=False)

    # Archivo de tareas eliminadas
    deleted_file = temp_data_dir / "tareas_eliminadas.json"
    with open(deleted_file, "w", encoding="utf-8") as f:
        json.dump(sample_deleted_tasks, f, indent=2, ensure_ascii=False)

    return {
        "tasks_file": tasks_file,
        "deleted_file": deleted_file,
        "temp_dir": temp_data_dir,
    }
