import json

from app.tests import BaseTestClass


class TestUserModels(BaseTestClass):
    """These tests below test if the user can successfully sign """

    def test_user_sign_up(self):
        """Test if user can sign up if they provide valid information"""

        res = self.client.post(
            "/api/v2/auth/signup", data=json.dumps(self.generic_user), content_type="application/json")
        result = json.loads(res.data)
        self.assertEqual(
            result["Success"], "Succesfully created account for testing@gmail.com")
        self.assertEqual(res.status_code, 201)

    def test_duplicate_signup_attempt(self):
        """If the user attempts to sign up and they are already in the database,
        they shouldn't be allowed to"""

        self.client.post(
            "api/v2/auth/signup", data=json.dumps(self.generic_user), content_type="application/json")
        res = self.client.post(
            "api/v2/auth/signup", data=json.dumps(self.generic_user), content_type="application/json")
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

    def test_user_sign_in(self):
        """User should be able to sign in"""

        self.client.post("/api/v2/auth/signup", data=json.dumps(
            self.generic_user), content_type="application/json")
        res = self.client.post(
            "/api/v2/auth/login", data=json.dumps(self.generic_user_details),
            content_type="application/json")
        result = json.loads(res.data)
        self.assertEqual(result["Success"],
                         "You are logged in as testing@gmail.com.")
        self.assertEqual(res.status_code, 201)

    def test_wrong_password_login(self):
        """User should not be able to log in if they provide a wrong password"""

        self.client.post("/api/v2/auth/signup", data=json.dumps(
            self.generic_user), content_type="application/json")

        wrong_info = {"email": "admin@admin.admin",
                      "password": "obviouslyfake"}

        res = self.client.post(
            "/api/v2/auth/login", data=json.dumps(wrong_info), content_type="application/json")
        result = json.loads(res.data)
        self.assertEqual(
            result["Error"], "Incorrect credentials. Please try again")
        self.assertEqual(res.status_code, 401)

    def test_nonexistent_user_login(self):
        """Users who don't exist should not be able to log in"""

        fake_user = {"email": "eat@me.com",
                     "password": "lolzIKid"}

        res = self.client.post(
            "/api/v2/auth/login", data=json.dumps(fake_user), content_type="application/json")
        result = json.loads(res.data)
        self.assertEqual(result["Error"], "User does not exist")
        self.assertEqual(res.status_code, 404)

    def test_invalid_email_when_logging_in(self):
        """Only users who provide valid email address should be able to log in"""
        pass

    def test_invalid_password(self):
        """passwords should be at least 6 characters long and must contain strings"""
        pass
