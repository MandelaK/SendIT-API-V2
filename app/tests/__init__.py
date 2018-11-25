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

        #set up, sign up and log in a default user
        self.default_user = {"first_name": "Default",
                             "last_name": "User",
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

        #get default user token
        self.default_user_token = user_data["token"]
        self.headers = {"AUTHORIZATION": "Bearer " + self.default_user_token}

        #set up generic user information
        self.generic_user = {"first_name": "Generic",
                             "last_name": "User",
                             "email": "generic@user.com",
                             "password": "password",
                             "confirm_password": "password",
                             "phone": "09323834134"}
        self.generic_user_details = {"email": "generic@user.com",
                                     "password": "password"}

        #set up generic parcel details
        self.generic_parcel = {"parcel_name": "Generic Test Parcel",
                               "recipient_name": "Generic Recipient",
                               "pickup_location": "Generic Pickup",
                               "destination": "Generic Destination",
                               "weight": "420"
                               }

        #set up default parcel details
        self.default_parcel = {"parcel_name": "Default Test Parcel",
                               "recipient_name": "Default Recipient",
                               "pickup_location": "Default Location",
                               "destination": "Default Destination",
                               "weight": "420"}

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
        self.client.post("/api/v2/users/parcels", data=json.dumps(self.default_parcel),
                         content_type="application/json", headers=self.headers)

    def tearDown(self):
        destroy_tables()
