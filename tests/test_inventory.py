import unittest

from app import create_app
from app.models import db, Inventory


class TestInventory(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            inventory_item = Inventory(
                name="Alternator",
                price=189.99
            )

            db.session.add(inventory_item)
            db.session.commit()

            self.inventory_item_id = inventory_item.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_inventory_item(self):
        inventory_payload = {
            "name": "Starter Motor",
            "price": 149.99
        }

        response = self.client.post(
            "/inventory/",
            json=inventory_payload
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], "Starter Motor")
        self.assertEqual(response.json["price"], 149.99)
        self.assertIn("id", response.json)

    def test_invalid_inventory_creation(self):
        inventory_payload = {
            "name": "Starter Motor"
        }

        response = self.client.post(
            "/inventory/",
            json=inventory_payload
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("price", response.json)

    def test_get_inventory(self):
        response = self.client.get("/inventory/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]["name"], "Alternator")
        self.assertEqual(response.json[0]["price"], 189.99)

    def test_get_inventory_item_by_id(self):
        response = self.client.get(
            f"/inventory/{self.inventory_item_id}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Alternator")
        self.assertEqual(response.json["price"], 189.99)

    def test_get_inventory_item_not_found(self):
        response = self.client.get("/inventory/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json["error"],
            "Inventory item not found"
        )

    def test_update_inventory_item(self):
        update_payload = {
            "price": 199.99
        }

        response = self.client.put(
            f"/inventory/{self.inventory_item_id}",
            json=update_payload
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Alternator")
        self.assertEqual(response.json["price"], 199.99)

    def test_update_inventory_item_not_found(self):
        response = self.client.put(
            "/inventory/999",
            json={"price": 199.99}
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json["error"],
            "Inventory item not found"
        )

    def test_invalid_inventory_update(self):
        response = self.client.put(
            f"/inventory/{self.inventory_item_id}",
            json={"unknown_field": "invalid"}
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("unknown_field", response.json)

    def test_delete_inventory_item(self):
        response = self.client.delete(
            f"/inventory/{self.inventory_item_id}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json["message"],
            f"Inventory item {self.inventory_item_id} deleted successfully"
        )

    def test_delete_inventory_item_not_found(self):
        response = self.client.delete("/inventory/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json["error"],
            "Inventory item not found"
        )