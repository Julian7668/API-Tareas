import json
from unittest.mock import patch, mock_open
import pytest


def test_guardar_eliminada_exito(sample_tasks):
    """Debe guardar la tarea eliminada correctamente"""
    tarea = sample_tasks[0]

    with patch("utils.leer_eliminadas_json", return_value=[]), patch(
        "builtins.open", mock_open()
    ) as mock_file:
        from utils import guardar_eliminada

        guardar_eliminada(tarea)

        # Verificar que se abrió el archivo para escritura
        # El path será relativo desde constants/
        expected_path = "data/tareas_eliminadas.json"
        mock_file.assert_called_once_with(expected_path, "w", encoding="utf-8")

        # Verificar que se escribió el JSON correcto
        written_data = json.loads(mock_file().write.call_args[0][0])
        assert len(written_data) == 1
        assert written_data[0]["id"] == tarea["id"]
        assert "fecha_eliminacion" in written_data[0]


def test_guardar_eliminada_error(sample_tasks):
    """Debe lanzar excepción en caso de error de escritura"""
    tarea = sample_tasks[0]

    with patch("utils.leer_eliminadas_json", return_value=[]), patch(
        "builtins.open", side_effect=Exception("Error de escritura")
    ):
        from utils import guardar_eliminada

        with pytest.raises(Exception):
            guardar_eliminada(tarea)
