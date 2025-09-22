from unittest.mock import patch


class TestGetRouter:
    """Pruebas para el router GET"""

    def test_obtener_tareas(self, client, sample_tasks, mock_data_files):
        """Debe retornar todas las tareas"""
        with patch("utils.MDleer_json.leer_json", return_value=sample_tasks):
            response = client.get("/tareas")
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["titulo"] == "Tarea 1"

    def test_obtener_tarea_existente(self, client, sample_tasks, mock_data_files):
        """Debe retornar una tarea específica"""
        with patch("utils.MDleer_json.leer_json", return_value=sample_tasks), patch(
            "utils.MDleer_eliminadas_json.leer_eliminadas_json", return_value=[]
        ):
            response = client.get("/tareas/1")
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == 1
            assert data["titulo"] == "Tarea 1"

    def test_obtener_tarea_no_existente(self, client, mock_data_files):
        """Debe retornar 404 para tarea no existente"""
        with patch("utils.MDleer_json.leer_json", return_value=[]), patch(
            "utils.MDleer_eliminadas_json.leer_eliminadas_json", return_value=[]
        ):
            response = client.get("/tareas/999")
            assert response.status_code == 404
            assert "no encontrada" in response.json()["detail"]

    def test_obtener_tarea_eliminada(self, client, sample_deleted_tasks):
        """Debe retornar 410 para tarea eliminada"""
        with patch("utils.MDleer_json.leer_json", return_value=[]), patch(
            "utils.MDleer_eliminadas_json.leer_eliminadas_json",
            return_value=sample_deleted_tasks,
        ):
            response = client.get("/tareas/3")
            assert response.status_code == 410
            assert "eliminada" in response.json()["detail"]


class TestPostRouter:
    """Pruebas para el router POST"""

    def test_crear_tarea_valida(self, client, mock_data_files):
        """Debe crear una nueva tarea"""
        nueva_tarea = {
            "titulo": "Nueva Tarea",
            "descripcion": "Descripción nueva",
            "completada": False,
        }

        with patch("utils.MDleer_json.leer_json", return_value=[]), patch(
            "utils.MDobtener_proximo_id.leer_json", return_value=[]
        ), patch(
            "utils.MDobtener_proximo_id.leer_eliminadas_json", return_value=[]
        ), patch(
            "utils.MDescribir_datos.escribir_datos"
        ) as mock_escribir:
            response = client.post("/tareas", json=nueva_tarea)
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == 1
            assert data["titulo"] == "Nueva Tarea"
            mock_escribir.assert_called_once()

    def test_crear_tarea_datos_invalidos(self, client):
        """Debe retornar error para datos inválidos"""
        datos_invalidos = {
            "titulo": "",  # Título vacío
            "descripcion": "Descripción",
            "completada": False,
        }
        response = client.post("/tareas", json=datos_invalidos)
        assert response.status_code == 422  # Error de validación


class TestPutRouter:
    """Pruebas para el router PUT"""

    def test_actualizar_tarea_completa_existente(
        self, client, sample_tasks, mock_data_files
    ):
        """Debe actualizar una tarea existente completamente"""
        tarea_actualizada = {
            "titulo": "Tarea Actualizada",
            "descripcion": "Descripción actualizada",
            "completada": True,
        }

        with patch("utils.MDleer_json.leer_json", return_value=sample_tasks), patch(
            "utils.MDescribir_datos.escribir_datos"
        ) as mock_escribir:
            response = client.put("/tareas/1", json=tarea_actualizada)
            assert response.status_code == 200
            data = response.json()
            assert data["titulo"] == "Tarea Actualizada"
            assert data["completada"] is True
            mock_escribir.assert_called_once()

    def test_actualizar_tarea_no_existente(self, client, mock_data_files):
        """Debe retornar 404 para tarea no existente"""
        tarea_actualizada = {
            "titulo": "Tarea",
            "descripcion": "Descripción",
            "completada": False,
        }

        with patch("utils.MDleer_json.leer_json", return_value=[]):
            response = client.put("/tareas/999", json=tarea_actualizada)
            assert response.status_code == 404


class TestPatchRouter:
    """Pruebas para el router PATCH"""

    def test_actualizar_tarea_parcial(self, client, sample_tasks, mock_data_files):
        """Debe actualizar parcialmente una tarea"""
        cambios = {"completada": True}

        with patch("utils.MDleer_json.leer_json", return_value=sample_tasks), patch(
            "utils.MDescribir_datos.escribir_datos"
        ) as mock_escribir:
            response = client.patch("/tareas/1", json=cambios)
            assert response.status_code == 200
            data = response.json()
            assert data["completada"] is True
            assert data["titulo"] == "Tarea 1"  # Sin cambios
            mock_escribir.assert_called_once()

    def test_actualizar_tarea_parcial_no_existente(self, client, mock_data_files):
        """Debe retornar 404 para tarea no existente"""
        cambios = {"titulo": "Nuevo título"}

        with patch("utils.MDleer_json.leer_json", return_value=[]):
            response = client.patch("/tareas/999", json=cambios)
            assert response.status_code == 404


class TestDeleteRouter:
    """Pruebas para el router DELETE"""

    def test_eliminar_tarea_existente(self, client, sample_tasks, mock_data_files):
        """Debe eliminar una tarea existente"""
        with patch("utils.MDleer_json.leer_json", return_value=sample_tasks), patch(
            "utils.MDescribir_datos.escribir_datos"
        ) as mock_escribir, patch(
            "utils.MDguardar_eliminada.guardar_eliminada"
        ) as mock_guardar:
            response = client.delete("/tareas/1")
            assert response.status_code == 200
            data = response.json()
            assert "eliminada" in data["mensaje"]
            mock_escribir.assert_called_once()
            mock_guardar.assert_called_once()

    def test_eliminar_tarea_no_existente(self, client, mock_data_files):
        """Debe retornar 404 para tarea no existente"""
        with patch("utils.MDleer_json.leer_json", return_value=[]):
            response = client.delete("/tareas/999")
            assert response.status_code == 404


class TestOthersRouter:
    """Pruebas para el router OTHERS"""

    def test_get_root(self, client):
        """Debe retornar mensaje de bienvenida"""
        response = client.get("/")
        assert response.status_code == 200
        assert "API de Tareas" in response.json()["mensaje"]

    def test_get_frontend(self, client):
        """Debe servir el frontend"""
        response = client.get("/app")
        assert response.status_code == 200
        # Verificar que retorna HTML
        assert "<!DOCTYPE html>" in response.text
