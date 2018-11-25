import json

from app.tests import BaseTestClass


class TestParcelView(BaseTestClass):
    """"""

    def test__create_order(self):
        """This will test POST /parcels"""

        res = self.client.post(
            "api/v2/users/parcels", data=json.dumps(self.generic_parcel),
            content_type="application/json", headers=self.headers)

        result = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(result["Success"], "Your parcel order has been saved")

    def test_invalid_parcel_name(self):
        """Parcels must have valid names in order to be sent"""
        fake_parcel = {"parcel_name": "   ",
                       "recipient_name": "Generic Recipient",
                       "pickup_location": "Generic Pickup",
                       "destination": "Generic Destination",
                       "weight": "420"
                       }
        res = self.client.post("/api/v2/users/parcels",
                               data=json.dumps(fake_parcel),
                               content_type="application/json", headers=self.headers)
        result = json.loads(res.data)
        self.assertEqual(result["Error"], "Please enter valid parcel name")
        self.assertEqual(res.status_code, 400)

    def test_invalid_pickup_location(self):
        """Parcels must have valid pickup location"""
        fake_parcel = {"parcel_name": "fake",
                       "recipient_name": "Generic Recipient",
                       "pickup_location": "     ",
                       "destination": "Generic Destination",
                       "weight": "420"
                       }

        res = self.client.post("/api/v2/users/parcels",
                               data=json.dumps(fake_parcel),
                               content_type="application/json", headers=self.headers)
        result = json.loads(res.data)
        self.assertEqual(result["Error"], "Please enter valid pickup location")
        self.assertEqual(res.status_code, 400)

    def test_invalid_destination(self):
        """Parcels must have valid destination"""
        fake_parcel = {"parcel_name": "fake",
                       "recipient_name": "Generic Recipient",
                       "pickup_location": "Over here",
                       "destination": "   ",
                       "weight": "420"
                       }

        res = self.client.post("/api/v2/users/parcels",
                               data=json.dumps(fake_parcel),
                               content_type="application/json", headers=self.headers)
        result = json.loads(res.data)
        self.assertEqual(result["Error"], "Please enter valid destination")
        self.assertEqual(res.status_code, 400)

    def test_valid_weight(self):
        """Parcels must have valid weight"""
        fake_parcel = {"parcel_name": "fake",
                       "recipient_name": "Generic Recipient",
                       "pickup_location": "Over here",
                       "destination": "Over there",
                       "weight": "so fake"
                       }

        res = self.client.post("/api/v2/users/parcels",
                               data=json.dumps(fake_parcel),
                               content_type="application/json", headers=self.headers)
        result = json.loads(res.data)
        self.assertEqual(
            result["Error"], "Please enter postive weight in integers")
        self.assertEqual(res.status_code, 400)

    def test_admin_can_create_parcel(self):
        """Admins should not be able to create parcels"""
        res = self.client.post("/api/v2/users/parcels", data=json.dumps(
            self.generic_parcel), content_type="application/json", headers=self.admin_header)

        result = json.loads(res.data)
        self.assertEqual(result["Forbidden"], "Admins cannot create parcels")
        self.assertEqual(res.status_code, 403)

    def test_user_change_destination(self):
        """User should be able to change destination of parcels
        that are pending"""

        self.client.post("/api/v2/users/parcels", data=json.dumps(self.generic_parcel),
                         content_type="application/json", headers=self.headers)

        update_destination = {"destination": "Malibu"}

        res = self.client.put("/api/v2/parcels/1/destination", data=json.dumps(
            update_destination), content_type="application/json", headers=self.headers)
        result = json.loads(res.data)
        self.assertEqual(result["Success"],
                         "Destination for parcel 1 succesfully changed")
        self.assertEqual(res.status_code, 200)

    def test_user_enters_numbers_as_destination(self):
        """User should not be able to add numbers as destination"""

        parcel = {"parcel_name": "Contracts",
                  "recipient_name": "Irelia",
                  "pickup_location": "Mount DOOM",
                  "destination": "1234123452",
                  "weight": "323"}

        res = self.client.post("api/v2/users/parcels", data=json.dumps(parcel),
                               content_type="application/json", headers=self.headers)
        result = json.loads(res.data)
        self.assertEqual(result["Error"], "Please enter valid destination")
        self.assertEqual(res.status_code, 400)

    def test_nonexistent_parcel_destination(self):
        """User should not be able to change destination of parcels
        that don't exist"""

        des = {"destination": "Nairoberry"}
        res = self.client.put("/api/v2/parcels/5/destination",
                              data=json.dumps(des), content_type="application/json",
                              headers=self.headers)
        result = json.loads(res.data)
        self.assertEqual(result["Error"], "Parcel not found")
        self.assertEqual(res.status_code, 404)

    def test_admin_change_destination(self):
        """Admin should not be able to change the destination of parcels"""

        self.client.post(
            "api/v2/users/parcels", data=(json.dumps(self.generic_parcel)),
            content_type="application/json", headers=self.headers)

        des = {"destination": "Nairoberry"}

        res = self.client.put("/api/v2/parcels/1/destination",
                              data=json.dumps(des), content_type="application/json",
                              headers=self.admin_header)
        result = json.loads(res.data)
        self.assertEqual(result["Forbidden"],
                         "Admins cannot change destinaion of parcels")
        self.assertEqual(res.status_code, 403)

    def test_user_cannot_change_destination_of_parcel_they_did_not_create(self):
        """Users should not be able to change destination of parcels that are
        not theirs"""

        self.client.post(
            "api/v2/users/parcels", data=(json.dumps(self.generic_parcel)),
            content_type="application/json", headers=self.headers)

        self.client.post("/api/v2/auth/signup",
                         data=json.dumps(self.generic_user),
                         content_type="application/json")
        log = self.client.post("/api/v2/auth/login",
                               data=json.dumps(self.generic_user_details),
                               content_type="application/json")
        logs = json.loads(log.get_data(as_text=True))
        log_token = logs["token"]
        temp_headers = {"AUTHORIZATION": "Bearer " + log_token}
        update_destination = {"destination": "Nairoberry"}
        res = self.client.put("api/v2/parcels/1/destination", data=json.dumps(
            update_destination), content_type="application/json", headers=temp_headers)
        result = json.loads(res.data)
        self.assertEqual(
            result["Unauthorized"], "You can only update destination of your own parcels")
        self.assertEqual(res.status_code, 401)

    def test_user_can_get_their_parcel(self):
        """Users can only see parcels if they made one"""

        self.client.post(
            "api/v2/users/parcels", data=(json.dumps(self.generic_parcel)),
            content_type="application/json", headers=self.headers)
        res = self.client.get("/api/v2/parcels", headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def test_user_cannot_see_parcels_not_theirs(self):
        """"""
        self.client.post(
            "api/v2/users/parcels", data=(json.dumps(self.generic_parcel)),
            content_type="application/json", headers=self.headers)

        self.client.post("/api/v2/auth/signup",
                         data=json.dumps(self.generic_user),
                         content_type="application/json")
        log = self.client.post("/api/v2/auth/login",
                               data=json.dumps(self.generic_user_details),
                               content_type="application/json")
        logs = json.loads(log.get_data(as_text=True))
        log_token = logs["token"]
        temp_headers = {"AUTHORIZATION": "Bearer " + log_token}

        res = self.client.get("/api/v2/parcels", headers=temp_headers)
        self.assertEqual(res.status_code, 404)

    def test_user_change_status(self):
        """User should not be able to change the status of deliveries"""

        self.client.post(
            "api/v2/users/parcels", data=(json.dumps(self.generic_parcel)),
            content_type="application/json", headers=self.headers)

        status = {"status": "transit"}
        res = self.client.put("/api/v2/parcels/1/status", data=json.dumps(
            status), content_type="application/json", headers=self.headers)
        result = json.loads(res.data)
        self.assertEqual(result["Forbidden"],
                         "Only admins can change status of parcels")
        self.assertEqual(res.status_code, 403)

    def test_admin_change_status(self):
        """Admins should be able to change status of parcels that are not delivered or cancelled"""

        self.client.post(
            "api/v2/users/parcels", data=(json.dumps(self.generic_parcel)),
            content_type="application/json", headers=self.headers)

        status = {"status": "transit"}
        res = self.client.put("/api/v2/parcels/1/status", data=json.dumps(
            status), content_type="application/json", headers=self.admin_header)
        result = json.loads(res.data)
        self.assertEqual(result["Success"],
                         "The status for parcel number 1 was successfully changed")
        self.assertEqual(res.status_code, 200)

    def test_admin_change_invalid_status(self):
        """Admin should only be able to change status to being on transit or delivered"""

        self.client.post(
            "api/v2/users/parcels", data=(json.dumps(self.generic_parcel)),
            content_type="application/json", headers=self.headers)

        status = {"status": "invalid"}
        res = self.client.put("/api/v2/parcels/1/status", data=json.dumps(
            status), content_type="application/json", headers=self.admin_header)
        result = json.loads(res.data)
        self.assertEqual(result["Error"],
                         "Status can only be changed to 'transit' or 'delivered'.")
        self.assertEqual(res.status_code, 400)

    def test_admin_change_status_of_nonexistent_parcel(self):
        """Admin should only change status of parcels that exist"""

        status = {"status": "delivered"}
        res = self.client.put("/api/v2/parcels/5/status", data=json.dumps(
            status), content_type="application/json", headers=self.admin_header)
        result = json.loads(res.data)
        self.assertEqual(result["Error"],
                         "Parcel not found.")
        self.assertEqual(res.status_code, 404)

    def test_admin_change_status_of_delivered_parcels(self):
        """Admin should not be able to change status of parcels that have been cancelled
        or delivered"""

        status = {"status": "delivered"}
        self.client.put("/api/v2/parcels/1/status", data=json.dumps(
            status), content_type="application/json", headers=self.admin_header)
        new_status = {"status": "transit"}
        res = self.client.put("/api/v2/parcels/1/status", data=json.dumps(
            new_status), content_type="application/json", headers=self.admin_header)
        result = json.loads(res.data)
        self.assertEqual(result["Error"],
                         "Status cannot be changed for delivered or cancelled parcels")
        self.assertEqual(res.status_code, 400)

    def test_user_can_change_location(self):
        """Users should not be able to change location of parcels"""

        self.client.post(
            "api/v2/users/parcels", data=(json.dumps(self.generic_parcel)),
            content_type="application/json", headers=self.headers)

        location = {"current_location": "invalid"}
        res = self.client.put("/api/v2/parcels/1/presentLocation", data=json.dumps(
            location), content_type="application/json", headers=self.headers)
        result = json.loads(res.data)
        self.assertEqual(result["Forbidden"],
                         "Only admins can update the present location of a parcel.")
        self.assertEqual(res.status_code, 403)

    def test_admin_can_change_current_location(self):
        """Admins should be able to update current location of parcels in transit"""

        self.client.post(
            "api/v2/users/parcels", data=(json.dumps(self.generic_parcel)),
            content_type="application/json", headers=self.headers)

        status = {"status": "transit"}
        res = self.client.put("/api/v2/parcels/1/status", data=json.dumps(
            status), content_type="application/json", headers=self.admin_header)
        location = {"current_location": "Nairoberry"}
        res = self.client.put("/api/v2/parcels/1/presentLocation", data=json.dumps(
            location), content_type="application/json", headers=self.admin_header)
        result = json.loads(res.data)

        self.assertEqual(result["Success"],
                         "Successfully updated current location")
        self.assertEqual(res.status_code, 200)

    def test_admin_can_change_location_of_nonexistent_parcel(self):
        """Admin should not be able to change location of parcels that don't exist"""

        location = {"current_location": "Nairoberry"}
        res = self.client.put("/api/v2/parcels/5/presentLocation", data=json.dumps(
            location), content_type="application/json", headers=self.admin_header)
        result = json.loads(res.data)

        self.assertEqual(result["Error"],
                         "Parcel not found")
        self.assertEqual(res.status_code, 404)

    def test_admin_can_change_location_of_pending_parcels(self):
        """Admins should not be able to change current location of parcels not in transit"""

        self.client.post(
            "api/v2/users/parcels", data=(json.dumps(self.generic_parcel)),
            content_type="application/json", headers=self.headers)

        location = {"current_location": "Nairoberry"}
        res = self.client.put("/api/v2/parcels/1/presentLocation", data=json.dumps(
            location), content_type="application/json", headers=self.admin_header)
        result = json.loads(res.data)

        self.assertEqual(result["Error"],
                         "You can only change location of parcels in transit")
        self.assertEqual(res.status_code, 400)

    def test_admin_can_add_invalid_current_location(self):
        """Admins should not be able to add current locations that are not valid"""

        self.client.post(
            "api/v2/users/parcels", data=(json.dumps(self.generic_parcel)),
            content_type="application/json", headers=self.headers)

        status = {"status": "transit"}
        res = self.client.put("/api/v2/parcels/1/status", data=json.dumps(
            status), content_type="application/json", headers=self.admin_header)
        location = {"current_location": "      "}
        res = self.client.put("/api/v2/parcels/1/presentLocation", data=json.dumps(
            location), content_type="application/json", headers=self.admin_header)
        result = json.loads(res.data)

        self.assertEqual(result["Error"],
                         "Please enter a valid location")
        self.assertEqual(res.status_code, 400)

    def test_admin_can_cancel_parcel(self):
        """Admin should not be able to cancel parcels"""

        self.client.post(
            "api/v2/users/parcels", data=(json.dumps(self.generic_parcel)),
            content_type="application/json", headers=self.headers)

        res = self.client.put("/api/v2/parcels/1/cancel",
                              headers=self.admin_header)
        result = json.loads(res.data)

        self.assertEqual(result["Forbidden"],
                         "Admins cannot cancel parcels")
        self.assertEqual(res.status_code, 403)

    def test_user_can_cancel_pending_parcel(self):
        """User should be able to cancel pending or parcels in transit"""

        self.client.post(
            "api/v2/users/parcels", data=(json.dumps(self.generic_parcel)),
            content_type="application/json", headers=self.headers)

        res = self.client.put("/api/v2/parcels/1/cancel",
                              headers=self.headers)
        result = json.loads(res.data)

        self.assertEqual(result["Success"],
                         "Successfully cancelled your parcel")
        self.assertEqual(res.status_code, 200)

    def test_user_can_cancel_cancelled_parcel(self):
        """User should not be able to cancel cancelled or delivered parcels"""

        self.client.post(
            "api/v2/users/parcels", data=(json.dumps(self.generic_parcel)),
            content_type="application/json", headers=self.headers)

        self.client.put("/api/v2/parcels/1/cancel",
                        headers=self.headers)
        res = self.client.put("/api/v2/parcels/1/cancel",
                              headers=self.headers)
        result = json.loads(res.data)

        self.assertEqual(result["Error"],
                         "You can only cancel parcels in transit")
        self.assertEqual(res.status_code, 400)

    def test_user_can_cancel_nonexistent_parcels(self):
        """User should not be able to cancel parcels that don't exist"""

        res = self.client.put("/api/v2/parcels/5/cancel",
                              headers=self.headers)
        result = json.loads(res.data)

        self.assertEqual(result["Error"],
                         "Parcel not found")
        self.assertEqual(res.status_code, 404)

    def test_user_can_cancel_parcel_by_another_user(self):
        """User should not be able to cancel parcels they did no create"""

        self.client.post(
            "api/v2/users/parcels", data=(json.dumps(self.generic_parcel)),
            content_type="application/json", headers=self.headers)

        self.client.post("/api/v2/auth/signup", data=json.dumps(self.generic_user),
                         content_type="application/json")
        log = self.client.post("/api/v2/auth/login", data=json.dumps(self.generic_user_details),
                               content_type="application/json")
        logs = json.loads(log.get_data(as_text=True))
        log_token = logs["token"]
        temp_headers = {"AUTHORIZATION": "Bearer " + log_token}

        res = self.client.put("/api/v2/parcels/1/cancel",
                              headers=temp_headers)
        result = json.loads(res.data)
        self.assertEqual(result["Error"],
                         "You can only cancel parcels you created")
        self.assertEqual(res.status_code, 401)
