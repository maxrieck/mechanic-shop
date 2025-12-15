from app import create_app
from app.models import db
import unittest


class TestCustomer(unittest.TestCase):

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

    def test_create_customer(self):
        customer_payload = {
            "name": "John Doe",
            "email": 'doe@test.com',
            "password": "password1234",
            "phone": "555-555-5555",
        }
        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")

    def test_login(self):
        self.test_create_customer()
        login_payload = {
            "email": 'doe@test.com',
            "password": "password1234"
        }
        response = self.client.post('/customers/login', json=login_payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('auth_token', response.json)

    def test_get_customers(self):
        self.test_create_customer()
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))

    def test_get_customer_by_id(self):
        self.test_create_customer()
        login_payload = {
            "email": 'doe@test.com',
            "password": "password1234"
        }
        login_resp = self.client.post('/customers/login', json=login_payload)
        token = login_resp.json.get('auth_token', '')
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        # The test customer will have id=1
        response = self.client.get('/customers/1', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "John Doe")

    def test_update_customer(self):
        self.test_create_customer()
        # Simulate login to get token (if needed)
        login_payload = {
            "email": 'doe@test.com',
            "password": "password1234"
        }
        login_resp = self.client.post('/customers/login', json=login_payload)
        token = login_resp.json.get('auth_token', '')
        update_payload = {
            "name": "Jane Doe",
            "email": 'doe@test.com',
            "password": "password1234",
            "phone": "555-555-5555",
        }
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        response = self.client.put('/customers/', json=update_payload, headers=headers)
        self.assertIn(response.status_code, [200, 401])

    def test_delete_customer(self):
        self.test_create_customer()
        login_payload = {
            "email": 'doe@test.com',
            "password": "password1234"
        }
        login_resp = self.client.post('/customers/login', json=login_payload)
        token = login_resp.json.get('auth_token', '')
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        response = self.client.delete('/customers/', headers=headers)
        self.assertIn(response.status_code, [200, 401])

    def test_get_customer_service_tickets(self):
        self.test_create_customer()
        login_payload = {
            "email": 'doe@test.com',
            "password": "password1234"
        }
        login_resp = self.client.post('/customers/login', json=login_payload)
        token = login_resp.json.get('auth_token', '')
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        # The test customer will have id=1
        response = self.client.get('/customers/1/service_tickets', headers=headers)
        self.assertIn(response.status_code, [200, 401])

    def test_search_customer(self):
        self.test_create_customer()
        response = self.client.get('/customers/search?name=John')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))