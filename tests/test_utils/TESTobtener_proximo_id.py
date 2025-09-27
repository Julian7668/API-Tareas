from unittest.mock import patch


def test_obtener_proximo_id_sin_datos():
    """Debe retornar 1 si no hay datos"""
    with patch("utils.leer_json", return_value=[]), patch(
        "utils.leer_eliminadas_json", return_value=[]
    ):
        from utils import obtener_proximo_id

        result = obtener_proximo_id()
        assert result == 1


def test_obtener_proximo_id_con_datos_activos(sample_tasks):
    """Debe calcular el próximo ID basado en tareas activas"""
    with patch("utils.leer_json", return_value=sample_tasks), patch(
        "utils.leer_eliminadas_json", return_value=[]
    ):
        from utils import obtener_proximo_id

        result = obtener_proximo_id()
        assert result == 3  # max id en sample_tasks es 2, próximo es 3


def test_obtener_proximo_id_con_datos_eliminados(sample_tasks, sample_deleted_tasks):
    """Debe considerar IDs de tareas eliminadas"""
    with patch("utils.leer_json", return_value=sample_tasks), patch(
        "utils.leer_eliminadas_json",
        return_value=sample_deleted_tasks,
    ):
        from utils import obtener_proximo_id

        result = obtener_proximo_id()
        assert result == 4  # max id es 3 (de eliminadas), próximo es 4
