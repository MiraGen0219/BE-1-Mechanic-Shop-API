import unittest
from app import create_app
from app.models import db, Item
from app.extensions import cache

class TestItems(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            cache.clear()
            
            item = Item(
                item_name="Brake Pads",
                price=49.99
            )
            
            db.session.add(item)
            db.session.commit()
            
            self.item_id = item.id
            
    def tearDown(self):
        with self.app.app_context():
            cache.clear()
            db.session.remove()
            db.drop_all()
            
    def test_create_item(self):
        item_payload = {
            "item_name": "Oil Filter",
            "price": 12.99
        }
        
        response = self.client.post("/items/", json=item_payload)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["item_name"], "Oil Filter")
        self.assertEqual(response.json["price"], 12.99)
        self.assertIn("id", response.json)
        
    def test_invalid_item_creation(self):
        item_payload = {
            "item_name": "Oil Filter"
        }
        
        response = self.client.post("/items/", json=item_payload)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("price", response.json)
        
    def test_get_items(self):
        response = self.client.get("/items/")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]["item_name"], "Brake Pads")
        self.assertEqual(response.json[0]["price"], 49.99)
        
    def test_get_item_by_id(self):
        response = self.client.get(f"/items/{self.item_id}")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["item_name"], "Brake Pads")
        self.assertEqual(response.json["price"], 49.99)
        
    def test_get_item_not_found(self):
        response = self.client.get("/items/999")
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"], "Item not found.")
        
    def test_update_item(self):
        update_payload = {
            "price": 59.99
        }
        
        response = self.client.put(f"/items/{self.item_id}", json=update_payload)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["item_name"], "Brake Pads")
        self.assertEqual(response.json["price"], 59.99)
        
    def test_update_item_not_found(self):
        response = self.client.put("/items/999", json={"price": 59.99})
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"], "Item not found.")
        
    def test_invalid_item_update(self):
        response = self.client.put(f"/items/{self.item_id}", json={"unknown_field": "invalid"})
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("unknown_field", response.json)
        
    def test_delete_item(self):
        response = self.client.delete(f"/items/{self.item_id}")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], f"Item {self.item_id} deleted successfully.")
        
    def test_delete_item_not_found(self):
        response = self.client.delete("/items/999")
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"], "Item not found.")