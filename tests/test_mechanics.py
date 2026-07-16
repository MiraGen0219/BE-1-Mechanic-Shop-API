import unittest
from app import create_app
from app.models import db, Mechanic

class TestMechanic(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            
            mechanic = Mechanic(
                name="Joe Bosh",
                email="joe@email.com",
                phone="555-555-5555",
                salary=50000.00
            )
            
            db.session.add(mechanic)
            db.session.commit()
            
            self.mechanic_id = mechanic.id
            
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            
    def test_create_mechanic(self):
        mechanic_payload = {
            "name": "Jane Smith",
            "email": "jane@email.com",
            "phone": "555-555-5555",
            "salary": 55000.00
        }
        
        response = self.client.post("/mechanics/", json=mechanic_payload)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], "Jane Smith")
        self.assertEqual(response.json["email"], "jane@email.com")
        self.assertIn("id", response.json)
        
    def test_invalid_mechanic_creation(self):
        mechanic_payload = {
            "name": "Jane Smith"
        }
        
        response = self.client.post("/mechanics/", json=mechanic_payload)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.json)
        
    def test_duplicate_mechanic_email(self):
        mechanic_payload = {
            "name": "Another Joe",
            "email": "joe@email.com",
            "phone": "555-555-5555",
            "salary": 55000.00
        }
        
        response = self.client.post("/mechanics/", json=mechanic_payload)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Email already associated with a mechanic.")
        
    def test_get_mechanics(self):
        response = self.client.get("/mechanics/")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]["name"], "Joe Bosh")
        self.assertEqual(response.json[0]["email"], "joe@email.com")
        
    def test_search_mechanics(self): 
        response = self.client.get("/mechanics/search?name=Joe")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]["name"], "Joe Bosh")
        
    def test_search_mechanics_no_matches(self):
        response = self.client.get("/mechanics/search?name=Harold")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])
        
    def test_update_mechanic(self):
        update_payload = {
            "name": "Joseph Bosh"
        }
        
        response = self.client.put(f"/mechanics/{self.mechanic_id}", json=update_payload)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Joseph Bosh")
        self.assertEqual(response.json["email"], "joe@email.com")
        
    def test_update_mechanic_not_found(self):
        response = self.client.put("/mechanics/999", json={"name": "Joseph Bosh"})
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"], "Mechanic not found.")
        
    def test_invalid_mechanic_update(self):
        response = self.client.put(f"/mechanics/{self.mechanic_id}", json={"unknown_field": "invalid"})
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("unknown_field", response.json)
        
    def test_delete_mechanic(self):
        response = self.client.delete(f"/mechanics/{self.mechanic_id}")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Mechanic deleted successfully")
        
    def test_delete_mechanic_not_found(self):
        response = self.client.delete("/mechanics/999")
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"], "Mechanic not found.")
        
    def test_frequent_mechanics(self):
        response = self.client.get("/mechanics/frequent")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]["name"], "Joe Bosh")
        self.assertEqual(response.json[0]["ticket_count"], 0)