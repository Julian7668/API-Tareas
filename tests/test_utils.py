import json
from unittest.mock import patch, mock_open
import pytest

from ..utils import (
    leer_json,
    obtener_proximo_id,
    guardar_eliminada,
    leer_eliminadas_json,
)


class TestLeerJson:
    """Pruebas para la función leer_json"""

    def test_leer_json_archivo_no_existe(self):
        """Debe retornar lista vacía si el archivo no existe"""
        with patch("os.path.exists", return_value=False):
            result = leer_json()
            assert result == []

    def test_leer_json_archivo_vacio(self):
        """Debe retornar lista vacía si el archivo está vacío o mal formado"""
        mock_data = "[]"
        with patch("os.path.exists", return_value=True), patch(
            "builtins.open", mock_open(read_data=mock_data)
        ):
            result = leer_json()
            assert result == []

    def test_leer_json_datos_validos(self, sample_tasks):
        """Debe retornar los datos correctamente"""
        mock_data = json.dumps(sample_tasks)
        with patch("os.path.exists", return_value=True), patch(
            "builtins.open", mock_open(read_data=mock_data)
        ):
            result = leer_json()
            assert result == sample_tasks

    def test_leer_json_error_json(self):
        """Debe retornar lista vacía en caso de error de JSON"""
        mock_data = "{invalid json}"
        with patch("os.path.exists", return_value=True), patch(
            "builtins.open", mock_open(read_data=mock_data)
        ):
            result = leer_json()
            assert result == []


class TestObtenerProximoId:
    """Pruebas para la función obtener_proximo_id"""

    def test_obtener_proximo_id_sin_datos(self):
        """Debe retornar 1 si no hay datos"""
        with patch("utils.MDobtener_proximo_id.leer_json", return_value=[]), patch(
            "utils.MDobtener_proximo_id.leer_eliminadas_json", return_value=[]
        ):
            result = obtener_proximo_id()
            assert result == 1

    def test_obtener_proximo_id_con_datos_activos(self, sample_tasks):
        """Debe calcular el próximo ID basado en tareas activas"""
        with patch(
            "utils.MDobtener_proximo_id.leer_json", return_value=sample_tasks
        ), patch("utils.MDobtener_proximo_id.leer_eliminadas_json", return_value=[]):
            result = obtener_proximo_id()
            assert result == 3  # max id en sample_tasks es 2, próximo es 3

    def test_obtener_proximo_id_con_datos_eliminados(
        self, sample_tasks, sample_deleted_tasks
    ):
        """Debe considerar IDs de tareas eliminadas"""
        with patch(
            "utils.MDobtener_proximo_id.leer_json", return_value=sample_tasks
        ), patch(
            "utils.MDobtener_proximo_id.leer_eliminadas_json",
            return_value=sample_deleted_tasks,
        ):
            result = obtener_proximo_id()
            assert result == 4  # max id es 3 (de eliminadas), próximo es 4


class TestGuardarEliminada:
    """Pruebas para la función guardar_eliminada"""

    def test_guardar_eliminada_exito(self, sample_tasks):
        """Debe guardar la tarea eliminada correctamente"""
        tarea = sample_tasks[0]

        with patch(
            "utils.MDguardar_eliminada.leer_eliminadas_json", return_value=[]
        ), patch("builtins.open", mock_open()) as mock_file:
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

    def test_guardar_eliminada_error(self, sample_tasks):
        """Debe lanzar excepción en caso de error de escritura"""
        tarea = sample_tasks[0]

        with patch(
            "utils.MDguardar_eliminada.leer_eliminadas_json", return_value=[]
        ), patch("builtins.open", side_effect=Exception("Error de escritura")):
            with pytest.raises(Exception):
                guardar_eliminada(tarea)


class TestLeerEliminadasJson:
    """Pruebas para la función leer_eliminadas_json"""

    def test_leer_eliminadas_json_archivo_no_existe(self):
        """Debe retornar lista vacía si el archivo no existe"""
        with patch("os.path.exists", return_value=False):
            result = leer_eliminadas_json()
            assert result == []

    def test_leer_eliminadas_json_datos_validos(self, sample_deleted_tasks):
        """Debe retornar los datos correctamente"""
        mock_data = json.dumps(sample_deleted_tasks)
        with patch("os.path.exists", return_value=True), patch(
            "builtins.open", mock_open(read_data=mock_data)
        ):
            result = leer_eliminadas_json()
            assert result == sample_deleted_tasks
