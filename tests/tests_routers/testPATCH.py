from unittest.mock import patch


def test_actualizar_tarea_parcial(client, sample_tasks, mock_data_files):
    """Debe actualizar parcialmente una tarea"""
    cambios = {"completada": True}

    with patch("routers.GET.leer_json", return_value=sample_tasks), patch(
        "routers.POST.escribir_datos"
    ) as mock_escribir:
        response = client.patch("/tareas/1", json=cambios)
        assert response.status_code == 200
        data = response.json()
        assert data["completada"] is True
        assert data["titulo"] == "Tarea 1"  # Sin cambios
        mock_escribir.assert_called_once()


def test_actualizar_tarea_parcial_no_existente(client, mock_data_files):
    """Debe retornar 404 para tarea no existente"""
    cambios = {"titulo": "Nuevo título"}

    with patch("routers.GET.leer_json", return_value=[]):
        response = client.patch("/tareas/999", json=cambios)
        assert response.status_code == 404
