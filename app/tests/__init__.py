import unittest
import json

from app import create_app
from db_config import destroy_tables


class BaseTestClass(unittest.TestCase):
    """This is our base test class"""

    def setUp(self):
        """This will be run before each test"""
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app.testing = True

        self.default_user = {"first_name": "Default",
                             "last_name": "Last Name",
                             "email": "default@user.com",
                             "password": "password",
                             "confirm_password": "password",
                             "phone": "09329479245"}

        self.default_user_login = {"email": "default@user.com",
                                   "password": "password"}

        self.client.post("/api/v2/auth/signup",
                         data=json.dumps(self.default_user),
                         content_type="application/json")
        log = self.client.post("/api/v2/auth/login", data=json.dumps(
            self.default_user_login), content_type="application/json")
        user_data = json.loads(log.get_data(as_text=True))
        self.generic_user_token = user_data["token"]
        self.headers = {"AUTHORIZATION": "Bearer " + self.generic_user_token}

        self.generic_user = {"first_name": "Test First",
                             "last_name": "Test Second",
                             "email": "testing@gmail.com",
                             "password": "testing",
                             "confirm_password": "testing",
                             "phone": "09323834134"}

        self.generic_parcel = {"parcel_name": "Contracts",
                               "recipient_name": "Irelia",
                               "pickup_location": "Mount DOOM",
                               "destination": "Gondor",
                               "weight": "323"
                               }

        self.default_parcel = {"parcel_name": "Contracts",
                               "recipient_name": "Irelia",
                               "pickup_location": "Mount DOOM",
                               "destination": "Gondor",
                               "weight": "323"}

        # we need to sign in the admin
        admin_details = {"email": "admin@admin.admin",
                         "password": "adminpassword"}

        admin_log = self.client.post(
            "/api/v2/auth/login", data=json.dumps(admin_details),
            content_type="application/json")
        admin_data = json.loads(admin_log.get_data(as_text=True))
        self.admin_token = admin_data["token"]
        self.admin_header = {"AUTHORIZATION": "Bearer " + self.admin_token}

        # the default user creates a default parcel each time a test is run
        self.client.post("/api/v2/parcels", data=json.dumps(self.default_parcel),
                         content_type="application/json", headers=self.headers)

    def tearDown(self):
        destroy_tables()
