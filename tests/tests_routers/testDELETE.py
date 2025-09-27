from unittest.mock import patch


def test_eliminar_tarea_existente(client, sample_tasks, mock_data_files):
    """Debe eliminar una tarea existente"""
    with patch("routers.GET.leer_json", return_value=sample_tasks), patch(
        "routers.POST.escribir_datos"
    ) as mock_escribir, patch("routers.DELETE.guardar_eliminada") as mock_guardar:
        response = client.delete("/tareas/1")
        assert response.status_code == 200
        data = response.json()
        assert "eliminada" in data["mensaje"]
        mock_escribir.assert_called_once()
        mock_guardar.assert_called_once()


def test_eliminar_tarea_no_existente(client, mock_data_files):
    """Debe retornar 404 para tarea no existente"""
    with patch("routers.GET.leer_json", return_value=[]):
        response = client.delete("/tareas/999")
        assert response.status_code == 404
