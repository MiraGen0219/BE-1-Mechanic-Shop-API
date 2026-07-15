import unittest
from datetime import date
from app import create_app
from app.extensions import cache
from app.models import (
    db,
    Inventory,
    Mechanic,
    ServiceTicket
)


class TestServiceTickets(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            cache.clear()

            self.mechanic = Mechanic(
                name="Test Mechanic",
                email="mechanic@test.com",
                phone="555-555-1234",
                salary=50000.00
            )

            self.second_mechanic = Mechanic(
                name="Second Mechanic",
                email="mechanic2@test.com",
                phone="555-555-5678",
                salary=55000.00
            )

            self.inventory_item = Inventory(
                name="Brake Pads",
                price=49.99
            )

            self.service_ticket = ServiceTicket(
                service_date=date(2026, 7, 15),
                service_desc="Replace worn brake pads",
                VIN="1HGCM82633A123456"
            )

            db.session.add_all([
                self.mechanic,
                self.second_mechanic,
                self.inventory_item,
                self.service_ticket
            ])

            db.session.commit()

            self.mechanic_id = self.mechanic.id
            self.second_mechanic_id = self.second_mechanic.id
            self.inventory_id = self.inventory_item.id
            self.ticket_id = self.service_ticket.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # CREATE SERVICE TICKET
    def test_create_service_ticket(self):
        ticket_data = {
            "service_date": "2026-07-20",
            "service_desc": "Perform oil change",
            "VIN": "2HGCM82633A654321"
        }

        response = self.client.post(
            "/service-tickets/",
            json=ticket_data
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json["service_desc"],
            "Perform oil change"
        )
        self.assertEqual(
            response.json["VIN"],
            "2HGCM82633A654321"
        )

        with self.app.app_context():
            created_ticket = db.session.get(
                ServiceTicket,
                response.json["id"]
            )

            self.assertIsNotNone(created_ticket)

    # INVALID CREATE DATA
    def test_create_service_ticket_invalid_data(self):
        ticket_data = {
            "service_desc": "Missing service date and VIN"
        }

        response = self.client.post(
            "/service-tickets/",
            json=ticket_data
        )

        self.assertEqual(response.status_code, 400)

    # GET ALL SERVICE TICKETS
    def test_get_service_tickets(self):
        response = self.client.get("/service-tickets/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("service_tickets", response.json)
        self.assertEqual(len(response.json["service_tickets"]), 1)
        self.assertEqual(response.json["total"], 1)
        self.assertEqual(response.json["page"], 1)
        self.assertEqual(response.json["per_page"], 10)

    # GET SERVICE TICKETS WITH PAGINATION
    def test_get_service_tickets_pagination(self):
        with self.app.app_context():
            second_ticket = ServiceTicket(
                service_date=date(2026, 7, 16),
                service_desc="Replace alternator",
                VIN="3HGCM82633A111111"
            )

            third_ticket = ServiceTicket(
                service_date=date(2026, 7, 17),
                service_desc="Inspect transmission",
                VIN="4HGCM82633A222222"
            )

            db.session.add_all([second_ticket, third_ticket])
            db.session.commit()

        response = self.client.get(
            "/service-tickets/?page=1&per_page=2"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["service_tickets"]), 2)
        self.assertEqual(response.json["page"], 1)
        self.assertEqual(response.json["per_page"], 2)
        self.assertEqual(response.json["total"], 3)
        self.assertEqual(response.json["pages"], 2)

    # GET SERVICE TICKET BY ID
    def test_get_service_ticket(self):
        response = self.client.get(
            f"/service-tickets/{self.ticket_id}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["id"], self.ticket_id)
        self.assertEqual(
            response.json["service_desc"],
            "Replace worn brake pads"
        )
        self.assertEqual(
            response.json["VIN"],
            "1HGCM82633A123456"
        )

    # GET SERVICE TICKET NOT FOUND
    def test_get_service_ticket_not_found(self):
        response = self.client.get("/service-tickets/9999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json["error"],
            "Service ticket not found."
        )

    # ASSIGN MECHANIC
    def test_assign_mechanic(self):
        response = self.client.put(
            f"/service-tickets/{self.ticket_id}"
            f"/assign-mechanic/{self.mechanic_id}"
        )

        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            ticket = db.session.get(
                ServiceTicket,
                self.ticket_id
            )

            mechanic_ids = [
                mechanic.id
                for mechanic in ticket.mechanics
            ]

            self.assertIn(self.mechanic_id, mechanic_ids)

    # ASSIGN MECHANIC TO MISSING TICKET
    def test_assign_mechanic_ticket_not_found(self):
        response = self.client.put(
            f"/service-tickets/9999/"
            f"assign-mechanic/{self.mechanic_id}"
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json["error"],
            "Service ticket not found."
        )

    # ASSIGN MISSING MECHANIC
    def test_assign_mechanic_not_found(self):
        response = self.client.put(
            f"/service-tickets/{self.ticket_id}/"
            "assign-mechanic/9999"
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json["error"],
            "Mechanic not found."
        )

    # REMOVE MECHANIC
    def test_remove_mechanic(self):
        with self.app.app_context():
            ticket = db.session.get(
                ServiceTicket,
                self.ticket_id
            )

            mechanic = db.session.get(
                Mechanic,
                self.mechanic_id
            )

            ticket.mechanics.append(mechanic)
            db.session.commit()

        response = self.client.put(
            f"/service-tickets/{self.ticket_id}/"
            f"remove-mechanic/{self.mechanic_id}"
        )

        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            ticket = db.session.get(
                ServiceTicket,
                self.ticket_id
            )

            mechanic_ids = [
                mechanic.id
                for mechanic in ticket.mechanics
            ]

            self.assertNotIn(self.mechanic_id, mechanic_ids)

    # EDIT SERVICE TICKET MECHANIC ASSIGNMENTS
    def test_edit_service_ticket(self):
        with self.app.app_context():
            ticket = db.session.get(
                ServiceTicket,
                self.ticket_id
            )

            first_mechanic = db.session.get(
                Mechanic,
                self.mechanic_id
            )

            ticket.mechanics.append(first_mechanic)
            db.session.commit()

        edit_data = {
            "add_mechanic_ids": [
                self.second_mechanic_id
            ],
            "remove_mechanic_ids": [
                self.mechanic_id
            ]
        }

        response = self.client.put(
            f"/service-tickets/{self.ticket_id}",
            json=edit_data
        )

        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            ticket = db.session.get(
                ServiceTicket,
                self.ticket_id
            )

            mechanic_ids = [
                mechanic.id
                for mechanic in ticket.mechanics
            ]

            self.assertNotIn(self.mechanic_id, mechanic_ids)
            self.assertIn(
                self.second_mechanic_id,
                mechanic_ids
            )

    # EDIT MISSING SERVICE TICKET
    def test_edit_service_ticket_not_found(self):
        edit_data = {
            "add_mechanic_ids": [
                self.mechanic_id
            ]
        }

        response = self.client.put(
            "/service-tickets/9999",
            json=edit_data
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json["error"],
            "Service ticket not found."
        )

    # ADD PART TO SERVICE TICKET
    def test_add_part_to_ticket(self):
        response = self.client.put(
            f"/service-tickets/{self.ticket_id}/"
            f"add-part/{self.inventory_id}"
        )

        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            ticket = db.session.get(
                ServiceTicket,
                self.ticket_id
            )

            part_ids = [
                part.id
                for part in ticket.parts
            ]

            self.assertIn(self.inventory_id, part_ids)

    # ADD PART TO MISSING TICKET
    def test_add_part_ticket_not_found(self):
        response = self.client.put(
            f"/service-tickets/9999/"
            f"add-part/{self.inventory_id}"
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json["error"],
            "Service ticket not found"
        )

    # ADD MISSING INVENTORY PART
    def test_add_part_inventory_not_found(self):
        response = self.client.put(
            f"/service-tickets/{self.ticket_id}/"
            "add-part/9999"
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json["error"],
            "Inventory item not found"
        )

    # DELETE SERVICE TICKET
    def test_delete_service_ticket(self):
        response = self.client.delete(
            f"/service-tickets/{self.ticket_id}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json["message"],
            (
                f"Service ticket {self.ticket_id} "
                "successfully deleted."
            )
        )

        with self.app.app_context():
            deleted_ticket = db.session.get(
                ServiceTicket,
                self.ticket_id
            )

            self.assertIsNone(deleted_ticket)

    # DELETE SERVICE TICKET NOT FOUND
    def test_delete_service_ticket_not_found(self):
        response = self.client.delete(
            "/service-tickets/9999"
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json["error"],
            "Service ticket not found."
        )


if __name__ == "__main__":
    unittest.main()