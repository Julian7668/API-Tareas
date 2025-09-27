from unittest.mock import patch


def test_obtener_tareas(client, sample_tasks, mock_data_files):
    """Debe retornar todas las tareas"""
    with patch("routers.GET.leer_json", return_value=sample_tasks):
        response = client.get("/tareas")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["titulo"] == "Tarea 1"


def test_obtener_tarea_existente(client, sample_tasks, mock_data_files):
    """Debe retornar una tarea específica"""
    with patch("routers.GET.leer_json", return_value=sample_tasks), patch(
        "routers.GET.leer_eliminadas_json", return_value=[]
    ):
        response = client.get("/tareas/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["titulo"] == "Tarea 1"


def test_obtener_tarea_no_existente(client, mock_data_files):
    """Debe retornar 404 para tarea no existente"""
    with patch("routers.GET.leer_json", return_value=[]), patch(
        "routers.GET.leer_eliminadas_json", return_value=[]
    ):
        response = client.get("/tareas/999")
        assert response.status_code == 404
        assert "no encontrada" in response.json()["detail"]


def test_obtener_tarea_eliminada(client, sample_deleted_tasks):
    """Debe retornar 410 para tarea eliminada"""
    with patch("routers.GET.leer_json", return_value=[]), patch(
        "routers.GET.leer_eliminadas_json",
        return_value=sample_deleted_tasks,
    ):
        response = client.get("/tareas/3")
        assert response.status_code == 410
        assert "eliminada" in response.json()["detail"]
