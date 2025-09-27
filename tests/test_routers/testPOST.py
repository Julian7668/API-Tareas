from unittest.mock import patch


def test_crear_tarea_valida(client, mock_data_files):
    """Debe crear una nueva tarea"""
    nueva_tarea = {
        "titulo": "Nueva Tarea",
        "descripcion": "Descripción nueva",
        "completada": False,
    }

    with patch("routers.GET.leer_json", return_value=[]), patch(
        "routers.POST.obtener_proximo_id", return_value=1
    ), patch(
        "routers.POST.leer_json", return_value=[]
    ), patch(
        "routers.POST.escribir_datos"
    ) as mock_escribir:
        response = client.post("/tareas", json=nueva_tarea)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["titulo"] == "Nueva Tarea"
        mock_escribir.assert_called_once()


def test_crear_tarea_datos_invalidos(client):
    """Debe retornar error para datos inválidos"""
    datos_invalidos = {
        "titulo": "",  # Título vacío
        "descripcion": "Descripción",
        "completada": False,
    }
    response = client.post("/tareas", json=datos_invalidos)
    assert response.status_code == 422  # Error de validación
