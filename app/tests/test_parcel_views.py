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
        pass

    def test_invalid_pickup_location(self):
        """Parcels must have valid pickup location"""
        pass

    def test_invalid_destination(self):
        """Parcels must have valid destination"""
        pass

    def test_valid_weight(self):
        """Parcels must have valid weight"""
        pass

    def test_admin_can_create_parcel(self):
        """Admins should not be able to create parcels"""
        pass

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
        res = self.client.put("/api/v2/parcels/1/destination",
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

        self.client.post("/api/v2/auth/signup", data=json.dumps(self.generic_user),
                         content_type="application/json")
        log = self.client.post("/api/v2/auth/login", data=json.dumps(self.generic_user_details),
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
