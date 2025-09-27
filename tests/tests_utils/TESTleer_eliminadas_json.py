import json
from unittest.mock import patch, mock_open


def test_leer_eliminadas_json_archivo_no_existe():
    """Debe retornar lista vacía si el archivo no existe"""
    with patch("os.path.exists", return_value=False):
        from utils import leer_eliminadas_json

        result = leer_eliminadas_json()
        assert result == []


def test_leer_eliminadas_json_datos_validos(sample_deleted_tasks):
    """Debe retornar los datos correctamente"""
    mock_data = json.dumps(sample_deleted_tasks)
    with patch("os.path.exists", return_value=True), patch(
        "builtins.open", mock_open(read_data=mock_data)
    ):
        from utils import leer_eliminadas_json

        result = leer_eliminadas_json()
        assert result == sample_deleted_tasks
