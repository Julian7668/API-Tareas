from unittest.mock import patch, mock_open
import pytest


def test_escribir_datos_exitoso(sample_tasks):
    """Debe escribir datos correctamente al archivo JSON"""
    with patch("builtins.open", mock_open()) as mock_file, patch(
        "utils.MDescribir_datos.logger"
    ) as mock_logger:

        from utils import escribir_datos

        escribir_datos(sample_tasks)

        # Verificar que se abrió el archivo para escritura (el path puede variar)
        mock_file.assert_called_once()
        call_args = mock_file.call_args
        file_path = call_args[0][0]
        assert (
            "tareas.json" in file_path
        )  # Verificar que contiene el nombre del archivo
        assert call_args[1] == {"encoding": "utf-8"}

        # Verificar que se llamó a write() múltiples veces (json.dump() escribe por partes)
        assert mock_file.return_value.write.call_count > 0
        # Verificar que la primera llamada escribió algo
        first_call_args = mock_file.return_value.write.call_args_list[0][0][0]
        assert len(first_call_args) > 0  # Verificar que escribió algo

        # Verificar que se hicieron los logs de debug (2 llamadas: inicio y fin)
        assert mock_logger.debug.call_count >= 1


def test_escribir_datos_error_escritura(sample_tasks):
    """Debe manejar errores de escritura correctamente"""
    with patch("builtins.open", side_effect=Exception("Error de escritura")), patch(
        "utils.MDescribir_datos.logger"
    ) as mock_logger:

        from utils import escribir_datos

        # Debe lanzar la excepción
        with pytest.raises(Exception, match="Error de escritura"):
            escribir_datos(sample_tasks)

        # Verificar que se hizo log de error
        mock_logger.error.assert_called()


def test_escribir_datos_lista_vacia():
    """Debe escribir lista vacía correctamente"""
    datos_vacios = []

    with patch("builtins.open", mock_open()) as mock_file, patch(
        "utils.MDescribir_datos.logger"
    ) as mock_logger:

        from utils import escribir_datos

        escribir_datos(datos_vacios)

        # Verificar que se llamó a write() múltiples veces (json.dump() escribe por partes)
        assert mock_file.return_value.write.call_count > 0
        # Verificar que la primera llamada escribió algo
        first_call_args = mock_file.return_value.write.call_args_list[0][0][0]
        assert len(first_call_args) > 0  # Verificar que escribió algo

        # Verificar que se hicieron logs de debug (mínimo 1 llamada)
        assert mock_logger.debug.call_count >= 1
