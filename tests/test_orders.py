import unittest
from datetime import date
from app import create_app
from app.models import db, Order, OrderItem, Item, Customer
from app.extensions import cache

class TestOrders(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            cache.clear()
            
            self.customer = Customer(
                name="Test Customer",
                email="testcustomer@email.com",
                DOB=date(1990, 1, 1),
                password="testpassword"
            )
            
            self.item = Item(
                item_name="Brake Pads",
                price=40.00
            )
            
            db.session.add_all([self.customer, self.item])
            db.session.commit()
            
            self.customer_id = self.customer.id
            self.item_id = self.item.id
            
            self.order = Order(
                customer_id=self.customer_id,
                order_date=date.today()
            )
            
            db.session.add(self.order)
            db.session.commit()
            
            self.order_item = OrderItem(
                order_id=self.order.id,
                item_id=self.item_id,
                quantity=2
            )
            
            db.session.add(self.order_item)
            db.session.commit()
            
            self.order_id = self.order.id
            self.order_item_id = self.order_item.id
            
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            
    def test_create_order(self):
        order_data = {
            "customer_id": self.customer_id,
            "item_quantity": [{
                "item_id": self.item_id,
                "item_quantity": 3
            }]
        }
        
        response = self.client.post("/orders/", json=order_data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["customer_id"], self.customer_id)
        self.assertEqual(response.json["total"], 120.00)
        self.assertEqual(len(response.json["items"]), 1)
        self.assertEqual(response.json["items"][0]["item"], "Brake Pads")
        self.assertEqual(response.json["items"][0]["quantity"], 3)
        self.assertEqual(response.json["items"][0]["subtotal"], 120.00)
        
    def test_get_orders(self):
        response = self.client.get("/orders/")
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]["id"], self.order_id)
        
    def test_get_order(self):
        response = self.client.get(f"/orders/{self.order_id}")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["id"], self.order_id)
        
    def test_get_order_not_found(self):
        response = self.client.get("/orders/9999")
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["message"], "Order not found")
        
    def test_get_order_receipt(self):
        response = self.client.get(f"/orders/{self.order_id}/receipt")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["order_id"], self.order_id)
        self.assertEqual(response.json["customer_id"], self.customer_id)
        self.assertEqual(response.json["total"], 80.00)
        self.assertEqual(len(response.json["items"]), 1)
        self.assertEqual(response.json["items"][0]["item"], "Brake Pads")
        self.assertEqual(response.json["items"][0]["quantity"], 2)
        self.assertEqual(response.json["items"][0]["subtotal"], 80.00)
        
    def test_get_order_receipt_not_found(self):
        response = self.client.get("/orders/9999/receipt")
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["message"], "Order not found")
        
    def test_delete_order(self):
        response = self.client.delete(f"/orders/{self.order_id}")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], f"Order {self.order_id} successfully deleted")
        
        with self.app.app_context():
            deleted_order = db.session.get(Order, self.order_id)
            deleted_order_item = db.session.get(
                OrderItem,
                self.order_item.id
            )
            
            self.assertIsNone(deleted_order)
            self.assertIsNone(deleted_order_item)
            
    def test_delete_order_not_found(self):
        response = self.client.delete("/orders/9999")
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["message"], "Order not found")