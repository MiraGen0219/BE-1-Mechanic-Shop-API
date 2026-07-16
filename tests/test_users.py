import unittest

from app import create_app
from app.extensions import cache, limiter
from app.models import User, db
from app.utils.util import encode_token


class TestUsers(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            cache.clear()

            # Prevent rate-limit counts from carrying between tests.
            limiter.reset()

            self.user = User(
                username="testuser",
                email="testuser@email.com",
                password="testpassword"
            )

            db.session.add(self.user)
            db.session.commit()

            self.user_id = self.user.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            cache.clear()
            limiter.reset()

    # CREATE USER
    def test_create_user(self):
        user_data = {
            "username": "newuser",
            "email": "newuser@email.com",
            "password": "newpassword"
        }

        response = self.client.post(
            "/users/",
            json=user_data
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json["username"],
            "newuser"
        )
        self.assertEqual(
            response.json["email"],
            "newuser@email.com"
        )

        # Password should not be serialized because it is load_only.
        self.assertNotIn("password", response.json)

        with self.app.app_context():
            created_user = User.query.filter_by(
                email="newuser@email.com"
            ).first()

            self.assertIsNotNone(created_user)
            self.assertEqual(
                created_user.username,
                "newuser"
            )

    # CREATE USER WITH INVALID EMAIL
    def test_create_user_invalid_email(self):
        user_data = {
            "username": "newuser",
            "email": "not-an-email",
            "password": "newpassword"
        }

        response = self.client.post(
            "/users/",
            json=user_data
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.json)

    # CREATE USER WITH MISSING DATA
    def test_create_user_missing_data(self):
        user_data = {
            "email": "newuser@email.com"
        }

        response = self.client.post(
            "/users/",
            json=user_data
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("username", response.json)
        self.assertIn("password", response.json)

    # CREATE USER WITH DUPLICATE EMAIL
    def test_create_user_duplicate_email(self):
        user_data = {
            "username": "differentuser",
            "email": "testuser@email.com",
            "password": "newpassword"
        }

        response = self.client.post(
            "/users/",
            json=user_data
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response.json["message"],
            "A user with that email already exists"
        )

    # CREATE USER WITH DUPLICATE USERNAME
    def test_create_user_duplicate_username(self):
        user_data = {
            "username": "testuser",
            "email": "different@email.com",
            "password": "newpassword"
        }

        response = self.client.post(
            "/users/",
            json=user_data
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response.json["message"],
            "A user with that username already exists"
        )

    # GET ALL USERS
    def test_get_users(self):
        response = self.client.get("/users/")

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 1)

        self.assertEqual(
            response.json[0]["id"],
            self.user_id
        )
        self.assertEqual(
            response.json[0]["username"],
            "testuser"
        )
        self.assertEqual(
            response.json[0]["email"],
            "testuser@email.com"
        )

        # Password should never appear in the response.
        self.assertNotIn(
            "password",
            response.json[0]
        )

    # SUCCESSFUL LOGIN
    def test_login(self):
        credentials = {
            "email": "testuser@email.com",
            "password": "testpassword"
        }

        response = self.client.post(
            "/users/login",
            json=credentials
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json["status"],
            "success"
        )
        self.assertEqual(
            response.json["message"],
            "Successfully Logged In"
        )
        self.assertIn("auth_token", response.json)

    # INVALID LOGIN
    def test_invalid_login(self):
        credentials = {
            "email": "testuser@email.com",
            "password": "wrongpassword"
        }

        response = self.client.post(
            "/users/login",
            json=credentials
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json["message"],
            "Invalid email or password"
        )

    # LOGIN WITH INVALID PAYLOAD
    def test_login_invalid_payload(self):
        credentials = {
            "email": "testuser@email.com"
        }

        response = self.client.post(
            "/users/login",
            json=credentials
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json["message"],
            "Invalid payload, expecting email and password"
        )

    # DELETE AUTHENTICATED USER
    def test_delete_user(self):
        token = encode_token(self.user_id)

        response = self.client.delete(
            "/users/",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json["message"],
            f"Successfully deleted user {self.user_id}"
        )

        with self.app.app_context():
            deleted_user = db.session.get(
                User,
                self.user_id
            )

            self.assertIsNone(deleted_user)

    # DELETE WITHOUT AUTHENTICATION
    def test_delete_user_without_token(self):
        response = self.client.delete("/users/")

        self.assertIn(
            response.status_code,
            [401, 403]
        )

    # CREATE USER RATE LIMIT
    def test_create_user_rate_limit(self):
        for number in range(3):
            user_data = {
                "username": f"rateuser{number}",
                "email": f"rateuser{number}@email.com",
                "password": "testpassword"
            }

            response = self.client.post(
                "/users/",
                json=user_data
            )

            self.assertEqual(
                response.status_code,
                201
            )

        fourth_user = {
            "username": "rateuser4",
            "email": "rateuser4@email.com",
            "password": "testpassword"
        }

        response = self.client.post(
            "/users/",
            json=fourth_user
        )

        self.assertEqual(response.status_code, 429)


if __name__ == "__main__":
    unittest.main()