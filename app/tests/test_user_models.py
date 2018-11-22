import json

from app.tests import BaseTestClass


class TestUserPassing(BaseTestClass):
    """These tests below test if the user can successfully sign """

    def test_user_sign_up(self):
        """Test if user can sign up if they provide valid information"""

        generic_user = {"first_name": "Test First",
                        "last_name": "Test Second",
                        "email": "testing@gmail.com",
                        "password": "testing",
                        "confirm_password": "testing",
                        "phone": "09323834134"}

        res = self.client.post(
            "/api/v2/auth/signup", data=json.dumps(generic_user), content_type="application/json")
        result = json.loads(res.data)
        self.assertEqual(
            result["Success"], "Succesfully created account for testing@gmail.com")
        self.assertEqual(res.status_code, 201)

    def test_duplicate_signup_attempt(self):
        """If the user attempts to sign up and they are already in the database,
        they shouldn't be allowed to"""

        generic_user = {"first_name": "Test First",
                        "last_name": "Test Second",
                        "email": "testing@gmail.com",
                        "password": "testing",
                        "confirm_password": "testing",
                        "phone": "09323834134"}

        self.client.post(
            "api/v2/auth/signup", data=json.dumps(generic_user), content_type="application/json")
        res = self.client.post(
            "api/v2/auth/signup", data=json.dumps(generic_user), content_type="application/json")
        result = json.loads(res.data)
        self.assertEqual(result["Error"], "User already exists")
        self.assertEqual(res.status_code, 409)

    def test_user_signup_with_invalid_first_name(self):
        """User should not be able to sign up with invalid first name"""
        pass

    def test_user_signup_with_invalid_last_name(self):
        """"""
        pass

    def test_signup_attempt_with_nonexistent_user(self):
        """If a user tries to log in but they do not have an account, view should return 404"""

        details = {"email": "admooin@admin.admin",
                   "password": "oiudof987ewrqlwe"}

        res = self.client.post(
            "/api/v2/auth/login", data=json.dumps(details), content_type="application/json")
        self.assertEqual(res.status_code, 404)
