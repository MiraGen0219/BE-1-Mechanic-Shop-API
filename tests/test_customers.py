from app import create_app
from app.models import db, Customer
from datetime import datetime
from app.utils.util import encode_token
import unittest

class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.client = self.app.test_client()
        
        self.customer = Customer(name="test_user", email="test@email.com",
DOB=datetime.strptime("1990-01-01", "%Y-%m-%d").date() , password='test')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
            
            self.customer_id = self.customer.id
            self.token = encode_token(self.customer_id)
        
    def test_create_customer(self):
        customer_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "DOB": "1990-01-01",
            "password": "123"
        }
        
        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")
        
    def test_invalid_creation(self):
        customer_payload = {
            "name": "John Doe",
            "phone": "123-456-7890",
            "password": "123"
        }
        
        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ['Missing data for required field.'])
        
    def test_login_customer(self):
        credentials = {
            "email": "test@email.com",
            "password": "test"
        }
        
        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        self.assertIn("token", response.json)
    
    def test_invalid_login(self):
        credentials = {
            "email": "bad_email@email.com",
            "password": "bad_pw"
        }
        
        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Invalid email or password!')
        
    def test_update_customer(self):
        update_payload = {
            "name": "Peter",
        }
        
        response = self.client.put(f"/customers/{self.customer_id}", json=update_payload)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Peter')
        self.assertEqual(response.json['email'], 'test@email.com')
        
    def test_get_customers(self):
        response = self.client.get("/customers/")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]["email"], "test@email.com")
        
    def test_get_customer_by_id(self):
        response = self.client.get(f"/customers/{self.customer_id}")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "test_user")
        
    def test_customer_not_found(self): 
        response = self.client.get("/customers/999")
        
        self.assertEqual(response.status_code, 404)
        
    def test_delete_customer(self):
        response = self.client.delete(f"/customers/{self.customer_id}")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Customer deleted successfully.")
        
    def test_update_customer_not_found(self):
        response = self.client.put("/customers/999", json={"name": "Peter"})
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"], "Customer not found.")
        
    def test_delete_customer_not_found(self):
        response = self.client.delete("/customers/999")
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"], "Customer not found.")
        
    def test_invalid_customer_update(self):
        response = self.client.put(f"/customers/{self.customer_id}", json={"DOB": "not-a-date"})
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("DOB", response.json)