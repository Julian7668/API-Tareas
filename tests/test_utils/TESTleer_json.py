import json
from unittest.mock import patch, mock_open


def test_leer_json_archivo_no_existe():
    """Debe retornar lista vacía si el archivo no existe"""
    with patch("os.path.exists", return_value=False):
        from utils import leer_json

        result = leer_json()
        assert result == []


def test_leer_json_archivo_vacio():
    """Debe retornar lista vacía si el archivo está vacío o mal formado"""
    mock_data = "[]"
    with patch("os.path.exists", return_value=True), patch(
        "builtins.open", mock_open(read_data=mock_data)
    ):
        from utils import leer_json

        result = leer_json()
        assert result == []


def test_leer_json_datos_validos(sample_tasks):
    """Debe retornar los datos correctamente"""
    mock_data = json.dumps(sample_tasks)
    with patch("os.path.exists", return_value=True), patch(
        "builtins.open", mock_open(read_data=mock_data)
    ):
        from utils import leer_json

        result = leer_json()
        assert result == sample_tasks


def test_leer_json_error_json():
    """Debe retornar lista vacía en caso de error de JSON"""
    mock_data = "{invalid json}"
    with patch("os.path.exists", return_value=True), patch(
        "builtins.open", mock_open(read_data=mock_data)
    ):
        from utils import leer_json

        result = leer_json()
        assert result == []
