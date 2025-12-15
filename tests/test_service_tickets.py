from app import create_app
from app.models import db
import unittest


class TestServiceTicket(unittest.TestCase):

    def create_mechanic(self):
        mechanic_payload = {
            "name": "Jane Smith",
            "email": 'jane@test.com',
            "phone": "555-777-5555",
            "salary": 50000.00
        }
        self.client.post('/mechanics/', json=mechanic_payload)

    def create_inventory(self):
        inventory_payload = {
            "name": "Brake Pads",
            "price": 49.99
        }
        self.client.post('/inventory/', json=inventory_payload)

    def test_add_item_to_ticket(self):
        self.test_create_service_ticket()
        self.create_inventory()
        response = self.client.put('/service_tickets/1/add_item/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully added item', response.json['Message'])

    def test_assign_mechanic_to_ticket(self):
        self.test_create_service_ticket()
        self.create_mechanic()
        response = self.client.put('/service_tickets/1/assign_mechanic/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully assigned mechanic', response.json['Message'])

    def test_remove_mechanic_from_ticket(self):
        self.test_create_service_ticket()
        self.create_mechanic()
        # Assign mechanic first
        self.client.put('/service_tickets/1/assign_mechanic/1')
        response = self.client.put('/service_tickets/1/remove_mechanic/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully removed mechanic', response.json['Message'])

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

    def test_create_service_ticket(self):
        
        customer_payload = {
            "name": "John Doe",
            "email": 'doe@test.com',
            "password": "password1234",
            "phone": "555-555-5555",
        }
        self.client.post('/customers/', json=customer_payload)
        ticket_payload = {
            "VIN": "1HGCM82633A004352",
            "service_date": "2025-12-14",
            "service_desc": "Brake replacement",
            "customer_id": 1
        }
        response = self.client.post('/service_tickets/', json=ticket_payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn('ticket', response.json['Message'])



    def test_get_service_tickets(self):
        self.test_create_service_ticket()
        response = self.client.get('/service_tickets/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))

    def test_get_service_ticket_by_id(self):
        self.test_create_service_ticket()
        response = self.client.get('/service_tickets/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], 1)

    def test_update_service_ticket(self):
        self.test_create_service_ticket()
        update_payload = {
            "add_mechanic_ids": [],
            "remove_mechanic_ids": []
        }
        response = self.client.put('/service_tickets/1', json=update_payload)
        self.assertEqual(response.status_code, 200)


