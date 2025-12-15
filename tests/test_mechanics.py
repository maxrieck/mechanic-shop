from app import create_app
from app.models import db
import unittest


class TestMechanic(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.engine.dispose()
        self.app_context.pop()

    def test_create_mechanic(self):
        mechanic_payload = {
            "name": "Jane Smith",
            "email": 'jane@test.com',
            "phone": "555-777-5555",
            "salary": 50000.00
        }
        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Jane Smith")

    def test_get_mechanics(self):
        self.test_create_mechanic()
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))

    def test_get_mechanic_by_id(self):
        self.test_create_mechanic()
        response = self.client.get('/mechanics/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Jane Smith")

    def test_update_mechanic(self):
        self.test_create_mechanic()
        update_payload = {
            "name": "Jane Doe",
            "email": 'jane@test.com',
            "phone": "555-888-5555",
            "salary": 60000.00
        }
        response = self.client.put('/mechanics/1', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Jane Doe")

    def test_delete_mechanic(self):
        self.test_create_mechanic()
        response = self.client.delete('/mechanics/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('successfully deleted', response.json['message'])

    def test_popular_mechanics(self):
        self.test_create_mechanic()
        response = self.client.get('/mechanics/popular')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))