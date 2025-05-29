import unittest
import json
from app import app

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_ordenes_servicio(self):
        response = self.app.get('/api/ordenes_servicio')
        self.assertEqual(response.status_code, 401)  # Sin login debe dar no autorizado

    def test_login_logout(self):
        # Intento login con datos inválidos
        response = self.app.post('/api/login', data=json.dumps({
            'email': 'noexiste@example.com',
            'password': '1234'
        }), content_type='application/json')
        self.assertIn(response.status_code, [400, 404, 401])

        # Aquí se debería probar login con usuario válido si se conoce

    # Más pruebas pueden agregarse para clientes, creación de órdenes, etc.

if __name__ == '__main__':
    unittest.main()
