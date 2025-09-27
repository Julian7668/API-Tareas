def test_get_root(client):
    """Debe retornar mensaje de bienvenida"""
    response = client.get("/")
    assert response.status_code == 200
    assert "API de Tareas" in response.json()["mensaje"]


def test_get_frontend(client):
    """Debe servir el frontend"""
    response = client.get("/app")
    assert response.status_code == 200
    # Verificar que retorna HTML
    assert "<!DOCTYPE html>" in response.text
