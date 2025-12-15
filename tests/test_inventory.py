from app import create_app
from app.models import db
import unittest


class TestInventory(unittest.TestCase):

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

    def test_create_item(self):
        item_payload = {
            "name": "Brake Pads",
            "price": 49.99
        }
        response = self.client.post('/inventory/', json=item_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Brake Pads")



    def test_get_inventory(self):
        self.test_create_item()
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))

    def test_get_item_by_id(self):
        self.test_create_item()
        response = self.client.get('/inventory/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Brake Pads")

    def test_update_item(self):
        self.test_create_item()
        update_payload = {
            "name": "Brake Pads XL",
            "price": 59.99
        }
        response = self.client.put('/inventory/1', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Brake Pads XL")

    def test_delete_item(self):
        self.test_create_item()
        response = self.client.delete('/inventory/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('successfully deleted', response.json['message'])



