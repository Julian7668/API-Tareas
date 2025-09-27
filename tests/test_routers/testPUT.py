from unittest.mock import patch


def test_actualizar_tarea_completa_existente(client, sample_tasks, mock_data_files):
    """Debe actualizar una tarea existente completamente"""
    tarea_actualizada = {
        "titulo": "Tarea Actualizada",
        "descripcion": "Descripción actualizada",
        "completada": True,
    }

    with patch("routers.GET.leer_json", return_value=sample_tasks), patch(
        "routers.POST.escribir_datos"
    ) as mock_escribir:
        response = client.put("/tareas/1", json=tarea_actualizada)
        assert response.status_code == 200
        data = response.json()
        assert data["titulo"] == "Tarea Actualizada"
        assert data["completada"] is True
        mock_escribir.assert_called_once()


def test_actualizar_tarea_no_existente(client, mock_data_files):
    """Debe retornar 404 para tarea no existente"""
    tarea_actualizada = {
        "titulo": "Tarea",
        "descripcion": "Descripción",
        "completada": False,
    }

    with patch("routers.GET.leer_json", return_value=[]):
        response = client.put("/tareas/999", json=tarea_actualizada)
        assert response.status_code == 404
