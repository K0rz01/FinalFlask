import pytest
import json
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_ordenes_servicio(client):
    response = client.get('/api/ordenes_servicio')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_post_ordenes_servicio(client):
    new_order = {
        "marca": "TestMarca",
        "modelo": "TestModelo",
        "serial": "123456789",
        "diag_inicial": "Diagnóstico inicial de prueba",
        "id_cliente": "cliente_test_01"
    }
    response = client.post('/api/ordenes_servicio', json=new_order)
    assert response.status_code in (200, 201)

def test_get_clientes(client):
    response = client.get('/api/clientes')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_post_clientes(client):
    new_client = {
        "cliente_id": "cliente_test_02",
        "first_name": "Test",
        "last_name": "Cliente",
        "email": "testcliente@example.com"
    }
    response = client.post('/api/clientes', json=new_client)
    assert response.status_code in (200, 201)

def test_get_cliente_by_id(client):
    cliente_id = "cliente_test_02"
    response = client.get(f'/api/clientes/{cliente_id}')
    # Puede ser 200 o 404 si no existe
    assert response.status_code in (200, 404)
